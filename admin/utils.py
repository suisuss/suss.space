import os
import secrets
from PIL import Image
from werkzeug.utils import secure_filename
from . import app

ALLOWED_EXTENSIONS = set(['css', 'html', 'jpg', 'png'])


def valid_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file(filename):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def save_picture(form_picture, _path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(_path, picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def upload_file(file, _path):
    if valid_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(_path, filename)
        file.save(file_path)

    return file_path
