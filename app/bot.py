import os
import json
import schedule
import time
from datetime import datetime
from googleapiclient.discovery import build
import telebot
from groq import Groq

YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

CHANNELS = [
    {"handle": "@funnydamon", "name": "Funny Damon Show"},
    {"handle": "@damondylan", "name": "Damon Dylan"},
]

bot = telebot.TeleBot(TELEGRAM_TOKEN)
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)


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


def get_ai_analysis(all_stats):
    stats_text = ""
    for s in all_stats:
        stats_text += f"{s['title']}: {s['subscribers']:,} подписчиков, {s['views']:,} просмотров, {s['videos']} видео\n"

    prompt = f"""Ты аналитик YouTube каналов. Вот сегодняшняя статистика:

{stats_text}

Дай короткий анализ в 2-3 предложениях на русском языке.
Отметь что хорошо, что можно улучшить, общий тренд."""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI анализ недоступен: {e}"


def send_daily_report():
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    message = f"📊 *YouTube Stats — {date}*\n\n"

    all_stats = []
    total_subs = 0

    for ch in CHANNELS:
        stats = get_stats(ch["handle"])
        if stats:
            all_stats.append(stats)
            total_subs += stats["subscribers"]
            message += (
                f"*{stats['title']}*\n"
                f"👥 Подписчики: {stats['subscribers']:,}\n"
                f"👁 Просмотры: {stats['views']:,}\n"
                f"🎬 Видео: {stats['videos']}\n\n"
            )

    message += f"*Всего подписчиков: {total_subs:,}*\n\n"

    ai_analysis = get_ai_analysis(all_stats)
    message += f"*Всего подписчиков: {total_subs:,}*"

    bot.send_message(TELEGRAM_CHAT_ID, message, parse_mode="Markdown")
    bot.send_message(TELEGRAM_CHAT_ID, f"🤖 AI Анализ:\n{ai_analysis}")
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
