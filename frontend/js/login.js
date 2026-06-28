console.log("login.js latest version 100");

const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    console.log("login.js loaded");

    const loginBtn = document.getElementById("loginSubmitBtn");

    if (!loginBtn) {
        console.error("loginSubmitBtn을 찾지 못했습니다.");
        return;
    }

    loginBtn.addEventListener("click", handleLogin);
    console.log("click event registered");
});

async function handleLogin(event) {
    console.log("handleLogin called");

    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const messageBox = document.getElementById("loginMessage");

    messageBox.style.display = "none";
    messageBox.textContent = "";

    if (!email || !password) {
        showLoginMessage("이메일과 비밀번호를 입력해주세요.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const result = await response.json();

        console.log("login result:", result);

        if (result.success === true) {
            sessionStorage.setItem("user", JSON.stringify(result.user));

            alert(result.message || "로그인 성공");
            window.location.replace("/html/index.html");
            return;
        }

        showLoginMessage(result.message || "로그인에 실패했습니다.");

    } catch (error) {
        console.error(error);
        showLoginMessage("로그인 요청 중 오류가 발생했습니다.");
    }
}

function showLoginMessage(message) {
    const messageBox = document.getElementById("loginMessage");

    messageBox.textContent = message;
    messageBox.style.display = "block";
}