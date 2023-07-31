from flask import Blueprint, render_template

from app import cache

bp = Blueprint("people", __name__, url_prefix="/people")

@bp.route("/")
@cache.cached(timeout=1800)
def main():
    return render_template("page/people/main.jinja-html")
