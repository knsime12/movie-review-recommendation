import json

from services.llm_explanation_service import generate_recommendation_explanation


class FakeResponses:
    def __init__(self):
        self.create_calls = []

    def create(self, model, input):
        self.create_calls.append(
            {
                "model": model,
                "input": input,
            }
        )

        class FakeResponse:
            output_text = json.dumps(
                {
                    "summary": "리뷰 감성과 기준 영화의 유사도를 바탕으로 추천 결과를 설명했습니다.",
                    "criteria": [
                        "리뷰 키워드는 사용자의 감상 포인트를 이해하는 보조 근거로 사용했습니다.",
                        "추천 영화는 기준 영화와의 장르, 줄거리, 배우, 감독 유사도를 바탕으로 선정되었습니다.",
                        "긍정 감성이 높아 비슷한 만족감을 줄 수 있는 추천 결과를 자연스럽게 설명했습니다.",
                    ],
                },
                ensure_ascii=False,
            )

        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_generate_recommendation_explanation_uses_review_keywords_as_supporting_context():
    fake_client = FakeClient()

    request_data = {
        "review": "스토리가 감동적이고 정말 좋았다",
        "sentiment": "긍정",
        "positive_prob": 0.8,
        "expected_rating": 4,
        "keywords": ["스토리", "감동"],
        "base_movie_title": "인터스텔라",
        "recommendations": [
            {
                "title": "그래비티",
                "genre": "SF",
                "match_score": 87.5,
            }
        ],
    }

    result = generate_recommendation_explanation(
        request_data,
        client=fake_client,
        model="test-model",
    )

    assert result["success"] is True
    assert "summary" in result
    assert len(result["criteria"]) == 3

    prompt = fake_client.responses.create_calls[0]["input"]

    assert "keywords는 사용자가 작성한 리뷰 원문에서 추출된 핵심 키워드" in prompt
    assert "현재 추천 알고리즘은 keywords를 직접 사용해서 영화를 고르지 않는다" in prompt
    assert "장르, 줄거리, 배우, 감독 유사도" in prompt
    assert "summary는 35자 이내" in prompt
    assert "summary에서 사용자가 쓴 리뷰 문장을 그대로 반복하지 마라" in prompt