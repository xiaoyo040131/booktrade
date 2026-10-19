# 📚 校园二手书交易平台

《软件开发实践》课程项目（第 2 周：需求分析与页面原型）

基于 **Flask** 的校园二手书交易平台，目前为页面原型阶段，使用假数据渲染，后续周次将逐步接入数据库、登录鉴权、发布接口等功能。

## ✨ 功能特性

- 首页展示在售二手书卡片列表（假数据，共 6 本）
- 图书卡片网格自适应布局（Grid `auto-fill`）
- 明暗双主题一键切换（跟随系统 + localStorage 记忆）
- 登录页 / 注册页 / 发布图书页（页面原型）
- 我的订单页面（表格展示 + 三种订单状态标签）
- 我的名片扩展页（B 级独立实现任务）
- 模板继承（`base.html` 统一导航 / 页脚）
- 学生扩展入口 `extensions.py` 自动挂载，与课程骨架分离

## 🚀 运行环境

- Python 3.10+
- Flask >= 3.0.0

## ⚙️ 快速开始

```bash
# 1. 克隆项目
 git clone https://github.com/xiaoyo040131/booktrade.git
 cd booktrade

# 2. （推荐）创建虚拟环境
 python -m venv .venv
 # Windows:
 .venv\Scripts\activate
 # macOS / Linux:
 source .venv/bin/activate

# 3. 安装依赖
 pip install -r requirements.txt

# 4. 启动应用
 python app.py
```

启动后浏览器访问：**http://127.0.0.1:5000**

## 📁 项目结构

```
booktrade/
├── app.py                     # 主程序入口 + 假数据
├── extensions.py              # 学生自主扩展入口（自动挂载）
├── requirements.txt           # 依赖
├── check/
│   ├── checker.py             # 自测工具基类（课程提供）
│   └── check_week02.py        # 第 2 周自测脚本
├── static/
│   ├── css/style.css          # 统一样式表（含明暗双主题）
│   └── js/theme.js            # 主题切换脚本
└── templates/
    ├── base.html              # 基础模板（导航 + 页脚）
    ├── index.html             # 首页图书列表
    ├── login.html             # 登录页
    ├── register.html          # 注册页
    ├── publish.html           # 发布图书页
    └── extra/                 # 学生扩展页面（不会被子骨架覆盖）
        ├── my_orders.html     # 我的订单
        ├── nav.html           # 扩展导航
        └── profile.html       # 个人名片
```

## ✅ 自测

在 `booktrade` 目录下运行：

```bash
python check/check_week02.py
```

## 📅 开发计划

| 周次 | 主题 | 状态 |
|------|------|------|
| 第 2 周 | 需求分析与页面原型（模板继承 + 假数据） | ✅ 已完成 |
| 第 3 周 | 数据库设计与接入 | ⏳ 待进行 |
| 第 5 周 | 登录鉴权 | ⏳ 待进行 |
| 第 6 周 | 发布图书接口 | ⏳ 待进行 |
| 第 7 周 | 真实订单数据 | ⏳ 待进行 |

## 📄 许可

本项目为《软件开发实践》课程作业，仅供学习交流使用。
