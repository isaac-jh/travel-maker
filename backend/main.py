from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging

from src.util.config import settings
from src.util.database import get_db, init_db, check_db_connection

logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Travel Maker API",
    description="여행 계획 및 추천 서비스 API",
    version="1.0.0",
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("애플리케이션 시작 중...")
    
    if check_db_connection():
        logger.info("데이터베이스 연결 성공")
    else:
        logger.warning("데이터베이스 연결 실패 - 서비스가 정상 작동하지 않을 수 있습니다")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("애플리케이션 종료 중...")


@app.get("/")
async def root():
    return {
        "message": "Travel Maker API에 오신 것을 환영합니다!",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    db_status = check_db_connection()
    
    return {
        "status": "healthy" if db_status else "degraded",
        "database": "connected" if db_status else "disconnected",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"서버 시작: http://{settings.app_host}:{settings.app_port}")
    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug
    )
