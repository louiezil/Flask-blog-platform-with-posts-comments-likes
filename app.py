from flask import Flask, session, redirect, url_for, render_template, request
from functools import wraps
from database import conn_cursor, create_tables
from auth import register_user, Login
from post_actions import (
    get_all_posts,
    get_single_post,
    get_user_posts,
    user_related_posts_liked,
    delete_post,
    verify_delete_post,
)
from post_class import Post
from comments_action import get_post_comments
from likes_actions import user_liked, toggle_like
from comments_action import comment_register, delete_comment
from user_actions import get_user
import os
# Imports:
# ├── Flask (app, render_template, request, redirect, url_for, session)
# ├── functools.wraps (for decorator)
# ├── database (conn_cursor, create_tables)
# ├── auth (register_user, Login)


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY',"this_is_the_secret_key")
conn, cursor = conn_cursor()
create_tables(conn, cursor)

data = {
    "Technology": {
        "title": "Technology",
        "description": "ndustry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride",
    },
    "social": {
        "title": "social",
        "description": "ndustry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride",
    },
    "Anime": {
        "title": "Anime",
        "description": "ndustry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride",
    },
    "Python": {
        "title": "Python",
        "description": "ndustry's standard dummy text ever since 1966, when designers at Letraset and James Mosley, the librarian at St Bride",
    },
}


def create_cat():
    for each, info in data.items():
        cursor.execute(
            "INSERT INTO categories (name,description)VALUES(?,?)",
            (
                each,
                info["description"],
            ),
        )
        conn.commit()
    return True



# Setup:
# ├── app = Flask(__name__)
# ├── app.secret_key = "your-secret-key"
# ├── conn, cursor = conn_cursor()
# ├── create_tables(conn, cursor)


def Login_required(f):
    @wraps(f)
    def login_decorator(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return login_decorator


@app.route("/")
@Login_required
def home():
    posts = get_all_posts(cursor)
    all_posts = []

    for each in posts:

        post_id = each.post_id
        user_liked_post = user_liked(
            cursor=cursor,
            user_id=session.get("user_id"),
            post_id=post_id,
        )
        post_liked = each, user_liked_post
        all_posts.append(post_liked)
    return render_template(
        "home.html",
        all_posts=all_posts,
    )


@app.route("/register", methods=["POST", "GET"])
def register():
    if session.get("username"):
        return redirect(url_for("home"))

    error = None
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if not username:
            error = "username cant be empty"
        elif len(username) < 4:
            error = "min length Required >4"
        elif "@" not in email:
            error = "Email requires an @ sign"
        elif len(email) < 9:
            error = "MIn Email length Required >9"
        elif not password:
            error = "password required"
        elif len(password) < 6:
            error = "password is weak"

        if not error:
            if register_user(conn, cursor, username, email, password):
                return redirect(url_for("login"))

    return render_template("register.html", error=error)


@app.route("/login", methods=["POST", "GET"])
def login():
    if session.get("username"):
        return redirect(url_for("home"))

    error = None
    if request.method == "POST":
        email = request.form["email"]

        if not email:
            error = "email is Empty"
        elif "@" not in email:
            error = "Email requires an @ sign"
        elif len(email) < 9:
            error = "MIn Email length Required >9"
        else:
            password = request.form["password"]
            if not password:
                error = "password is empty"
            elif len(password) < 6:
                error = "password is Short..."

        if not error:
            logged_in = Login(cursor, email, password)
            if not logged_in:
                error = "username or password Incorrect..."
            else:
                is_active = logged_in.is_active
                username = logged_in.name
                user_id = logged_in.user_id
                if not is_active:
                    error = "user Account is De-Activated"
                else:
                    session["username"] = username
                    session["user_id"] = user_id

                    return redirect(url_for("home"))

    return render_template("login.html", error=error)


@app.route("/logout")
@Login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/post/<int:post_id>")
@Login_required
def single_post(post_id):
    # 1. Get the post
    # 2. If not found → 404
    # 3. Get comments
    # 4. Check if user liked
    # 5. Render post.html

    post = get_single_post(cursor, post_id)
    if not post:
        return "post Not found...", 403
    comments = get_post_comments(
        cursor,
        post_id,
    )
    user_id = session.get("user_id")
    user_liked_post = user_liked(
        cursor,
        user_id,
        post_id,
    )

    return render_template(
        "post.html",
        post=post,
        comments=comments,
        user_liked=user_liked_post,
    )


@app.route("/like_unlike/<int:post_id>", methods=["POST", "GET"])
@Login_required
def toggle(post_id):
    user_id = session.get("user_id")
    toggle_like(
        cursor,
        conn,
        post_id,
        user_id,
    )
    return redirect(request.referrer or url_for("home"))


@app.route("/comment/post/<int:post_id>", methods=["POST"])
@Login_required
def comment(post_id):
    if request.method == "POST":
        content = request.form["content"]
        user_id = session.get("user_id")
        if not content:
            return redirect(request.referrer or url_for("home"))
    comment_register(
        cursor,
        conn,
        content,
        post_id,
        user_id,
    )
    return redirect(request.referrer or url_for("home"))


@app.route("/post/delete/comment/<int:comment_id>/<int:post_id>", methods=["POST"])
@Login_required
def deleting_comment(comment_id, post_id):
    delete_comment(cursor, conn, comment_id)
    return redirect(request.referrer or url_for("single_post", post_id=post_id))


@app.route("/dashboard/<int:user_id>")
@Login_required
def user_dashboard(user_id):
    "get the user"
    if session.get("user_id") != user_id:
        return "Unauthorized Access", 403

    user = get_user(cursor, user_id=session.get("user_id"))
    user_posts = get_user_posts(
        cursor,
        user_id=session.get(
            "user_id",
        ),
    )
    posts_liked = []
    for user_post in user_posts:
        user_liked_post = user_liked(
            cursor,
            user_id=user.user_id,
            post_id=user_post.post_id,
        )
        combined = user_post, user_liked_post
        posts_liked.append(combined)

        # ############
        "get all posts"
    all_posts_liked = []
    all_posts = user_related_posts_liked(cursor, user.user_id)
    if all_posts:
        for post in all_posts:
            combined = post, True
            all_posts_liked.append(combined)
    return render_template(
        "dashboard.html", user=user, user_posts=posts_liked, all_posts=all_posts_liked
    )


@app.route("/delete_post/<int:post_id>", methods=["POST"])
@Login_required
def post_delete(post_id):

    author_id = verify_delete_post(cursor, post_id)
    if author_id and session.get("user_id") == author_id:
        delete_post(cursor, conn, post_id)
        return redirect(url_for("home"))
    return "unauthorized Action...", 403


@app.route("/create_post", methods=["POST", "GET"])
@Login_required
def create_post():
    error = None
    if request.method == "POST":
        author_id = session.get("user_id")
        title = request.form["title"]
        content = request.form["content"]
        image = request.form.get("image", "")
        category_id_str = request.form["category"]

        if not title or not content:
            error = "Fill Field with valid Inputs..."
        try:

            category_id = int(category_id_str)
        except ValueError as e:
            error = "Improper Value In Categories"

        if not error:
            post_created = Post(
                title,
                content,
                author_id,
                category_id,
                image,
            )
            post_created.save_post(
                conn,
                cursor,
            )
            return redirect(url_for("single_post", post_id=post_created.post_id))

    return render_template(
        "create_post.html",
        error=error,
        username=session.get("username"),
        user_id=session.get("user_id"),
    )


@app.route("/post_edit/<int:post_id>", methods=["POST", "GET"])
@Login_required
def edit_post(post_id):
    error = None
    post = get_single_post(cursor, post_id)
    if session.get("user_id") != post.author_id:
        return redirect(request.referrer or url_for("home"))

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        image = request.form["image"]
        category_id_str = request.form["category"]

        if not title or not content or not category_id_str:
            error = "Enter the Field with required Inputs..."
        try:
            category_id = int(category_id_str)
            if not error:
                post = Post(
                    post_id=post_id,
                    title=title,
                    content=content,
                    author_id=post.author_id,
                    category_id=category_id,
                    image=image,
                )
                if post.update_post(
                    conn,
                    cursor,
                ):
                    return redirect(url_for("single_post", post_id=post_id))
        except ValueError as e:
            error = "Unauthorized Category Input..."

    return render_template(
        "edit_post.html",
        error=error,
        post=post,
    )


if __name__ == "__main__":
    import os

    debug = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(debug=debug)
