# Structure:
# 1. Import sqlite3
# 2. conn_cursor() function (copy pattern from School)
# 3. create_tables() with 5 tables
# 4. close_connection() function
# 5. Test block: python database.py
# from auth import register_user, Login
# from database import conn_cursor, create_tables
# from post_actions import register_post,get_all_posts,get_single_post,get_user_posts
# from comments_action import comment_register, get_post_comments

# name = "louis"
# password = "password"
# email = f"{name}@gmail.com"
# bio = ""


# def register(conn, cursor):

#     registered = register_user(conn, cursor, name, email, password, bio)
#     if registered:
#         print("user registered success")
#         return True
#     print("registration failed")
#     return False


# create post


# if __name__ == "__main__":
#     conn, cursor = conn_cursor()
#     create_tables(conn, cursor)
#     "creating comment"
    
    
# 'get post and view the likes and comments'



#     # content = "y dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at L"
#     # post_id = 1
#     # user_id = 1
#     # comment_register(cursor, conn, content, post_id, user_id)
#     # comments = get_post_comments(cursor, post_id)

#     # for each in comments:
#     #     print(each.user_name)
#     # register(conn, cursor)
#     # user = Login(cursor, email, password)
#     # if user:
#     #     print(user.name)
#     #     print(user.email)
#     #     print(user.date_created)
#     #     print(user.bio)

#     # "register a post"

# # user_id = 1
# # title = "Beginner Guide for python Program"
# # content = " is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride Printing Library in London, took a 1914 Cicero translation and scrambled it to make dummy text for Letraset's Body Type sheets. It has survived not only many decades, but also the leap into "

# # image = ""
# # category_id = 1

# # let seed a category

# data = {
#     "Technology": {
#         "title": "Technology",
#         "description": "ndustry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride",
#     },
#     "social": {
#         "title": "social",
#         "description": "ndustry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride",
#     },
#     "Anime": {
#         "title": "Anime",
#         "description": "ndustry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride",
#     },
#     "Python": {
#         "title": "Python",
#         "description": "ndustry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride",
#     },
# }


# def create_cat():
#     for each, info in data.items():
#         cursor.execute(
#             "INSERT INTO categories (name,description)VALUES(?,?)",
#             (
#                 each,
#                 info["description"],
#             ),
#         )
#         conn.commit()
#     return True


# if create_cat():
#     print('success')
# else:
#     print('failed')

# if register_post(conn,cursor,user_id,title,content,image,category_id):
#     print("post registered success")
# else:
#     print("failed to post")