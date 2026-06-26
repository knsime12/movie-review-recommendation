const analyzeBtn = document.getElementById("analyzeBtn");
const reviewInput = document.getElementById("reviewInput");
const resultBox = document.getElementById("resultBox");

analyzeBtn.addEventListener("click", async () => {
    const review = reviewInput.value;

    const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            review: review
        })
    });

    const data = await response.json();

    resultBox.innerHTML = `
        <h3>분석결과</h3>
        <p><strong>감성:</strong> ${data.sentiment}</p>
        <p><strong>긍정 확률:</strong> ${(data.positive_prob * 100).toFixed(1)}%</p>
        <p><strong>예상 평점:</strong> ${data.expected_rating}점</p>
        <p><strong>키워드:</strong> ${data.keywords.join(", ")}</p>
    `;
});

