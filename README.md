# 🎬 AI Video Producer (Antigravity Skill)

> Autonomous end-to-end AI video production pipeline for high-retention tech explainers, open-source showcases, and storytelling videos (TikTok/Reels/Shorts 9:16 vertical and YouTube 16:9 landscape).

---

## 🌟 Tính Năng Nổi Bật

- **Tự động hóa 100%**: Từ kịch bản giữ chân 5 màn đến xuất video MP4 Full HD và Thumbnail.
- **Giọng đọc tiếng Việt tự nhiên**: Tích hợp `edge-tts` với cơ chế vượt qua bộ lọc an toàn của Azure và tăng tốc nhịp đọc (`atempo=1.16x`).
- **Âm thanh đa tầng (Multitrack Sound Design)**: Tự động sinh nhạc nền (Tech-thriller hoặc Lo-Fi) kèm hiệu ứng âm thanh (còi báo động, khóa bảo mật, radar scan).
- **Engine Render "Zero-Disk"**: Puppeteer (Chrome Headless) stream trực tiếp byte ảnh vào luồng `stdin` của FFmpeg mà không lưu file ảnh tạm ra ổ cứng.
- **Hỗ trợ đa định dạng**:
  - **9:16 Dọc** (1080x1920): Tối ưu vùng an toàn (Safe-Zone) cho TikTok, Reels, Shorts.
  - **16:9 Ngang** (1920x1080): Chuẩn điện ảnh cho YouTube Long-form / Devlog.

---

## 📁 Cấu Trúc Thư Mục

```
ai-video-producer/
├── SKILL.md                   # Khai báo Skill và bộ luật sản xuất cho AI Assistant
├── README.md                  # Hướng dẫn sử dụng
├── requirements.txt           # Thư viện Python cần thiết
├── package.json               # Thư viện Node.js cần thiết
└── scripts/
    ├── synthesize_voice.py    # Bộ tổng hợp giọng đọc và mix nhạc nền tự động
    └── render_pipeline.js     # Engine render video headless Chrome + FFmpeg pipe
```

---

## 🛠️ Yêu Cầu Cài Đặt (Prerequisites)

1. **FFmpeg**: Đã cài đặt và có trong biến môi trường `PATH`.
2. **Google Chrome**: Đã cài đặt trên máy.
3. **Python 3.10+**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Node.js 18+**:
   ```bash
   npm install
   ```

---

## 🚀 Cách Cài Đặt Vào Google Antigravity / Gemini CLI

Clone trực tiếp thư mục này vào thư mục skills toàn cục:

```bash
# Trên Windows PowerShell:
git clone https://github.com/<YOUR_USERNAME>/ai-video-producer.git "$env:USERPROFILE\.gemini\config\skills\ai-video-producer"

# Trên macOS / Linux:
git clone https://github.com/<YOUR_USERNAME>/ai-video-producer.git ~/.gemini/config/skills/ai-video-producer
```

---

## 💬 Cách Sử Dụng Trong Antigravity

Sau khi cài đặt, bạn chỉ cần ra lệnh cho AI trong cửa sổ chat:
- *"Làm video TikTok 1p30s về chủ đề DeepSeek R1"*
- *"Tạo video dọc 9:16 giới thiệu thư viện Crawl4AI"*
- *"Làm video YouTube 16:9 kể chuyện Devlog"*

Hệ thống sẽ tự động kích hoạt Skill và thực hiện toàn bộ quy trình!
