from flask import Blueprint, render_template

bp = Blueprint("faq", __name__, url_prefix="/faq")

@bp.route("/")
def main():
    return render_template("page/faq/main.jinja-html")
