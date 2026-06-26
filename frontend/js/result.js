const API_BASE_URL = "";

document.addEventListener("DOMContentLoaded", () => {
    loadResult();
});

async function loadResult() {
    const review = sessionStorage.getItem("review");
    const movieId = sessionStorage.getItem("movieId");

    if (!review || !movieId) {
        alert("작성된 리뷰가 없습니다.");
        location.href = "/html/list.html";
        return;
    }

    try {
        // 1. 영화 정보 조회
        const movieResponse = await fetch(`${API_BASE_URL}/movies/${movieId}`);

        if (!movieResponse.ok) {
            throw new Error("영화 정보 조회 실패");
        }

        const movie = await movieResponse.json();

        // 2. 감성 분석
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

        console.log("감성 분석 결과:", result);

        const positiveProb = result.positive_prob || 0;
        const positivePercent = Math.round(positiveProb * 100);
        const negativePercent = 100 - positivePercent;
        const sentiment = result.sentiment || "-";
        const expectedRating = result.expected_rating || 0;

        // 3. 결과 화면 출력
        const isPositive = sentiment === "긍정";

        document.getElementById("sentimentFace").textContent = isPositive ? "😊" : "😢";
        document.getElementById("sentimentText").textContent = isPositive ? "긍정 리뷰" : "부정 리뷰";
        document.getElementById("sentimentLabel").textContent = sentiment;

        document.getElementById("positivePercent").textContent = positivePercent;
        document.getElementById("positiveRatio").textContent = positivePercent;
        document.getElementById("positiveStandard").textContent = positivePercent;

        document.getElementById("negativeRatio").textContent = negativePercent;
        document.getElementById("negativeStandard").textContent = negativePercent;

        document.getElementById("expectedRating").textContent = expectedRating;

        const progressFill = document.getElementById("progressFill");
        progressFill.style.width = `${positivePercent}%`;

        // 4. 추천 영화 조회
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

        console.log("추천 결과:", recommendData);

        renderRecommendations(recommendData.recommendations || []);

    } catch (error) {
        console.error(error);
        alert("분석 결과를 불러오지 못했습니다.");
    }
}

function renderRecommendations(recommendations) {
    const recommendGrid = document.getElementById("recommendGrid");

    if (!recommendations || recommendations.length === 0) {
        recommendGrid.innerHTML = `<p style="color:#999;">추천 영화가 없습니다.</p>`;
        return;
    }

    recommendGrid.innerHTML = "";

    recommendations.forEach(movie => {
        const title = movie["영화제목"] || movie.title || "영화 제목";
        const genre = movie["장르"] || movie.genre || "장르 없음";
        const matchScore = movie["매칭률(%)"] || movie.match_score || 0;
        const posterUrl = movie.poster_url || movie.posterUrl || "";
        const movieID  = movie.id || "";

        const card = document.createElement("a");
        card.className = "recommend-card";
        card.href = `/html/detail.html?id=${movieId}`;
        card.style.textDecoration = "none";
        card.style.color = "inherit";

        card.innerHTML = `
            ${posterUrl ? `<img src="${posterUrl}" alt="추천 영화 포스터">` : ""}
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