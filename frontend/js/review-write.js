const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    loadMovieInfo();

    const reviewForm = document.getElementById("reviewForm");

    reviewForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const review = document.getElementById("reviewContent").value.trim();

        if (!review) {
            alert("리뷰를 입력해주세요.");
            return;
        }

        const params = new URLSearchParams(window.location.search);
        const movieId = params.get("id");

        sessionStorage.setItem("review", review);
        sessionStorage.setItem("movieId", movieId);

        location.href = `/html/result.html?id=${movieId}`;
    });
});

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