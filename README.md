# 🚀 AutoTriage

> **AI 기반 자동 티켓 트리아지 & 분석 시스템**
> Django + PostgreSQL + Redis + Prisma + AI 파이프라인을 활용한 백엔드 중심 풀스택 프로젝트

---

## 📌 프로젝트 소개

**AutoTriage**는 리뷰, 고객 문의(CS), 이슈 티켓과 같은 텍스트 데이터를 수집하여
AI를 통해 **자동 분류·요약·긴급도 판단**을 수행하고,
이를 **확장성과 정합성을 고려한 백엔드 아키텍처**로 처리·분석하는 시스템입니다.

이 프로젝트는 단순 기능 구현이 아니라 다음 질문에서 출발했습니다.

> “AI 파이프라인이 포함된 백엔드 시스템을
> 실제 서비스처럼 설계하려면 무엇을 고민해야 할까?”

---

## 🎯 프로젝트 목표

* 🔄 **AI 자동화 파이프라인**을 실제 서비스 구조로 설계
* 🧱 **데이터 정합성**을 고려한 도메인 모델링 및 DB 설계
* ⚡ **읽기/쓰기 분리**를 통한 API 성능 최적화
* 🧠 Django(Python) + Prisma(Node.js)를 함께 사용하는 **멀티 런타임 구조 경험**
* 🛠️ Redis, Celery, PostgreSQL 등 **현업에서 쓰이는 기술 스택 직접 적용**

---

## 🧩 전체 아키텍처 개요

```
Client
  │
  ▼
[Django API]
  ├─ Ticket 생성/조회 (Write 중심)
  ├─ 데이터 검증 & 상태 관리
  └─ Celery 기반 AI 파이프라인 오케스트레이션
        │
        ▼
     [Redis]
        │
        ▼
   [PostgreSQL]
        ▲
        │
[Node.js Analytics BFF]
  ├─ Prisma ORM 기반 집계/조회
  ├─ 대시보드용 API
  └─ 캐시 적용 (Redis)
```

---

## 🛠️ 기술 스택

### 🔹 Backend (Core API)

* **Python / Django / Django REST Framework**
* **PostgreSQL** (정합성 중심 RDB 설계)
* **Redis** (캐시, 메시지 브로커)
* **Celery** (비동기 AI 파이프라인)

### 🔹 Analytics / BFF

* **Node.js (TypeScript)**
* **Prisma ORM**
* PostgreSQL (동일 DB, 읽기 전용 접근)

### 🔹 Infra & Tooling

* Docker / Docker Compose
* Git & GitHub (브랜치 전략 기반 협업)
* VSCode

---

## 🧠 핵심 설계 포인트

### 1️⃣ 데이터 정합성 (Data Consistency)

* `(source, external_id)` 기반 **중복 유입 방지 (idempotency)**
* 상태 머신 기반 파이프라인 관리
  (`RECEIVED → VALIDATED → ENRICHED → READY / FAILED`)
* 명시적인 인덱스 설계로 조회 성능 확보

### 2️⃣ AI 파이프라인 구조

* 비동기 처리(Celery)로 AI 작업 분리
* 재시도/중복 처리 방지(분산 락)
* 모델 버전 관리 고려한 AI 결과 저장

### 3️⃣ API 성능 최적화

* 읽기/쓰기 책임 분리
* 집계 테이블 기반 Analytics API
* Redis 캐시 적용
* Keyset pagination 적용 예정

---

## 🌱 이 프로젝트를 통해 공부할 것들

* Django 기반 **도메인 중심 설계**
* PostgreSQL 인덱스/제약조건 설계 전략
* Redis를 활용한 캐시 및 비동기 처리
* Celery를 이용한 AI 자동화 파이프라인
* Prisma ORM을 활용한 **Type-safe DB 접근**

---

## 🗂️ 레포지토리 구조

```
auto-triage/
├── backend-django/        # Django Core API
├── analytics-bff/         # Node.js + Prisma Analytics API
├── infra/                 # Docker, 환경 설정
├── docs/                  # 설계 문서
└── README.md
```

---

## 🖼️ 아키텍처 다이어그램 (이미지)

> 실제 README에는 아래 다이어그램 이미지를 추가할 예정입니다.
> (Mermaid 또는 draw.io 기반으로 작성)

**예정 다이어그램 구성 요소**
- Client → Django API (Write Path)
- Django → Redis → Celery Worker → AI 처리
- PostgreSQL 단일 DB (Write/Read 공유)
- Node.js Analytics BFF → PostgreSQL (Read Only)
- Redis Cache → Analytics 응답

---

## 🧭 개발 진행 상태
- [ ] API 문서화 (OpenAPI/Swagger)


### 🔜 Redis
- [ ] Redis 연결 및 헬스체크
- [ ] 대시보드/집계 응답 캐시(TTL) 적용
- [ ] 분산 락으로 중복 처리 방지 (ticket 단위)
- [ ] 레이트 리밋(선택) 적용


### 🔜 Async / Pipeline (Celery)
- [ ] Celery 기본 설정 + Redis broker
- [ ] 파이프라인 태스크 구성: validate → enrich(ai) → persist
- [ ] 재시도 정책/백오프 설정 + 실패 상태 전환
- [ ] Dead-letter(선택) 또는 실패 이벤트 기록
- [ ] 스케줄 작업(beat): 일별 집계 갱신


### 🔜 AI
- [ ] AI 결과 스키마 확정 (topic, sentiment, urgency_score, summary, model_version)
- [ ] 더미 모델로 파이프라인 end-to-end 연결
- [ ] LLM/모델 연동 (프롬프트/출력 스키마 고정)
- [ ] 모델 버전 관리 및 재처리 API (`POST /tickets/{id}/reprocess`)
- [ ] 유사 티켓 추천(선택): 임베딩/검색 도입


### 🔜 Analytics BFF (Node.js / Prisma)
- [ ] TypeScript 프로젝트 초기 구성
- [ ] Prisma 스키마 작성 및 마이그레이션/연결
- [ ] 요약 API: `GET /analytics/summary` (캐시 적용)
- [ ] 추이 API: `GET /analytics/trends?range=30d`
- [ ] 검색 API: `GET /analytics/tickets` (필터/키셋 페이지네이션)
- [ ] 집계 테이블 설계/갱신 전략 (event 기반 또는 스케줄 기반)
- [ ] 핫쿼리 Raw SQL 최적화(선택)


### 🔜 Frontend (Dashboard)
- [ ] 프로젝트 초기 구성 (Next.js 또는 단순 SPA)
- [ ] 티켓 목록/상세 화면
- [ ] 필터(토픽/긴급도/기간) UI
- [ ] 대시보드 요약/추이 차트
- [ ] 재처리 버튼 및 상태 표시


### 🔜 Observability / Quality
- [ ] 로깅 포맷 통일(structured logging)
- [ ] 헬스체크 엔드포인트(Django/Node)
- [ ] 테스트: 단위 테스트 + API 테스트
- [ ] 부하 테스트(k6/locust)로 성능 지표 산출
- [ ] 성능 개선 전/후 비교(p95 latency, 캐시 히트율)


### 🔜 Infra / DevEx
- [ ] Docker Compose로 Postgres/Redis/서비스 기동
- [ ] 환경변수 템플릿 정리(.env.example 확장)
- [ ] pre-commit/format/lint 설정 (ruff/black/isort, eslint/prettier)
- [ ] CI(선택): GitHub Actions로 테스트/린트 자동화

---

## ✨ 앞으로의 계획

* AI 기반 유사 티켓 추천 기능
* SLA 기반 긴급 알림 처리
* 성능 테스트 및 지표 시각화
* 실서비스 배포 환경 구성

---

> 이 프로젝트는 **AI + 백엔드 시스템 설계 역량을 함께 보여주기 위한 개인 포트폴리오 프로젝트**입니다.


