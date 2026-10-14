from actions import check_password, generate_password
from user_class import User

def Login(cursor, email, password):

    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        exists = cursor.fetchone()
        if not exists:
            return None
        (
            user_id,
            name,
            email,
            hw_password,
            bio,
            date_created,
            updated_at,
            is_active,
        ) = exists

        password_checked = check_password(hw_password, password)
        if password_checked:
            user = User(
                name,
                email,
                hw_password,
                updated_at,
                user_id,
                bio,
                date_created,
                is_active,
            )
            return user
        return None
    except Exception as e:
        print(f"error with Login:{e}")
        return None


def register_user(
    conn,
    cursor,
    name,
    email,
    password,
):

    try:
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ? OR email = ?",
            (
                name,
                email,
            ),
        )
        exists = cursor.fetchone()
        if exists:
            return False
        hw_password = generate_password(password)
        new_user = User(
            name=name,
            email=email,
            password=hw_password,
            
        )
        if new_user.save_user(cursor, conn):
            return True
        return False
    except Exception as e:
        print(f"error saving user: {e}")
        return False
