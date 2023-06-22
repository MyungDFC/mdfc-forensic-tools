import json
from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from app.engine.case_manager import CaseManager

bp = Blueprint("main", __name__, url_prefix="/")

# NOTE: This is the main view of the application.
@bp.route("/")
def home():
    return render_template("page/home/index.jinja-html")
