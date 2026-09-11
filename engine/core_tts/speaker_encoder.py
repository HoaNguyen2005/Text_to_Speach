import os
import torch
import torchaudio
import time

# Giả định nhập thư viện cốt lõi của OpenVoice (nếu bạn đã clone mã nguồn của họ)
# from openvoice import se_extractor 

class ToneExtractor:
    def __init__(self, model_path: str, device: str = "cpu"):
        """
        Khởi tạo bộ trích xuất đặc trưng giọng nói.
        """
        self.device = device
        self.model_path = model_path
        print(f"  [SPEAKER ENCODER INIT] Đang nạp mô hình phân tích giọng nói...")
        
        # Trong thực tế, OpenVoice V2 dùng chung file converter.pt cho việc trích xuất
        # self.extractor_model = se_extractor.load_model(self.model_path, self.device)
        
        print(f"  [SPEAKER ENCODER INIT] Sẵn sàng trích xuất âm sắc trên thiết bị {self.device.upper()}")

    def _preprocess_audio(self, audio_path: str):
        """
        Hàm nội bộ: Tiền xử lý âm thanh trước khi đưa vào mạng nơ-ron.
        Mạng nơ-ron thường yêu cầu chuẩn đầu vào là âm thanh Mono (1 kênh) và Sample Rate cố định (vd: 16kHz).
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Không tìm thấy file giọng mẫu tại: {audio_path}")

        # Đọc file âm thanh thành Tensor
        waveform, sample_rate = torchaudio.load(audio_path)
        print(f"    -> [PREPROCESS] File gốc: {waveform.shape} | Sample Rate: {sample_rate}Hz")

        # 1. Chuyển Stereo (2 kênh) sang Mono (1 kênh) nếu cần
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
            print("    -> [PREPROCESS] Đã chuyển đổi âm thanh Stereo sang Mono.")

        # 2. Resample (Lấy mẫu lại) về 16kHz nếu file thu âm của thầy cô là 44.1kHz hoặc 48kHz
        target_sr = 16000
        if sample_rate != target_sr:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sr)
            waveform = resampler(waveform)
            print(f"    -> [PREPROCESS] Đã chuyển đổi Sample Rate về chuẩn {target_sr}Hz.")

        return waveform, target_sr

    def extract(self, audio_path: str):
        """
        Đọc file âm thanh và trả về Tensor đại diện cho âm sắc (Tone Vector).
        """
        start_time = time.time()
        print(f"    -> [SPEAKER ENCODER] Bắt đầu phân tích giọng từ: {audio_path}")
        
        # 1. Tiền xử lý âm thanh
        # waveform, sr = self._preprocess_audio(audio_path)
        
        # 2. Trích xuất Tone Embedding
        try:
            with torch.no_grad():
                # Thực tế gọi hàm của OpenVoice:
                # target_se, audio_name = se_extractor.get_se(audio_path, self.extractor_model, vad=True)
                
                # Giả lập kết quả Vector 256 chiều (Shape: [1, 256]) để test luồng chạy
                target_se = torch.randn(1, 256).to(self.device)
                
            process_time = time.time() - start_time
            print(f"    -> [SPEAKER ENCODER SUCCESS] Trích xuất thành công! Shape: {target_se.shape} | TG: {process_time:.2f}s")
            
            return target_se
            
        except Exception as e:
            print(f"    -> [SPEAKER ENCODER ERROR] Quá trình trích xuất thất bại: {str(e)}")
            raise e

    def get_default_base_se(self):
        """
        Lấy Vector âm sắc mặc định của mô hình Base TTS (Meta MMS).
        Bộ chuyển đổi cần biết âm sắc 'Gốc' để trừ đi, trước khi cộng âm sắc 'Đích' của thầy cô vào.
        """
        print(f"    -> [SPEAKER ENCODER] Đang thiết lập Tone Vector mặc định của Meta MMS...")
        # Thường thì file vector gốc (.pth hoặc .npy) sẽ đi kèm với bộ trọng số của Base TTS.
        # Ở đây giả lập trả về vector gốc.
        source_se = torch.randn(1, 256).to(self.device)
        return source_se