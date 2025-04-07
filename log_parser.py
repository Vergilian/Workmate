import re
from collections import defaultdict
from typing import Dict

LogData = Dict[str, Dict[str, int]]

# Обновленное регулярное выражение для логов
LOG_PATTERN = re.compile(
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) (?P<handler>django\.[a-z.]+): (?P<message>.+)")


def parse_log_file(filepath: str) -> dict:
    print(f"📄 Парсим файл: {filepath}")
    result = defaultdict(lambda: defaultdict(int))

    with open(filepath, encoding='utf-8') as f:
        for line in f:
            match = LOG_PATTERN.search(line)
            if match:
                level = match.group("level")
                handler = match.group("handler")
                message = match.group("message")

                # Если это запрос (метод GET/POST и URL в сообщении)
                if "GET" in message or "POST" in message:
                    url = message.split(" ")[1]  # Извлекаем URL после метода (например, /admin/dashboard/)
                    result[url][level] += 1
                else:
                    # Если это ошибка или другое сообщение, записываем по обработчику
                    result[handler][level] += 1

                result["__total__"]["requests"] += 1

    # Убедимся, что для каждой ручки и каждого уровня логирования есть ключи, даже если они равны 0
    for url in result:
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            result[url].setdefault(level, 0)

    return result


# Для примера:
if __name__ == "__main__":
    log_files = ["logs/app1.log", "logs/app2.log", "logs/app3.log"]  # Пример путей
    all_results = defaultdict(lambda: defaultdict(int))

    for log_file in log_files:
        data = parse_log_file(log_file)
        # Мержим данные из разных файлов
        for url, levels in data.items():
            for level, count in levels.items():
                all_results[url][level] += count

    # Сортировка URL по алфавиту
    sorted_urls = sorted(all_results.keys())

    # Вывод отчета
    total_requests = all_results['__total__']['requests']
    print(f"Total requests: {total_requests }✅")
    print("\nHANDLER               DEBUG   INFO    WARNING  ERROR   CRITICAL")

    for url in sorted_urls:
        # Вывод данных по каждому URL
        line = f"{url:<20}"  # Сначала выводим URL, выравнивая его по левому краю
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            line += f"{all_results[url][level]:<8}"  # Для каждого уровня логирования добавляем количество
        print(line)

    # Сумма по каждому уровню
    print(" " * 20, end="")
    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        total_level = sum(all_results[url][level] for url in sorted_urls)
        print(f"{total_level:<8}", end="")
    print()
