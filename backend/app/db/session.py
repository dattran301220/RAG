from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Tạo Engine kết nối PostgreSQL
# pool_pre_ping=True: Tự động kiểm tra kết nối còn sống trước khi query
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# 2. Tạo SessionLocal: Dùng để thực hiện các thao tác Thêm, Sửa, Xóa, Đọc dữ liệu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base class: Tất cả các bảng trong models.py sẽ kế thừa từ class này
Base = declarative_base()


# 4. Hàm Dependency cho FastAPI: Mở session khi có request và tự đóng sau khi xong
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
