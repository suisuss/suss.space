from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    header = "Oops. Page Not Found (404)"
    sub = "That page does not exist."
    return render_template('errors/error.html', sub=sub, header=header), 404


@errors.app_errorhandler(403)
def error_403(error):
    header = "You don't have permission to access this page (403)"
    sub = "Go Home"
    return render_template('errors/error.html', sub=sub, header=header), 403


@errors.app_errorhandler(500)
def error_500(error):
    header = "SOMETHING WENT WRONG (500)"
    sub = "It's not you its me. We're experiencing some trouble on our end. Please try again in the near future."
    return render_template('errors/error.html', sub=sub, header=header), 500
