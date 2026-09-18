import os
import uuid
import tempfile
import subprocess

class EdgeTTSModel:
    def __init__(self, voice="vi-VN-HoaiMyNeural"):
        """
        Khởi tạo mô hình Edge TTS (Base TTS tiếng Việt chuẩn)
        Giọng mặc định: vi-VN-HoaiMyNeural (Nữ)
        Giọng nam có thể dùng: vi-VN-NamMinhNeural
        """
        self.default_voice = voice
        self.tmp_dir = os.path.join(tempfile.gettempdir(), "edge_tts_cache")
        os.makedirs(self.tmp_dir, exist_ok=True)
        print(f"  [EDGE-TTS INIT] Khởi tạo Base TTS (Giọng mặc định: {self.default_voice})")

    def synthesize(self, text: str, voice: str = None, style_id: str = None) -> str:
        """
        Tạo audio từ văn bản.
        Trả về đường dẫn tới file âm thanh tạm thời (.mp3).
        """
        if not voice:
            voice = self.default_voice
            
        print(f"    -> [EDGE-TTS] Đang sinh âm thanh gốc (Giọng: {voice}, Style: {style_id})...")
        
        tmp_file = os.path.join(self.tmp_dir, f"base_{uuid.uuid4().hex}.mp3")
        
        # Gọi edge-tts qua CLI để tránh xung đột asyncio với FastAPI
        import sys
        python_exe = sys.executable
            
        cmd = [
            python_exe, "-m", "edge_tts",
            "--text", text,
            "--voice", voice,
            "--write-media", tmp_file
        ]
        
        # Tùy chỉnh tốc độ và cao độ dựa trên style_id
        if style_id == "news":
            # Đọc bản tin: Nhanh hơn, cao hơn một chút, dứt khoát
            cmd.extend(["--rate=+15%", "--pitch=+5Hz"])
        elif style_id == "novel" or style_id == "story":
            # Đọc tiểu thuyết/kể chuyện: Chậm rãi, truyền cảm, trầm hơn
            cmd.extend(["--rate=-15%", "--pitch=-5Hz"])
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            print(f"    -> [EDGE-TTS ERROR] {result.stderr}")
            raise Exception("Lỗi khi chạy edge-tts")
            
        return tmp_file
