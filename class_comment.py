




class Comment:
    def __init__(
        self,
        content,
        user_id,
        post_id,
        date_created=None,
        user_name=None,
        comment_id=None,
    ):
        self.comment_id = comment_id if comment_id else None
        self.content = content
        self.date_created = date_created if not None else None
        self.user_id = user_id
        self.user_name = None if not user_name else user_name
        self.post_id = post_id

    def save_comment(self, cursor, conn):
        try:
            if not self.comment_id:
                cursor.execute(
                    "INSERT INTO comments (content,post_id,user_id)VALUES(?,?,?)",
                    (
                        self.content,
                        self.post_id,
                        self.user_id,
                    ),
                )
                conn.commit()
                return True
            cursor.execute(
                "UPDATE comments SET content = ? WHERE id= ?",
                (
                    self.content,
                    self.comment_id,
                ),
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"error saving Comment: {e}")
            return False


#     NEW FILES:
# ├── comment_class.py      ← Comment class
# └── comment_actions.py    ← Get, delete, count functions

# PATTERN:
# ├── Class: Comment
# │   ├── __init__
# │   ├── save()    → INSERT new comment
# │   └── update()  → UPDATE own comment
# │