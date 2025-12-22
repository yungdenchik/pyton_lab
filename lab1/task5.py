import hashlib

users = {}


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def add_user(login, password, full_name):
    users[login] = {
        "password": hash_password(password),
        "full_name": full_name
    }


login = input("Створіть логін: ")
password = input("Створіть пароль: ")
full_name = input("Введіть ПІБ: ")

add_user(login, password, full_name)

print("=== Вхід в систему ===")
login_input = input("Логін: ")
password_input = input("Пароль: ")

if login_input in users and hash_password(password_input) == users[login_input]["password"]:
    print("Вхід успішний. Вітаю,", users[login_input]["full_name"])
else:
    print("Невірний логін або пароль")
