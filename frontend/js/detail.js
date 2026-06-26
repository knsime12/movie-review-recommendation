const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    loadMovieDetail();
});

async function loadMovieDetail() {
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
            throw new Error("영화 상세 조회 실패");
        }

        const movie = await response.json();

        console.log("영화 상세:", movie);

        const posterUrl = movie.poster_url || movie.posterUrl || "";
        const title = movie.title || "영화 제목";
        const genre = movie.genre || "장르 없음";
        const director = movie.director || "정보 없음";
        const releaseDate = movie.release_date || movie.releaseDate || "-";
        const overview = movie.overview || movie.description || "설명이 없습니다.";
        const rating = movie.rating || 4.5;

        document.getElementById("moviePoster").src = posterUrl;
        document.getElementById("movieTitle").textContent = title;
        document.getElementById("movieRating").textContent = rating;
        document.getElementById("movieGenre").textContent = genre;
        document.getElementById("movieDirector").textContent = director;
        document.getElementById("movieReleaseDate").textContent = releaseDate;
        document.getElementById("movieOverview").textContent = overview;

        const reviewBtn = document.getElementById("reviewWriteBtn");
        reviewBtn.href = `/html/review-write.html?id=${movieId}`;

    } catch (error) {
        console.error(error);
        alert("영화 상세 정보를 불러오지 못했습니다.");
    }
}