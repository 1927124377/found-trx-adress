# found-trx-adress v1.0 - 模块化重构

## 📦 项目结构

```
found-trx-adress/
├── core/                      # 核心抽象层
│   ├── __init__.py
│   ├── base_crawler.py        # 爬虫基类
│   └── base_analyzer.py       # 分析器基类
├── chains/                    # 链实现层
│   ├── tron/
│   │   ├── crawler.py         # TRON 爬虫实现
│   │   └── analyzer.py        # TRON 分析器实现
│   └── binance/               # (待实现)
├── config/                    # 配置管理
│   ├── settings.py            # 配置加载模块
│   └── settings.example.json  # 配置示例
├── utils/                     # 工具函数
├── .env.example               # 环境变量示例
├── requirements.txt           # 依赖
└── README.md                  # 本文档
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd found-trx-adress
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入 API key
```

### 3. 使用示例

#### TRON 爬虫

```python
from chains.tron.crawler import TronCrawler

# 初始化爬虫
crawler = TronCrawler()

# 爬取交易数据
address = "TYourTronAddressHere"
transactions = crawler.crawl_transactions(address, limit=50)

# 扁平化数据
for tx in transactions:
    flat_tx = crawler.flatten_transaction(tx)
    print(flat_tx)
```

#### TRON 分析器

```python
from chains.tron.analyzer import TronAnalyzer
import pandas as pd

# 初始化分析器
analyzer = TronAnalyzer()

# 准备数据
df = pd.DataFrame(transactions)

# 基础统计
stats = analyzer.analyze_basic_stats(df, address)
print(stats)

# 主要交易对手
top_counterparties = analyzer.get_top_counterparties(df, limit=5)
print(top_counterparties)

# 完整报告
report = analyzer.generate_analysis_report(df, address)
print(report)
```

---

## 📋 配置说明

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `TRON_API_KEY` | TronScan API Key | 否（无 key 有速率限制） |
| `BINANCE_API_KEY` | Binance API Key | 否 |
| `BINANCE_API_SECRET` | Binance API Secret | 否 |
| `OUTPUT_FORMAT` | 输出格式 (excel/csv/json) | 否（默认 excel） |
| `OUTPUT_DIR` | 输出目录 | 否（默认 ./output） |

### 配置文件

`config/settings.json` 支持以下配置：

```json
{
  "tron": {
    "api_key": "your_key",
    "base_url": "https://apilist.tronscanapi.com/api",
    "rate_limit": 100
  },
  "output": {
    "format": "excel",
    "dir": "./output"
  }
}
```

---

## 🔧 架构设计

### 核心原则

1. **单一职责**: 每个模块只负责一个功能
2. **专业化**: TRON 和 Binance 模块独立
3. **可组合**: 通过配置组合，不硬编码
4. **易扩展**: 添加新链只需实现基类

### 类关系

```
BaseCrawler (抽象基类)
    ↓
TronCrawler (实现)

BaseAnalyzer (抽象基类)
    ↓
TronAnalyzer (实现)

Config (配置管理)
    ↓
所有模块使用
```

---

## 📊 功能特性

### TRON 爬虫
- ✅ 爬取 TRX 交易数据
- ✅ 获取账户信息
- ✅ 获取 TRC20 转账记录
- ✅ 数据扁平化处理

### TRON 分析器
- ✅ 基础统计分析
- ✅ 交易对手分析
- ✅ 完整报告生成
- ✅ 鲸鱼活动检测
- ✅ 活跃度评分

---

## 🎯 下一步

### 待实现
- [ ] Binance 模块（独立插件）
- [ ] 数据导出工具（Excel/CSV）
- [ ] 命令行界面
- [ ] 单元测试
- [ ] 集成测试

### 计划中
- [ ] 更多链支持（ETH、BSC 等）
- [ ] 可视化报告
- [ ] API 服务接口

---

## 📝 版本历史

### v1.0 (2026-03-05)
- ✅ 核心基类完成
- ✅ TRON 模块实现
- ✅ 配置管理系统
- ✅ 文档完善

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
