from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.api.v1.healthy import router as healthy_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo schema cơ sở dữ liệu nếu bảng chưa tồn tại
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[Database Warning] Không thể kết nối hoặc tạo bảng: {e}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Academic RAG Assistant API - Tra cứu học thuật thông minh",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# Cấu hình CORS cho phép giao diện Frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký Health Check router
app.include_router(
    healthy_router,
    prefix=f"{settings.API_V1_STR}/health",
    tags=["Health"]
)
app.include_router(
    healthy_router,
    prefix=f"{settings.API_V1_STR}/healthy",
    include_in_schema=False
)


@app.get("/", summary="Root API")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs",
        "health": f"{settings.API_V1_STR}/health",
    }
