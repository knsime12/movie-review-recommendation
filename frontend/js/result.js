const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    loadResult();
});

async function loadResult() {
    const review = sessionStorage.getItem("review");
    const movieId =
        sessionStorage.getItem("movieId") ||
        new URLSearchParams(location.search).get("id");

    if (!review || !movieId) {
        alert("작성된 리뷰가 없습니다.");
        location.href = "/html/list.html";
        return;
    }

    try {
        const movieResponse = await fetch(`${API_BASE_URL}/movies/${movieId}`);

        if (!movieResponse.ok) {
            throw new Error("영화 정보 조회 실패");
        }

        const movie = await movieResponse.json();

        renderReviewedMovie(movie, review);

        const analyzeResponse = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                review: review
            })
        });

        if (!analyzeResponse.ok) {
            throw new Error("감성 분석 실패");
        }

        const result = await analyzeResponse.json();

        renderSentimentResult(result);

        const recommendResponse = await fetch(`${API_BASE_URL}/recommend`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                movie_title: movie.title,
                top_n: 5
            })
        });

        if (!recommendResponse.ok) {
            throw new Error("추천 영화 조회 실패");
        }

        const recommendData = await recommendResponse.json();

        renderRecommendations(recommendData.recommendations || []);

    } catch (error) {
        console.error(error);
        alert("분석 결과를 불러오지 못했습니다.");
    }
}

function renderReviewedMovie(movie, review) {
    const poster = document.getElementById("reviewedMoviePoster");
    const title = document.getElementById("reviewedMovieTitle");
    const genre = document.getElementById("reviewedMovieGenre");
    const reviewText = document.getElementById("reviewText");

    poster.src = movie.poster_url || movie.posterUrl || "/images/no-image.png";
    poster.alt = `${movie.title} 포스터`;

    title.textContent = movie.title || "영화 제목";
    genre.textContent = movie.genre || "장르 없음";
    reviewText.textContent = review;
}

function renderSentimentResult(result) {
    const positiveProb = result.positive_prob || 0;
    const positivePercent = Math.round(positiveProb * 100);
    const negativePercent = 100 - positivePercent;
    const sentiment = result.sentiment || "-";
    const expectedRating = result.expected_rating || 0;

    const isPositive = sentiment === "긍정";

    const sentimentText = document.getElementById("sentimentText");
    const progressFill = document.getElementById("progressFill");
    const sentimentFace = document.getElementById("sentimentFace");

    sentimentFace.textContent = isPositive ? "😊" : "😢";
    sentimentFace.className = isPositive ? "face positive-face" : "face negative-face";

    sentimentText.textContent = isPositive ? "긍정리뷰" : "부정리뷰";
    sentimentText.className = isPositive ? "positive-text" : "negative-text";

    progressFill.style.width = `${positivePercent}%`;
    progressFill.style.background = isPositive ? "linear-gradient(90deg,#22c55e,#47e07e)" : "linear-gradient(90deg,#ef4444,#ff6b6b)";

    document.getElementById("sentimentLabel").textContent = sentiment;

    document.getElementById("positivePercent").textContent = positivePercent;
    document.getElementById("positiveRatio").textContent = positivePercent;
    document.getElementById("positiveStandard").textContent = positivePercent;

    document.getElementById("negativeRatio").textContent = negativePercent;
    document.getElementById("negativeStandard").textContent = negativePercent;

    document.getElementById("expectedRating").textContent = Number(expectedRating).toFixed(1);

}

function renderRecommendations(recommendations) {
    const recommendGrid = document.getElementById("recommendGrid");

    if (!recommendations || recommendations.length === 0) {
        recommendGrid.innerHTML = `<p style="color:#999;">추천 영화가 없습니다.</p>`;
        return;
    }

    recommendGrid.innerHTML = "";

    recommendations.forEach(movie => {
        const movieId = movie.id;
        const title = movie.title || movie["영화제목"] || "영화 제목";
        const genre = movie.genre || movie["장르"] || "장르 없음";
        const posterUrl = movie.poster_url || movie.posterUrl || "/images/no-image.png";
        const matchScore = movie.match_score || movie["매칭률(%)"] || 0;

        const card = document.createElement("a");
        card.className = "recommend-card";

        if (movieId) {
            card.href = `/html/detail.html?id=${movieId}`;
        } else {
            card.href = "#";
        }

        card.innerHTML = `
            <img src="${posterUrl}" alt="${title} 포스터">

            <div class="recommend-info">
                <h3>${title}</h3>

                <div class="recommend-rating">
                    🎬 ${genre}
                </div>

                <div class="recommend-match">
                    🔥 매칭률 ${matchScore}%
                </div>
            </div>
        `;

        recommendGrid.appendChild(card);
    });
}