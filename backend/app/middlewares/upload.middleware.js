const multer = require('multer');

// Lưu file tạm vào RAM (memory buffer) để xử lý nhanh thay vì ghi ra đĩa
const storage = multer.memoryStorage();

// Chỉ cho phép upload file text và word
const fileFilter = (req, file, cb) => {
    const allowedMimeTypes = [
        'text/plain',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // docx
        'application/msword' // doc
    ];

    if (allowedMimeTypes.includes(file.mimetype) || file.originalname.match(/\.(txt|docx|doc)$/)) {
        cb(null, true);
    } else {
        cb(new Error('Chỉ chấp nhận file định dạng .txt hoặc .docx!'), false);
    }
};

const upload = multer({
    storage: storage,
    limits: {
        fileSize: 5 * 1024 * 1024 // Giới hạn 5MB
    },
    fileFilter: fileFilter
});

module.exports = upload;
