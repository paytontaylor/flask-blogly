"""Blogly application."""

from flask import Flask, render_template, redirect, request, url_for
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
@app.route('/users')
def show_users():
    """ Displays a list of all users """

    users = User.query.all()
    return render_template("user/show_users.html", users=users)


@app.route('/users/new', methods=['POST', 'GET'])
def add_user():
    """ Creates a new user w/ POST request or Displays the Create User Form if GET request """

    if request.method == 'POST':
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        image_url = request.form.get("img-url", None)

        if image_url:
            new_user = User(first_name=first_name,
                            last_name=last_name, image_url=image_url)
            db.session.add(new_user)
            db.session.commit()
        else:
            new_user = User(first_name=first_name,
                            last_name=last_name)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for("show_users"))

    return render_template("user/create_user_form.html")


@app.route('/users/<int:uid>')
def show_user(uid):
    """ Displays an individual user """
    user = User.query.get_or_404(uid)
    posts = user.posts

    return render_template("user/show_user.html", user=user, posts=posts)


@app.route('/users/<int:uid>/edit', methods=['POST', 'GET'])
def edit_user(uid):
    """ Displays an edit form for an user and saves changes with POST request """
    user = User.query.get(uid)

    if request.method == 'POST':

        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        image_url = request.form.get("img-url", None)

        if image_url:
            new_user = User(first_name=first_name,
                            last_name=last_name, image_url=image_url)
            db.session.add(new_user)
            db.session.commit()
        else:
            new_user = User(first_name=first_name,
                            last_name=last_name)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for("show_users"))

    return render_template("user/edit_user_form.html", user=user)


@app.route('/users/<int:uid>/delete', methods=['POST'])
def delete_user(uid):
    """ Deletes User """
    user = User.query.get_or_404(uid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("show_users"))


@app.route('/users/<int:uid>/posts/new', methods=['POST', 'GET'])
def show_add_post_form(uid):
    """ Displays Add Post Form and Adds Posts On Submit """

    user = User.query.get_or_404(uid)
    tags = Tag.query.all()

    if request.method == 'POST':

        title = request.form.get("title")
        content = request.form.get("content")
        tags = request.form.getlist('tags')

        tag_ids = [int(id) for id in tags]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        post = Post(title=title, content=content,
                    user_id=user.id, tags=tags)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("show_user", uid=uid))

    return render_template("post/add_post_form.html", user=user, tags=tags)


@app.route('/posts/<int:pid>')
def show_post(pid):
    """ Displays an indivual post """
    post = Post.query.get_or_404(pid)
    tags = post.tags

    return render_template("post/show_post.html", post=post, tags=tags)


@app.route('/posts/<int:pid>/edit', methods=['POST', 'GET'])
def edit_post(pid):
    """ Shows Post Edit Form and Edits Post on Submit """
    post = Post.query.get(pid)
    tags = Tag.query.all()

    if request.method == 'POST':

        title = request.form.get("title")
        content = request.form.get("content")

        post.title = title
        post.content = content
        db.session.commit()

        return redirect(url_for("show_post", pid=pid))

    return render_template("/post/edit_post_form.html", post=post, tags=tags)


@app.route('/posts/<int:pid>/delete', methods=['POST'])
def delete_post(pid):
    """ Deletes Post """
    post = Post.query.get(pid)
    PostTag.query.filter_by(post_id=pid).delete()

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("show_users"))


@app.route('/tags')
def show_tags():
    """ Shows a list of all tags """
    tags = Tag.query.all()

    return render_template(
        "tag/tags.html", tags=tags)


@app.route('/tags/<int:tid>')
def show_tag(tid):
    """ Shows Individual Tag by ID """
    tag = Tag.query.get(tid)
    posts = tag.posts

    return render_template("tag/tag.html", tag=tag, posts=posts)


@app.route('/tags/new', methods=['POST', 'GET'])
def create_new_tag():

    if request.method == 'POST':

        name = request.form.get("tag-name")
        new_tag = Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()

        return redirect(url_for("show_tags"))

    return render_template("tag/create_tag_form.html")


@app.route('/tags/<int:tid>/edit', methods=['POST', 'GET'])
def edit_tag(tid):
    tag = Tag.query.get_or_404(tid)

    if request.method == 'POST':

        name = request.form.get('tag-name')
        tag.name = name
        db.session.commit()

        return redirect(url_for('show_tags'))

    return render_template('tag/edit_tag_form.html', tag=tag)


@app.route('/tags/<int:tid>/delete', methods=['POST'])
def delete_tag(tid):
    tag = Tag.query.get_or_404(tid)

    PostTag.query.filter_by(tag_id=tid).delete()

    db.session.delete(tag)
    db.session.commit()

    return redirect(url_for("show_tags"))
