def analyze_log_file(log_file_path):
    status_codes = {}

    try:
        with open(log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.split()

                for part in parts:
                    if part.isdigit():
                        code = int(part)

                        # фільтрація тільки реальних HTTP-кодів
                        #if 100 <= code <= 599:
                        status_codes[str(code)] = status_codes.get(str(code), 0) + 1

        return status_codes

    except FileNotFoundError:
        print("Помилка: файл не знайдено")
    except IOError:
        print("Помилка читання файлу")


result = analyze_log_file("apache_logs.txt")
print("HTTP коди:", result)
