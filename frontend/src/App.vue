<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { createClient } from '@supabase/supabase-js';

// Khởi tạo Supabase
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

// Kiểm tra xem đã cấu hình env chưa
const isSupabaseConfigured = supabaseUrl && supabaseAnonKey;
const supabase = isSupabaseConfigured ? createClient(supabaseUrl, supabaseAnonKey) : null;

// User state
const session = ref(null);
const authEmail = ref('');
const authPassword = ref('');
const authLoading = ref(false);
const authError = ref('');
const isRegisterMode = ref(false);

// Lecture state
const text = ref('');
const teacherId = ref('thay_giao_01');
const styleId = ref('news');
const loading = ref(false);
const resultAudioUrl = ref(null);
const errorMessage = ref('');

const teachers = [
  { id: 'thay_giao_01', name: 'Thầy Giáo 01 (Cơ bản)' },
  { id: 'co_giao_02', name: 'Cô Giáo 02 (Nhẹ nhàng)' }
];

const styles = [
  { id: 'news', name: 'Bảng tin thời sự (Trang trọng)' },
  { id: 'story', name: 'Đọc tiểu thuyết (Truyền cảm)' },
  { id: 'normal', name: 'Bình thường (Mặc định)' }
];

onMounted(() => {
  if (supabase) {
    supabase.auth.getSession().then(({ data }) => {
      session.value = data.session;
    });

    supabase.auth.onAuthStateChange((_event, _session) => {
      session.value = _session;
    });
  }
});

const handleLogin = async () => {
  if (!supabase) {
    authError.value = "Chưa cấu hình Supabase URL và Anon Key trong file .env";
    return;
  }
  
  authLoading.value = true;
  authError.value = '';
  
  const { error } = await supabase.auth.signInWithPassword({
    email: authEmail.value,
    password: authPassword.value,
  });

  if (error) {
    authError.value = error.message;
  }
  authLoading.value = false;
};

const handleRegister = async () => {
  if (!supabase) {
    authError.value = "Chưa cấu hình Supabase URL và Anon Key trong file .env";
    return;
  }
  
  authLoading.value = true;
  authError.value = '';
  
  const { error } = await supabase.auth.signUp({
    email: authEmail.value,
    password: authPassword.value,
  });

  if (error) {
    authError.value = error.message;
  } else {
    authError.value = "Đăng ký thành công! Vui lòng kiểm tra email để xác thực (nếu yêu cầu) hoặc đăng nhập.";
    isRegisterMode.value = false;
  }
  authLoading.value = false;
};

const handleLogout = async () => {
  if (supabase) await supabase.auth.signOut();
};

const generateLecture = async () => {
  if (!text.value.trim()) {
    errorMessage.value = 'Vui lòng nhập kịch bản bài giảng!';
    return;
  }
  
  loading.value = true;
  errorMessage.value = '';
  resultAudioUrl.value = null;

  try {
    const response = await axios.post('http://localhost:3000/api/generate-lecture', {
      text: text.value,
      teacher_id: teacherId.value,
      style_id: styleId.value
    });

    if (response.data.status === 'success') {
      resultAudioUrl.value = response.data.audio_url;
    } else {
      errorMessage.value = 'Có lỗi xảy ra từ máy chủ.';
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Không thể kết nối đến máy chủ!';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="app-container">
    <div class="glass-panel">
      <!-- MÀN HÌNH ĐĂNG NHẬP / ĐĂNG KÝ -->
      <div v-if="!session" class="auth-container">
        <header class="header">
          <h1>Đăng Nhập Hệ Thống</h1>
          <p v-if="!isSupabaseConfigured" class="warning-text">Lưu ý: Chưa cấu hình .env cho Supabase</p>
          <p v-else>Vui lòng đăng nhập để tạo bài giảng</p>
        </header>

        <div class="form-group">
          <label>Email của bạn</label>
          <input type="email" v-model="authEmail" placeholder="teacher@university.edu.vn" />
        </div>
        
        <div class="form-group">
          <label>Mật khẩu</label>
          <input type="password" v-model="authPassword" placeholder="••••••••" />
        </div>

        <div class="error-box" v-if="authError">
          {{ authError }}
        </div>

        <button 
          v-if="!isRegisterMode" 
          class="generate-btn" 
          @click="handleLogin" 
          :disabled="authLoading"
        >
          <span v-if="!authLoading">Đăng Nhập</span>
          <span v-else class="spinner"></span>
        </button>

        <button 
          v-else 
          class="generate-btn register-btn" 
          @click="handleRegister" 
          :disabled="authLoading"
        >
          <span v-if="!authLoading">Đăng Ký Tài Khoản</span>
          <span v-else class="spinner"></span>
        </button>

        <div class="auth-switch">
          <p v-if="!isRegisterMode">Chưa có tài khoản? <a href="#" @click.prevent="isRegisterMode = true">Đăng ký ngay</a></p>
          <p v-else>Đã có tài khoản? <a href="#" @click.prevent="isRegisterMode = false">Đăng nhập</a></p>
        </div>
      </div>

      <!-- MÀN HÌNH TẠO BÀI GIẢNG -->
      <div v-else>
        <header class="header app-header">
          <div>
            <h1>Voice Cloning TTS</h1>
            <p>Hệ thống tổng hợp bài giảng bằng AI</p>
          </div>
          <div class="user-info">
            <span>👤 {{ session.user.email }}</span>
            <button class="logout-btn" @click="handleLogout">Đăng Xuất</button>
          </div>
        </header>

        <main class="main-content">
          <div class="form-group">
            <label for="script">Kịch bản bài giảng</label>
            <textarea 
              id="script" 
              v-model="text" 
              placeholder="Nhập nội dung bài giảng vào đây..." 
              rows="6"
            ></textarea>
          </div>

          <div class="controls-row">
            <div class="form-group">
              <label for="teacher">Giọng Giảng Viên (Âm sắc)</label>
              <select id="teacher" v-model="teacherId">
                <option v-for="teacher in teachers" :key="teacher.id" :value="teacher.id">
                  {{ teacher.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="style">Giọng Điệu (Cảm xúc)</label>
              <select id="style" v-model="styleId">
                <option v-for="style in styles" :key="style.id" :value="style.id">
                  {{ style.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="error-box" v-if="errorMessage">
            {{ errorMessage }}
          </div>

          <button 
            class="generate-btn" 
            :class="{ 'is-loading': loading }" 
            @click="generateLecture" 
            :disabled="loading"
          >
            <span v-if="!loading">Tạo Bài Giảng (Generate)</span>
            <span v-else class="spinner"></span>
          </button>

          <div class="result-panel" v-if="resultAudioUrl">
            <h3>Kết quả âm thanh</h3>
            <audio controls :src="resultAudioUrl" class="custom-audio"></audio>
          </div>
        </main>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Reset basic */
* {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  padding: 0;
  background-color: #0f172a;
}

.app-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #e2e8f0;
  padding: 2rem;
}

.glass-panel {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2.5rem;
  width: 100%;
  max-width: 800px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  text-align: left;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #cbd5e1;
}

.logout-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.4);
}

.header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(to right, #38bdf8, #818cf8, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.header p {
  color: #94a3b8;
  margin-top: 0.5rem;
  font-size: 1.1rem;
}

.warning-text {
  color: #fbbf24 !important;
}

.form-group {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  text-align: left;
}

.form-group label {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #cbd5e1;
}

textarea, select, input {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 1rem;
  color: #f8fafc;
  font-size: 1rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

textarea:focus, select:focus, input:focus {
  outline: none;
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
}

textarea {
  resize: vertical;
  min-height: 120px;
}

.controls-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.generate-btn {
  width: 100%;
  background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 1rem;
}

.register-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
}

.generate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.auth-switch {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.95rem;
}

.auth-switch a {
  color: #818cf8;
  text-decoration: none;
  font-weight: 600;
}

.auth-switch a:hover {
  text-decoration: underline;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-panel {
  margin-top: 2rem;
  padding: 1.5rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 16px;
  text-align: center;
  animation: fadeIn 0.5s ease;
}

.result-panel h3 {
  color: #34d399;
  margin-top: 0;
  margin-bottom: 1rem;
}

.custom-audio {
  width: 100%;
  height: 48px;
  border-radius: 24px;
}

.custom-audio::-webkit-media-controls-panel {
  background-color: #f1f5f9;
}

.error-box {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 500;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
  .controls-row {
    grid-template-columns: 1fr;
  }
  .app-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  .user-info {
    align-items: center;
  }
}
</style>