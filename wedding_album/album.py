from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.utils import secure_filename
from wedding_album.auth import login_required, host_required
from .helpers import *
import uuid
from .models import Photo, Comment, Like

bp = Blueprint('album', __name__)


@bp.route('/')
def index():
    photos = Photo.objects(public=True)
    my_likes = Like.objects(user_id=g.user.id)
    my_list = []
    for item in my_likes:
        my_list.append(item.photo_id)

    return render_template('album/index.html', photos=photos, my_likes=my_list)


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
    photos = Photo.objects()
    return render_template('album/all_photos.html', photos=photos)


@bp.route('/_change_visibility')
@login_required
@host_required
def change_visibility():
    photo_id = request.args.get('id', 0, type=str)
    status = request.args.get('status', 0, type=str)
    if status == 'True':
        status = True
    else:
        status = False
    photo = Photo.objects(id=photo_id)[0]
    photo.public = status
    photo.save()

    return jsonify(result='success')


@bp.route('/single_photo', methods=["GET", "POST"])
@login_required
def single_photo():
    if request.method == 'POST':
        error = None
        content = request.form['content']
        photo_id = request.form['photo_id']
        new_comment = Comment(user_id=g.user.id, username=g.user.username,
                              photo_id=photo_id, content=content)

        if not content:
            error = 'Content required'
        if content.strip() == '':
            error = 'Content required'

        if error is None:
            new_comment.save()
            return redirect(url_for('album.single_photo') + '?id=' + photo_id)

        flash(error, category='error')

    photo_id = request.args.get('id', 0, type=str)
    photo = Photo.objects(id=photo_id)[0]

    comments = Comment.objects(photo_id=photo_id)

    liked = Like.objects(photo_id=photo_id, user_id=g.user.id)
    if len(liked) == 0:
        liked = False
    else:
        liked = True

    return render_template('album/single_photo.html', photo=photo, comments=comments, liked=liked)


@bp.route('/_like')
@login_required
@host_required
def like():
    photo_id = request.args.get('photo_id', 0, type=str)

    like_photo = Like.objects(photo_id=photo_id, user_id=g.user.id)

    if len(like_photo) == 0:
        new_like = Like(user_id=g.user.id, photo_id=photo_id)
        new_like.save()
        result = 'liked'
    else:
        like_photo.delete()
        result = 'disliked'

    return jsonify(result=result)
