3. Hệ thống RAG (Retrieval-Augmented Generation)
Hệ thống hỏi–đáp dựa trên tài liệu nội bộ: ingest tài liệu (PDF, web, văn bản…), chunking, embedding, lưu vector, truy vấn ngữ nghĩa và sinh câu trả lời có trích dẫn nguồn. Queue nền dùng cho ingest / tái embedding khi cập nhật kho tri thức.

Tham khảo (chọn stack phù hợp): LangChain — RAG tutorial, LlamaIndex, hoặc tự lắp pipeline với API LLM + vector DB đã nêu ở mục yêu cầu kỹ thuật.

Trường hợp 1: Trợ lý nội bộ doanh nghiệp (hỏi đáp trên quy trình, hướng dẫn nội bộ, wiki).
Trường hợp 2: Hỗ trợ tra cứu học thuật / tài liệu môn học (hỏi theo nội dung giáo trình, bài tập, đề cương đã được cung cấp)

.
Với nhánh RAG: xây dựng luồng ingest → truy vấn → trả lời (có thể hiển thị streaming), kèm quản lý kho tài liệu.
Frontend: với RAG — giao diện đặt câu hỏi, hiển thị câu trả lời và (tối thiểu) nguồn trích dẫn / đoạn liên quan.
Frontend quản trị (admin):với RAG — quản lý tài liệu / kho tri thức (tải lên, xóa, tái index), trạng thái ingest.Backend: logic nghiệp vụ, API kết nối các phần (vision hoặc RAG).
Lưu trữ: tận dụng tối thiểu ba loại:
Database (SQL, NoSQL, …)
Object storage (S3, file storage, MinIO, …) — lưu file gốc / snapshot tài liệu
Vector database (Qdrant, Pinecone, Milvus, FAISS, …) — embedding cho RAG hoặc đặc trưng cần vector hoá
Message / event queue cho tác vụ nền (ví dụ: chunking → embedding → lưu vector; tái xử lý khi đổi tài liệu, những tác vụ như vậy cần được chạy trong nền thay vì phải để người dùng chờ API hoạt động xong, làm ảnh hưởng đến UX).
Load balancer (nginx) điều phối request tới frontend, backend và dịch vụ khác (nếu cần).
Điểm cộng (không bắt buộc) - Sinh viên có thể chọn một hoặc nhiều phương án sau:

Xây dựng luồng CI/CD hoàn chỉnh