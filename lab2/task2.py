import hashlib


def generate_file_hashes(*file_paths):
    hashes = {}

    for path in file_paths:
        try:
            with open(path, "rb") as file:
                content = file.read()
                file_hash = hashlib.sha256(content).hexdigest()
                hashes[path] = file_hash

        except FileNotFoundError:
            print(f"Файл не знайдено: {path}")
        except IOError:
            print(f"Помилка читання файлу: {path}")

    return hashes


# приклад виклику
result = generate_file_hashes("file1.txt", "file2.txt")
print("Хеші файлів:", result)
