import os
import time
import torch
import re

# (Giả định bạn đã viết các file này trong thư mục core_tts)
# from core_tts.base_tts import ExpressiveBaseTTS
# from core_tts.tone_converter import OpenVoiceConverter
# from core_tts.speaker_encoder import ToneExtractor
# from core_tts.audio_utils import concatenate_audios

class LectureTTSPipeline:
    def __init__(self):
        print("\n" + "="*80)
        print("[SYSTEM INIT] KHỞI TẠO PIPELINE TỔNG HỢP GIỌNG NÓI")
        print("="*80)
        
        # 1. Khai báo đường dẫn tương đối tới thư mục cục tạ (models_weights)
        # Sử dụng os.path để tránh lỗi đường dẫn khi chạy trên các hệ điều hành khác nhau
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_tts_path = os.path.join(self.base_dir, "models_weights", "base_tts_vi")
        self.openvoice_path = os.path.join(self.base_dir, "models_weights", "openvoice", "checkpoints", "converter")

        # 2. Thiết lập thiết bị xử lý (Ưu tiên GPU nếu có, không thì CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[INFO] Thiết bị tính toán được chọn: {self.device.upper()}")

        # 3. Nạp các mô hình lên RAM/VRAM (Singleton Concept - Chỉ nạp 1 lần)
        self._load_models()

    def _load_models(self):
        """Hàm nội bộ để load các trọng số khổng lồ lên RAM"""
        try:
            print(f"[LOADER] Đang nạp Base TTS (Expressive TTS) từ: {self.base_tts_path}...")
            # self.base_tts = ExpressiveBaseTTS(self.base_tts_path, self.device)
            
            print(f"[LOADER] Đang nạp Tone Extractor & Converter từ: {self.openvoice_path}...")
            # self.tone_extractor = ToneExtractor(self.openvoice_path, self.device)
            # self.tone_converter = OpenVoiceConverter(self.openvoice_path, self.device)
            
            # Cấu hình giọng mặc định của Base TTS để làm mốc hoán đổi
            # self.source_se = self.tone_extractor.get_default_base_se()
            
            if self.device == "cuda":
                print(f"[MEMORY] VRAM đang chiếm dụng sau khi nạp Model: {torch.cuda.memory_allocated() / 1024**2:.2f} MB")
            print("[SUCCESS] Toàn bộ Model đã sẵn sàng trên bộ nhớ!\n")
            
        except Exception as e:
            print(f"[CRITICAL ERROR] Lỗi nạp trọng số! Thiếu file hoặc file bị hỏng: {str(e)}")
            raise e

    def _chunk_text(self, text):
        """Thuật toán băm nhỏ văn bản kịch bản dài để tránh tràn RAM"""
        # Tách câu dựa trên dấu chấm, phẩy, chấm hỏi, chấm than, hoặc xuống dòng
        sentences = re.split(r'(?<=[.!?,\n]) +', text)
        return [s.strip() for s in sentences if len(s.strip()) > 0]

    def generate_lecture(self, lecture_text: str, reference_audio_path: str, style_audio_path: str, output_path: str):
        """
        Hàm chính (Public Method) để API gọi vào.
        - lecture_text: Đoạn văn bản dài thầy cô nhập.
        - reference_audio_path: File .wav giọng mẫu của thầy cô (âm sắc).
        - style_audio_path: File .wav giọng đọc mẫu (quy định ngữ điệu: bảng tin, tiểu thuyết...).
        - output_path: Nơi lưu file kết quả.
        """
        start_time = time.time()
        print("\n" + "="*80)
        print(f"[PIPELINE START] BẮT ĐẦU XỬ LÝ BÀI GIẢNG DÀI")
        
        # 1. Trích xuất âm sắc của giảng viên (Chỉ cần làm 1 LẦN duy nhất cho toàn bộ bài giảng)
        print(f"[PHASE 0] Đang trích xuất Vector âm sắc từ file: {reference_audio_path}")
        # target_se = self.tone_extractor.extract(reference_audio_path)
        
        # 2. Băm văn bản
        chunks = self._chunk_text(lecture_text)
        print(f"[INFO] Tổng số câu cần xử lý: {len(chunks)}")
        
        audio_chunks = []
        
        # 3. Xử lý qua Vòng lặp Decoupling
        for i, text_chunk in enumerate(chunks):
            print(f"  -> [Xử lý câu {i+1}/{len(chunks)}] '{text_chunk[:30]}...'")
            
            # Bước A: Chữ -> Âm thanh mang ngữ điệu (Expressive Base TTS)
            # base_audio, _ = self.base_tts.synthesize(text_chunk, style_reference_path=style_audio_path)
            
            # Bước B: Âm thanh người máy + Vector âm sắc -> Âm thanh Giảng viên
            # cloned_audio = self.tone_converter.convert(
            #     audio=base_audio, 
            #     source_se=self.source_se, 
            #     target_se=target_se
            # )
            
            # Lưu tạm vào mảng
            # audio_chunks.append(cloned_audio)
            pass # (Giữ chỗ cho code thật)

        # 4. Ghép nối và xuất file
        print(f"\n[PHASE 3] Ghép nối {len(chunks)} đoạn âm thanh và lưu file...")
        # final_audio = concatenate_audios(audio_chunks)
        # self.base_tts.save_audio(final_audio, output_path)
        
        # 5. Dọn dẹp RAM GPU (Rất quan trọng cho Server chạy liên tục 24/7)
        if self.device == "cuda":
            torch.cuda.empty_cache()
            
        total_time = time.time() - start_time
        print(f"[PIPELINE END] THÀNH CÔNG! File lưu tại: {output_path} (Thời gian: {total_time:.2f}s)")
        print("="*80 + "\n")
        
        return output_path

# ==========================================
# KHU VỰC TEST ĐỘC LẬP (Chỉ chạy khi test trực tiếp file này)
# ==========================================
if __name__ == "__main__":
    # Khởi tạo Pipeline (Load weights)
    pipeline = LectureTTSPipeline()
    
    # Giả lập kịch bản dài
    sample_text = "Chào mừng các em đến với môn học Kiến trúc Phần mềm. Hôm nay, chúng ta sẽ tìm hiểu về Design Pattern. Đây là một chủ đề rất thú vị và thiết thực."
    sample_ref = "data/reference_audios/thay_giao_01.wav" # Quy định giọng nói
    style_ref = "data/reference_audios/giong_doc_tieu_thuyet.wav" # Quy định cảm xúc/giọng điệu
    out_file = "data/output_audios/bai_giang_demo.wav"
    
    # Chạy thử
    pipeline.generate_lecture(sample_text, sample_ref, style_ref, out_file)