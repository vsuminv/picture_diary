# Picture Diary — 여행 야경 일기 자동 시각화 파이프라인

> GitHub: https://github.com/vsuminv/picture_diary

여행 일기 텍스트를 입력하면 GPT-4o-mini가 핵심 장면을 추출하고, DALL-E 3가 여행 야경 이미지를 자동 생성하는 멀티 LLM 파이프라인입니다.  
`일기 텍스트 → 장면 추출(GPT-4o-mini) → 이미지 생성(DALL-E 3)` 순서로 파이프라인이 동작합니다.

---

## 빠른 시작

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. .env 파일에 API 키 설정
# OPENAI_API_KEY=sk-...
# FAL_KEY=...

# 3. 파이프라인 실행
python pipeline.py
```

> `domains/travel_prompts.json` 이 없으면 GPT-4o-mini가 자동 생성합니다.  
> 따로 생성하려면: `python generate_domain_prompts.py`

---

## 결과 미리보기

| 장면 | 생성 파일 |
|------|-----------|
| 도시 야경 (시부야 교차로) | `outputs/travel_1.png` |
| 강변 반사 야경 | `outputs/travel_2.png` |
| 별밤 아래 마을 | `outputs/travel_3.png` |
| 골든아워 vs 블루아워 비교 | `outputs/travel_golden_hour.png` / `outputs/travel_blue_hour.png` |

---

## 파일 구조

```text
picture_diary/
├── .env                           ← API 키 (⛔ 커밋 금지)
├── .gitignore
├── README.md
├── requirements.txt
├── pipeline.py                    ← 전체 파이프라인 진입점
├── generate_domain_prompts.py     ← GPT-4o-mini로 도메인 JSON 자동 생성
├── agents/
│   ├── __init__.py
│   ├── scene.py                   ← 일기 → 장면 추출 (extract_scenes)
│   ├── image.py                   ← 장면 → 이미지 생성 (generate_image)
│   └── video.py                   ← 이미지 → 영상 생성 (generate_video)
├── domains/                       ← GPT가 자동 생성하는 도메인 설정 JSON
│   ├── travel_prompts.json
│   └── emoji_prompts.json
├── day5_01_product_catalog.py
├── day5_02_emoticons.py
├── day5_03_travel_blog.py         ← golden_hour vs blue_hour 비교
├── week7_retrospective.md
└── outputs/                       ← 생성 결과물 (gitignore 처리)
```

---

## 도메인 응용 — 여행 야경

선택 도메인: **travel**

| 프롬프트 어휘 | 설정값 |
|-------------|--------|
| shot | cinematic wide shot |
| angle | eye-level |
| lighting | city night lights, moonlight, long exposure glow |
| lens | 24mm wide-angle lens, photorealistic 8K |
| mood | atmospheric, breathtaking, cinematic |
| 시간대 변형 | `golden_hour` vs `blue_hour` 비교 (`day5_03_travel_blog.py`) |

`generate_domain_prompts.py`가 GPT-4o-mini를 호출하여 도메인 JSON을 자동 생성합니다.  
수동으로 작성하지 않으며, `pipeline.py` 실행 시 파일이 없으면 자동으로 생성됩니다.

---

## 보안 체크리스트

- [x] `.env` 파일이 `.gitignore`에 등록되어 Git에 커밋되지 않음
- [x] 모든 API 키는 `load_dotenv()` + `os.getenv()`로만 로드
- [x] 코드 어디에도 API 키가 하드코딩되지 않음
- [x] README에 실제 API 키 값(`sk-` 패턴) 없음
