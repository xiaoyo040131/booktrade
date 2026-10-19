/**
 * 明暗主题切换（课程提供，不用修改）
 *
 * 原理：
 * 1. 把 data-theme="dark" / "light" 写在 <html> 上，CSS 变量随之切换；
 * 2. 用户的选择记在浏览器 localStorage 里，下次打开还是同一套主题；
 * 3. 没选过时不写任何值，CSS 会自动跟随操作系统的深色/浅色设置。
 */
(function () {
    var KEY = "booktrade-theme";

    /** 读取用户之前的选择；读不到返回 null（表示跟随系统） */
    function saved() {
        try {
            return localStorage.getItem(KEY);
        } catch (e) {
            return null;   // 浏览器禁用了本地存储时不报错，降级成跟随系统
        }
    }

    /** 当前实际显示的是不是深色 */
    function isDark() {
        var s = saved();
        if (s) return s === "dark";
        return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    }

    function apply(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        var btn = document.getElementById("themeToggle");
        if (btn) {
            btn.textContent = theme === "dark" ? "☀️" : "🌙";
            btn.title = theme === "dark" ? "切换到浅色模式" : "切换到深色模式";
        }
    }

    // 页面一加载就定好主题，避免先白一下再变黑（俗称"闪白"）
    apply(isDark() ? "dark" : "light");

    document.addEventListener("DOMContentLoaded", function () {
        apply(isDark() ? "dark" : "light");
        var btn = document.getElementById("themeToggle");
        if (!btn) return;
        btn.addEventListener("click", function () {
            var next = isDark() ? "light" : "dark";
            try {
                localStorage.setItem(KEY, next);
            } catch (e) { /* 存不了就只在本页生效，不影响使用 */ }
            apply(next);
        });
    });
})();
