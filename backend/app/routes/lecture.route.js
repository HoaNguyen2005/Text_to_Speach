const express = require('express');
const router = express.Router();
const lectureController = require('../controllers/lecture.controller');
const upload = require('../middlewares/upload.middleware');

// Lấy danh sách
router.get('/', lectureController.getAllLectures);

// 1. Tạo bài giảng qua nhập liệu trực tiếp (gửi JSON)
router.post('/direct', lectureController.createLectureDirect);

// 2. Tạo bài giảng từ việc upload file (gửi FormData có chứa file)
router.post('/upload', upload.single('document_file'), lectureController.createLectureFromFile);

module.exports = router;
