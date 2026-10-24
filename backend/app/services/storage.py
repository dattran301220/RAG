import io
from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from typing import BinaryIO, Optional


class StorageService:
    """Dịch vụ tương tác với Object Storage MinIO """

    def __init__(self):
        # 1. Khởi tạo MinIO Client từ cấu hình trong config.py
        self.client = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ROOT_USER,
            secret_key=settings.MINIO_ROOT_PASSWORD,
            secure=settings.MINIO_SECURE,  # False nếu chạy local HTTP
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME

    def ensure_bucket_exists(self) -> None:
        """Tự động kiểm tra và tạo Bucket nếu chưa tồn tại"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"[MinIO] Đã tạo thành công bucket: {self.bucket_name}")
        except S3Error as e:
            print(f"[MinIO Error] Không thể kiểm tra/tạo bucket: {e}")
            raise e
    
    def upload_file(
        self,
        file_data: BinaryIO,
        object_name: str,
        length: int,
        content_type: str = "application/pdf",
    ) -> str:
        """
        Tải một file lên MinIO.
        - file_data: Luồng dữ liệu (BytesIO hoặc file upload từ FastAPI)
        - object_name: Tên file lưu trên MinIO (VD: CS101/giao_trinh_giai_tich.pdf)
        - length: Kích thước file (bytes)
        """
        try:
            self.ensure_bucket_exists()
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file_data,
                length=length,
                content_type=content_type,
            )
            return object_name
        except S3Error as e:
            print(f"[MinIO Error] Upload file {object_name} thất bại: {e}")
            raise e
    def download_file(self, object_name: str, file_path: str) -> None:
        """Tải file từ MinIO về ổ đĩa cục bộ của Worker để cắt chunk"""
        try:
            self.client.fget_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                file_path=file_path,
            )
        except S3Error as e:
            print(f"[MinIO Error] Download file {object_name} thất bại: {e}")
            raise e
    def get_file_bytes(self, object_name: str) -> bytes:
        """Đọc trực tiếp nội dung file thành mảng byte trong bộ nhớ (RAM)"""
        response = None
        try:
            response = self.client.get_object(self.bucket_name, object_name)
            return response.read()
        except S3Error as e:
            print(f"[MinIO Error] Lấy dữ liệu file {object_name} thất bại: {e}")
            raise e
        finally:
            if response:
                response.close()
                response.release_conn()
    def delete_file(self, object_name: str) -> bool:
        """Xóa file khỏi MinIO khi người dùng xóa tài liệu"""
        try:
            self.client.remove_object(self.bucket_name, object_name)
            return True
        except S3Error as e:
            print(f"[MinIO Error] Xóa file {object_name} thất bại: {e}")
            return False
# Tạo đối tượng Singleton để các nơi khác tái sử dụng kết nối
storage_service = StorageService()
    