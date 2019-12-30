from flaskapp import db
from flaskapp.main.forms import MessageForm
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskapp.main.models import Messages, Post, PArticle
from flaskapp.admin.models import User
from flaskapp.main.utils import send_message_email, arabic_to_roman
from datetime import datetime

launch_date = datetime(2019, 12, 28)
now = datetime.today()
year = arabic_to_roman(int(datetime.today().year))
duration = now - launch_date
days_since_launch = duration.days

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
@main.route("/index", methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        message = Messages(name=form.name.data, email=form.email.data,
                           phone=form.phone.data, body=form.body.data)
        db.session.add(message)
        db.session.commit()
        if form.phone.data:
            send_message_email(form.name.data, form.body.data, form.email.data, form.phone.data)
        else:
            send_message_email(form.name.data, form.body.data, form.email.data)
        flash('Your message has been sent.', 'success')
        return redirect(url_for('main.index'))
    return render_template('index.html', title='Home', header="HOME", form=form, days_since_launch=days_since_launch, year=year)


@main.route("/programming/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('programming/blog/blog-home.html', header='BLOG', posts=posts)


@main.route("/programming/blog/user/<string:username>")
def user_post(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('programming/blog/blog-user_post.html', posts=posts, user=user)


@main.route("/programming/blog/post/<int:post_id>")
def post(post_id):
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    post = Post.query.get_or_404(post_id)
    return render_template('programming/blog/blog-post.html', title=post.title, post=post, posts=posts)


@main.route("/programming/blog/tag/<string:tag>")
def user_post_tag(tag):
    username = "Jacob Sussmilch"
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=3)
    return render_template('programming/blog/blog-tag.html', user=user, posts=posts, tag=tag)


@main.route("/programming", methods=['GET', 'POST'])
def programming():
    page = request.args.get('page', 1, type=int)
    articles = PArticle.query.order_by(PArticle.date_posted.desc()).paginate(page=page, per_page=3)
    categories = set(
        [article.category for article in PArticle.query.order_by(PArticle.date_posted.desc())])
    return render_template('programming/index.html', title='Programming', header='PROGRAMMING', articles=articles, categories=categories, page=page)


@main.route("/programming/article/<int:article_id>")
def programming_article(article_id):
    page = request.args.get('page', 1, type=int)
    articles = PArticle.query.order_by(
        PArticle.date_posted.desc()).paginate(page=page, per_page=3)
    articles_by_category = PArticle.query.order_by(
        PArticle.category).paginate(page=page, per_page=3)
    article = PArticle.query.get_or_404(article_id)
    return render_template(f'programming/article/{article.html_filename}', title=article.title, article=article, articles=articles, articles_by_category=articles_by_category)


@main.route("/termsofuse")
def terms():
    return render_template('terms.html', title='Website Terms of Use', page="tof")


@main.route("/privacypolicy")
def privacy():
    return render_template('privacy.html', title='Website PRIVACY POLICY', page="pp")


@main.route("/programming/blog/popular")
def popular():
    return render_template('blog-policy.html', title='Policy')


@main.route("/programming/blog/announcements")
def announcements():
    return render_template('programming/blog/blog-policy.html', title='Policy')


@main.route("/programming/blog/enquiry")
def enquiry():
    return render_template('programming/blog/blog-policy.html', title='Policy')


@main.route("/programming/blog/report_user")
def report_user():
    return render_template('programming/blog/blog-policy.html', title='Policy')


@main.route("/programming/blog/report_fault")
def report_fault():
    return render_template('programming/blog/blog-policy.html', title='Policy')


@main.route("/programming/blog/suggestion")
def suggestion():
    return render_template('programming/blog/blog-policy.html', title='Policy')

# Add unique route? or simply link html
@main.route("/underconstruction")
def construction():
    return render_template('errors/underconstruction.html', title='Policy')
