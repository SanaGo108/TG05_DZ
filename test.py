from prokerala_api import ApiClient
from config import CLIENT_ID, CLIENT_SECRET
from datetime import datetime

# Инициализация клиента API
api_client = ApiClient(CLIENT_ID, CLIENT_SECRET)

def check_api():
    latitude = 28.6139  # Широта (Дели, Индия)
    longitude = 77.2090  # Долгота (Дели, Индия)
    datetime_now = datetime.now()

    try:
        # Запрос к API
        panchang = api_client.astrology.panchang(
            latitude=latitude,
            longitude=longitude,
            datetime=datetime_now
        )
        return panchang.data
    except Exception as e:
        print(f"Ошибка при запросе к API: {e}")
        return None

# Проверка ответа
data = check_api()
if data:
    print("Данные панчанга получены успешно:")
    print(data)
else:
    print("Не удалось получить данные панчанга.")
