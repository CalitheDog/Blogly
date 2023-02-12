from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretlol'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def root():
    """Homepage for Blogly App"""
    users = User.query.all()
    posts = Post.recent_posts()
    return render_template('index.html', users=users, posts=posts)


@app.route('/users/new')
def users_index():
    """Page to create Users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('newUser.html', users=users)


@app.route("/users/new", methods=["POST"])
def users_new():
    """form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Shows user details"""

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_edit(user_id):
    """edits user info form"""
    user = User.query.get_or_404(user_id)
    return render_template('editUser.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Updates user info in db, redirects to home page"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Destroys the user from the db"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Adds post form for selected user"""

    user = User.query.get_or_404(user_id)
    return render_template('newPost.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    """Submit new post and redirect to user details page"""

    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def display_post(post_id):
    """Displays post of given post_id"""

    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Display edit post form"""

    post = Post.query.get_or_404(post_id)
    return render_template('editPost.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Edits post and redirect back to post page"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post and return to user page"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
