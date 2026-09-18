# Hệ Thống Sinh Bài Giảng Tự Động (Voice Cloning TTS)

Chào mừng bạn đến với dự án Hệ Thống Sinh Bài Giảng Tự Động áp dụng công nghệ nhân bản giọng nói và chuyển đổi văn bản thành giọng nói.

Dự án này được thiết kế theo mô hình Microservices với 3 thành phần chính hoạt động song song để mang lại hiệu năng và trải nghiệm tốt nhất.

## Kiến Trúc Hệ Thống 

1. **Frontend (Vue.js 3 + Vite):** 
   - Giao diện người dùng (UI) mượt mà, hỗ trợ tạo kịch bản, chọn giọng đọc mẫu và phong cách đọc.
   - Thư mục: `frontend/`
   - Cổng mặc định: `5173`

2. **Backend Gateway (Node.js + Express):**
   - Đóng vai trò làm cầu nối (Gateway) điều hướng dữ liệu từ Frontend sang Engine xử lý AI, đồng thời là máy chủ lưu trữ (Host) tĩnh cho các file âm thanh kết quả.
   - Hỗ trợ kết nối cơ sở dữ liệu (Supabase) để quản lý tài khoản người dùng.
   - Thư mục: `backend/`
   - Cổng mặc định: `3000`

3. **AI Engine (Python + FastAPI):**
   - Trái tim của hệ thống. Chịu trách nhiệm tổng hợp giọng nói tiếng Việt chuẩn xác bằng **Edge-TTS** và nhân bản âm sắc cá nhân (Voice Cloning) bằng **OpenVoice V2**.
   - Thư mục: `engine/`
   - Cổng mặc định: `8000`

---

## Hướng Dẫn Cài Đặt & Khởi Chạy 

Để hệ thống hoạt động hoàn chỉnh, bạn cần khởi chạy đồng thời cả 3 dịch vụ trên 3 terminal (cửa sổ dòng lệnh) khác nhau.

### Bước 1: Khởi chạy AI Engine (Python)
Mở Terminal 1 và đi tới thư mục `engine`:
```bash
cd engine
# Nếu chạy lần đầu, hãy xem hướng dẫn cài đặt chi tiết trong thư mục engine/README.md
# Bao gồm việc tạo venv và pip install -r requirements.txt

# Kích hoạt môi trường ảo (trên Windows)
.\venv\Scripts\activate

# Khởi chạy server AI
python main.py
```
*(Trong lần chạy đầu tiên, Engine sẽ tự động tải các trọng số mô hình AI cần thiết).*

### Bước 2: Khởi chạy Backend (Node.js)
Mở Terminal 2 và đi tới thư mục `backend`:
```bash
cd backend

# Cài đặt thư viện (nếu chạy lần đầu)
npm install

# Khởi chạy Backend Server
node server.js
```

### Bước 3: Khởi chạy Frontend (Vue.js)
Mở Terminal 3 và đi tới thư mục `frontend`:
```bash
cd frontend

# Cài đặt thư viện (nếu chạy lần đầu)
npm install

# Khởi chạy giao diện web
npm run dev
```

---

## Cách Sử Dụng
1. Mở trình duyệt và truy cập vào đường dẫn: `http://localhost:5173`
2. Nhập văn bản kịch bản bài giảng bạn muốn tạo.
3. Lựa chọn giọng giảng viên (Nam/Nữ) và phong cách đọc (Bản tin / Tiểu thuyết).
4. Bấm **Tạo Bài Giảng** và chờ AI xử lý (khoảng 3-5 giây tùy độ dài văn bản).
5. Nghe thử ngay trên trình duyệt!

## Thêm Giọng Đọc Mẫu
Để thêm một giọng đọc mới cho hệ thống, bạn chỉ cần copy file ghi âm mẫu (`.wav`) vào thư mục `backend/public/audio/samples/`. 
*(Vui lòng đặt tên file chứa từ `male` nếu đó là giọng nam, hệ thống sẽ tự động điều chỉnh giọng gốc phù hợp nhất).* Sau đó, cập nhật danh sách hiển thị trong mã nguồn `frontend/src/App.vue`.

---
*Dự án Niên Luận được xây dựng với mục tiêu tối ưu hóa trải nghiệm học tập và số hóa bài giảng.*
