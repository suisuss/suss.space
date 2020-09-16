from flaskapp import db, bcrypt, app, guard
from flaskapp.admin.forms import RegistrationForm
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskapp.admin.models import User
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import requests

date = datetime.today().strftime('%m-%d-%y')

admin = Blueprint('admin', __name__)

@admin.route("/admin/register", methods=['GET', 'POST'])
def admin_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # api_password is password but hashed again with the guard
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, api_password=guard.hash_password(hashed_password))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.index'))
    return render_template('admin/register.html', header='Register', form=form)