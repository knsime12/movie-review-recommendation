const API_BASE_URL = "";
const NO_IMAGE_URL =
    "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=800";

document.addEventListener("DOMContentLoaded", () => {
    loadMyPage();
});

async function loadMyPage() {
    const userId = sessionStorage.getItem("userId");
    const username = sessionStorage.getItem("username");
    const email = sessionStorage.getItem("email");

    if (!userId) {
        alert("로그인이 필요합니다.");
        location.href = "/html/login.html";
        return;
    }

    renderUserInfo(username, email);
    await loadMyReviews(userId);
}

function renderUserInfo(username, email) {
    setText("#userName", username || "사용자");
    setText("#userEmail", email || "");
}

async function loadMyReviews(userId) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/${userId}/reviews`);

        if (!response.ok) {
            throw new Error("내 리뷰 조회 실패");
        }

        const result = await response.json();

        console.log("my reviews result =", result);

        if (!result.success) {
            throw new Error(result.message || "내 리뷰 조회 실패");
        }

        const reviews = result.reviews || [];

        renderReviewCounts(reviews);
        renderMyReviews(reviews);

    } catch (error) {
        console.error("mypage error:", error);

        const myReviewList = document.querySelector("#myReviewList");

        if (myReviewList) {
            myReviewList.innerHTML = `
                <p>리뷰를 불러오는 중 오류가 발생했습니다.</p>
            `;
        }
    }
}

function renderReviewCounts(reviews) {
    const positiveCount = reviews.filter(review => review.sentiment === "긍정").length;
    const negativeCount = reviews.filter(review => review.sentiment === "부정").length;

    setText("#positiveCount", positiveCount);
    setText("#negativeCount", negativeCount);

    setText("#positiveReviewSummary", `${positiveCount}개`);
    setText("#negativeReviewSummary", `${negativeCount}개`);
}

function renderMyReviews(reviews) {
    const myReviewList = document.querySelector("#myReviewList");

    if (!myReviewList) {
        return;
    }

    myReviewList.innerHTML = "";

    if (reviews.length === 0) {
        myReviewList.innerHTML = `
            <p>아직 작성한 리뷰가 없습니다.</p>
        `;
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement("div");
        reviewCard.className = "my-review-item";

        const sentimentClass =
            review.sentiment === "긍정" ? "positive-text" : "negative-text";

        const sentimentEmoji =
            review.sentiment === "긍정" ? "😊" : "😢";

        reviewCard.innerHTML = `
            <div class="review-top">
                <div class="review-title-area">
                    <a href="/html/detail.html?id=${review.movie_id}" class="review-movie-title">
                        ${review.title || "영화 제목"}
                    </a>

                    <p class="review-genre">
                        ${review.genre || "장르 정보 없음"}
                    </p>
                </div>

                <strong class="${sentimentClass}">
                    ${sentimentEmoji} ${review.sentiment || "-"}
                </strong>
            </div>

            <div class="review-body">

                <img class="review-poster"
                    src="${review.poster_url || NO_IMAGE_URL}"
                    alt="영화 포스터"
                    onerror="this.src='${NO_IMAGE_URL}'">

                <div class="review-content-wrap">

                    <p class="review-content">
                        ${review.content || ""}
                    </p>

                    <div class="review-bottom">
                        <span class="review-rating">
                            ⭐ AI 예상 평점 ${review.expected_rating || "-"}
                        </span>

                        <span class="review-date">
                            ${formatDate(review.created_at)}
                        </span>
                    </div>

                </div>

            </div>
        `;

        myReviewList.appendChild(reviewCard);
    });
}

function showTab(event, tabId) {
    const buttons = document.querySelectorAll(".menu-btn");
    const sections = document.querySelectorAll(".content-section");

    buttons.forEach(button => {
        button.classList.remove("active");
    });

    sections.forEach(section => {
        section.classList.remove("active-section");
    });

    const targetSection = document.querySelector(`#${tabId}`);

    if (targetSection) {
        targetSection.classList.add("active-section");
    }

    event.currentTarget.classList.add("active");
}

function formatDate(dateString) {
    if (!dateString) {
        return "";
    }

    const date = new Date(dateString);

    if (Number.isNaN(date.getTime())) {
        return dateString;
    }

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}.${month}.${day}`;
}

function setText(selector, value) {
    const element = document.querySelector(selector);

    if (element) {
        element.textContent = value;
    }
}