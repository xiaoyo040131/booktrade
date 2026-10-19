# -*- coding: utf-8 -*-
"""
自测工具（课程提供，不用修改）
《软件开发实践》

用法：在 booktrade 目录下执行
    python check/check_week03.py

说明：
1. 检查在临时数据库上进行，不会动你自己的 booktrade.db；
2. 任何一项失败都会给出提示，照着提示改再跑一遍即可；
3. [A] 是本周必做的补全项，[B] 是独立实现任务，[C] 是选做挑战。
"""

import os
import re
import sys
import tempfile
import traceback

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

GREEN, RED, YELLOW, GRAY, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[90m", "\033[0m"
if os.name == "nt" and not os.environ.get("WT_SESSION"):
    try:                       # 让老版本 Windows 终端也能显示颜色
        os.system("")
    except Exception:
        GREEN = RED = YELLOW = GRAY = RESET = ""


class Checker:
    def __init__(self, week, title):
        self.week = week
        self.title = title
        self.items = []
        print("=" * 64)
        print(f"《软件开发实践》第 {week} 周 自测：{title}")
        print("=" * 64)

    def check(self, level, name, fn, hint=""):
        """level 取 A / B / C；fn 返回 True 视为通过"""
        try:
            passed = bool(fn())
            detail = "" if passed else hint
        except Exception as e:
            passed = False
            detail = f"{type(e).__name__}: {e}"
            if hint:
                detail += f"　提示：{hint}"
        self.items.append((level, name, passed))
        mark = f"{GREEN}✔{RESET}" if passed else f"{RED}✘{RESET}"
        print(f"  {mark} [{level}] {name}")
        if not passed and detail:
            print(f"{GRAY}      → {detail}{RESET}")
        return passed

    def section(self, text):
        print(f"\n{YELLOW}—— {text} ——{RESET}")

    def summary(self):
        print("\n" + "=" * 64)
        stat = {}
        for level, _, passed in self.items:
            a, b = stat.get(level, (0, 0))
            stat[level] = (a + (1 if passed else 0), b + 1)
        for level in ("A", "B", "C"):
            if level in stat:
                ok, total = stat[level]
                tag = {"A": "基础补全", "B": "独立实现", "C": "挑战选做"}[level]
                color = GREEN if ok == total else RED
                print(f"  {level} 级（{tag}）：{color}{ok}/{total}{RESET} 项通过")
        ok_a, total_a = stat.get("A", (0, 0))
        ok_b, total_b = stat.get("B", (0, 0))
        print("-" * 64)
        if total_a and ok_a == total_a and (not total_b or ok_b == total_b):
            print(f"{GREEN}本周任务全部完成，可以提交了。{RESET}")
        elif total_a and ok_a == total_a:
            print(f"{YELLOW}A 级已全部完成（保底达标）。B 级还有 {total_b - ok_b} 项没过，继续加油。{RESET}")
        else:
            print(f"{RED}还有 {total_a - ok_a} 项基础任务没通过，先把 A 级补全。{RESET}")
        print("=" * 64)
        return ok_a == total_a


def boot(need_db=True, seed=True):
    """
    导入 app 并返回 (app, client)。数据库指向临时文件，不影响你的 booktrade.db。
    学生代码有语法错误或没补全时，这里会给出友好提示。
    """
    try:
        if need_db:
            import db
            tmp = os.path.join(tempfile.mkdtemp(), "check.db")
            db.DB_PATH = tmp
            if seed:
                import init_db as seeder
                seeder.DB_PATH = tmp
                _stdout = sys.stdout
                sys.stdout = open(os.devnull, "w")
                try:
                    seeder.main()
                finally:
                    sys.stdout.close()
                    sys.stdout = _stdout
        from app import app
        app.config["TESTING"] = True
        app.config.setdefault("SECRET_KEY", "check-key")
        if not app.config.get("SECRET_KEY"):
            app.config["SECRET_KEY"] = "check-key"
        return app, app.test_client()
    except Exception:
        print(f"{RED}无法启动你的项目，自测中止。完整错误如下：{RESET}\n")
        traceback.print_exc()
        print(f"\n{YELLOW}常见原因：代码还没补全（有 None / pass 没改）、缩进错误、"
              f"或者没在 booktrade 目录下运行本脚本。{RESET}")
        sys.exit(1)


def read(path):
    """读项目里的某个文件，读不到返回空串"""
    p = os.path.join(BASE_DIR, path)
    if not os.path.exists(p):
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


def exists(path):
    return os.path.exists(os.path.join(BASE_DIR, path))


def has_todo(path):
    """文件里是否还留着未完成的 TODO 标记"""
    return "==== TODO-" in read(path)


_PLACEHOLDER = re.compile(r'^(app\s*=\s*None|return\s*None|return\s*"")\s*$')


def has_placeholder(path):
    """检查文件里是否还有没换掉的占位符（app = None / return None / return ""）。
    只认真正的代码行——注释里、字符串提示语里出现同样的文字不算，
    所以哪怕忘了删 ==== TODO- ==== 那行注释也不会被误判。"""
    for line in read(path).splitlines():
        code = line.split("#", 1)[0].strip()
        if _PLACEHOLDER.match(code):
            return True
    return False


def has_real_call(path, prefix):
    """检查文件里是否有一行代码真的以 prefix 开头调用（不是写在注释或字符串里）。
    例如 has_real_call("app.py", "app.run(") 判断 app.run(...) 是否真的被调用了。"""
    pattern = re.compile(r'^\s*' + re.escape(prefix), re.MULTILINE)
    return bool(pattern.search(read(path)))


def login(client, username="zhangsan", password="123456"):
    return client.post("/api/auth/login",
                       json={"username": username, "password": password})
