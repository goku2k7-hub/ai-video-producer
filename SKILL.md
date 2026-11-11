---
name: ai-video-producer
description: Autonomous end-to-end AI video production pipeline for high-retention tech explainers, open-source showcases, and storytelling devlogs (TikTok/Reels/Shorts 9:16 vertical and YouTube 16:9 landscape). Covers research, retention scripting, Edge-TTS audio generation, multitrack SFX mixing, GSAP HTML5 motion graphics, and zero-disk Puppeteer FFmpeg pipe rendering.
---

# 🎬 AI Video Producer Skill (v1.0 — Director & Engine Edition)

This skill provides the complete end-to-end autonomous engineering and motion design workflow to produce viral, high-retention tech videos, open-source repo showcases, and narrative devlogs.

---

## 📌 1. When to Activate This Skill

Activate this skill whenever:
* The user asks to produce, script, or render a video for TikTok, YouTube Shorts, Reels (9:16 vertical) or YouTube (16:9 landscape).
* The user wants to showcase a new tech trend, GitHub repository, AI model, or software tool.
* The user asks to create a video of specific duration (e.g. 40s quick bite, 60s standard, or 1m30s - 2m deep-dive).
* The user mentions automating video creation, batch video rendering, or generating video scripts and thumbnails.

---

## ⚡ 2. The 5 Core Production Laws

### Law 1: The 5-Act High-Retention Scripting Formula
Never read documentation line-by-line. Structure every video into an emotional roller-coaster:
1. **Act 1: The Shocking Hook (0s - 3s/15s)**: A controversial question, unexpected contradiction, or restricted secret (*"Google vừa âm thầm khóa AI mạnh nhất lịch sử..."*).
2. **Act 2: The Benchmark Shatterer (15s - 40s)**: Tangible proof, stats, leaderboard ranking (#1 Artificial Analysis, 100k stars on GitHub).
3. **Act 3: The Killer Feature / Simulation (40s - 70s)**: Tangible demonstration (scanning 1M lines of code, hunting zero-day bugs, auto-patching).
4. **Act 4: The Twist / High-Stakes Dilemma (70s - 90s)**: High stakes, challenges, or "double-edged sword" implications.
5. **Act 5: Paradigm Shift & Community CTA (90s - 110s)**: Call-to-action question encouraging comments (*"Lập trình viên có bị thay thế? Bình luận bên dưới nhé!"*).

### Law 2: Azure Edge-TTS Safety & Audio Pacing
* **Voice Engine**: Microsoft Edge-TTS with voice `vi-VN-NamMinhNeural`.
* **Chunking Rules**: Never send paragraphs $> 200$ characters. Split into single punchy sentences.
* **Safety Filter Bypass**: Microsoft Azure automatically drops connection (`NoAudioReceived`) if text contains words related to distress, gambling, or violence (e.g. "lệch rate", "hút máu", "nô lệ", "trắng tay", "đập nát"). Rephrase cleanly:
  * "lệch rate / trắng tay" ➔ "chưa mở khóa được nhân vật mong muốn" / "lệch tướng".
  * "hút máu" ➔ "tiêu tốn nhiều tài nguyên".
* **Pacing**: Short-form videos require urgency. Always apply FFmpeg `atempo=1.16` to `1.18`.
* **Audio Multitrack Mixing**:
  * Voiceover: 100% volume, centered, crisp stereo.
  * BGM: Tech-thriller / Lo-fi synthwave set to `-16dB` to `-18dB`.
  * Timed SFX: Add alarms, whooshes, metal vault clanks, radar pings, and bass drops aligned with GSAP timeline events.

### Law 3: Visual Layout & Safe-Zone Rules
* **Format 9:16 Vertical (1080 x 1920)**:
  * **Top Safety Margin**: Keep 120px padding from the top to avoid phone camera cutouts and notch.
  * **Bottom TikTok Safe Area**: Place all subtitles and critical text **at least 220px - 260px above the bottom** (`bottom: 230px`) so they are never obscured by TikTok caption bars, audio discs, or navigation buttons.
  * **Right Margin**: Keep interactive badges away from the far-right edge (TikTok like/comment/share icons).
* **Format 16:9 Landscape (1920 x 1080)**:
  * Subtitles centered at `bottom: 45px - 50px`.
  * Cinematic aspect ratio, widescreen parallax, and anime backdrop framing.

### Law 4: Zero-Disk Headless Pipe Rendering
* **Never dump thousands of JPEG/PNG files to disk**:
  * Use Puppeteer headless Chrome:
    ```javascript
    await page.evaluate((f, fps) => window.seekToFrame(f, fps), f, fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    ffmpeg.stdin.write(buf);
    ```
  * Pipe raw image stream directly into FFmpeg `stdin` (`-f image2pipe -vcodec mjpeg -i -`).
  * Yields zero temporary disk clutter, maximum I/O throughput, and instant 30 FPS MP4 encoding.

### Law 5: High-CTR Thumbnail Engineering
* Generate a dedicated high-contrast thumbnail alongside every video:
  * High-impact keywords: 2-3 words per line, font-size $\ge 80\text{px}$.
  * Triple-layer drop shadow (`0 6px 0 #000, 0 12px 30px rgba(0,0,0,1), 0 0 50px glow`).
  * Contrast colors: White + Bright Yellow (`#ffd700` / `#ffeb3b`) + Neon Cyan (`#00f2fe`) on dark carbon or anime background.

---

## 🛠️ 3. Standard Production Directory Structure

Maintain this clean workspace structure for all video projects:
```
video AI/
├── 01_Output_Videos/       # Rendered final MP4 videos
├── 02_Thumbnails/          # Generated JPG thumbnails and preview frames
├── 03_Audio_Tracks/        # Voiceover tracks, BGM, and final mixed audio
├── 04_Templates/           # HTML5/CSS/GSAP templates and visual assets
│   └── assets/             # Backgrounds, sprites, logos, sound FX
├── 05_Scripts/             # Python & Node.js automation scripts
└── 06_Data_Configs/        # Script JSONs, scene configs, and timestamps
```

---

## 🚀 4. Step-by-Step Execution Workflow

When a user requests a video:
1. **Define Specs**: Determine format (9:16 or 16:9), duration (40s, 60s, or 1m30s - 2m), and theme.
2. **Draft Script**: Create 5-act script segmented into $\le 200$-character chunks.
3. **Generate Voice & Mix Audio**:
   - Run Edge-TTS with polite delay (~1.5s between chunks).
   - Apply `atempo=1.16` speedup.
   - Mix with procedural BGM and SFX into `final_audio_<name>.m4a`.
   - Measure exact audio duration $T$.
4. **Build HTML5 Template**:
   - Design animated scenes matching the audio timestamps.
   - Implement `window.seekToFrame(frameIndex, fps)` driven by GSAP `masterTL.time(t)`.
5. **Verify Preview**:
   - Capture 5 sample frames at key timestamps.
   - Inspect visually for contrast, safe-zone compliance, and layout balance.
6. **Execute Headless Render**:
   - Run Puppeteer script to render $\lceil T \times 30 \rceil$ frames into FFmpeg stdin.
   - Generate dedicated thumbnail.
7. **Verify & Deliver**:
   - Verify with `ffprobe` (resolution, duration, audio-video sync).
   - Provide clickable file links (`file://`) to the user.
