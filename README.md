# HSE
Новый репозиторий под домашние задания и обучения в Вышке на кибербезопасность 

📌 Описание

Скрипт scapy_analyzer.py предназначен для:

перехвата HTTP-трафика локального веб-приложения (например, Gruyere);

сохранения перехваченного трафика в .pcap;

анализа HTTP-запросов и ответов с целью обнаружения XSS-полезных нагрузок.

Скрипт использует библиотеку Scapy и работает на Windows (Npcap).

🚀 Запуск
python scapy_analyzer.py [аргументы]

🧩 Аргументы командной строки
--capture <HOST>

Перехватывает HTTP-трафик для указанного хоста.

Используется для записи сетевого трафика в .pcap

Предназначен для анализа действий пользователя в браузере

Пример:

python scapy_analyzer.py --capture localhost --timeout 30 --output gruyere.pcap

--timeout <SECONDS>

Время перехвата трафика в секундах.

По умолчанию: 30

Пример:

--timeout 60

--output <FILE>

Имя файла для сохранения перехваченного трафика.

Если не указан, используется gruyere.pcap

Пример:

--output traffic.pcap

--analyze <PCAP_FILE>

Анализирует ранее сохранённый .pcap-файл.

Извлекает HTTP-сообщения

Показывает запросы и ответы, содержащие данные HTTP

Пример:

python scapy_analyzer.py --analyze gruyere.pcap

--send <URL>

Отправляет HTTP-запрос на указанный URL вручную (через Scapy).

Устанавливает TCP-соединение вручную

Может использоваться для тестовых запросов

Пример:

python scapy_analyzer.py --send http://localhost:8008/<ID>/search

--request <HTTP_REQUEST>

Позволяет задать кастомный HTTP-запрос.

Используется совместно с --send

Поддерживает ручное указание HTTP-payload

Пример:

--request "GET /test?q=<script>alert(1)</script> HTTP/1.1\r\nHost: localhost\r\n\r\n"

🛠 Требования

Python 3.x

Scapy

Npcap (с включённой опцией Support loopback traffic)

Запуск от имени администратора

📎 Пример сценария использования

Запустить Gruyere:

python gruyere.py


Запустить перехват трафика:

python scapy_analyzer.py --capture localhost --timeout 30


Выполнить действия в браузере (включая XSS-атаки)

Проанализировать трафик:

python scapy_analyzer.py --analyze gruyere.pcap