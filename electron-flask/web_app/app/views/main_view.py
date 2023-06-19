from flask import Blueprint, render_template
from werkzeug.utils import redirect

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def index():
    return render_template("page/home/index.html")