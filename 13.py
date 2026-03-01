import os
from dotenv import load_dotenv
import sys
import requests
import json

load_dotenv(load_dotenv(dotenv_path="C:/Users/User/Desktop/Python/maga/13/.gitignore/.env"))
# Получаем API-ключ из переменной окружения
API_KEY = os.getenv("VT_API_KEY")


if not API_KEY:
    print("Ошибка: не задана переменная окружения VT_API_KEY")
    sys.exit(1)

if len(sys.argv) != 2:
    print("Использование: python vt_check.py <SHA256_ХЭШ_ФАЙЛА>")
    sys.exit(1)

file_hash = sys.argv[1]

# URL API VirusTotal v3 для получения информации о файле
url = f"https://www.virustotal.com/api/v3/files/{file_hash}"

headers = {
    "x-apikey": API_KEY
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверка на HTTP-ошибки

    data = response.json()

    # Вывод полного JSON-ответа
    print(json.dumps(data, indent=4, ensure_ascii=False))

    # Пример извлечения конкретных данных (статистика детекта)
    stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
    print("\n=== Статистика анализа ===")
    print(json.dumps(stats, indent=4, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")
    sys.exit(1)