import unittest
import tempfile
import asyncio
from unittest.mock import AsyncMock, patch
from pathlib import Path
import bot
from downloader import (
    find_urls,
    detect_platform,
    is_pinterest_url,
    resolve_pinterest_url,
    is_twitter_url,
    render_progress_bar,
    MediaDownloader,
    FFMPEG_EXE,
    VIDEO_EXTS,
    IMAGE_EXTS,
)
import config
import analytics


class DummyTelegramUser:
    def __init__(self, id: int, username: str = "", first_name: str = ""):
        self.id = id
        self.username = username
        self.first_name = first_name


class TestDownloader(unittest.TestCase):

    def test_find_urls(self):
        text = "Check out this reel https://www.instagram.com/reel/C3abc123/ and this yt https://youtu.be/dQw4w9WgXcQ"
        urls = find_urls(text)
        self.assertEqual(len(urls), 2)
        self.assertIn("https://www.instagram.com/reel/C3abc123/", urls)
        self.assertIn("https://youtu.be/dQw4w9WgXcQ", urls)

    def test_youtube_quality_options_skip_metadata_probe(self):
        with patch("downloader.yt_dlp.YoutubeDL") as youtube_dl:
            options = asyncio.run(
                MediaDownloader().extract_media_options("https://youtu.be/dQw4w9WgXcQ")
            )

        youtube_dl.assert_not_called()
        self.assertEqual(
            [quality["code"] for quality in options["qualities"]],
            ["res_1080", "res_720", "res_480", "res_360"],
        )

    def test_youtube_playlist_link_shows_quality_picker(self):
        class DummyStatusMessage:
            message_id = 654
            chat = type("Chat", (), {"id": 321})()

            async def edit_text(self, text, **kwargs):
                self.text = text
                self.reply_markup = kwargs.get("reply_markup")

        class DummyMessage:
            text = "https://youtube.com/watch?v=-JifAmfOtAQ&list=RDdG-SSbhlMdA&index=5"
            chat = type("Chat", (), {"id": 321})()

            async def reply_text(self, *_args, **_kwargs):
                self.status_message = DummyStatusMessage()
                return self.status_message

        update = type(
            "DummyUpdate",
            (),
            {
                "effective_user": DummyTelegramUser(id=456, username="tester", first_name="Test"),
                "message": DummyMessage(),
            },
        )()
        original_sessions = bot.url_sessions.copy()
        bot.url_sessions.clear()

        try:
            with patch.object(bot, "check_user_auth", new=AsyncMock(return_value=True)):
                asyncio.run(bot.text_handler(update, object()))
            status_message = update.message.status_message
            self.assertIn("YouTube video", status_message.text)
            callback_data = [
                button.callback_data
                for row in status_message.reply_markup.inline_keyboard
                for button in row
            ]
            self.assertTrue(any("res_1080" in value for value in callback_data))
            self.assertTrue(any("res_720" in value for value in callback_data))
        finally:
            bot.url_sessions.clear()
            bot.url_sessions.update(original_sessions)

    def test_professional_link_status_messages(self):
        self.assertIn("Connecting to YouTube", bot.build_platform_status("YouTube", "video", "connect"))
        self.assertIn("Analyzing video", bot.build_platform_status("YouTube", "video", "analyze"))
        self.assertIn("Connecting to Instagram", bot.build_platform_status("Instagram", "reel", "connect"))
        self.assertIn("Analyzing video", bot.build_platform_status("Instagram", "reel", "analyze"))

    def test_detect_platform(self):
        self.assertEqual(detect_platform("https://www.instagram.com/reel/abc123/"), "Instagram")
        self.assertEqual(detect_platform("https://youtu.be/abc123"), "YouTube")
        self.assertEqual(detect_platform("https://x.com/user/status/123"), "X (Twitter)")
        self.assertEqual(detect_platform("https://www.tiktok.com/@user/video/123"), "TikTok")
        self.assertEqual(detect_platform("https://pin.it/abc123"), "Pinterest")
        self.assertEqual(detect_platform("https://www.reddit.com/r/videos/comments/123/"), "Reddit")
        self.assertEqual(detect_platform("https://example.com/video.mp4"), "Web Video")

    def test_platform_helpers(self):
        self.assertTrue(is_pinterest_url("https://www.pinterest.com/pin/123456/"))
        self.assertTrue(is_pinterest_url("https://pin.it/abc1234"))
        self.assertFalse(is_pinterest_url("https://youtube.com/watch?v=123"))
        self.assertEqual(
            resolve_pinterest_url("https://www.pinterest.com/pin/123456/"),
            "https://www.pinterest.com/pin/123456/",
        )

        self.assertTrue(is_twitter_url("https://x.com/NASA/status/1783547844005695627"))
        self.assertTrue(is_twitter_url("https://twitter.com/user/status/123"))
        self.assertFalse(is_twitter_url("https://instagram.com/p/123"))

    def test_media_extensions(self):
        self.assertIn(".mp4", VIDEO_EXTS)
        self.assertIn(".png", IMAGE_EXTS)
        self.assertIn(".jpg", IMAGE_EXTS)
        self.assertIn(".webp", IMAGE_EXTS)

    def test_render_progress_bar(self):
        bar_0 = render_progress_bar(0, width=10)
        self.assertEqual(bar_0, "[░░░░░░░░░░] 0%")

        bar_50 = render_progress_bar(50, width=10)
        self.assertEqual(bar_50, "[█████░░░░░] 50%")

        bar_100 = render_progress_bar(100, width=10)
        self.assertEqual(bar_100, "[██████████] 100%")

    def test_user_auth(self):
        # By default when whitelist is empty, any user is allowed
        self.assertTrue(config.is_user_allowed(12345678))

    def test_ffmpeg_resolved(self):
        self.assertTrue(bool(FFMPEG_EXE), "FFmpeg binary should be resolved")

    def test_ytdlp_uses_parallel_fragment_downloads(self):
        options = MediaDownloader()._get_ydl_base_opts()
        self.assertEqual(options["concurrent_fragment_downloads"], 8)

    def test_admin_config(self):
        self.assertEqual(config.ADMIN_USERNAME, "@MrMahnurAlam")
        self.assertIn("MrMahnurAlam", config.ADMIN_LINK)

    def test_telegram_size_limits(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as fh:
            fh.write(b"x" * (11 * 1024 * 1024))
            path = fh.name
        try:
            self.assertTrue(bot.is_telegram_size_limit_exceeded(path, "photo"))
            self.assertFalse(bot.is_telegram_size_limit_exceeded(path, "video"))
        finally:
            Path(path).unlink(missing_ok=True)

    def test_user_modes(self):
        uid = 999999
        # Default mode is instant
        self.assertEqual(config.get_user_mode(uid), "instant")
        config.set_user_mode(uid, "picker")
        self.assertEqual(config.get_user_mode(uid), "picker")
        config.set_user_mode(uid, "instant")
        self.assertEqual(config.get_user_mode(uid), "instant")

    def test_start_command_from_callback_query(self):
        class DummyMessage:
            def __init__(self):
                self.text = None
                self.reply_markup = None

            async def reply_text(self, text, **kwargs):
                self.text = text
                self.reply_markup = kwargs.get("reply_markup")

        class DummyCallbackQuery:
            def __init__(self, message):
                self.message = message

        class DummyContext:
            bot = type("Bot", (), {"username": "testbot"})()

        message = DummyMessage()
        update = type(
            "DummyUpdate",
            (),
            {
                "effective_user": DummyTelegramUser(id=123, username="tester", first_name="Test"),
                "message": None,
                "callback_query": DummyCallbackQuery(message),
            },
        )()

        async def fake_check_user_auth(_):
            return True

        original = bot.check_user_auth
        bot.check_user_auth = fake_check_user_auth
        try:
            asyncio.run(bot.start_command(update, DummyContext()))
        finally:
            bot.check_user_auth = original

        self.assertIn("Hello, Test!", message.text)
        self.assertIsNotNone(message.reply_markup)

    def test_start_button_cancels_pending_analysis(self):
        class DummyMessage:
            message_id = 4242
            chat = type("Chat", (), {"id": 99})()

        class DummyCallbackQuery:
            data = "start_bot"
            message = DummyMessage()

            async def answer(self):
                pass

        update = type(
            "DummyUpdate",
            (),
            {
                "effective_user": DummyTelegramUser(id=123, username="tester", first_name="Test"),
                "callback_query": DummyCallbackQuery(),
            },
        )()
        original_sessions = bot.url_sessions.copy()
        bot.url_sessions.clear()
        bot.url_sessions.update({
            "pending": {
                "analysis_message_id": 4242,
                "analysis_chat_id": 99,
                "user_id": 123,
            },
            "other": {"analysis_message_id": 7, "analysis_chat_id": 99, "user_id": 456},
        })

        try:
            with patch.object(bot, "check_user_auth", new=AsyncMock(return_value=True)):
                with patch.object(bot, "start_command", new=AsyncMock()) as start_command:
                    asyncio.run(bot.button_callback_handler(update, object()))
                    start_command.assert_awaited_once()

            self.assertNotIn("pending", bot.url_sessions)
            self.assertIn("other", bot.url_sessions)
        finally:
            bot.url_sessions.clear()
            bot.url_sessions.update(original_sessions)

    def test_admin_check(self):
        admin_user = DummyTelegramUser(id=12345, username="MrMahnurAlam")
        self.assertTrue(config.is_admin(admin_user))

        normal_user = DummyTelegramUser(id=67890, username="regular_joe")
        self.assertFalse(config.is_admin(normal_user))

    def test_analytics(self):
        test_uid = 777888999
        analytics.track_user(test_uid, "tester_bot", "Tester")
        self.assertIn(test_uid, analytics.get_all_user_ids())

        analytics.track_download(test_uid, "YouTube", "video")
        analytics.track_download(test_uid, "Instagram", "photo")

        summary = analytics.get_analytics_summary()
        self.assertGreaterEqual(summary["total_users"], 1)
        self.assertGreaterEqual(summary["total_downloads"], 2)

        # Check dashboard generators return non-empty strings
        admin_dash = analytics.format_admin_dashboard()
        self.assertIn("Bot Analytics", admin_dash)
        self.assertIn("YouTube", admin_dash)

        pub_dash = analytics.format_public_dashboard()
        self.assertIn("All Media/Video Downloader", pub_dash)


if __name__ == "__main__":
    unittest.main()

