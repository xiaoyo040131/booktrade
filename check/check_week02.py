# -*- coding: utf-8 -*-
"""第 2 周自测：需求分析与页面原型开发"""
from checker import Checker, boot, read, exists, has_todo

c = Checker(2, "需求分析与页面原型开发")
app, client = boot(need_db=False)


def page(path):
    return client.get(path).get_data(as_text=True)


c.section("A 级：基础补全")
for f in ("app.py", "templates/base.html", "templates/index.html", "static/css/style.css"):
    c.check("A", f"{f} 里没有遗漏的 ==== TODO- ==== 标记",
        (lambda f=f: not has_todo(f)),
        f"{f} 里还留着 ==== TODO-N ==== 这行注释——如果对应的功能已经写完，"
        "把这一行注释删掉就行；如果确实还没写，对照上面的要求继续补")
c.check("A", "四个页面都能打开",
        lambda: all(client.get(p).status_code == 200
                    for p in ("/", "/login", "/register", "/publish")))
c.check("A", "首页渲染出了至少 6 张图书卡片",
        lambda: page("/").count("book-card") >= 6,
        "检查 TODO-5 的 for 循环是否包住了整个 <article>")
c.check("A", "价格显示为两位小数（如 ￥15.00）",
        lambda: "￥15.00" in page("/") or "￥12.50" in page("/"),
        "检查 TODO-6 的 format 过滤器")
c.check("A", "模板继承生效：登录页也带导航栏",
        lambda: "校园二手书" in page("/login") and "navbar" in page("/login"),
        "检查 TODO-4 的 extends 和 TODO-3 的 content 块")
c.check("A", "子页面内容写在 content 块里（页面不是空壳）",
        lambda: "用户登录" in page("/login"),
        "写在 block 外面的内容不会被渲染，检查 TODO-3/TODO-4")
c.check("A", "卡片使用了 Grid 自适应布局",
        lambda: "auto-fill" in read("static/css/style.css"),
        "检查 TODO-7 的 grid-template-columns")

c.section("B 级：独立实现（我的订单原型 + 扩展导航）")
c.check("B", "新增了 /my/orders 页面",
        lambda: client.get("/my/orders").status_code == 200,
        "在 app.py 里加路由，渲染 templates/extra/my_orders.html")
c.check("B", "订单页放在 templates/extra/ 下（不会被骨架覆盖）",
        lambda: exists("templates/extra/my_orders.html"),
        "新建 templates/extra/my_orders.html")
c.check("B", "订单页用表格展示，且至少 3 条数据",
        lambda: page("/my/orders").count("<tr") >= 4,
        "用 <table class='table'> 展示，表头 1 行 + 数据 3 行")
c.check("B", "三种订单状态用不同标签显示",
        lambda: all(k in page("/my/orders")
                    for k in ("tag-pending", "tag-done", "tag-cancel")),
        "用 {% if %}{% elif %}{% else %} 分别输出三种 tag 样式")
c.check("B", "写了扩展导航 templates/extra/nav.html",
        lambda: exists("templates/extra/nav.html"),
        "新建 templates/extra/nav.html，base.html 会自动引入它")
c.check("B", "扩展导航真的显示在页面上了",
        lambda: "我的订单" in page("/"),
        "在 extra/nav.html 里加一个指向 /my/orders 的链接")

c.summary()
