import hashlib
from datetime import datetime


def md5_hash(text: str) -> str:
    """Хешування MD5 (навчальний приклад)."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


class User:
    def __init__(self, username: str, password: str, is_active: bool = True):
        self.username = username
        self.password_hash = md5_hash(password)
        self.is_active = is_active

    def verify_password(self, password: str) -> bool:
        """Перевіряє пароль шляхом порівняння хешів."""
        return md5_hash(password) == self.password_hash

    def role_name(self) -> str:
        return "User"

    def __str__(self) -> str:
        return f"{self.username} ({self.role_name()}), active={self.is_active}"


class Administrator(User):
    def __init__(self, username: str, password: str, is_active: bool = True, permissions=None):
        super().__init__(username, password, is_active)
        self.permissions = permissions if permissions is not None else ["ALL"]

    def role_name(self) -> str:
        return "Administrator"


class RegularUser(User):
    def __init__(self, username: str, password: str, is_active: bool = True):
        super().__init__(username, password, is_active)
        self.last_login = None  # str або None

    def set_last_login_now(self) -> None:
        # Строка до секунд, як у твоєму варіанті
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def role_name(self) -> str:
        return "RegularUser"


class GuestUser(User):
    def __init__(self, username: str = "guest", password: str = "guest", is_active: bool = True):
        super().__init__(username, password, is_active)
        self.limited_access = True

    def role_name(self) -> str:
        return "GuestUser"


class AccessControl:
    def __init__(self):
        self.users: dict[str, User] = {}

    def add_user(self, user: User) -> bool:
        """Додає користувача. False якщо username зайнятий."""
        if user.username in self.users:
            return False
        self.users[user.username] = user
        return True

    def authenticate_user(self, username: str, password: str):
        """Повертає користувача при успіху або None."""
        user = self.users.get(username)
        if user is None:
            return None
        if not user.is_active:
            return None
        if not user.verify_password(password):
            return None

        # бонус: для RegularUser оновлюємо last_login
        if isinstance(user, RegularUser):
            user.set_last_login_now()

        return user

    def change_password(self, user: User, old_password: str, new_password: str) -> bool:
        """Змінює пароль (користувач сам собі)."""
        if not user.verify_password(old_password):
            return False
        user.password_hash = md5_hash(new_password)
        return True


def main():  # pragma: no cover
    # Невелика демонстрація (не для тестів)
    ac = AccessControl()
    ac.add_user(Administrator("admin", "admin123"))
    print("Demo:", ac.authenticate_user("admin", "admin123"))


if __name__ == "__main__":  # pragma: no cover
    main()
