import os
import random
import asyncio
import time
import schedule
import sqlite3
from pyrogram import Client, types
from configs import API_ID, API_HASH, BOT_TOKEN, TARGET_CHANNEL_USERNAME, DOWNLOAD_DIR1, DOWNLOAD_DIR2

# Подключение к базе данных
DB_PATH = "posted_images.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posted_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

init_db()

def is_posted(filename: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM posted_images WHERE filename = ?", (filename,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_as_posted(filename: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posted_images (filename) VALUES (?)", (filename,))
    conn.commit()
    conn.close()

def get_image_files(folder: str):
    """Возвращает список путей к файлам с изображениями в папке."""
    valid_ext = (".jpg", ".jpeg", ".png", ".gif")
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(valid_ext) and os.path.isfile(os.path.join(folder, f))
    ]

def get_random_image(folder: str) -> str:
    """
    Выбирает случайное изображение из папки, исключая уже опубликованные.
    Если все изображения использованы, база очищается.
    """
    files = get_image_files(folder)
    available = [f for f in files if not is_posted(f)]
    
    if not available:  # Если все файлы использованы, очищаем базу
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posted_images")
        conn.commit()
        conn.close()
        available = files
    
    selected = random.choice(available)
    mark_as_posted(selected)
    return selected

async def post_images():
    """
    Формирует пост из 10 фотографий (первая из DOWNLOAD_DIR1, остальные 9 из DOWNLOAD_DIR2)
    и публикует их в заданный телеграм-канал.
    """
    image1 = get_random_image(DOWNLOAD_DIR1)
    images_folder2 = [get_random_image(DOWNLOAD_DIR2) for _ in range(9)]
    
    media = [types.InputMediaPhoto(media=image1)]
    for img in images_folder2:
        media.append(types.InputMediaPhoto(media=img))
    
    async with Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
        await app.send_media_group(chat_id=TARGET_CHANNEL_USERNAME, media=media)
        print("Пост опубликован!")

def job():
    """Функция-обёртка для запуска асинхронной публикации."""
    try:
        asyncio.run(post_images())
    except Exception as e:
        print(f"Ошибка при публикации: {e}")

def main():
    schedule.every(3).hours.do(job)
    print("Скрипт запущен. Публикация будет производиться каждые 3 часа.")
    job()
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
