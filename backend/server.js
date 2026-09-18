const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors()); 
app.use(express.json()); 
const path = require('path');
app.use('/public', express.static(path.join(__dirname, 'public')));

// Import các routes
const lectureRoutes = require('./app/routes/lecture.route');
// TODO: Import các routes khác (auth, user, slide, media) khi đã có nội dung

// Mount các routes vào ứng dụng
app.use('/api/lectures', lectureRoutes);

const PORT = 3000;

app.post('/api/generate-lecture', async (req, res) => {
    const startTime = Date.now();
    
    console.log("\n" + "=".repeat(100));
    console.log(`[DEBUG - BACKEND GATEWAY] ĐÃ BẮT ĐƯỢC REQUEST TỪ FRONTEND VUE.JS`);
    console.log(`[DEBUG - TIME] Thời điểm nhận Request : ${new Date().toISOString()}`);
    console.log("=".repeat(100));

    try {
        // 1. Kiểm tra Request Header và Body
        console.log(`[DEBUG - HTTP REQUEST] Method: ${req.method} | Path: ${req.path}`);
        console.log(`[DEBUG - HTTP REQUEST] Headers Origin: ${req.headers.origin}`);
        
        const { text, teacher_id, style_id } = req.body;
        console.log(`[DEBUG - PAYLOAD EXTRACT] Text Length : ${text ? text.length : 0} chars`);
        console.log(`[DEBUG - PAYLOAD EXTRACT] Teacher ID  : ${teacher_id || 'Chưa cung cấp'}`);
        console.log(`[DEBUG - PAYLOAD EXTRACT] Style ID    : ${style_id || 'Mặc định'}`);
        
        // 2. Validate dữ liệu
        if (!text || text.trim() === '') {
            console.log(`[DEBUG - VALIDATION] THẤT BẠI! Text bị rỗng. Trả về mã lỗi 400.`);
            return res.status(400).json({ error: "Vui lòng nhập kịch bản bài giảng!" });
        }

        // 3. Giám sát tài nguyên máy chủ
        const memUsage = process.memoryUsage();
        console.log(`[DEBUG - MEMORY] Hệ thống Node.js đang dùng : ${(memUsage.heapUsed / 1024 / 1024).toFixed(2)} MB RAM`);

        // 4. Gọi sang Python FastAPI Engine thực sự
        console.log(`\n[DEBUG - AI FORWARDING] Đang gửi yêu cầu sang Python Engine tại http://localhost:8000/generate...`);
        
        try {
            // Sử dụng fetch API có sẵn trong Node.js > 18
            const aiResponse = await fetch('http://localhost:8000/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    teacher_id: teacher_id,
                    style_id: style_id || 'normal'
                })
            });
            
            if (!aiResponse.ok) {
                const errorData = await aiResponse.json();
                throw new Error(errorData.detail || 'Lỗi từ AI Engine');
            }
            
            const aiResult = await aiResponse.json();
            console.log(`[DEBUG - AI RESPONSE] AI đã xử lý xong và trả về kết quả!`);

            // 5. Trả kết quả về cho Vue
            const totalTime = (Date.now() - startTime) / 1000;
            console.log(`\n[DEBUG - API COMPLETION] Trả response HTTP 200 về cho Client Vue.js.`);
            console.log(`[DEBUG - PERFORMANCE] Tổng thời gian phản hồi: ${totalTime.toFixed(3)} giây`);
            console.log("=".repeat(100) + "\n");

            res.json({
                status: "success",
                message: "Đã tạo bài giảng thành công!",
                audio_url: aiResult.audio_url // Lấy URL trả về từ Python
            });
            
        } catch (aiError) {
            console.error(`[DEBUG - AI ERROR] Không thể gọi tới Python Engine. Có thể Python chưa chạy hoặc lỗi nội bộ:`, aiError.message);
            return res.status(500).json({ error: `Lỗi AI Engine: ${aiError.message}` });
        }

    } catch (error) {
        console.log(`\n[CRITICAL ERROR - BACKEND] CÓ LỖI XẢY RA TRONG LUỒNG XỬ LÝ!`);
        console.log(`[CRITICAL ERROR - TRACE] ${error.message}`);
        console.log(`[CRITICAL ERROR - STACK]`, error.stack);
        console.log("=".repeat(100) + "\n");
        res.status(500).json({ error: "Lỗi máy chủ nội bộ." });
    }
});

app.listen(PORT, () => {
    console.log(`[DEBUG - SERVER START] Backend Node.js đang chạy tại: http://localhost:${PORT}`);
});