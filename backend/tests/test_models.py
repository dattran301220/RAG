from app.db import Base, Course, Document, DocumentChunk, ChatSession, ChatMessage, IngestStatus


def test_models_registered():
    """Kiểm tra toàn bộ 5 bảng cơ sở dữ liệu đã được định nghĩa và đăng ký thành công"""
    tables = Base.metadata.tables
    assert "courses" in tables
    assert "documents" in tables
    assert "document_chunks" in tables
    assert "chat_sessions" in tables
    assert "chat_messages" in tables


def test_ingest_status_enum():
    """Kiểm tra các trạng thái của IngestStatus"""
    assert IngestStatus.PENDING == "PENDING"
    assert IngestStatus.PROCESSING == "PROCESSING"
    assert IngestStatus.COMPLETED == "COMPLETED"
    assert IngestStatus.FAILED == "FAILED"
