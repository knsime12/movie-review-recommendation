import json
import os

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_EXPLANATION_MODEL", "gpt-5.4-nano")


def _build_prompt(data):
    return f"""
너는 영화 추천 서비스 CineFeel의 추천 결과를 설명하는 AI야.

아래 데이터를 바탕으로 사용자가 이해하기 쉬운 한국어 설명을 만들어줘.

반드시 지켜야 할 사실:
- keywords는 추천 영화의 키워드가 아니다.
- keywords는 사용자가 작성한 리뷰 원문에서 추출된 핵심 키워드다.
- 현재 추천 알고리즘은 keywords를 직접 사용해서 영화를 고르지 않는다.
- 추천 영화는 기준 영화와의 장르, 줄거리, 배우, 감독 유사도를 바탕으로 선정된다.
- keywords는 사용자가 어떤 감상 포인트를 중요하게 느꼈는지 설명하는 보조 근거로만 사용해라.
- 입력 데이터에 없는 내용을 지어내지 마라.

응답은 반드시 아래 JSON 형식만 사용해라.

summary 작성 규칙:
- summary는 화면의 "추천 기준" 칸에 들어갈 짧은 문장이다.
- summary는 35자 이내로 작성해라.
- summary에는 줄바꿈을 넣지 마라.
- summary에는 따옴표를 넣지 마라.
- summary에는 "~ 기반 추천" 또는 "~ 중심 추천" 처럼 간결한 추천 기준 문장으로 작성해라.
- summary에서 사용자가 쓴 리뷰 문장을 그대로 반복하지 마라.

criteria 작성 규칙:
- criteria는 추천 이유를 설명하는 문장 3개다.
- 각 문장은 60자 이내로 작성해라.
- keywords가 추천 알고리즘에 직접 사용된 것처럼 말하지 마라.
- keywords는 사용자의 감상 포인트를 설명하는 보조 근거로만 언급해라.

{{
    "summary": "감성·장르 유사도 기반 추천",
    "criteria": [
        "긍정 감성이 높아 비슷한 만족감을 줄 수 있는 영화를 고려했습니다.",
        "리뷰 키워드는 사용자의 감상 포인트를 이해하는 데 참고했습니다.",
        "추천은 기준 영화와의 장르, 줄거리, 배우, 감독 유사도를 반영했습니다."
    ]
}}

입력 데이터:
{json.dumps(data, ensure_ascii=False)}
""".strip()


def _parse_response_text(text):
    parsed = json.loads(text)
    
    return {
        "success": True,
        "summary": parsed["summary"],
        "criteria": parsed["criteria"]
    }
    
    
def generate_recommendation_explanation(request_data, client=None, model=DEFAULT_MODEL):
    client = client or OpenAI()
    
    response = client.responses.create(
        model=model,
        input=_build_prompt(request_data)
    )
    
    return _parse_response_text(response.output_text)