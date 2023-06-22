from flask import Blueprint, render_template

bp = Blueprint("youtube", __name__, url_prefix="/youtube")

@bp.route("/")
def main():
    return render_template("page/youtube/main.jinja-html")
