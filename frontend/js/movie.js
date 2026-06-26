const movieGrid = document.getElementById("movieGrid");
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");

let allMovies = [];

async function loadMovies() {
    try {
        const response = await fetch("http://127.0.0.1:8000/movies");

        if (!response.ok) {
            throw new Error("영화 목록 API 호출 실패");
        }

        const movies = await response.json();

        console.log("조회된 영화:", movies);

        allMovies = movies;
        renderMovies(allMovies);

    } catch (error) {
        console.error("영화 목록 로딩 에러:", error);

        movieGrid.innerHTML = `
            <p style="color:white;">영화 목록을 불러오지 못했습니다.</p>
        `;
    }
}

function renderMovies(movies) {
    movieGrid.innerHTML = "";

    movies.forEach(movie => {
        const card = document.createElement("a");

        card.className = "movie-card";
        card.href = `./detail.html?id=${movie.id}`;

        card.innerHTML = `
            <div class="poster-wrap">
                <img src="${movie.poster_url || 'https://via.placeholder.com/210x315?text=No+Image'}"
                     alt="영화 포스터">

                <div class="movie-overlay">
                    상세보기
                </div>
            </div>

            <div class="movie-info">
                <h3>${movie.title || "제목 없음"}</h3>
                <p>${movie.genre || "장르 정보 없음"}</p>
                <span>⭐ ${movie.rating || "0.0"}</span>
            </div>
        `;

        movieGrid.appendChild(card);
    });
}

searchForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const keyword = searchInput.value.trim();

    const filteredMovies = allMovies.filter(movie =>
        movie.title &&
        movie.title.includes(keyword)
    );

    renderMovies(filteredMovies);
});

loadMovies()