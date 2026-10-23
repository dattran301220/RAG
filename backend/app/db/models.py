import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base


# Trạng thái của tác vụ xử lý tài liệu nền
class IngestStatus(str, enum.Enum):
    PENDING = "PENDING"          # Vừa upload lên MinIO, đang đợi trong hàng đợi
    PROCESSING = "PROCESSING"    # Worker đang đọc PDF, cắt chunk và sinh vector
    COMPLETED = "COMPLETED"      # Đã nạp thành công vào Qdrant
    FAILED = "FAILED"            # Xử lý thất bại (file lỗi, corrupt...)


# 1. Bảng Môn học / Học phần
class Course(Base):
    __tablename__ = "courses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(50), unique=True, nullable=False, index=True)  # VD: CS101, IT3020
    name = Column(String(255), nullable=False)                         # VD: Cấu trúc dữ liệu và giải thuật
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 1 Môn học có nhiều Tài liệu
    documents = relationship("Document", back_populates="course", cascade="all, delete-orphan")


# 2. Bảng Tài liệu giáo trình / bài tập môn học
class Document(Base):
    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=True, index=True)
    
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)       # pdf, docx, txt
    file_size = Column(Integer, nullable=False)          # Dung lượng (bytes)
    minio_path = Column(String(500), nullable=False)     # Vị trí lưu trên MinIO S3
    
    status = Column(String(20), default=IngestStatus.PENDING, index=True)
    error_message = Column(Text, nullable=True)
    chunks_count = Column(Integer, default=0)            # Số đoạn chunks được tạo
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = relationship("Course", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


# 3. Bảng các đoạn văn bản nhỏ (Chunks) phục vụ RAG
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    
    chunk_index = Column(Integer, nullable=False)        # Thứ tự đoạn văn trong tài liệu
    page_number = Column(Integer, nullable=True)         # Số trang (để trích dẫn nguồn)
    chunk_text = Column(Text, nullable=False)            # Nội dung đoạn văn bản
    qdrant_point_id = Column(String(36), nullable=True)  # ID vector trên Qdrant

    document = relationship("Document", back_populates="chunks")


# 4. Bảng Lịch sử Phiên hỏi đáp & Tin nhắn
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), default="Phiên hỏi đáp mới")
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False, index=True)
    
    role = Column(String(20), nullable=False)            # "user" hoặc "assistant"
    content = Column(Text, nullable=False)               # Nội dung tin nhắn
    citations = Column(JSON, nullable=True)              # Trích dẫn nguồn [{doc_name, page, text}]
    
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
