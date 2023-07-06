from flask import Blueprint, render_template

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route("/digital_forensics", methods=["GET"])
def digital_forensics():
    return render_template("page/services/digital_forensics/dashboard.jinja-html")

@bp.route("/data_recovery", methods=["GET"])
def data_recovery():
    return render_template("page/services/data_recovery/dashboard.jinja-html")

