from post_class import Post


def get_all_posts(cursor):
    try:
        cursor.execute("""
            SELECT posts.*,
                        (SELECT username FROM users WHERE users.id = posts.author_id) AS author_name,
                        categories.name as category_name,
                        COUNT(DISTINCT likes.id) as likes_count,
                        COUNT(DISTINCT comments.id) as comments_count
            FROM posts
            LEFT JOIN categories ON posts.category_id = categories.id
            LEFT JOIN likes ON likes.post_id = posts.id
            LEFT JOIN comments ON comments.post_id = posts.id
            GROUP BY posts.id
            """)
        data = cursor.fetchall()
        posts = []
        if not data:
            return posts

        for (
            post_id,
            author_id,
            title,
            content,
            image,
            category_id,
            date_created,
            updated_at,
            author_name,
            category_name,
            likes_count,
            comments_count,
        ) in data:
            post = Post(
                post_id=post_id,
                author_name=author_name,
                author_id=author_id,
                title=title,
                content=content,
                image=image,
                category_id=category_id,
                date_created=date_created,
                category_name=category_name,
                updated_at=updated_at,
                likes_count=likes_count,
                comments_count=comments_count,
            )
            posts.append(post)
        return posts
    except Exception as e:
        print(f"error fetching posts : {e}")
        return []


# def get_post(cursor, post_id):
#     # Same JOIN + WHERE id = ?
#     # Return one Post or None


def get_single_post(cursor, post_id):
    try:
        cursor.execute(
            """
    SELECT posts.* ,
                    users.username AS author_name,
                    categories.name AS category_name,
                    COUNT(DISTINCT likes.id) AS likes_count,
                    COUNT(DISTINCT comments.id) AS comments_count
    FROM posts
    JOIN users ON posts.author_id = users.id
    LEFT JOIN likes ON likes.post_id = posts.id
    LEFT JOIN categories ON posts.category_id = categories.id
    LEFT JOIN comments ON comments.post_id = posts.id
    WHERE posts.id =?
    """,
            (post_id,),
        )
        data = cursor.fetchone()
        if not data:
            return None
        (
            post_id,
            author_id,
            title,
            content,
            image,
            category_id,
            date_created,
            updated_at,
            author_name,
            category_name,
            likes_count,
            comments_count,
        ) = data
        post = Post(
            post_id=post_id,
            author_name=author_name,
            author_id=author_id,
            title=title,
            content=content,
            image=image,
            category_id=category_id,
            date_created=date_created,
            category_name=category_name,
            updated_at=updated_at,
            likes_count=likes_count,
            comments_count=comments_count,
        )
        return post
    except Exception as e:
        print(f"error fetching post:{e}")
        return None


def get_user_posts(cursor, user_id):
    try:
        cursor.execute(
            """
    SELECT posts.*,
                    users.username AS author_name,
                    categories.name AS category_name,
                    COUNT(DISTINCT likes.id) AS likes_count,
                    (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) AS comments_count
    FROM posts
    JOIN users ON posts.author_id = users.id
    LEFT JOIN categories ON posts.category_id = categories.id
    LEFT JOIN likes ON likes.post_id = posts.id
    LEFT JOIN comments ON comments.post_id = posts.id
    WHERE author_id = ?
    GROUP BY posts.id
    ORDER BY posts.date_created DESC
    """,
            (user_id,),
        )
        user_posts = []
        data = cursor.fetchall()
        if not data:
            return user_posts

        for (
            post_id,
            author_id,
            title,
            content,
            image,
            category_id,
            date_created,
            updated_at,
            author_name,
            category_name,
            likes_count,
            comments_count,
        ) in data:
            post = Post(
                post_id=post_id,
                author_name=author_name,
                author_id=author_id,
                title=title,
                content=content,
                image=image,
                category_id=category_id,
                date_created=date_created,
                category_name=category_name,
                updated_at=updated_at,
                likes_count=likes_count,
                comments_count=comments_count,
            )

            user_posts.append(post)
        return user_posts
    except Exception as e:
        print(f"error fetching user_posts :{e}")
        return []


def verify_delete_post(cursor, post_id):
    try:
        cursor.execute("SELECT author_id FROM posts WHERE id =?", (post_id,))
        data = cursor.fetchone()[0]
        if data:
            return data
        return None

    except Exception as e:
        print(f"error verifying deleting post :{e}")
        return None


def delete_post(cursor, conn, post_id):
    try:
        cursor.execute("DELETE FROM posts WHERE id =?", (post_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"error deleting post :{e}")
        return False


def register_post(conn, cursor, user_id, title, content, image, category_id):
    post = Post(
        content=content,
        title=title,
        author_id=user_id,
        category_id=category_id,
        image=image,
    )
    post.save_post(conn, cursor)
    return True


"join posts with likes only posts.id = likes.id,...now i want all the posts with likes.user_id  which is equal to the user_id in parameter"


def user_related_posts_liked(
    cursor,
    user_id,
):
    try:
        cursor.execute(
            """
    SELECT posts.*,
                    categories.name AS category_name,
                    users.username AS author_name,
                    COUNT(DISTINCT comments.id) AS comments_count
    FROM posts
    LEFT JOIN categories ON posts.category_id = categories.id
    JOIN users ON users.id = posts.author_id
    LEFT JOIN likes ON likes.post_id = posts.id
    LEFT JOIN comments ON comments.post_id = posts.id
    WHERE likes.user_id =?
    GROUP BY posts.id
    """,
            (user_id,),
        )

        data = cursor.fetchall()
        related_liked_posts = []
        if not data:
            return related_liked_posts
        for (
            post_id,
            author_id,
            title,
            content,
            image,
            category_id,
            date_created,
            updated_at,
            category_name,
            author_name,
            comments_count,
        ) in data:
            cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id =? ", (post_id,))
            likes = cursor.fetchone()
            post = Post(
                title=title,
                content=content,
                author_id=author_id,
                category_id=category_id,
                image=image,
                post_id=post_id,
                date_created=date_created,
                updated_at=updated_at,
                author_name=author_name,
                category_name=category_name,
                likes_count=likes[0],
                comments_count=comments_count,
            )
            related_liked_posts.append(post)
        return related_liked_posts
    except Exception as e:
        print(f"error with related posts : {e}")
        return []
