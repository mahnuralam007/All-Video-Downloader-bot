<div align="center">

# 📥 All Media/Video Downloader Bot

### An open-source, ultra-fast Telegram bot for downloading media and extracting MP3 audio from all major social platforms.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10 | 3.11](https://img.shields.io/badge/Python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-v20%2B-blue?logo=telegram)](https://core.telegram.org/bots/api)
[![yt-dlp](https://img.shields.io/badge/Powered%20By-yt--dlp-red?logo=youtube)](https://github.com/yt-dlp/yt-dlp)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![CI Tests](https://github.com/MrMahnurAlam/universal-media-downloader-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/MrMahnurAlam/universal-media-downloader-bot/actions)

[Live Bot Demo](https://t.me/videodownloader_allbot) • [Report Bug](https://github.com/mahnuralam007/allvideodownloaderbot/issues/new) • [Request Feature](.github/ISSUE_TEMPLATE/feature_request.md)

</div>

---

## 🌟 Supported Platforms

| Platform | Supported Content | Notes |
|---|---|---|
| 📸 **Instagram** | Reels, Posts, Carousels, Stories | HD Audio & Video |
| 🎥 **YouTube** | Shorts, Full Videos, Live Recordings | 1080p, 720p, 480p, 360p |
| 🐦 **X (Twitter)** | Videos, Clips, Animated GIFs | Best available stream |
| 🎵 **TikTok** | Videos & Sounds | No watermark |
| 📌 **Pinterest** | Video Pins & High-Res Clips | Clean MP4 |
| 🤖 **Reddit** | Videos with Audio | Audio/Video auto-merged |
| 📘 **Facebook** | Reels & Public Watch Videos | Fast delivery |
| 🌐 **1000+ Others** | Vimeo, Dailymotion, Twitch Clips, etc. | Powered by `yt-dlp` |

---

## ✨ Key Features

- **🎛️ Video Quality Picker:** Choose up to 1080p, 720p, 480p, or 360p before downloading. YouTube uses fast "up to" quality choices; other supported sites can provide detected formats.
- **⚡ Faster Downloads:** Uses parallel fragment downloads where supported and prefers a combined audio/video stream when it matches the selected quality.
- **📊 Real-time Animated Progress Bar:** Live updates directly on the Telegram message showing percentage, speed, downloaded size, and ETA:
  ```text
  ⏳ Downloading from YouTube...
  [████████░░░░] 67%
  ⚡ Speed: 5.4 MB/s | Size: 16.2 MB / 24.1 MB
  ⏱️ ETA: 1s
  ```
- **🎵 Studio MP3 Extraction:** Converts any video into a 192k MP3 audio file with the **official video thumbnail embedded as Album Cover Art** for Telegram's built-in music player.
- **📈 Built-in User Analytics & Admin Dashboard:** Real-time user tracking and download statistics:
  - Run `/stats` (or `/analytics`) to view total registered users, 24h & 7d active users, total downloads, breakdown by platform (Instagram, YouTube, etc.), and media types.
  - Interactive "🔄 Refresh Stats" button.
  - Broadcast announcements directly to all registered users via `/broadcast <message>`.
- **👥 Group Chat Ready:** Add the bot to any Telegram group chat with the 1-tap `[➕ Add Me to Your Group]` button in `/start`!
- **🛡️ Cross-Platform Filename Sanitization:** Built-in sanitization avoids Windows/Linux filesystem path issues (`[Errno 22]`) on unusual characters and emojis.

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/MrMahnurAlam/universal-media-downloader-bot.git
cd universal-media-downloader-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and fill in your Bot Token from [@BotFather](https://t.me/BotFather):
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### 4. Run the Bot
```bash
python bot.py
```

---

## 🐳 Docker Deployment (1-Command)

Run locally or on any Linux VPS (Ubuntu, Debian, CentOS):

```bash
docker compose up -d
```

To view logs:
```bash
docker compose logs -f
```

---

## ☁️ 1-Click Cloud Deployment (Free 24/7)

### Deploy on Koyeb:
1. Fork or push this repository to your GitHub.
2. Sign up at [koyeb.com](https://www.koyeb.com/) (Free).
3. Create a new service from your GitHub repository.
4. Set Environment Variable:
   - `TELEGRAM_BOT_TOKEN` = `your_bot_token`
5. Click **Deploy**!

---

## ⌨️ Bot Commands

| Command | Description |
|---|---|
| `/start` | Welcome greeting, supported platforms, and status |
| `/quality <url>` | Show quality choices for a video link |
| `/mode` | Show or toggle the saved download-mode preference |
| `/mp3 <url>` | Directly extract 192k MP3 audio with cover art |
| `/stats` | View download and user analytics |
| `/admin` | Contact the bot developer & admin directly (@MrMahnurAlam) |
| `/about` | Technical specs, engine versions, and architecture |
| `/help` | Complete user manual and instructions |

---

## 👑 Author & Admin Contact

- **Admin / Developer:** MrMahnurAlam ([@MrMahnurAlam](https://t.me/MrMahnurAlam))
- **Telegram Support:** [t.me/MrMahnurAlam](https://t.me/MrMahnurAlam)

Feel free to reach out for feature requests, issues, or feedback!

---

## 🧪 Running Tests

To run the automated unit test suite:
```bash
python -m unittest test_downloader.py
```

---

## 🤝 Contributing

Contributions are always welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

1. Fork the repo.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
⭐ Star this repository if you find it helpful!
</div>
