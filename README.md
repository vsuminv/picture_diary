# Picture Diary — 여행 야경 일기 자동 시각화 파이프라인

여행 일기 텍스트를 입력하면 AI가 핵심 장면을 추출하고, DALL-E 3 또는 Flux로 여행 야경 이미지를 자동 생성하는 멀티 LLM 파이프라인입니다.

## 빠른 시작

패키지 설치:

```bash
uv sync
# 또는
pip install -r requirements.txt
```

`.env` 파일에 API 키 설정:

```env
OPENAI_API_KEY=your_openai_key_here
FAL_KEY=your_fal_key_here
```

파이프라인 실행:

```bash
python pipeline.py
```

## 결과 미리보기

| 장면 | 파일 |
|------|------|
| 시부야 야경 (blue_hour) | `outputs/travel_1.png` |
| 강변 도시 반사 (golden_hour) | `outputs/travel_2.png` |
| 별밤 아래 마을 (midnight) | `outputs/travel_3.png` |
| 시간대 비교 — 골든아워 | `outputs/travel_golden_hour.png` |
| 시간대 비교 — 블루아워 | `outputs/travel_blue_hour.png` |

## 파일 구조

```text
picture_diary/
├── .env                        ← API 키 (커밋 금지)
├── .gitignore
├── README.md
├── requirements.txt
├── pipeline.py                 ← 전체 파이프라인 진입점
├── agents/
│   ├── __init__.py
│   ├── scene.py                ← 일기 → 장면 JSON 추출 (GPT-4o-mini)
│   ├── image.py                ← 장면 → 이미지 생성 (DALL-E 3 / Flux)
│   └── video.py                ← 이미지 → 영상 생성 (stub)
├── domains/
│   ├── travel_prompts.json     ← 여행 야경 도메인 프롬프트
│   └── emoji_prompts.json      ← 이모티콘 도메인 프롬프트
├── day5_01_product_catalog.py  ← 제품 카탈로그 세션 코드
├── day5_02_emoticons.py        ← 이모티콘 세션 코드
├── day5_03_travel_blog.py      ← 여행 블로그 golden_hour vs blue_hour 비교
├── week7_retrospective.md
└── outputs/                    ← 생성된 이미지·영상 (gitignore)
```

## 도메인 응용 — 여행 야경

선택 도메인: **travel**

| 프롬프트 어휘 | 적용값 |
|-------------|--------|
| shot | cinematic wide shot |
| angle | eye-level |
| lighting | city lights, moonlight, long exposure glow |
| lens | 24mm wide-angle, 8K photorealistic |
| mood | atmospheric, breathtaking, cinematic |
| 시간대 변형 | `golden_hour` vs `blue_hour` 비교 (`day5_03_travel_blog.py`) |

## 보안 체크리스트

- [x] `.env` 파일이 `.gitignore`에 등록되어 Git에 커밋되지 않음
- [x] 모든 API 키는 `os.getenv()`로만 로드 (`load_dotenv()` 사용)
- [x] 코드 어디에도 API 키가 하드코딩되지 않음
- [x] README에 실제 API 키 값 없음
