import sqlite3
import hashlib

DB_NAME = "users.db"


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


# task 1
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            login TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# task 2
def add_user(login: str, password: str, full_name: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (login, password, full_name) VALUES (?, ?, ?)",
            (login, hash_password(password), full_name)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # login вже існує (PRIMARY KEY)
        return False
    finally:
        conn.close()


def update_password(login: str, new_password: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET password = ? WHERE login = ?",
        (hash_password(new_password), login)
    )
    conn.commit()

    updated = cur.rowcount > 0
    conn.close()
    return updated


def authenticate_user(login: str, password: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT password FROM users WHERE login = ?", (login,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return False

    stored_hash = row[0]
    return stored_hash == hash_password(password)


def list_users():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT login, full_name FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows


def print_menu():
    print("\n=== Users DB Menu ===")
    print("1) Додати нового користувача")
    print("2) Оновити пароль користувача")
    print("3) Перевірити автентифікацію (login + password)")
    print("4) Показати список користувачів")
    print("0) Вихід")


def main():
    init_db()

    while True:
        print_menu()
        choice = input("Виберіть дію: ").strip()

        if choice == "1":
            login = input("Login: ").strip()
            password = input("Password: ").strip()
            full_name = input("Full name (ПІБ): ").strip()

            ok = add_user(login, password, full_name)
            if ok:
                print("Користувача додано")
            else:
                print("Такий login вже існує")

        elif choice == "2":
            login = input("Login: ").strip()
            new_password = input("New password: ").strip()

            ok = update_password(login, new_password)
            if ok:
                print("Пароль оновлено")
            else:
                print("Користувача з таким login не знайдено")

        elif choice == "3":
            login = input("Login: ").strip()
            password = input("Password: ").strip()

            ok = authenticate_user(login, password)
            print("Вхід успішний" if ok else "Невірний login або пароль")

        elif choice == "4":
            users = list_users()
            if not users:
                print("(поки немає користувачів)")
            else:
                for u_login, u_name in users:
                    print(f"- {u_login}: {u_name}")

        elif choice == "0":
            print("Вихід...")
            break

        else:
            print("Невірна команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
