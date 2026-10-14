from user_class import User


def get_user(cursor, user_id):

    cursor.execute(
        """
                   SELECT users.* ,
                                COUNT(DISTINCT posts.id) AS posts_count
                   FROM users
                   LEFT JOIN posts ON posts.author_id = users.id
                   WHERE users.id =?
                   """,
        (user_id,),
    )
    data = cursor.fetchone()
    if not data:
        return None
    (
        user_id,
        username,
        email,
        password,
        bio,
        date_created,
        updated_at,
        is_active,
        post_count,
    ) = data

    "select likes join posts only posts thats have posts.id = likes.post_id  and count where the posts.author_id = user_id "

    cursor.execute(
        """
    SELECT  COUNT(likes.id)
    FROM likes
    JOIN posts ON posts.id = likes.post_id
    WHERE posts.author_id =?
    
    """,
        (user_id,),
    )
    user_likes = cursor.fetchone()[0]

    # total_likes = []
    # cursor.execute("SELECT id FROM posts WHERE author_id =?", (user_id,))
    # all_posts_id = cursor.fetchall()
    # if all_posts_id:
    #     for each_post_id in all_posts_id:
    #         post_id = each_post_id[0]
    #         cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id = ?", (post_id,))
    #         likes = cursor.fetchone()[0]
    #         total_likes.append(likes)

    user = User(
        name=username,
        email=email,
        password=password,
        updated_at=updated_at,
        user_id=user_id,
        is_active=is_active,
        date_created=date_created,
        posts_count=post_count,
        user_likes=user_likes,
        bio=bio,
    )
    return user
