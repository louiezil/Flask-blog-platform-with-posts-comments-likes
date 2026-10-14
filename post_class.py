# Class: Post

# __init__(self, title, content, author_id, image=None, category_id=None,
#          post_id=None, date_created=None, updated_at=None)
# ├── title
# ├── content
# ├── author_id
# ├── image
# ├── category_id
# ├── post_id
# ├── date_created
# └── updated_at


from datetime import datetime


class Post:

    def __init__(
        self,
        title,
        content,
        author_id,
        category_id,
        image=None,
        post_id=None,
        date_created=None,
        updated_at=None,
        author_name=None,
        category_name=None,
        likes_count=None,
        comments_count=None,
    ):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.category_id = category_id
        self.image = "" if not image else image
        self.post_id = post_id
        self.date_created = date_created
        self.updated_at = (
            datetime.now().strftime("%d/%m/%Y, %H:%M") if not updated_at else updated_at
        )
        self.author_name = author_name
        self.category_name = category_name
        self.likes_count = likes_count if not None else None
        self.comments_count = comments_count if not None else None
        # Methods:

    # ├── save(cursor, conn)     → INSERT new post
    # └── update(cursor, conn)   → UPDATE title, content, category_id

    def save_post(self, conn, cursor):
        try:
            cursor.execute(
                "INSERT INTO posts(title,content,image,author_id,category_id)VALUES(?,?,?,?,?)",
                (
                    self.title,
                    self.content,
                    self.image,
                    self.author_id,
                    self.category_id,
                ),
            )
            conn.commit()
            self.post_id = cursor.lastrowid
            return True
        except Exception as e:
            print(f"error saving post :{e}")
            return False

    def update_post(self, conn, cursor):
        try:
            cursor.execute(
                " UPDATE posts SET title = ?, content = ?,image =?,category_id = ? WHERE id = ?",
                (
                    self.title,
                    self.content,
                    self.image,
                    self.category_id,
                    self.post_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error saving post :{e}")
            return False
