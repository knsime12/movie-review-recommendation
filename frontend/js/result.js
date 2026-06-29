const API_BASE_URL = "";
const NO_IMAGE_URL =
    "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=800";

document.addEventListener("DOMContentLoaded", () => {
    loadResult();
});

async function saveRecommendationHistory(baseMovieId, recommendations) {
    const userId = Number(sessionStorage.getItem("userId"));

    if (!userId || recommendations.length === 0) {
        return;
    }

    for (const movie of recommendations) {
        const recommendedMovieId = movie.id || movie.movie_id;

        if (!recommendedMovieId) {
            console.warn("recommended movie id 없음:", movie);
            continue;
        }

        const similarity = 
            movie.match_rate ||
            movie.match_score || 
            movie.similarity ||
            movie["매칭률(%)"] || 
            0;

        const payload = {
            user_id: userId,
            base_movie_id: Number(baseMovieId),
            recommended_movie_id: Number(recommendedMovieId),
            similarity: Number(similarity)
        };

        console.log("recommendation payload =", JSON.stringify(payload, null, 2));

        try {
            const response = await fetch(`${API_BASE_URL}/recommendation-history`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json().catch(() => null);

            console.log("recommendation history status =", JSON.stringify(result, null, 2));
            console.log("recommendation history save result =", result);

            if (!response.ok || result?.success === false) {
                console.warn("추천 이력 저장 실패:", result);
            }

        } catch (error) {
            console.warn("추천 이력 저장 요청 실패:", error);
        }
    }
}

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
        console.log("1. result.js 시작");

        const movieResponse = await fetch(`${API_BASE_URL}/movies/${movieId}`);

        if (!movieResponse.ok) {
            throw new Error("영화 정보 조회 실패");
        }

        const movie = await movieResponse.json();
        console.log("2. movie result", movie);

        renderReviewedMovie(movie, review);

        const analyzeResponse = await fetch(`${API_BASE_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                content: review
            })
        });

        if (!analyzeResponse.ok) {
            throw new Error("감성분석 실패");
        }

        const result = await analyzeResponse.json();
        console.log("3. analyze result", result);

        renderSentimentResult(result);

        console.log("4. saveReview 실행 직전");

        await saveReview(movieId, review, result);

        console.log("5. saveReview 완료");

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

        const recommendResult = await recommendResponse.json();
        console.log("6. recommend result", recommendResult);

        renderRecommendations(recommendResult.recommendations || []);

        await saveRecommendationHistory(movieId, recommendResult.recommendations || []);

    } catch (error) {
        console.error("result.js error:", error);
        alert("결과 페이지 처리 중 오류가 발생했습니다.");
    }
}

function renderReviewedMovie(movie, review) {
    const poster = document.querySelector("#reviewedMoviePoster");
    const title = document.querySelector("#reviewedMovieTitle");
    const genre = document.querySelector("#reviewedMovieGenre");
    const content = document.querySelector("#reviewContent");

    if (poster) {
        poster.src = movie.poster_url || movie.posterUrl || NO_IMAGE_URL;
        poster.onerror = () => {
            poster.src = NO_IMAGE_URL;
        };
    }

    if (title) {
        title.textContent = movie.title || "영화 제목";
    }

    if (genre) {
        genre.textContent = movie.genre || "장르 정보 없음";
    }

    if (content) {
        content.textContent = review;
    }
}

function renderSentimentResult(result) {
    const positiveProb = Number(result.positive_prob || 0);
    const positivePercent = Math.round(positiveProb * 100);
    const negativePercent = 100 - positivePercent;

    const sentiment = result.sentiment || "-";
    const rating = result.expected_rating || "-";

    setText("#sentimentText", `${sentiment} 리뷰`);
    setText("#sentimentLabel", sentiment);

    setText("#positivePercent", positivePercent);
    setText("#positiveRatio", positivePercent);
    setText("#positiveStandard", positivePercent);

    setText("#negativeRatio", negativePercent);
    setText("#negativeStandard", negativePercent);

    setText("#expectedRating", rating);

    renderResultKeywords(result.keywords || []);

    const face = document.querySelector("#sentimentFace");
    if (face) {
        face.classList.remove("positive-face", "negative-face");

        if (sentiment === "긍정") {
            face.textContent = "😊";
            face.classList.add("positive-face");
        } else {
            face.textContent = "😢";
            face.classList.add("negative-face");
        }
    }

    const progressFill = document.querySelector("#progressFill");
    if (progressFill) {
        progressFill.style.width = `${positivePercent}%`;
    }
}

async function saveReview(movieId, review, result) {
    const saveKey = `savedReview_${movieId}_${review}`;

    if (sessionStorage.getItem(saveKey)) {
        console.log("review save skip: 이미 저장됨");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/reviews`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                movie_id: Number(movieId),
                user_id: Number(sessionStorage.getItem("userId")),
                content: review,
                sentiment: result.sentiment,
                positive_prob: result.positive_prob,
                expected_rating: result.expected_rating,
                keywords: result.keywords || []
            })
        });

        const saveResult = await response.json().catch(() => null);

        console.log("reviews status =", response.status);
        console.log("review save result =", saveResult);
        console.log("review save error =", saveResult?.error);

        if (!response.ok || saveResult?.success === false) {
            console.warn("리뷰 저장 실패:", saveResult);
            return;
        }

        sessionStorage.setItem(saveKey, "true");

    } catch (error) {
        console.warn("리뷰 저장 요청 실패:", error);
    }
}

function renderRecommendations(recommendations) {
    const recommendGrid = document.querySelector("#recommendGrid");

    if (!recommendGrid) {
        console.warn("recommendGrid 요소 없음");
        return;
    }

    recommendGrid.innerHTML = "";

    recommendations.forEach(movie => {
        const title = movie.title || movie.영화제목;
        const genre = movie.genre || movie.장르 || "장르 정보 없음";
        const matchRate = 
            movie.match_rate || 
            movie.match_score ||
            movie.similarity ||
            movie["매칭률(%)"] || 
            0;

        const movieId = movie.id || movie.movie_id;

        const card = document.createElement("a");
        card.className = "recommend-card";
        card.href = movieId
            ? `/html/detail.html?id=${movieId}`
            : "#";

        card.innerHTML = `
            <img src="${movie.poster_url || movie.posterUrl || NO_IMAGE_URL}" 
                 alt="추천 영화 포스터"
                 onerror="this.src='${NO_IMAGE_URL}'">

            <div class="recommend-info">
                <h3>${title}</h3>
                <p>${genre}</p>
                <div class="recommend-match">
                    🔥 매칭률 ${matchRate}%
                </div>
            </div>
        `;

        recommendGrid.appendChild(card);
    });
}

function setText(selector, value) {
    const element = document.querySelector(selector);

    if (element) {
        element.textContent = value;
    }
}

function renderResultKeywords(keywords) {
    const keywordList = document.querySelector("#resultKeywordList");

    if (!keywordList) {
        return;
    }

    keywordList.innerHTML = "";

    if (!Array.isArray(keywords) || keywords.length === 0) {
        keywordList.innerHTML = `<span class="empty-keyword">키워드 없음</span>`;
        return;
    }

    keywords.forEach(keyword => {
        const span = document.createElement("span");
        span.textContent = keyword;
        keywordList.appendChild(span);
    });
}