from flask import Blueprint, render_template
from werkzeug.utils import redirect
from engine.case_manager import CaseManager

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def index():
    artifacts = [
        "Chrome",
        "Edge",
        # "RecycleBin",
        # "Prefetch",
        # "JumpList",
        # "LogonEvent",
        # "USB(EventLog)",
        # "WLAN",
    ]
    cm = CaseManager(_artifacts=artifacts)
    cm.parse_all()

    return render_template("page/home/index.html", cm=cm)