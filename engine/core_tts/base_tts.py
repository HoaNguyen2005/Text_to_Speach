import torch
from TTS.api import TTS
import time

class ExpressiveBaseTTS:
    def __init__(self, model_path: str, device: str = "cpu"):
        """
        Khởi tạo mô hình XTTS v2 để sinh tiếng Việt với nhiều giọng điệu.
        Sử dụng thư viện Coqui TTS.
        """
        self.device = device
        # XTTS_v2 là mô hình tốt nhất hiện tại cho zero-shot voice cloning và truyền tải cảm xúc
        self.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        print(f"  [BASE TTS INIT] Đang nạp trọng số Expressive TTS ({self.model_name})")
        
        try:
            # Khởi tạo mô hình XTTS
            # Nếu chạy lần đầu, thư viện sẽ tự động tải model về (hoặc load từ model_path nếu đã tải offline)
            self.model = TTS(self.model_name).to(self.device)
            
            # Sample rate chuẩn của XTTS thường là 24000
            self.sample_rate = 24000 
            
            print(f"  [BASE TTS INIT] Thành công! Sample Rate của Base Audio là: {self.sample_rate}Hz")
            
        except Exception as e:
            print(f"  [BASE TTS ERROR] Lỗi nạp mô hình Expressive TTS: {str(e)}")
            raise e

    def synthesize(self, text: str, style_reference_path: str):
        """
        Nhận văn bản đầu vào và file định hướng giọng điệu (style_reference_path),
        trả về Tensor sóng âm (Waveform) mang ĐÚNG ngữ điệu của file mẫu.
        """
        start_time = time.time()
        
        print(f"    -> [BASE TTS - TEXT] Sinh âm thanh mang ngữ điệu từ file: {style_reference_path}")

        # Sinh âm thanh (Suy luận)
        # Sử dụng tham số speaker_wav của XTTS để truyền tải giọng điệu (người đọc tin tức, tiểu thuyết...)
        with torch.no_grad():
            wav = self.model.tts(text=text, speaker_wav=style_reference_path, language="vi")
            
        # Kết quả trả về là một mảng Python thông thường, ta cần chuyển sang Tensor Pytorch (1, T)
        # để tương thích với luồng Pipeline tiếp theo của OpenVoice
        waveform_tensor = torch.tensor(wav).unsqueeze(0)
        
        process_time = time.time() - start_time
        print(f"    -> [BASE TTS - AUDIO] Kích thước Tensor đầu ra (Waveform): {waveform_tensor.shape}")
        print(f"    -> [BASE TTS - TIME] Sinh Base Audio mất: {process_time:.3f} giây")

        return waveform_tensor, self.sample_rate