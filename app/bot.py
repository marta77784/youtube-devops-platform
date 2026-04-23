import os
import json
import schedule
import time
from datetime import datetime
from googleapiclient.discovery import build
import telebot

YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

CHANNELS = [
    {"handle": "@funnydamon", "name": "Funny Damon Show"},
    {"handle": "@damondylan", "name": "Damon Dylan"},
]

bot = telebot.TeleBot(TELEGRAM_TOKEN)
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def get_stats(handle):
    response = youtube.channels().list(
        part="snippet,statistics",
        forHandle=handle
    ).execute()

    if not response.get("items"):
        return None

    ch = response["items"][0]
    return {
        "title": ch["snippet"]["title"],
        "subscribers": int(ch["statistics"].get("subscriberCount", 0)),
        "views": int(ch["statistics"].get("viewCount", 0)),
        "videos": int(ch["statistics"].get("videoCount", 0)),
    }


def send_daily_report():
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    message = f"📊 *YouTube Stats — {date}*\n\n"

    total_subs = 0
    for ch in CHANNELS:
        stats = get_stats(ch["handle"])
        if stats:
            total_subs += stats["subscribers"]
            message += (
                f"*{stats['title']}*\n"
                f"👥 Подписчики: {stats['subscribers']:,}\n"
                f"👁 Просмотры: {stats['views']:,}\n"
                f"🎬 Видео: {stats['videos']}\n\n"
            )

    message += f"*Всего подписчиков: {total_subs:,}*"

    bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode="Markdown")
    print(f"[{date}] Report sent")


def save_stats():
    data = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "channels": []}
    for ch in CHANNELS:
        stats = get_stats(ch["handle"])
        if stats:
            data["channels"].append(stats)

    with open("/data/stats.json", "w") as f:
        json.dump(data, f, indent=2)


def job():
    save_stats()
    send_daily_report()


schedule.every().day.at("09:00").do(job)

print("Bot started. Waiting for 09:00...")
job()

while True:
    schedule.run_pending()
    time.sleep(60)
