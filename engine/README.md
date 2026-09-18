# Hướng Dẫn Cài Đặt Text-to-Speech Engine (Edge-TTS + OpenVoice)

Đây là Python Engine đảm nhiệm việc chuyển đổi văn bản thành giọng nói (TTS) và nhân bản âm sắc (Voice Cloning).

## Yêu Cầu Hệ Thống
- Python 3.9 hoặc 3.10
- Môi trường Windows / Linux / macOS
- Có Card Đồ Họa (GPU) hỗ trợ CUDA (NVIDIA) để tăng tốc xử lý (không bắt buộc nhưng rất khuyến khích).

## Bước 1: Khởi tạo môi trường ảo (Virtual Environment)
Mở terminal tại thư mục `engine` và chạy:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

## Bước 2: Cài đặt các thư viện Python
Cài đặt toàn bộ các thư viện cần thiết từ file `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Bước 3: Cài đặt FFmpeg (Rất quan trọng)
Thư viện xử lý âm thanh `pydub` và `OpenVoice` yêu cầu phải có `FFmpeg` trong hệ thống.
- **Trên Windows:** Tải FFmpeg (.zip) tại [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/), giải nén và chép 3 file `ffmpeg.exe`, `ffprobe.exe`, `ffplay.exe` vào thư mục `engine/venv/Scripts/`.
- **Trên macOS:** Chạy `brew install ffmpeg`
- **Trên Linux (Ubuntu):** Chạy `sudo apt update && sudo apt install ffmpeg`

## Bước 4: Chạy Máy Chủ API (Và Tự Động Tải Weights)
Sau khi cài đặt xong, hãy khởi động FastAPI Server:
```bash
python main.py
```
*Lưu ý: Trong lần khởi chạy đầu tiên, mã nguồn sẽ tự động kết nối với HuggingFace để tải trọng số mô hình OpenVoice V2 (~260MB) về thư mục `engine/checkpoints/converter/`. Quá trình này hoàn toàn tự động, hãy kiên nhẫn chờ đến khi Server báo chạy thành công.*

Server sẽ chạy mặc định tại: `http://localhost:8000`
