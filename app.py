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
            ["python", "-m", "yt_dlp", "-g", url],
            capture_output=True,
            text=True,
            timeout=60
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode != 0:
            return None

        video_url = result.stdout.strip().split("\n")[0]
        return video_url

    except Exception as e:
        print("ERROR:", e)
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
    raw_data = request.get_data()
    print("RAW BODY:", raw_data)

    try:
        json_data = request.get_json(force=True)
        print("PARSED JSON:", json_data)
    except Exception as e:
        print("JSON PARSE ERROR:", e)

    return "ok"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
