from flask import Blueprint, render_template

from app import cache

bp = Blueprint("contact", __name__, url_prefix="/contact")

@bp.route("/")
@cache.cached(timeout=1800)
def main():
    return render_template("page/contact/main.jinja-html")
