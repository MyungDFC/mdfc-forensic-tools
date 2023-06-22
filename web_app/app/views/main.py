from flask import Blueprint, render_template

bp = Blueprint("main", __name__, url_prefix="/")

# NOTE: This is the main view of the application.
@bp.route("/")
def home():
    return render_template("page/home/index.jinja-html")
