const API_BASE_URL = "";

let currentPage = 1;
const pageSize = 12;

document.addEventListener("DOMContentLoaded", () => {
    loadMovies();

    const searchForm = document.getElementById("searchForm");

    searchForm.addEventListener("submit", (event) => {
        event.preventDefault();
        currentPage = 1;
        loadMovies();
    });
});

async function loadMovies() {
    const movieGrid = document.getElementById("movieGrid");
    const pagination = document.getElementById("pagination");
    const keyword = document.getElementById("keywordInput").value.trim();

    try {
        const response = await fetch(
            `${API_BASE_URL}/movies?keyword=${encodeURIComponent(keyword)}&page=${currentPage}&size=${pageSize}`
        );

        if (!response.ok) {
            throw new Error("영화 목록 조회 실패");
        }

        const data = await response.json();

        const movies = data.movies || data.items || data;
        const totalPages = data.total_pages || data.totalPages || 1;

        movieGrid.innerHTML = "";

        movies.forEach(movie => {
            const posterUrl = movie.poster_url || movie.posterUrl || "";
            const detailUrl = `/html/detail.html?id=${movie.id}`;

            const card = document.createElement("a");
            card.className = "movie-card";
            card.href = detailUrl;

            card.innerHTML = `
                <div class="poster-wrap">
                    ${
                        posterUrl
                        ? `<img src="${posterUrl}" alt="영화 포스터">`
                        : `<div style="color:white;">NO IMAGE</div>`
                    }

                    <div class="movie-overlay">
                        상세보기
                    </div>
                </div>

                <div class="movie-info">
                    <h3>${movie.title || "영화 제목"}</h3>
                    <p>${movie.genre || "장르 없음"}</p>
                    <span>⭐ ${movie.rating || 4.5}</span>
                </div>
            `;

            movieGrid.appendChild(card);
        });

        renderPagination(totalPages);

    } catch (error) {
        console.error(error);
        movieGrid.innerHTML = `<p style="color:white;">영화 목록을 불러오지 못했습니다.</p>`;
        pagination.innerHTML = "";
    }
}

function renderPagination(totalPages) {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    const maxVisible = 5;

    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, startPage + maxVisible - 1);

    if (endPage - startPage < maxVisible - 1) {
        startPage = Math.max(1, endPage - maxVisible + 1);
    }

    if (currentPage > 1) {
        const prevBtn = document.createElement("button");
        prevBtn.textContent = "이전";
        prevBtn.addEventListener("click", () => {
            currentPage--;
            loadMovies();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
        pagination.appendChild(prevBtn);
    }

    for (let page = startPage; page <= endPage; page++) {
        const pageBtn = document.createElement("button");
        pageBtn.textContent = page;

        if (page === currentPage) {
            pageBtn.classList.add("active");
        }

        pageBtn.addEventListener("click", () => {
            currentPage = page;
            loadMovies();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });

        pagination.appendChild(pageBtn);
    }

    if (currentPage < totalPages) {
        const nextBtn = document.createElement("button");
        nextBtn.textContent = "다음";
        nextBtn.addEventListener("click", () => {
            currentPage++;
            loadMovies();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
        pagination.appendChild(nextBtn);
    }
}