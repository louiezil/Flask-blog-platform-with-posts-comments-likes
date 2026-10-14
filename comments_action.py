from class_comment import Comment


def get_post_comments(cursor, post_id):
    # need the comment plus username
    try:
        cursor.execute(
            """
    SELECT comments.*,
                    users.username as author_name
    FROM comments
    JOIN users ON comments.user_id = users.id
    WHERE comments.post_id = ?
    ORDER BY comments.date_created DESC

    """,
            (post_id,),
        )
        results = cursor.fetchall()
        comments = []
        if not results:
            return comments

        for (
            comment_id,
            post_id,
            user_id,
            content,
            date_created,
            author_name,
        ) in results:
            comment = Comment(
                content=content,
                user_id=user_id,
                post_id=post_id,
                date_created=date_created,
                user_name=author_name,
                comment_id=comment_id,
            )
            comments.append(comment)
        return comments
    except Exception as e:
        print(f"error getting post_comments:{e}")
        return []


def comment_register(cursor, conn, content, post_id, user_id):
    comment = Comment(content, user_id, post_id)
    if comment.save_comment(cursor, conn):
        return True
    return False


def total_post_comments(cursor, post_id):
    cursor.execute("SELECT COUNT(*) FROM comments WHERE post_id =?", (post_id,))
    data = cursor.fetchone()[0]
    return data


def delete_comment(cursor, conn, comment_id):
    try:
        cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"error deleting comment:{e}")
        return False


# total comments of a user

'every comment has a post_id'
'every post_id has an author_id'


