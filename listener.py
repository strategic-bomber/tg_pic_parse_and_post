from pyrogram import Client, filters, idle
from configs import CHANNEL_USERNAME, DOWNLOAD_DIR1, DOWNLOAD_DIR2
import os

# Укажите параметры сессии и рабочую директорию
app = Client("first_session", workdir=".")

# Создаем папку для скачивания, если её нет
os.makedirs(DOWNLOAD_DIR2, exist_ok=True)

# Функция для сохранения фото
def save_photo(message):
    channel_id = message.chat.id  # или message.chat.username, если есть
    file_path = os.path.join(DOWNLOAD_DIR2, f"{channel_id}_photo_{message.id}.jpg")

    if not os.path.exists(file_path):  # Проверяем, загружали ли уже фото
        message.download(file_path)
        print(f"✅ Фото {message.id} сохранено в {file_path}")
    else:
        print(f"⚠️ Фото {message.id} уже загружено, пропускаем...")

# Функция для загрузки всех предыдущих фото
def fetch_old_photos():
    print("🔄 Загружаем старые фото...")
    for message in app.get_chat_history(CHANNEL_USERNAME):
        if message.photo:
            save_photo(message)
    print("✅ Загрузка старых фото завершена.")

# Обработчик сообщений с фото
@app.on_message(filters.chat(CHANNEL_USERNAME) & filters.photo)
def handle_new_photo(client, message):
    print(f"📥 Новое фото обнаружено: {message.id}")
    save_photo(message)

# Запуск слушателя
def start_listener():
    app.start()  # Запускаем клиента вручную
    print("🔔 Слушатель запущен. Ожидание новых фото...")
    fetch_old_photos()  # Загружаем старые фото
    idle()  # Ожидаем новые сообщения (функция из pyrogram)
    app.stop()  # Останавливаем клиента после завершения работы

# Запуск скрипта
if __name__ == "__main__":
    start_listener()
