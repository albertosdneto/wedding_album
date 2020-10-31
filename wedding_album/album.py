from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)

bp = Blueprint('album', __name__)


@bp.route('/')
def index():
    return render_template('album/index.html', )
