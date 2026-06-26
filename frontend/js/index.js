const API_BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", () => {
    loadPopularMovies();
});

async function loadPopularMovies() {
    const movieGrid = document.getElementById("popularMovieGrid");

    try {
        const response = await fetch(`${API_BASE_URL}/movies/popular?limit=6`);

        if (!response.ok) {
            throw new Error("인기 영화 조회 실패");
        }

        const movies = await response.json();

        movieGrid.innerHTML = "";

        movies.forEach(movie => {
            const card = document.createElement("div");
            card.className = "movie-card";

            card.innerHTML = `
                <a href="./detail.html?id=${movie.id}">
                    <div class="movie-poster-wrap">
                        <img src="${movie.poster_url || '../images/no-image.png'}" alt="영화 포스터">

                        <div class="movie-overlay">
                            <span>상세보기</span>
                        </div>
                    </div>

                    <div class="movie-info">
                        <h3>${movie.title}</h3>

                        <div class="movie-meta">
                            <span class="movie-rating">
                                ⭐ ${movie.rating || 4.5}
                            </span>

                            <span class="movie-genre">
                                ${movie.genre || "장르 없음"}
                            </span>
                        </div>
                    </div>
                </a>
            `;

            movieGrid.appendChild(card);
        });

    } catch (error) {
        console.error(error);
        movieGrid.innerHTML = `<p style="color:white;">영화 정보를 불러오지 못했습니다.</p>`;
    }
}