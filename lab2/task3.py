def filter_ips(input_file_path, output_file_path, allowed_ips):
    ip_counter = {}

    try:
        with open(input_file_path, "r", encoding="utf-8") as infile:
            for line in infile:
                ip = line.split()[0]

                if ip in allowed_ips:
                    ip_counter[ip] = ip_counter.get(ip, 0) + 1

        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for ip, count in ip_counter.items():
                outfile.write(f"{ip} - {count}\n")

        print("Результат записано у файл:", output_file_path)

    except FileNotFoundError:
        print("Вхідний файл не знайдено")
    except IOError:
        print("Помилка роботи з файлами")


# ===== ВВІД allowed_ips З КЛАВІАТУРИ =====
allowed_ips = []

print("Введіть дозволені IP-адреси.")
print("Для завершення введіть: exit")

while True:
    ip = input("IP: ")
    if ip == "exit":
        break
    allowed_ips.append(ip)

# Виклик функції
filter_ips("apache_logs.txt", "filtered_ips.txt", allowed_ips)
