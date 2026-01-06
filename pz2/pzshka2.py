import hashlib
from datetime import datetime


# ХешMD5
def md5_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


# task 1
class User:
    def __init__(self, username: str, password: str, is_active: bool = True):
        self.username = username
        self.password_hash = md5_hash(password)
        self.is_active = is_active

    def verify_password(self, password: str) -> bool:
        return md5_hash(password) == self.password_hash

    def role_name(self) -> str:
        return "User"

    def __str__(self) -> str:
        return f"{self.username} ({self.role_name()}), active={self.is_active}"


# task 2
class Administrator(User):
    def __init__(self, username: str, password: str, is_active: bool = True, permissions=None):
        super().__init__(username, password, is_active)
        self.permissions = permissions if permissions is not None else ["ALL"]

    def role_name(self) -> str:
        return "Administrator"


class RegularUser(User):
    def __init__(self, username: str, password: str, is_active: bool = True):
        super().__init__(username, password, is_active)
        self.last_login = None

    def set_last_login_now(self):
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def role_name(self) -> str:
        return "RegularUser"


class GuestUser(User):
    def __init__(self, username: str = "guest", password: str = "guest", is_active: bool = True):
        super().__init__(username, password, is_active)
        self.limited_access = True

    def role_name(self) -> str:
        return "GuestUser"


# task 3
class AccessControl:
    def __init__(self):
        self.users: dict[str, User] = {}

    def add_user(self, user: User) -> bool:
        if user.username in self.users:
            return False
        self.users[user.username] = user
        return True

    def authenticate_user(self, username: str, password: str):
        user = self.users.get(username)
        if user is None:
            return None
        if not user.is_active:
            return None
        if not user.verify_password(password):
            return None

        if isinstance(user, RegularUser):
            user.set_last_login_now()

        return user

    # permissions
    def check_permission(self, current_user: User, permission: str) -> bool:
        """
        Приклад контроля доступа:
        - Administrator: ALL или конкретное permission
        - RegularUser: тількі VIEW
        - GuestUser: тількі VIEW
        """
        if isinstance(current_user, Administrator):
            return "ALL" in current_user.permissions or permission in current_user.permissions
        if isinstance(current_user, (RegularUser, GuestUser)):
            return permission == "VIEW"
        return False

    # only admin
    def deactivate_user(self, current_user: User, username_to_deactivate: str) -> bool:
        if not isinstance(current_user, Administrator):
            print("Доступ заборонено: тільки адміністратор може деактивувати користувачів.")
            return False

        user = self.users.get(username_to_deactivate)
        if not user:
            print("Користувача не знайдено.")
            return False

        user.is_active = False
        print(f"Користувач '{username_to_deactivate}' деактивований.")
        return True

    def activate_user(self, current_user: User, username_to_activate: str) -> bool:
        if not isinstance(current_user, Administrator):
            print("Доступ заборонено: тільки адміністратор може активувати користувачів.")
            return False

        user = self.users.get(username_to_activate)
        if not user:
            print("Користувача не знайдено.")
            return False

        user.is_active = True
        print(f"Користувач '{username_to_activate}' активований.")
        return True

    def change_password(self, current_user: User, old_password: str, new_password: str) -> bool:
        if not current_user.verify_password(old_password):
            print("Старий пароль невірний.")
            return False
        current_user.password_hash = md5_hash(new_password)
        print("Пароль змінено успішно.")
        return True

    def list_users(self):
        return list(self.users.values())


# меню
def print_menu():
    print("\n=== Меню ===")
    print("1) Додати RegularUser")
    print("2) Додати GuestUser")
    print("3) Додати Administrator (тільки якщо ви admin)")
    print("4) Увійти (login)")
    print("5) Показати користувачів (VIEW)")
    print("6) Деактивувати користувача (ADMIN)")
    print("7) Активувати користувача (ADMIN)")
    print("8) Змінити пароль (для поточного користувача)")
    print("9) Вийти з акаунту (logout)")
    print("0) Вихід")


def main():
    ac = AccessControl()

    # test
    ac.add_user(Administrator("admin", "admin123", permissions=["ALL"]))
    ac.add_user(RegularUser("user", "user123"))
    ac.add_user(GuestUser("guest", "guest"))

    current_user = None

    while True:
        print_menu()
        choice = input("Виберіть дію: ").strip()

        if choice == "0":
            print("Вихід...")
            break

        elif choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            ok = ac.add_user(RegularUser(username, password))
            print("Додано" if ok else "Такий username вже існує")

        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password (Enter = guest): ").strip() or "guest"
            ok = ac.add_user(GuestUser(username, password))
            print("Додано" if ok else "Такий username вже існує")

        elif choice == "3":
            if current_user is None:
                print("Спочатку увійдіть як адміністратор.")
                continue
            if not isinstance(current_user, Administrator):
                print("Доступ заборонено: тільки адміністратор може додавати адмінів.")
                continue

            username = input("Admin username: ").strip()
            password = input("Admin password: ").strip()
            perms_raw = input("Permissions через кому (Enter = ALL): ").strip()
            perms = ["ALL"] if perms_raw == "" else [p.strip() for p in perms_raw.split(",")]

            ok = ac.add_user(Administrator(username, password, permissions=perms))
            print("Додано" if ok else "Такий username вже існує")

        elif choice == "4":
            username = input("Login: ").strip()
            password = input("Password: ").strip()
            user = ac.authenticate_user(username, password)
            if user is None:
                print("Невірний логін/пароль або акаунт неактивний.")
            else:
                current_user = user
                print(f"Успішний вхід: {current_user}")

                if isinstance(current_user, RegularUser):
                    print("Last login:", current_user.last_login)
                if isinstance(current_user, Administrator):
                    print("Permissions:", current_user.permissions)

        elif choice == "5":
            if current_user is None:
                print("Спочатку увійдіть у систему.")
                continue
            if not ac.check_permission(current_user, "VIEW"):
                print("Немає прав для перегляду.")
                continue

            users = ac.list_users()
            for u in users:
                extra = ""
                if isinstance(u, Administrator):
                    extra = f", permissions={u.permissions}"
                if isinstance(u, RegularUser):
                    extra = f", last_login={u.last_login}"
                print("-", str(u) + extra)

        elif choice == "6":
            if current_user is None:
                print("Спочатку увійдіть у систему.")
                continue
            username = input("Кого деактивувати (username): ").strip()
            ac.deactivate_user(current_user, username)

        elif choice == "7":
            if current_user is None:
                print("Спочатку увійдіть у систему.")
                continue
            username = input("Кого активувати (username): ").strip()
            ac.activate_user(current_user, username)

        elif choice == "8":
            if current_user is None:
                print("Спочатку увійдіть у систему.")
                continue
            old_pwd = input("Старий пароль: ").strip()
            new_pwd = input("Новий пароль: ").strip()
            ac.change_password(current_user, old_pwd, new_pwd)

        elif choice == "9":
            current_user = None
            print("Ви вийшли з акаунту.")

        else:
            print("Невірна команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
