from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

from wedding_album.auth import login_required, host_required

bp = Blueprint('album', __name__)


@bp.route('/')
def index():
    return render_template('album/index.html', )


@bp.route('/my_uploads')
def my_uploads():
    return render_template('album/my_uploads.html', )


@bp.route('/all_photos')
@login_required
@host_required
def all_photos():
    return render_template('album/all_photos.html', )