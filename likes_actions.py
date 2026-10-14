def toggle_like(cursor, conn, post_id, user_id):
    try:
        cursor.execute(
            "SELECT id FROM likes WHERE post_id = ? AND user_id = ?",
            (
                post_id,
                user_id,
            ),
        )
        exist = cursor.fetchone()
        if exist:
            cursor.execute(
                "DELETE FROM likes WHERE post_id = ? AND user_id=?",
                (
                    post_id,
                    user_id,
                ),
            )
            conn.commit()
            return False
        else:
            cursor.execute(
                "INSERT INTO likes (post_id,user_id)VALUES(?,?)",
                (
                    post_id,
                    user_id,
                ),
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"error with likes:{e}")
        return None


def count_post_likes(cursor, post_id):
    try:
        cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id =?", (post_id,))
        likes = cursor.fetchone()
        if likes:
            return likes[0]
        return 0
    except Exception as e:
        print(f"error with post likes:{e}")
        return 0


def user_liked(cursor, user_id, post_id):
    try:
        cursor.execute(
            "SELECT 1 FROM likes WHERE user_id = ? AND post_id=?",
            (
                user_id,
                post_id,
            ),
        )
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"error with liked/un_liked:{e}")
        return None
