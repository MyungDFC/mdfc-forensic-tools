from flask import Blueprint, render_template

bp = Blueprint("people", __name__, url_prefix="/people")

@bp.route("/")
def main():
    return render_template("page/people/main.jinja-html")
