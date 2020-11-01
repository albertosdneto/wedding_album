from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.utils import secure_filename
from wedding_album.auth import login_required, host_required
from .helpers import *
import uuid
from .models import Photo

bp = Blueprint('album', __name__)


@bp.route('/')
def index():
    return render_template('album/index.html', )


@bp.route('/my_uploads', methods=["GET", "POST"])
@login_required
def my_uploads():
    if request.method == 'POST':
        error = None
        if "user_file" not in request.files:
            error = "No user_file key in request.files"

        file = request.files["user_file"]

        if file.filename == "":
            error = "Please select a file"

        if file and allowed_file(file.filename):
            extension = file.filename[-4:]
            file.filename = secure_filename(str(uuid.uuid4()) + extension)
            output = upload_file_to_s3(file, S3_BUCKET)
            new_photo = Photo(user_id=g.user.id, username=g.user.username, url=str(output), public=False)
            new_photo.save()
            flash('Successfully uploaded', category='message')
            return redirect(url_for('album.my_uploads'))

        flash(error, category='error')
        return redirect(url_for('album.my_uploads'))

    photos = Photo.objects(user_id=g.user.id)
    return render_template('album/my_uploads.html', photos=photos)


@bp.route('/delete_photo', methods=["GET", "POST"])
@login_required
def delete_photo():
    if request.method == 'POST':
        photo = Photo.objects(id=request.form['photo_id'])[0]
        photo.delete()
        return redirect(url_for('album.my_uploads'))

    photo_id = request.args.get('photo_id', 0, type=str)
    photo = Photo.objects(id=photo_id)[0]
    file_name = photo.url[-40:]

    return render_template('album/delete_confirmation.html', photo=photo, file_name=file_name)


@bp.route('/all_photos')
@login_required
@host_required
def all_photos():
    return render_template('album/all_photos.html', )
