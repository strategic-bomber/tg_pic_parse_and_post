import os
import random
import asyncio
import time
import schedule
from pyrogram import Client, types
from configs import API_ID, API_HASH, BOT_TOKEN, TARGET_CHANNEL_USERNAME, DOWNLOAD_DIR1, DOWNLOAD_DIR2

# Множества для отслеживания использованных файлов
used_folder1 = set()
used_folder2 = set()

def get_image_files(folder: str):
    """Возвращает список путей к файлам с изображениями в папке."""
    valid_ext = (".jpg", ".jpeg", ".png", ".gif")
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(valid_ext) and os.path.isfile(os.path.join(folder, f))
    ]

def get_random_image(folder: str, used_set: set) -> str:
    """
    Выбирает случайное изображение из папки, исключая уже использованные.
    Если все изображения использованы, сбрасывает список использованных.
    """
    files = get_image_files(folder)
    available = list(set(files) - used_set)
    if not available:  # если все файлы уже использованы, сбрасываем список
        used_set.clear()
        available = files
    selected = random.choice(available)
    used_set.add(selected)
    return selected

async def post_images():
    """
    Формирует пост из 10 фотографий (первая из DOWNLOAD_DIR1, остальные 9 из DOWNLOAD_DIR2)
    и публикует их в заданный телеграм-канал.
    """
    # Выбираем изображения
    image1 = get_random_image(DOWNLOAD_DIR1, used_folder1)
    images_folder2 = [get_random_image(DOWNLOAD_DIR2, used_folder2) for _ in range(9)]
    
    # Формируем группу медиа
    media = [types.InputMediaPhoto(media=image1)]
    for img in images_folder2:
        media.append(types.InputMediaPhoto(media=img))
    
    # Создаем клиента для бота с BOT_TOKEN, API_ID и API_HASH
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
    # Планируем выполнение задания каждые 3 часа
    schedule.every(30).seconds.do(job)
    # schedule.every(3).hours.do(job)
    print("Скрипт запущен. Публикация будет производиться каждые 3 часа.")
    # Немного подождем перед первым запуском (опционально)
    job()
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
