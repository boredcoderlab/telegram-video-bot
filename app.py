import os
import subprocess
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def extract_video_url(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-g", url],
            capture_output=True,
            text=True,
            timeout=60
        )
        video_url = result.stdout.strip().split("\n")[0]
        return video_url
    except Exception:
        return None

def send_video(chat_id, video_url):
    requests.post(
        f"{TELEGRAM_API}/sendVideo",
        data={
            "chat_id": chat_id,
            "video": video_url,
            "disable_notification": True
        }
    )

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message")

    if not message:
        return "ok"

    text = message.get("text", "")
    chat_id = message["chat"]["id"]

    if text.startswith("/soft"):
        parts = text.split(" ", 1)
        if len(parts) == 2:
            reddit_url = parts[1]
            video_url = extract_video_url(reddit_url)
            if video_url:
                send_video(chat_id, video_url)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
