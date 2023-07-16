from flask import Blueprint, render_template

bp = Blueprint("contact", __name__, url_prefix="/contact")

@bp.route("/")
def main():
    return render_template("page/contact/main.jinja-html")
