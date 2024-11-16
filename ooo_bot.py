import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN, DADATA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# URL для API Dadata
DADATA_URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"

# Заголовки для запроса
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Token {DADATA_API_KEY}"
}

# Функция для поиска информации по ИНН
def get_organization_info(inn):
    data = {
        "query": inn
    }

    try:
        response = requests.post(DADATA_URL, json=data, headers=HEADERS)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("suggestions"):
            org_info = response_data["suggestions"][0]["data"]
            name = org_info.get("name", {}).get("full_with_opf", "Неизвестно")
            address = org_info.get("address", {}).get("value", "Неизвестен")
            status = org_info.get("state", {}).get("status", "Неизвестен")

            return (
                f"📄 Название: {name}\n"
                f"📍 Адрес: {address}\n"
                f"🔍 Статус: {status}"
            )
        else:
            return "Организация не найдена. Проверьте ИНН и попробуйте снова."
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return "Произошла ошибка при запросе к Dadata API."

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Добро пожаловать! Отправьте мне ИНН организации, и я найду информацию о ней.")

# Обработчик для получения ИНН от пользователя
@dp.message()
async def handle_inn_query(message: types.Message):
    inn = message.text.strip()
    if not inn.isdigit() or len(inn) not in [10, 12]:
        await message.answer("Пожалуйста, введите корректный ИНН (10 или 12 цифр).")
        return

    info = get_organization_info(inn)
    await message.answer(info)

# Основная функция
async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
