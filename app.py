"""
校园二手书交易平台 —— 主程序入口
《软件开发实践》第 2 周：需求分析与页面原型（模板继承 + 假数据渲染）
"""

import os

from flask import Flask, render_template

app = Flask(__name__)

# ---------------------------------------------------------------
# 第 2 周先用「假数据」把页面撑起来，第 3 周会把它换成数据库查询。
# 每本书就是一个字典，字段名要和后面数据库的列名保持一致。
# ---------------------------------------------------------------
MOCK_BOOKS = [
    {"id": 1, "title": "C语言程序设计", "author": "谭浩强", "category": "计算机",
     "price": 15.0, "condition": "九成新", "seller": "张三", "cover": "📘"},
    {"id": 2, "title": "高等数学（上册）", "author": "同济大学", "category": "数学",
     "price": 12.5, "condition": "八成新", "seller": "李四", "cover": "📗"},
    {"id": 3, "title": "计算机网络（第8版）", "author": "谢希仁", "category": "计算机",
     "price": 25.0, "condition": "全新", "seller": "王五", "cover": "📙"},
    {"id": 4, "title": "大学英语四级真题", "author": "新东方", "category": "外语",
     "price": 9.9, "condition": "七成新", "seller": "赵六", "cover": "📕"},
    {"id": 5, "title": "数据结构（C语言版）", "author": "严蔚敏", "category": "计算机",
     "price": 18.0, "condition": "九成新", "seller": "孙七", "cover": "📓"},
    {"id": 6, "title": "线性代数", "author": "同济大学", "category": "数学",
     "price": 8.0, "condition": "八成新", "seller": "周八", "cover": "📔"},
]


@app.route("/")
def index():
    """首页：把书籍列表传给模板，由模板循环渲染成卡片"""
    return render_template("index.html", books=MOCK_BOOKS, total=len(MOCK_BOOKS))


@app.route("/login")
def login_page():
    """登录页（第 5 周才会真正实现登录逻辑）"""
    return render_template("login.html")


@app.route("/register")
def register_page():
    """注册页"""
    return render_template("register.html")


@app.route("/publish")
def publish_page():
    """发布二手书页面（第 6 周接后端接口）"""
    return render_template("publish.html")


@app.route("/about")
def about():
    return "《软件开发实践》第 2 周：页面原型完成！"


# ---------------------------------------------------------------
# 学生自主扩展入口（B 级独立实现任务）
# 你的扩展代码写在 extensions.py、templates/extra/、static/js/extra/ 里，
# 和课程骨架分开放，互不干扰。
# 只要项目根目录存在 extensions.py，就会自动加载。
#
# 为什么放在文件最末尾：让课程骨架自己的路由先注册完，扩展再上。
# 这样万一你的扩展和骨架用了同一个地址（比如 /my/orders），
# extensions.py 里的 _page() 能发现「这个地址主线已经占了」并自动让路，
# 而不是两边打架、启动直接报错。
# ---------------------------------------------------------------
_EXT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extensions.py")
if os.path.exists(_EXT):
    import extensions  # type: ignore  # 这是你自己的扩展文件（B 级任务创建），第 1 周还不存在，编辑器的黄色波浪线属正常现象
    extensions.init_app(app)
    print("[扩展] extensions.py 已加载")


if __name__ == "__main__":
    # ---------------------------------------------------------------
    # 位置自检（课程提供，不用改）
    # 你应该在【自己的项目文件夹】里做实验，不是在课程包里直接改。
    # 课程包是发给全班的原始材料，在里面改，下次拷贝就乱了。
    # ---------------------------------------------------------------
    # debug 模式会再开一个进程真正提供服务，只在那个进程里打印，免得出现两遍
    if ("代码补全" in os.path.abspath(__file__).split(os.sep)
            and os.environ.get("WERKZEUG_RUN_MAIN") == "true"):
        print("")
        print("*" * 64)
        print("  注意：你正在运行【课程包自带的骨架】，这不是你自己的项目。")
        print("  正确做法：把这个 booktrade 文件夹整个复制到你自己的目录下")
        print("  （比如 D:\\软件开发实践\\你的学号_姓名\\booktrade，路径别带中文和空格），")
        print("  本周的作业就在那一份上做。")
        print("*" * 64)
        print("")

    # ---------------------------------------------------------------
    # 启动前自检（课程提供，不用改）
    # 作用：TODO-1 还没补的时候先把话说清楚，
    #       免得你打开首页看到一屏红色报错，以为是 Python 或 Flask 装坏了。
    #       补完 TODO-1 之后，这段提示自己就不出现了。
    # ---------------------------------------------------------------
    import re as _re

    with open(os.path.abspath(__file__), "r", encoding="utf-8") as _f:
        _todo_lines = [i + 1 for i, _line in enumerate(_f.read().splitlines())
                       if _re.match(r"^\s*return\s+None\s*(#.*)?$", _line)]

    # debug 模式下 Flask 会再开一个进程来真正提供服务，
    # 这里只在那个进程里打印，免得同一段提示出现两遍。
    _serving = os.environ.get("WERKZEUG_RUN_MAIN") == "true"

    if _todo_lines and _serving:
        _where = "、".join(str(n) for n in _todo_lines)
        print("")
        print("!" * 64)
        print("  TODO-1 还没补完：app.py 第 %s 行现在还写着 return None。" % _where)
        print("")
        print("  服务照样会启动，但是打开首页 http://127.0.0.1:5000 会看到这句报错：")
        print("      The view function for 'index' did not return a valid response")
        print("")
        print("  这不是环境装坏了，也不是文件损坏 —— 它的意思就是")
        print("  「index 这个函数还没有 return 出任何东西」。")
        print("  照着实验手册 Step 6 把那一行换成 render_template(...)，报错就没了。")
        print("!" * 64)
        print("")

    app.run(debug=True, port=5000)
