import io
import pytest
from unittest.mock import MagicMock
from app.services.storage import StorageService, storage_service
from app.core.config import settings


def test_storage_service_initialization():
    """Kiểm tra StorageService khởi tạo đúng cấu hình từ settings"""
    assert storage_service is not None
    assert isinstance(storage_service, StorageService)
    assert storage_service.bucket_name == settings.MINIO_BUCKET_NAME
    assert storage_service.client is not None


def test_storage_service_methods_exist():
    """Kiểm tra đầy đủ các phương thức nghiệp vụ cần thiết"""
    assert hasattr(storage_service, "ensure_bucket_exists")
    assert hasattr(storage_service, "upload_file")
    assert hasattr(storage_service, "download_file")
    assert hasattr(storage_service, "get_file_bytes")
    assert hasattr(storage_service, "delete_file")


def test_storage_service_mock_upload():
    """Kiểm tra logic gọi put_object khi upload file"""
    service = StorageService()
    # Mock client để kiểm thử logic không cần bật MinIO server thật
    service.client = MagicMock()
    service.client.bucket_exists.return_value = True

    dummy_data = io.BytesIO(b"Giao trinh hoc thuat RAG")
    file_name = "test_doc.txt"
    
    result = service.upload_file(
        file_data=dummy_data,
        object_name=file_name,
        length=len(dummy_data.getvalue()),
        content_type="text/plain",
    )

    assert result == file_name
    service.client.put_object.assert_called_once()


def test_storage_service_mock_delete():
    """Kiểm tra logic gọi remove_object khi xóa file"""
    service = StorageService()
    service.client = MagicMock()

    success = service.delete_file("test_doc.txt")
    assert success is True
    service.client.remove_object.assert_called_once_with(service.bucket_name, "test_doc.txt")
