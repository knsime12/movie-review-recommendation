const params = new URLSearchParams(window.location.search);
const movieId = params.get("id");

const title = document.getElementById("title");
const poster = document.getElementById("poster");
const posterPlaceholder = document.getElementById("posterPlaceholder");
const genre = document.getElementById("genre");
const director = document.getElementById("director");
const actors = document.getElementById("actors");
const releaseDate = document.getElementById("releaseDate");
const overview = document.getElementById("overview");
const rating = document.getElementById("rating");
const reviewWriteBtn = document.getElementById("reviewWriteBtn");

async function loadMovieDetail() {
    try {
        if (!movieId) {
            throw new Error("영화 ID가 없습니다.");
        }

        const response = await fetch(`http://127.0.0.1:8000/movies/${movieId}`);

        if (!response.ok) {
            throw new Error("영화 상세 조회 실패");
        }

        const movie = await response.json();

        if (!movie) {
            throw new Error("영화 데이터가 없습니다.");
        }

        console.log("영화 상세:", movie);

        title.textContent = movie.title || "제목 없음";
        genre.textContent = movie.genre || "장르 정보 없음";
        director.textContent = movie.director || "정보 없음";
        actors.textContent = movie.actors || "정보 없음";
        releaseDate.textContent = movie.release_date || "-";
        overview.textContent = movie.overview || "설명이 없습니다.";

        rating.textContent = movie.rating || "0.0";

        if (movie.poster_url) {
            poster.src = movie.poster_url;
            poster.style.display = "block";
            posterPlaceholder.style.display = "none";
        } else {
            poster.style.display = "none";
            posterPlaceholder.style.display = "flex";
        }

        reviewWriteBtn.href = `./review-write.html?id=${movie.id}`;

        document.title = `${movie.title} - CineFeel`;

    } catch (error) {
        console.error(error);

        title.textContent = "영화 정보를 불러오지 못했습니다.";
        overview.textContent = "영화 상세 정보를 조회하는 중 문제가 발생했습니다.";
        poster.style.display = "none";
        posterPlaceholder.style.display = "flex";
    }
}

loadMovieDetail();