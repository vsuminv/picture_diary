# Picture Diary — 그림일기 시각화 파이프라인

> GitHub: https://github.com/vsuminv/picture_diary

Picture Diary는 텍스트를 기반으로 여행/제품 이미지를 생성하는 LLM 파이프라인입니다.  

한강 노을을 바라보는 그림일기, 제품 카탈로그 이미지, 그리고 여행 블로그(도시 야경/시간대 변화) 장면을 입력하면  
GPT-4o-mini가 핵심 장면을 추출하고 OpenAI 이미지 모델을 통해 시각적인 이미지로 변환합니다.

`일기 텍스트 → 장면 추출 → 이미지 및 동영상 생성` 순서로 파이프라인이 동작합니다.

---

## 빠른 시작

### 1. 패키지 설치
- pip install -r requirements.txt

### 2. .env 파일에 API 키 설정
- OPENAI_API_KEY=sk-...

### 3. 빠른 실행 - 파이프라인 실행
- **그림일기 실행**: `python pipeline.py`
- **제품 실행**: `python day5_01_product_catalog.py`
- **여행 블로그 실행**: `python day5_03_travel_blog.py`

---

## 결과 미리보기

| 장면 | 생성 파일 | 이미지 |
|------|-----------|-----------|
| 그림일기1 | `outputs/picture_diary_1.png` |<img width="200" height="200" alt="Image" src="https://github.com/user-attachments/assets/c5975459-b038-4ae5-9874-66642fa09c08" />|
| 그림일기2 | `outputs/picture_diary_2.png` |<img width="200" height="200" alt="Image" src="https://github.com/user-attachments/assets/10703f4c-8fa2-462e-8d4a-6c05e27156a5" />|
| 제품사진 | `outputs/product_laptop.png` |<img width="200" height="200" alt="Image" src="https://github.com/user-attachments/assets/b48a04b1-1ae1-4807-8383-9f03c9b58aba" />|
| 파리 에펠탑 골든아워 | `outputs/travel_1.png` |<img width="200" height="200" alt="Image" src="https://github.com/user-attachments/assets/a4b100ad-1299-4409-bae7-7fc77d6ce0e5" />|
| 파리 에펠탑 블루아워 | `outputs/travel_2.png` |<img width="200" height="200" alt="Image" src="https://github.com/user-attachments/assets/18c6264f-8aa8-4db6-bf80-d600a3aff798" />|
---

## 파일 구조

```text
picture_diary/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── pipeline.py                  ← 여행 그림일기 전체 파이프라인
├── agents/
│   ├── scene.py                 ← GPT 장면 추출
│   ├── image.py                 ← OpenAI 이미지 생성
│   └── video.py                 ← (추후) 이미지 → 영상 생성
├── day5_01_product_catalog.py   ← 제품 이미지 생성
├── day5_03_travel_blog.py      ← 시간대 비교 (golden/blue)
├── domains/
│   ├── travel_prompts.json
│   └── product_prompts.json
└── outputs/
    ├── picture_diary_1.png
    ├── picture_diary_2.png
    ├── product_laptop.png
    ├── travle_1.png           ← 시간대 비교 (golden)
    └── travle_2.png           ← 시간대 비교 (blue)
```

---

## 도메인 응용 — 여행 블로그

선택 도메인: **travel**

| 프롬프트 어휘 | 설정값 |
|-------------|--------|
| shot | cinematic wide shot |
| angle | eye-level |
| lighting | city night lights, moonlight, long exposure glow |
| lens | 24mm wide-angle lens, photorealistic 8K |
| mood | atmospheric, breathtaking, cinematic |
| 시간대 변형 | `golden_hour` vs `blue_hour` 비교 (`day5_03_travel_blog.py`) |

---

## 보안 체크리스트

- [✅] `.env` 파일이 `.gitignore`에 등록되어 Git에 커밋되지 않음
- [✅] 모든 API 키는 `load_dotenv()` + `os.getenv()`로만 로드
- [✅] 코드 어디에도 API 키가 하드코딩되지 않음
- [✅] README에 실제 API 키 값(`sk-` 패턴) 없음
