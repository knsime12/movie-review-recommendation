const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    console.log("signup.js loaded");

    const signupForm = document.getElementById("signupForm");

    if (!signupForm) {
        console.error("signupForm을 찾지 못했습니다.");
        return;
    }

    signupForm.addEventListener("submit", handleSignup);
});

async function handleSignup(event) {
    event.preventDefault();

    const messageBox = document.getElementById("signupMessage");

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const passwordCheck = document.getElementById("passwordCheck").value;

    messageBox.style.display = "none";
    messageBox.textContent = "";

    if (!username || !email || !password || !passwordCheck) {
        showMessage("모든 항목을 입력해주세요.");
        return;
    }

    if (password !== passwordCheck) {
        showMessage("비밀번호가 일치하지 않습니다.");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/signup`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const result = await response.json();

        console.log("signup result:", result);

        if (!response.ok || !result.success) {
            showMessage(result.message || "회원가입에 실패했습니다.");
            return;
        }

        alert("회원가입이 완료되었습니다.");
        location.href = "/html/login.html";

    } catch (error) {
        console.error(error);
        showMessage("회원가입 요청 중 오류가 발생했습니다.");
    }
}

function showMessage(message) {
    const messageBox = document.getElementById("signupMessage");

    messageBox.textContent = message;
    messageBox.style.display = "block";
}