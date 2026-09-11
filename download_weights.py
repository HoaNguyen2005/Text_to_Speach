import os
from huggingface_hub import snapshot_download

def download_vietnamese_base_tts():
    # Thư mục đích nằm song song với thư mục openvoice
    target_dir = "engine/models_weights/base_tts_vi"
    os.makedirs(target_dir, exist_ok=True)
    
    print("\n" + "="*70)
    print(f"[SYSTEM] BẮT ĐẦU TẢI TRỌNG SỐ BASE TTS TIẾNG VIỆT (MMS-VITS)")
    print("="*70 + "\n")

    try:
        # Tải mô hình VITS tiếng Việt của Meta
        snapshot_download(
            repo_id="facebook/mms-tts-vie",
            local_dir=target_dir,
            local_dir_use_symlinks=False,
            resume_download=True
        )
        
        print("\n" + "="*70)
        print("[SUCCESS] ĐÃ TẢI BASE TTS TIẾNG VIỆT THÀNH CÔNG!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] Quá trình tải thất bại: {str(e)}")

if __name__ == "__main__":
    download_vietnamese_base_tts()