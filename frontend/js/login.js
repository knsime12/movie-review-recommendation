const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    const loginBtn = document.querySelector("#loginSubmitBtn");

    if (loginBtn) {
        loginBtn.addEventListener("click", login);
    }
});

async function login() {
    const email = document.querySelector("#email").value.trim();
    const password = document.querySelector("#password").value.trim();
    const message = document.querySelector("#loginMessage");

    if (message) {
        message.style.display = "none";
    }

    if (!email || !password) {
        alert("이메일과 비밀번호를 입력해주세요.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            if (message) {
                message.textContent = result.message;
                message.style.display = "block";
            }
            return;
        }

        // 로그인 정보 저장
        sessionStorage.setItem("isLogin", "true");
        sessionStorage.setItem("isLoggedIn", "true");

        sessionStorage.setItem("userId", String(result.user.id));
        sessionStorage.setItem("username", result.user.username);
        sessionStorage.setItem("userName", result.user.username);
        sessionStorage.setItem("email", result.user.email);

        alert("로그인되었습니다.");

        location.href = "/html/index.html";

    } catch (error) {
        console.error("login error:", error);
        alert("로그인 중 오류가 발생했습니다.");
    }
}