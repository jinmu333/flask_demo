# -*- coding: utf-8 -*-
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
bp = Blueprint('upload', __name__)
UPLOAD_FOLDER = bp.root_path + '/../uploads/'

try:
    os.makedirs(UPLOAD_FOLDER)
except OSError:
    pass


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not file or not allowed_file(file.filename):
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return render_template('file/file.html', img='/uploads/' + filename)

    return render_template('file/file.html')
