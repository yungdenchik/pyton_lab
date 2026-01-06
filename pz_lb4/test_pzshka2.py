import time
from pzshka2 import User, RegularUser, Administrator, GuestUser, AccessControl


# =========================
# User.verify_password (2 тести)
# =========================
def test_verify_password_correct():
    u = User("u1", "pass")
    assert u.verify_password("pass") is True


def test_verify_password_wrong():
    u = User("u1", "pass")
    assert u.verify_password("wrong") is False


# =========================
# User.__str__ + role_name
# =========================
def test_user_str_and_role():
    u = User("john", "123")
    text = str(u)
    assert "john" in text
    assert "User" in text


# =========================
# Administrator
# =========================
def test_admin_role_name_and_permissions():
    admin = Administrator("admin", "pass")
    assert admin.role_name() == "Administrator"
    assert "ALL" in admin.permissions


# =========================
# GuestUser
# =========================
def test_guest_user_defaults():
    guest = GuestUser()
    assert guest.username == "guest"
    assert guest.limited_access is True


def test_guest_user_role_name():
    guest = GuestUser()
    assert guest.role_name() == "GuestUser"


# =========================
# AccessControl.add_user (2 тести)
# =========================
def test_add_user_success():
    ac = AccessControl()
    assert ac.add_user(User("u1", "pass")) is True
    assert "u1" in ac.users


def test_add_user_duplicate():
    ac = AccessControl()
    assert ac.add_user(User("u1", "pass")) is True
    assert ac.add_user(User("u1", "pass2")) is False
    assert len(ac.users) == 1


# =========================
# AccessControl.authenticate_user
# =========================
def test_authenticate_success_returns_user():
    ac = AccessControl()
    ac.add_user(User("u1", "pass"))
    logged = ac.authenticate_user("u1", "pass")
    assert logged is not None
    assert logged.username == "u1"


def test_authenticate_wrong_password_returns_none():
    ac = AccessControl()
    ac.add_user(User("u1", "pass"))
    assert ac.authenticate_user("u1", "bad") is None


def test_authenticate_inactive_returns_none():
    ac = AccessControl()
    ac.add_user(User("u1", "pass", is_active=False))
    assert ac.authenticate_user("u1", "pass") is None


# =========================
# RegularUser.set_last_login_now
# =========================
def test_regular_user_sets_last_login():
    u = RegularUser("u1", "pass")
    assert u.last_login is None
    u.set_last_login_now()
    assert u.last_login is not None


def test_regular_user_last_login_changes():
    u = RegularUser("u1", "pass")
    u.set_last_login_now()
    first = u.last_login
    time.sleep(1)  # чтобы точно сменилась секунда
    u.set_last_login_now()
    second = u.last_login
    assert first != second


# =========================
# authenticate updates last_login
# =========================
def test_authenticate_updates_last_login_for_regular_user():
    ac = AccessControl()
    user = RegularUser("u1", "pass")
    ac.add_user(user)

    assert user.last_login is None
    ac.authenticate_user("u1", "pass")
    assert user.last_login is not None


# =========================
# AccessControl.change_password
# =========================
def test_change_password_success():
    ac = AccessControl()
    user = User("u1", "old")
    ac.add_user(user)

    assert ac.change_password(user, "old", "new") is True
    assert user.verify_password("new") is True


def test_change_password_wrong_old_password():
    ac = AccessControl()
    user = User("u1", "old")
    ac.add_user(user)

    assert ac.change_password(user, "WRONG", "new") is False
    assert user.verify_password("old") is True
