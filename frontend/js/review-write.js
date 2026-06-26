const params = new URLSearchParams(window.location.search);
const movieId = params.get("id");

const poster = document.getElementById("poster");
const movieTitle = document.getElementById("movieTitle");
const genre = document.getElementById("genre");
const releaseDate = document.getElementById("releaseDate");
const rating = document.getElementById("rating");

const reviewForm = document.getElementById("reviewForm");
const reviewInput = document.getElementById("reviewInput");

let currentMovie = null;

async function loadMovie() {
    try {
        if (!movieId) {
            throw new Error("영화 ID가 없습니다.");
        }

        const response = await fetch(`http://127.0.0.1:8000/movies/${movieId}`);

        if (!response.ok) {
            throw new Error("영화 정보 조회 실패");
        }

        const movie = await response.json();

        if (!movie) {
            throw new Error("영화 데이터가 없습니다.");
        }

        currentMovie = movie;

        movieTitle.textContent = movie.title || "제목 없음";
        genre.textContent = movie.genre || "장르 정보 없음";
        releaseDate.textContent = movie.release_date || "-";
        rating.textContent = movie.rating || "0.0";

        if (movie.poster_url) {
            poster.src = movie.poster_url;
        } else {
            poster.src = "https://via.placeholder.com/86x126?text=No+Image";
        }

    } catch (error) {
        console.error(error);
        movieTitle.textContent = "영화 정보를 불러오지 못했습니다.";
    }
}

reviewForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const review = reviewInput.value.trim();

    if (!review) {
        alert("리뷰를 입력해주세요.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                review: review
            })
        });

        if (!response.ok) {
            throw new Error("감성 분석 실패");
        }

        const result = await response.json();

        const resultData = {
            movie: currentMovie,
            review: review,
            analysis: result
        };

        sessionStorage.setItem("analysisResult", JSON.stringify(resultData));

        location.href = "./result.html";

    } catch (error) {
        console.error(error);
        alert("감성 분석 중 문제가 발생했습니다.");
    }
});

loadMovie();