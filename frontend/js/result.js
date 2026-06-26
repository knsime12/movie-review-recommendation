const savedData = sessionStorage.getItem("analysisResult");

const movieTitle = document.getElementById("movieTitle");
const movieGenre = document.getElementById("movieGenre");
const reviewText = document.getElementById("reviewText");

const sentimentFace = document.getElementById("sentimentFace");
const sentimentText = document.getElementById("sentimentText");
const positivePercent = document.getElementById("positivePercent");
const progressFill = document.getElementById("progressFill");
const positiveRatio = document.getElementById("positiveRatio");
const negativeRatio = document.getElementById("negativeRatio");

const sentimentLabel = document.getElementById("sentimentLabel");
const positiveStandard = document.getElementById("positiveStandard");
const negativeStandard = document.getElementById("negativeStandard");
const expectedRating = document.getElementById("expectedRating");

const recommendGrid = document.getElementById("recommendGrid");

if (!savedData) {
    alert("분석 결과가 없습니다.");
    location.href = "./list.html";
} else {
    const data = JSON.parse(savedData);

    const movie = data.movie;
    const review = data.review;
    const analysis = data.analysis;

    const positive = Math.round(analysis.positive_prob * 100);
    const negative = 100 - positive;

    movieTitle.textContent = movie.title || "-";
    movieGenre.textContent = movie.genre || "-";
    reviewText.textContent = review || "-";

    positivePercent.textContent = positive;
    positiveRatio.textContent = positive;
    negativeRatio.textContent = negative;

    positiveStandard.textContent = positive;
    negativeStandard.textContent = negative;

    expectedRating.textContent = analysis.expected_rating || "0.0";

    progressFill.style.width = `${positive}%`;

    sentimentLabel.textContent = analysis.sentiment;

    if (analysis.sentiment === "긍정") {
        sentimentFace.textContent = "😊";
        sentimentFace.classList.add("positive-face");

        sentimentText.textContent = "긍정 리뷰";
        sentimentText.classList.add("positive-text");
    } else {
        sentimentFace.textContent = "😢";
        sentimentFace.classList.add("negative-face");

        sentimentText.textContent = "부정 리뷰";
        sentimentText.classList.add("negative-text");
    }

    loadRecommendations(movie.title);
}

async function loadRecommendations(title) {
    try {
        const response = await fetch("http://127.0.0.1:8000/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                movie_title: title,
                top_n: 4
            })
        });

        const data = await response.json();

        const recommendations = data.recommendations || [];

        if (recommendations.length === 0) {
            recommendGrid.innerHTML = `
                <p style="color:#999;">추천 영화가 없습니다.</p>
            `;
            return;
        }

        recommendGrid.innerHTML = "";

        recommendations.forEach(movie => {
            const card = document.createElement("a");
            card.className = "recommend-card";

            if (movie.id) {
                card.href = `./detail.html?id=${movie.id}`;
            } else {
                card.href = "./list.html";
            }

            card.innerHTML = `
                <img src="${movie.poster_url || 'https://via.placeholder.com/240x320?text=No+Image'}"
                    alt="추천 영화 포스터">

                <div class="recommend-info">
                    <h3>${movie.title || "제목 없음"}</h3>

                    <div class="recommend-rating">
                        ${movie.genre || "장르 정보 없음"}
                    </div>

                    <div class="recommend-match">
                        🔥 매칭률
                        <span>${movie.match_score || 0}</span>%
                    </div>
                </div>
            `;

            recommendGrid.appendChild(card);
        });

    } catch (error) {
        console.error(error);

        recommendGrid.innerHTML = `
            <p style="color:#999;">추천 영화를 불러오지 못했습니다.</p>
        `;
    }
}