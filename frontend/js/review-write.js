const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    checkLogin();
    loadMovieInfo();

    const reviewForm = document.getElementById("reviewForm");

    reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const userId = Number(sessionStorage.getItem("userId"));
        const params = new URLSearchParams(window.location.search);
        const movieId = params.get("id");

        if (!userId) {
            alert("로그인이 필요합니다.");
            location.href = "/html/login.html";
            return;
        }

        if (!movieId) {
            alert("영화 정보가 없습니다.");
            location.href = "/html/list.html";
            return;
        }

        const review = document.getElementById("reviewContent").value.trim();

        if (!review) {
            alert("리뷰를 입력해주세요.");
            return;
        }

        if (review.length < 5) {
            alert("리뷰는 5자 이상 작성해주세요.");
            return;
        }

        if (review.length > 500) {
            alert("리뷰는 500자 이하로 작성해주세요");
            return;
        }

        try {
            const duplicated = await checkDuplicateReview(userId, movieId);

            if (duplicated) {
                alert("이미 이 영화에 리뷰를 작성했습니다.");
                location.href = `/html/detail.html?id=${movieId}`;
                return;
            }

            sessionStorage.setItem("review", review);
            sessionStorage.setItem("movieId", movieId);

            location.href = `/html/result.html?id=${movieId}`;

        } catch (error) {
            console.error("review submit error:", error);
            alert("리뷰 작성 처리 중 오류가 발생했습니다.");
        }
    });
});

function checkLogin() {
    const userId = sessionStorage.getItem("userId");

    if (!userId) {
        alert("로그인이 필요합니다.");
        location.href = "/html/login.html";
    }
}

async function checkDuplicateReview(userId, movieId) {
    const response = await fetch(
        `${API_BASE_URL}/reviews/check?user_id=${userId}&movie_id=${movieId}`
    );

    const result = await response.json();

    if (!response.ok || !result.success) {
        throw new Error(result.message || "리뷰 중복 확인 실패");
    }

    return result.exists;
}

async function loadMovieInfo() {
    const params = new URLSearchParams(window.location.search);
    const movieId = params.get("id");

    if (!movieId) {
        alert("영화 ID가 없습니다.");
        location.href = "/html/list.html";
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/movies/${movieId}`);

        if (!response.ok) {
            throw new Error("영화 정보 조회 실패");
        }

        const movie = await response.json();

        const posterUrl = movie.poster_url || movie.posterUrl || "";
        const title = movie.title || "영화 정보를 불러오지 못했습니다.";
        const genre = movie.genre || "장르 없음";
        const releaseDate = movie.release_date || movie.releaseDate || "개봉일";
        const rating = movie.rating || 4.5;

        document.getElementById("moviePoster").src = posterUrl;
        document.getElementById("movieTitle").textContent = title;
        document.getElementById("movieGenre").textContent = genre;
        document.getElementById("movieReleaseDate").textContent = releaseDate;
        document.getElementById("movieRating").textContent = rating;

    } catch (error) {
        console.error(error);
        document.getElementById("movieTitle").textContent = "영화 정보를 불러오지 못했습니다.";
    }
}