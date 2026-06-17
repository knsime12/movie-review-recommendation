# CineFeel - 영화 리뷰 기반 추천 플랫폼

AI-powered movie recommendation platform using sentiment analysis and content-based filtering

사용자가 작성한 영화 리뷰를 분석하여 감성을 예측하고,
해당 영화와 유사한 영화를 추천하는 AI 기반 영화 추천 플랫폼 입니다.

---

## 프로젝트 소개

단순 평점 기반 추천의 한계를 보완하기 위해 감성 분석과 콘텐츠 기반 추천 시스템을 결합하여 개인화된 영화 추천 서비스를 구현하였습니다.

---

## 데이터셋

### NSMC
- 네이버 영화 리뷰 데이터
- 모델 학습용

### 자체 구축 영화 콘텐츠데이터(982건)
- 영화 메타정보(장르, 줄거리, 배우, 감독 등)
- 웹 서비스용

### 주요 기능

- 영화 리뷰 감성 분석
- 예상 평점 예측
- 리뷰 키워드 추출
- 콘텐츠 기반 영화 추천

---

## 프로젝트 기간

2026.05.11 ~ 2026.05.15

### 프로젝트 인원

5명

### 담당 역할

- 영화 리뷰 데이터 전처리
- TF-IDF 벡터화
- Logistic Regression 기반 감성 분석 모델 개발
- 콘텐츠 기반 추천 알고리즘 구현
- 모델 성능 평가 및 개선

---

## 사용 기술

### Language

- Python

### Data Processing

- Pandas
- NumPy

### NLP / Machine Learning

- TF-IDF
- Logistic Regression
- KoNLPy(Okt)

### Recommendation System

- Cosine Similarity
- Linear Kernel
- Content-Based Filtering

---

## 추천 시스템 구조

### 감성 분석

```text
사용자리뷰
    ↓
전처리
    ↓
TF-IDF 벡터화
    ↓
Logistic Regression
    ↓
감정 예측
    ↓
예상 평점 생성
```

### 영화 추천
```text
영화 정보
(장르, 줄거리, 배우, 감독)
    ↓
각 요소별 벡터화
    ↓
코사인 유사도 계산
    ↓
가중합 점수 계산
    ↓
유사 영화 추천
```

---

## 주요 기능

### 1. 리뷰 감성 분석

사용자가 작성한 영화 리뷰를 분석하여 긍정 또는 부정을 분류합니다.

제공 정보

- 감정 분류
- 긍정 확률
- 예상 평점

### 2. 키워드 추출

리뷰에서 핵심 키워드를 추출하여 사용자의 감상을 요약합니다.

예시
```text
#영상미
#음악
#몰입감
#엔딩
#여운
```

### 3. 영화 추천

입력한 영화와 유사한 영화를 추천합니다.

추천 기준

- 장르 유사도
- 줄거리 유사도
- 배우 유사도
- 감독 유사도

최종 추천 점수
```Python
final_similarity = (
    genre_similarity +
    overview_similarity +
    actor_similarity +
    director_similarity
)
```

---

## 모델 성능

| Metric | Score |
|---------|---------|
| Accuracy | 79.78% |
| Precision | 0.80 |
| Recall | 0.80 |
| F1-Score | 0.80 |

---

## 프로젝트 결과

- 감성 분석 정확도 79.78%
- 리뷰 기반 예상 평점 생성 기능 구현
- 핵심 키워드 추출 기능 구현
- 콘텐츠 기반 영화 추천 기능 구현
- 웹 서비스 연동 완료

---

## 프로젝트 구조

```text
project/
├── models/
│   ├── genre_matrix.pkl
│   ├── overview_matrix.pkl
│   ├── actor_matrix.pkl
│   ├── director_matrix.pkl
│   ├── tfidf_sentiment.pkl
│   └── lr_model.pkl
│
├── common.py
├── sentiment.py
├── recommend.py
├── main.py
│
├── movie_database_unique.csv
└── README.md
```

---

## 기대효과

- 리뷰 기반 개인화 영화 추천 제공
- 감성 분석과 추천 시스템 결합
- 자연어 처리 기반 AI 서비스 구현
- 머신러닝 모델 서비스화 경험 확보

---

## 실행 방법

### 라이브러리 설치

```Bash
pip install pandas numpy scikit-learn konlpy joblib
```

### 프로젝트 실행

```Bash
python main.py
```

---

## 향후 개선 사항

- 딥러닝 기반 감성 분석 모델 적용
- 사용자 선호도 기반 추천 기능 추가
- 실시간 리뷰 데이터 연동
- 웹 서비스 배포 및 사용자 기능 확장
