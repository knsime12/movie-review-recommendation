document.addEventListener("DOMContentLoaded", () => {
    const authMenu = document.querySelector(".auth-menu");

    if (!authMenu) return;

    const isLogin =
        sessionStorage.getItem("isLogin") === "true" ||
        sessionStorage.getItem("isLoggedIn") === "true";

    const username =
        sessionStorage.getItem("username") ||
        sessionStorage.getItem("userName");

    if (isLogin && username) {
        authMenu.innerHTML = `
            <span class="user-badge">👤 ${username}</span>
            <a href="/html/mypage.html">마이페이지</a>
            <a href="#" id="logoutBtn">로그아웃</a>
        `;

        document.querySelector("#logoutBtn").addEventListener("click", (e) => {
            e.preventDefault();
            sessionStorage.clear();
            location.href = "/html/index.html";
        });
    } else {
        authMenu.innerHTML = `
            <a href="/html/login.html">로그인</a>
            <a href="/html/signup.html">회원가입</a>
        `;
    }
});

function renderAuthMenu() {
    const userData = sessionStorage.getItem("user");

    const authMenus = document.querySelectorAll(".auth-menu, .nav-icons");

    authMenus.forEach(authMenu => {
        if (!authMenu) return;

        if (userData) {
            const user = JSON.parse(userData);

            authMenu.innerHTML = `
                <span class="user-name">👤 ${user.username}</span>
                <a href="/html/mypage.html">마이페이지</a>
                <a href="#" id="logoutBtn">로그아웃</a>
            `;

            const logoutBtn = authMenu.querySelector("#logoutBtn");

            logoutBtn.addEventListener("click", (event) => {
                event.preventDefault();

                sessionStorage.removeItem("user");
                location.href = "/html/index.html";
            });

        } else {
            authMenu.innerHTML = `
                <a href="/html/login.html">로그인</a>
                <a href="/html/signup.html">회원가입</a>
            `;
        }
    });
}