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

{{
    "summary": "추천 이유를 자연스럽게 요약한 한 문장",
    "criteria": [
        "추천 기준 설명 1",
        "추천 기준 설명 2",
        "추천 기준 설명 3"
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