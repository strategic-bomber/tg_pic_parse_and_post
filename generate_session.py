from pyrogram import Client
from configs import API_ID, API_HASH
api_id = API_ID
api_hash = API_HASH 
session_name = 'first_session'

app = Client(session_name, api_id, api_hash)

with app:
    print('Успешная авторизация. Сессия сохранена.')

