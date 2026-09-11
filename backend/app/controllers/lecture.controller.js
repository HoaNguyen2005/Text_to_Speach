const supabase = require('../config/supabase');
const mammoth = require('mammoth');

// Lấy danh sách bài giảng
exports.getAllLectures = async (req, res) => {
    try {
        const { data, error } = await supabase
            .from('lectures')
            .select('*')
            .order('created_at', { ascending: false });

        if (error) throw error;

        res.status(200).json({ status: 'success', data });
    } catch (error) {
        console.error('[ERROR] Lỗi khi lấy danh sách bài giảng:', error.message);
        res.status(500).json({ error: error.message });
    }
};

// Luồng 1: Tạo bài giảng bằng cách nhập liệu trực tiếp
exports.createLectureDirect = async (req, res) => {
    try {
        // Dữ liệu từ Frontend gửi lên: user_id (tạm hardcode nếu chưa có auth), title, description, slides (mảng text)
        const { user_id, title, description, slides } = req.body;

        if (!title || !slides || !Array.isArray(slides) || slides.length === 0) {
            return res.status(400).json({ error: "Thiếu tiêu đề hoặc danh sách slides rỗng!" });
        }

        // 1. Tạo bài giảng (lecture)
        const { data: lectureData, error: lectureError } = await supabase
            .from('lectures')
            .insert([{
                // Tạm thời nếu bạn chưa có luồng Auth, bạn phải truyền 1 user_id có sẵn trong Supabase vào đây. 
                // Hoặc bỏ qua user_id nếu bảng lectures của bạn cho phép user_id null.
                // Ở đây giả định bạn sẽ test với một UUID hợp lệ, hoặc để user_id tuỳ ý nếu đã chỉnh trong DB.
                user_id: user_id,
                title,
                description,
                status: 'draft'
            }])
            .select()
            .single();

        if (lectureError) throw lectureError;

        // 2. Chèn từng slide vào bảng slides
        const lectureId = lectureData.id;
        const slidesToInsert = slides.map((content, index) => ({
            lecture_id: lectureId,
            order_index: index + 1,
            content: content
        }));

        const { error: slidesError } = await supabase
            .from('slides')
            .insert(slidesToInsert);

        if (slidesError) throw slidesError;

        res.status(201).json({
            status: 'success',
            message: 'Tạo bài giảng trực tiếp thành công!',
            data: { lectureId, total_slides: slides.length }
        });

    } catch (error) {
        console.error('[ERROR] Lỗi khi tạo bài giảng trực tiếp:', error.message);
        res.status(500).json({ error: error.message });
    }
};

// Luồng 2: Tạo bài giảng từ việc Upload File (.txt, .docx)
exports.createLectureFromFile = async (req, res) => {
    try {
        const { user_id, title, description } = req.body;
        const file = req.file;

        if (!file) {
            return res.status(400).json({ error: "Vui lòng đính kèm file văn bản (.txt hoặc .docx)!" });
        }

        if (!title) {
            return res.status(400).json({ error: "Thiếu tiêu đề bài giảng!" });
        }

        let extractedText = "";

        // 1. Trích xuất text từ file
        if (file.mimetype === 'text/plain' || file.originalname.endsWith('.txt')) {
            extractedText = file.buffer.toString('utf-8');
        }
        else if (file.originalname.endsWith('.docx') || file.originalname.endsWith('.doc')) {
            const result = await mammoth.extractRawText({ buffer: file.buffer });
            extractedText = result.value;
        } else {
            return res.status(400).json({ error: "Định dạng file không được hỗ trợ!" });
        }

        // 2. Tách text thành các Slide (dựa trên khoảng trắng kép / xuống dòng kép)
        // Thay vì cắt mỗi dòng 1 slide, cắt theo cụm đoạn văn (có khoảng trắng ở giữa) để nội dung slide dài vừa phải.
        // Regex \n\s*\n dùng để tách các khối văn bản cách nhau bằng ít nhất 1 dòng trống.
        let rawSlides = extractedText.split(/\n\s*\n/);

        // Lọc bỏ các slide rỗng
        rawSlides = rawSlides.map(s => s.trim()).filter(s => s.length > 0);

        if (rawSlides.length === 0) {
            return res.status(400).json({ error: "Không tìm thấy nội dung hợp lệ trong file!" });
        }

        // 3. Ghi vào Database
        const { data: lectureData, error: lectureError } = await supabase
            .from('lectures')
            .insert([{ user_id, title, description, status: 'draft' }])
            .select()
            .single();

        if (lectureError) throw lectureError;

        const lectureId = lectureData.id;
        const slidesToInsert = rawSlides.map((content, index) => ({
            lecture_id: lectureId,
            order_index: index + 1,
            content: content
        }));

        const { error: slidesError } = await supabase
            .from('slides')
            .insert(slidesToInsert);

        if (slidesError) throw slidesError;

        res.status(201).json({
            status: 'success',
            message: 'Trích xuất và tạo bài giảng từ file thành công!',
            data: { lectureId, total_slides: rawSlides.length }
        });

    } catch (error) {
        console.error('[ERROR] Lỗi khi tạo bài giảng từ file:', error.message);
        res.status(500).json({ error: error.message });
    }
};
