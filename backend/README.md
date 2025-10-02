# Travel Maker Backend

FastAPI 기반 여행 계획 및 추천 서비스 백엔드 API

## 기술 스택

- **FastAPI**: 고성능 웹 프레임워크
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **MySQL**: 데이터베이스
- **PyMySQL**: MySQL 드라이버
- **Pydantic**: 데이터 검증 및 설정 관리

## 프로젝트 구조

```
backend/
├── main.py                 # FastAPI 애플리케이션 진입점
├── requirements.txt        # Python 의존성 패키지
├── .env.example           # 환경변수 예시 파일
└── src/
    ├── __init__.py
    ├── config.py          # 애플리케이션 설정
    └── database.py        # MySQL 연결 및 세션 관리
```

## 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
cd backend
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

프로젝트는 `ENV_CONFIG` 환경변수에 따라 다른 설정 파일을 로드합니다:

- `ENV_CONFIG=local` → `env/local.env` 로드 (개발 환경)
- `ENV_CONFIG=prod` → `env/prod.env` 로드 (운영 환경)
- 미설정 시 → `env/local.env` 로드 (기본값)

#### 로컬 개발 환경 (`env/local.env`)

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=local_password
DB_NAME=travel_maker_local
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True
```

#### 운영 환경 (`env/prod.env`)

```env
DB_HOST=your-prod-db-host.com
DB_PORT=3306
DB_USER=prod_user
DB_PASSWORD=your_secure_production_password
DB_NAME=travel_maker_prod
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False
```

**⚠️ 보안 주의사항**: 실제 운영 환경의 `env/prod.env` 파일은 git에 커밋하지 마세요!

### 4. MySQL 데이터베이스 생성

```sql
CREATE DATABASE travel_maker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 서버 실행

```bash
# 로컬 개발 환경으로 실행 (기본값)
python main.py

# 또는 ENV_CONFIG를 명시적으로 지정
ENV_CONFIG=local python main.py

# 운영 환경으로 실행
ENV_CONFIG=prod python main.py

# uvicorn으로 직접 실행
ENV_CONFIG=local uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API 엔드포인트

### 기본 엔드포인트

- `GET /` - 루트 엔드포인트 (API 정보)
- `GET /health` - 헬스체크 (데이터베이스 연결 상태 확인)
- `GET /docs` - Swagger UI API 문서
- `GET /redoc` - ReDoc API 문서

## 개발 가이드

### 데이터베이스 세션 사용

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_db

@app.get("/example")
def example_endpoint(db: Session = Depends(get_db)):
    # 데이터베이스 작업 수행
    return {"message": "success"}
```

### 새로운 라우터 추가

```python
# src/routers/example.py 생성 후
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_examples():
    return {"examples": []}

# main.py에 추가
from src.routers import example
app.include_router(example.router, prefix="/api/v1/example", tags=["Example"])
```

## TODO

- [ ] Alembic을 사용한 데이터베이스 마이그레이션 시스템 구축
- [ ] 사용자 인증/인가 시스템 추가
- [ ] API 라우터 구조화 (users, trips 등)
- [ ] 프로덕션 환경 CORS 설정 최적화
- [ ] Connection Pool 설정 최적화
- [ ] 로깅 시스템 고도화 (파일 로깅, 로그 레벨 관리)
- [ ] 테스트 코드 작성 (pytest)

## 참고사항

- 모든 핵심 함수에는 docstring으로 설명이 추가되어 있습니다
- 확장이 필요한 부분에는 TODO 주석이 명시되어 있습니다
- 개발 환경에서는 `DEBUG=True`로 설정하여 SQL 쿼리 로깅을 활성화할 수 있습니다

