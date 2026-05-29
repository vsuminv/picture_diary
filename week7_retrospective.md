# Week 7 학습 회고 — 멀티 LLM 파이프라인

# Week 7 Retrospective — Picture Diary Pipeline

## 1. 프로젝트 초기 목표

처음 목표는 다음과 같은 단일 파이프라인이었다.

- 여행 일기 또는 제품 설명 입력
- GPT-4o-mini로 장면 자동 추출
- gpt-image-1.5로 이미지 생성
- 생성된 이미지 중 대표 1장을 선택해 영상으로 변환

즉,

> 텍스트 → 장면 분석 → 이미지 생성 → 영상 생성

까지 자동화하는 멀티 LLM 시각화 시스템 구축이 목표였다.

---

## 2. 초기 예상과 실제 결과 차이

초기에는 다음과 같이 단순한 결과를 예상했다:

- 일기 → 감성 이미지 1~2장 생성
- 모든 이미지가 비슷한 스타일 유지
- 영상은 아무 이미지나 사용

하지만 실제 구현 과정에서는 다음 문제가 발생했다:

- 이미지 결과가 단조롭고 “비슷한 장면 반복” 발생
- 장면이 1개만 생성되는 경우 발생
- 프롬프트에 구조 정보(shot/angle/lighting)가 없으면 품질 급락
- 영상 생성용 이미지 선택 기준이 없음

---

## 3. 개선 1 — 장면 구조화 (Scene Schema 강화)

기존:

```json
{
  "scene_kr": "...",
  "prompt_en": "..."
}
```

개선 후 :
```json
{
  "scene_id": 1,
  "scene_kr": "...",
  "prompt_en": "...",
  "shot": "WS",
  "angle": "eye-level",
  "lighting": "soft lighting",
  "lens": "24mm wide",
  "composition": "rule of thirds"
}
```
### 효과
- 이미지 다양성 확보
- 동일 텍스트에서도 다른 카메라 연출 가능

## 4. 개선 2 — Product Pipeline 구조화

### 제품 카탈로그에서는 다음 구조 적용:

- size → shot 매핑
- shape → angle 매핑
- background 변수 추가

예:

size	shot
large	wide product shot
shape	angle
flat	top-down

### 효과
- 동일 제품도 다양한 구도 생성 가능
- 상업 사진 스타일 유지
- JSON 자동 생성 가능

## 5. 개선 3 — Travel 시간대 비교 (golden_hour vs blue_hour)

# 초기 문제:

- 여행 이미지가 단일 분위기로 생성됨

# 해결:

동일 장소 + 다른 lighting variant 적용
```json 
TIME_VARIANTS = {
  "golden_hour": warm sunset lighting,
  "blue_hour": cool dawn lighting
}
```

# 결과:
travel_1.png → golden hour
travel_2.png → blue hour

# 효과:
- “비교형 콘텐츠 생성” 가능
- 영상화 가능성 증가


## 5. 핵심 어려웠던 점
- OpenAI API parameter mismatch 
- scene 구조 없으면 결과 일관성 붕괴
- pipeline return 구조가 계속 깨짐 

## 6. 배운 점
LLM은 “텍스트 생성기”가 아니라 “구조 생성기”로 써야 안정적이다
이미지 품질은 프롬프트보다 구조화된 입력(JSON) 영향이 더 크다
영상 생성은 “이미지 선택 로직”이 핵심이다
도메인 분리가 없으면 프롬프트가 반드시 섞인다

## 7. 개선하고 싶은 점 
- video prompt를 scene sequence 기반으로 확장
- travel / product / diary 통합 pipeline 설계

## 비유 카드 연결 표

| # | 비유 카드 | 연결 개념 | 내 코드 / 파일 |
|---|-----------|----------|---------------|
| 1 | 영화 감독 | LLM이 시나리오를 분석해 장면을 구성·지시 | `agents/scene.py` — `extract_scenes()` |
| 2 | 공장 생산 라인 | 원자재(일기)가 단계별 자동화를 거쳐 완성품(이미지)으로 | `pipeline.py` — `picture_diary_pipeline()` |
| 3 | 동시 통역사 | 한국어 일기 → 영문 이미지 프롬프트로 실시간 변환 | `scene_kr` → `prompt_en` 필드 변환 |
| 4 | 사진작가 | 프롬프트 지시를 받아 구도·조명을 설정하고 이미지 촬영 | `agents/image.py` — `generate_image()` |
| 5 | 레시피 북 | 도메인별 시각 어휘를 체계적으로 정리한 참고서 | `domains/travel_prompts.json` |
| 6 | 우체국 | 요청(Request)을 적절한 API 엔드포인트로 배달 | OpenAI API / fal.ai API 라우팅 |
| 7 | 오케스트라 지휘자 | GPT·DALL-E·Flux 등 여러 AI 모델을 조율 | `pipeline.py` 전체 흐름 |
| 8 | 건축 청사진 | JSON 스키마가 데이터 구조를 사전에 명세 | `domains/*.json` 스키마 구조 |
| 9 | 조립 로봇 | 장면 반복마다 동일한 공정으로 이미지를 자동 생산 | `for i, scene in enumerate(scenes)` |
| 10 | 품질 검사관 | 반환값 구조를 검증하고 규격 미달 시 재작업 지시 | 채점 루브릭 기준 자체 점검 체크리스트 |
| 11 | 탐험가의 항해 일지 | 경험을 텍스트로 기록하고 나중에 시각화 | `diary_text` 입력 — 여행 야경 주제 |
| 12 | 시간 여행자 | 동일 장면을 golden_hour / blue_hour로 시간대를 바꿔 탐험 | `day5_03_travel_blog.py` 시간대 비교 |
| 13 | 도서관 사서 | 방대한 프롬프트 어휘를 체계적으로 분류·색인 | `prompt_style` 딕셔너리 + `TIME_VARIANTS` |

---