from flask import Blueprint, render_template

bp = Blueprint("blog", __name__, url_prefix="/")

@bp.route("/")
def main():
    return render_template("page/blog/main.jinja-html")
