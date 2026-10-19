"""
学生自主扩展入口（B 级独立实现任务）—— 第 1 周版本

app.py 启动时会检测项目根目录有没有 extensions.py，
有就调用这里的 init_app(app)。你自己写的功能都从这里挂上去，
所以下周换新骨架时，这个文件和 templates/extra/ 都不会被覆盖。
"""

from flask import render_template


def init_app(app):
    """app.py 启动时会调用这个函数"""

    @app.route("/profile")
    def profile_page():
        return render_template("extra/profile.html")
    
    @app.route("/my/orders")
    def my_orders_page():
        return render_template("extra/my_orders.html")
