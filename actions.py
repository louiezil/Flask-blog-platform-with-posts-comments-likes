from werkzeug.security import generate_password_hash, check_password_hash


def generate_password(password):
    hw_password = generate_password_hash(password)
    return hw_password


def check_password(hw_password, password):
    passed = check_password_hash(hw_password, password)
    if passed:
        return True
    return False
