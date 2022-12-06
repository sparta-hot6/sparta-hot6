import os
from flask import send_from_directory
from werkzeug.utils import secure_filename
from time import strftime

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return True # 임시
    # return '.' in filename and \
    #     filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_time_filename(filename):
    ext = filename.rsplit('.', 1)[1]
    timestr = strftime("%Y%m%d-%H%M%S")
    return '.'.join([timestr, ext])


def upload_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(create_time_filename(file.filename))
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename
    return None


def download_file(name):
    return send_from_directory(UPLOAD_FOLDER, name)
