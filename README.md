# CineFeel

FastAPI 기반 영화 리뷰 감성분석 및 콘텐츠 기반 영화 추천 웹서비스입니다.

기존 팀 프로젝트의 UI/UX 흐름은 유지하고, 백엔드는 Java 기반 구조에서 FastAPI 기반으로 새롭게 구현했습니다.
사용자 리뷰를 분석해 감성, 예상 평점, 핵심 키워드를 추출하고, 기준 영화와 유사한 영화를 추천합니다.
추천 결과에는 OpenAI API를 활용한 짧은 추천 기준 설명을 제공합니다.

---

## 주요 기능

- 영화 리뷰 감성분석
- 긍정 확률 기반 예상 평점 계산
- 리뷰 핵심 키워드 추출
- 콘텐츠 기반 영화 추천
- OpenAI API 기반 추천 기준 요약
- 영화 조회, 리뷰 저장, 추천 이력 관리 API
- Docker Compose 기반 FastAPI + MySQL 개발 환경 구성
- 유닛 테스트 및 스모크 테스트 구성

---

## 기술 스택

- Backend: Python, FastAPI, Uvicorn, PyMySQL
- ML/NLP: scikit-learn, TF-IDF, Logistic Regression, KoNLPy(Okt)
- Recommendation: Cosine Similarity, Linear Kernel
- Database: MySQL 8.0, Docker Compose
- LLM: OpenAI API
- Test: pytest, FastAPI TestClient, mock

---

## 데이터셋

### 모델 학습
- NSMC 영화 리뷰 데이터

### 웹 서비스
- 영화 메타데이터 982건

---

## 모델 성능

| Metric | Score |
|---|---:|
| Accuracy | 79.78% |
| Precision | 0.80 |
| Recall | 0.80 |
| F1-score | 0.80 |

※ 감성분석 모델은 TF-IDF 벡터화와 Logistic Regression을 사용했습니다.

---

## 백엔드 구조

```text
backend/
├─ routers/      # API 엔드포인트
├─ services/     # 감성분석, 추천, 리뷰, 유저 서비스 로직
├─ core/         # 모델 로딩, 경로 관리
├─ data/         # 영화 데이터 로딩
├─ utils/        # 전처리, DB 유틸
├─ scripts/      # schema.sql, import_movies.py
├─ models/       # 학습된 모델과 추천 행렬
├─ database.py
└─ main.py
```

---

## 핵심 로직

### 감성분석

```text
사용자 리뷰
    ↓
텍스트 전처리
    ↓
TF-IDF 벡터화
    ↓
Logistic Regression 예측
    ↓
긍정 확률 계산
    ↓
예상 평점 생성
    ↓
핵심 키워드 추출
```

응답 예시:

```json
{
    "review": "영화가 감동적이고 음악이 좋았다.",
    "sentiment": "긍정",
    "positive_prob": 0.85,
    "expected_rating": 4.0,
    "keywords": ["감동", "음악"]
}
```

---

### 영화 추천

```text
영화 정보
(장르, 줄거리, 배우, 감독)
    ↓
코사인 유사도 계산
    ↓
가중합 점수 계산
    ↓
추천 영화 목록 반환
```

추천 가중치:

|요소|가중치|
|---|---|
|장르|0.35|
|줄거리|0.35|
|배우|0.20|
|감독|0.10|

응답 예시:

```json
{
    "success": true,
    "title": "인터스텔라",
    "recommendations": [
        {
            "id": 1,
            "title": "마션",
            "genre": "SF",
            "poster_url": "https://...",
            "match_score": 92.5
        }
    ]
}
```

---

## LLM 추천 기준 설명

OpenAI API를 사용해 추천 기준을 짧게 요약합니다.

응답 예시:

```json
{
    "success": true,
    "summary": "감동·드라마 유사도 기반 추천",
    "criteria": [
        "긍정 감성이 높아 비슷한 만족감을 줄 수 있는 영화를 고려했습니다.",
        "리뷰 키워드는 사용자의 감상 포인트를 이해하는 보조 근거로 활용했습니다.",
        "추천은 기준 영화와의 장르, 줄거리, 배우, 감독 유사도를 반영했습니다."
    ]
}
```

※ `OPENAI_API_KEY`는 서버 환경변수로만 관리하며, 테스트에서는 실제 API를 호출하지 않고 mock을 사용합니다.

---

## 주요 API

|Method|URL|설명|
|---|---|---|
|POST|`/analyze`|리뷰 감성분석|
|POST|`/recommend`|영화 추천|
|POST|`/recommendation-explanation`|추천 기준 설명|
|GET| `/movies` | 영화 목록 조회 |
|GET| `/movies/{movie_id}` | 영화 상세 조회 |
|POST|`/reviews`|리뷰 저장|
|GET|`/users/{user_id}/reviews`|사용자 리뷰 조회|
|POST|`/recommendation-history`|추천 이력 저장|
|GET|`/users/{user_id}/recommendations`|사용자 추천 이력 조회|

---

## 실행 방법

### 1. 패키지 설치

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

※ KoNLPy(Okt)를 사용하므로 로컬 환경에 Java가 필요할 수 있습니다.

### 2. Docker compose 실행

```powershell
docker compose up -d
```

Docker Compose로 FastAPI app 서버와 MySQL 서버를 함께 실행합니다.

```text
http://localhost:8000 -> cinefeel-app:8000
localhost:3307 -> cinefeel-mysql:3306
```

---

### 3. 영화 데이터 import

Docker Compose 실행 시 `movie-importer` 컨테이너가 한 번 실행되어 영화 데이터를 MySQL에 저장합니다.

```powershell
docker logs cinefeel-movie-importer
```

정상 실행 시 아래 로그가 출력됩니다.

```text
영화 데이터 982건 저장 완료
```

수동으로 다시 import 하려면 아래 명령어를 실행합니다.

```powershell
docker compose run --rm movie-importer
```

데이터 확인:

```powershell
docker exec -it cinefeel-mysql mysql -uroot -p1234 cinefeel -e "SELECT COUNT(*) FROM movies;"
```

기대 결과:

```text
982
```

### 4. 로컬 서버 실행 ※ 선택사항

※ Docker Compose로 실행 중이면 별도로 로컬 서버를 실행하지 않아도 됩니다.

```powershell
uvicorn main:app --reload --app-dir backend
```

API 문서:

```text
http://127.0.0.1:8000/docs
```

---

## 환경변수

| 이름 | 설명 |
|---|---|
| `DB_HOST` | MySQL 호스트 |
| `DB_PORT` | MySQL 포트 |
| `DB_USER` | MySQL 사용자 |
| `DB_PASSWORD` | MySQL 비밀번호 |
| `DB_NAME` | MySQL DB 이름 |
| `OPENAI_API_KEY` | OpenAI API Key |
| `OPENAI_EXPLANATION_MODEL` | 추천 기준 설명 모델 |

---

## 테스트

```powershell
python -m pytest
```

※ 스모크 테스트는 로컬 서버 실행 후 별도로 수행합니다.

```powershell
$env:RUN_SMOKE_TESTS="true"
python -m pytest tests/test_api_smoke.py
```

---

## 개선 예정

- 사용자 비밀번호 해싱 적용
- 배포 환경용 환경변수 관리 정리
- 모델/데이터 인코딩 정리