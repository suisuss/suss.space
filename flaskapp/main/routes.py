from flaskapp import db
from flaskapp.main.forms import MessageForm
from flask import render_template, url_for, flash, redirect, Blueprint
from flaskapp.main.utils import arabic_to_roman
from flaskapp.main.models import Message
from datetime import datetime

date = datetime.today()
year = arabic_to_roman(int(date.year))

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
@main.route("/index", methods=['GET', 'POST'])
def index():
    image_file = url_for('static', filename='img/profile_pics/space.jpg')
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(name=form.name.data, email=form.email.data, phone=form.phone.data, body=form.body.data)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent.', 'success')
        return redirect(url_for('main.index'))
    return render_template('index.html', title='Home', form=form, year=year, image_file=image_file)

# Add unique route? or simply link html
@main.route("/underconstruction")
def construction():
    return render_template('errors/underconstruction.html', title='Policy')


@main.route("/termsofuse")
def terms():
    return render_template('terms.html', title='Website Terms of Use', page="tof")


@main.route("/privacypolicy")
def privacy():
    return render_template('privacy.html', title='Website PRIVACY POLICY', page="pp")
