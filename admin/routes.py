from flaskapp import db, bcrypt
from flaskapp.admin.forms import LoginForm, UpdateAccountForm, PostForm, PArticleForm, UploadForm
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskapp.main.models import Post, PArticle
from flaskapp.admin.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.admin.utils import save_picture, allowed_file
from werkzeug.utils import secure_filename
import os
from . import app

admin = Blueprint('admin', __name__)


@admin.route("/admin")
def adminn():
    return render_template('admin/index.html')


@admin.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.adminn'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin/login.html', header='BLOG', posts=posts, form=form)


@admin.route("/admin/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def admin_update_post(post_id):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = form.date_posted.data
        post.tags = form.tags.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('admin.adminn', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('admin/create_post.html', title='Update Post', form=form, legend='Update Post', posts=posts)


@admin.route("/admin/article/<int:article_id>/update", methods=['GET', 'POST'])
@login_required
def admin_update_article(article_id):
    page = request.args.get('page', 1, type=int)
    articles = PArticle.query.order_by(PArticle.date_posted.desc()).paginate(page=page, per_page=3)
    article = PArticle.query.get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    form1 = PArticleForm()
    if form1.validate_on_submit():
        article.title = form1.title.data
        article.date_posted = form1.date_posted.data
        article.tags = form1.tags.data
        article.overview = form1.overview.data
        article.category = form1.category.data
        article.thumbnail = form1.thumbnail.data
        article.html = form1.html.data
        db.session.commit()
        flash('Your article has been updated!', 'success')
        return redirect(url_for('admin.adminn', article_id=article.id))
    elif request.method == 'GET':
        form1.title.data = article.title
        form1.overview.data = article.overview
    return render_template('admin/create_article.html', title='Update Article', form1=form1, legend1='Update Article', articles=articles)


@admin.route("/admin/post/<int:post_id>/delete", methods=['POST'])
@login_required
def admin_delete_post(post_id):

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('admin.adminn'))


@admin.route("/admin/article/<int:article_id>/delete", methods=['POST'])
@login_required
def admin_delete_article(article_id):

    page = request.args.get('page', 1, type=int)
    articles = PArticle.query.order_by(PArticle.date_posted.desc()).paginate(page=page, per_page=3)
    article = PArticle.query.get_or_404(article_id)

    if article.author != current_user:
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash('Your article has been deleted!', 'success')
    return redirect(url_for('admin.adminn'))


@admin.route("/admin/logout")
def admin_logout():
    logout_user()
    return redirect(url_for('admin.adminn'))


@admin.route("/admin/account", methods=['GET', 'POST'])
@login_required
def admin_account():

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'flaskapp/static/img/profile_pics')
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('admin.admin_account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='img/profile_pics/' + current_user.image_file)

    return render_template('admin/account.html', title='Account', header="ADMIN", image_file=image_file, form=form, posts=posts)


@admin.route("/admin/new-post", methods=['GET', 'POST'])
@login_required
def admin_new_post():

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, tags=form.tags.data,
                    date_posted=form.date_posted.data, author=current_user)
        db.session.add(post)
        db.session.flush()
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('admin.admin_new_post'))

    return render_template('admin/create_post.html', title='New Post', header="ADMIN",
                           form=form, legend='New Post', posts=posts)


@admin.route("/admin/new-article", methods=['GET', 'POST'])
@login_required
def admin_new_article():

    form1 = PArticleForm()

    if form1.validate_on_submit():
        # Inputting form data to PArticle table in SQLite3
        article = PArticle(title=form1.title.data, date_posted=form1.date_posted.data, tags=form1.tags.data,
                           overview=form1.overview.data, category=form1.category.data, thumbnail=form1.thumbnail.data, html_filename=form1.html.data, user_id=current_user.id, author=current_user)
        db.session.add(article)
        db.session.flush()
        db.session.commit()
        flash('Your article card has been created!', 'success')
        return redirect(url_for('admin.admin_new_article'))

    return render_template('admin/create_article.html', header='ADMIN', title='New Article', legend0='New Writing Article', legend1='New Programming Article', form1=form1, legend='New Article')


@admin.route('/admin/upload-file', methods=['GET', 'POST'])
@login_required
def upload_file():

    form1 = UploadForm()

    if request.method == 'POST':

        file = request.files['file']
        path = form1.path.data

        if file.filename == '':
            flash(f'No file selected for uploading', 'danger')
            return redirect(url_for('admin.upload_file'))

        if allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join('flaskapp/', path, filename))
            flash('File successfully uploaded', 'success')
            return redirect(url_for('admin.upload_file'))

        else:
            flash('Allowed file types are jpeg, png, html and css', 'danger')
            return redirect(url_for('admin.upload_file'))

    return render_template('admin/upload_file.html', header='ADMIN', title='New Article', legend0='New Writing Article', legend1='New Programming Article', form1=form1, legend='New Article')


@admin.route("/admin/post/<int:post_id>")
@login_required
def admin_post(post_id):

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    post = Post.query.get_or_404(post_id)

    return render_template('admin/post.html', title=post.title, post=post, posts=posts, header="ADMIN")
