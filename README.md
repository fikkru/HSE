# Cyber Threat Analyzer

Скрипт выполняет простой анализ угроз.

Используемые источники данных:
1. Логи Suricata (JSON)
2. API Vulners

Функциональность:
- загрузка логов
- поиск подозрительных IP
- запрос к API Vulners
- имитация блокировки IP
- создание отчета CSV
- построение графика активности IP

Файлы:
- analyzer.py — основной скрипт
- suricata_logs.json — пример логов
- report.csv — отчет
- threat_graph.png — график

Используемые библиотеки:
- requests
- pandas
- matplotlib
- json