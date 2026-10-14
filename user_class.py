# Structure:
# ├── Class: User
# ├── __init__ with: username, email, password, bio, user_id, is_active, date_created
# ├── save(cursor, conn) → INSERT with duplicate check
# └── update(cursor, conn) → UPDATE bio/email

# Default values:
# ├── bio = None
# ├── user_id = None
# ├── is_active = True
# └── date_created = None
from datetime import datetime


class User:

    def __init__(
        self,
        name,
        email,
        password,
        updated_at=None,
        user_id=None,
        bio=None,
        date_created=None,
        is_active=True,
        posts_count=None,
        user_likes=None,
    ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.bio = bio if bio else ""
        self.date_created = date_created
        self.updated_at = (
            updated_at if updated_at else datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        self.is_active = is_active
        self.posts_count = posts_count if posts_count else None
        self.user_likes = user_likes if user_likes else None

    def save_user(self, cursor, conn):
        if not self.user_id:
            try:
                cursor.execute(
                    "INSERT INTO users(username,email,password,bio,updated_at)VALUES(?,?,?,?,?)",
                    (self.name, self.email, self.password, self.bio, self.updated_at),
                )
                conn.commit()
                return True
            except Exception as e:
                print(f"error saving user: {e}")
                return False
        try:

            cursor.execute(
                "UPDATE users SET username =?,email = ?,password =?, bio = ?,updated_at = ? WHERE id =?",
                (
                    self.name,
                    self.email,
                    self.password,
                    self.bio,
                    self.updated_at,
                    self.user_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error updating user:{e}")
            return False
