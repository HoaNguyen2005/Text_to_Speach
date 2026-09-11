const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const supabaseUrl = process.env.SUPABASE_URL;
// Sử dụng Service Role Key nếu bạn cần thao tác trên DB bỏ qua RLS (như backend admin)
// Hoặc sử dụng Anon Key nếu bạn thiết lập RLS. Ở đây ví dụ dùng KEY cấu hình trong .env
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
  throw new Error('Thiếu Supabase URL hoặc Supabase Key trong file .env');
}

const supabase = createClient(supabaseUrl, supabaseKey);

module.exports = supabase;
