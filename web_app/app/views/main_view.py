from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from app.engine.case_manager import CaseManager

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/")
def index():
    artifacts = [
        # "Chrome",
        # "Edge",
        # "RecycleBin",
        # "Prefetch",
        # "JumpList",
        # "LogonEvent",
        "USB(EventLog)",
        # "WLAN",
    ]
    cm = CaseManager(_artifacts=artifacts)
    cm.parse_all()


    return render_template("page/home/index.html", forensic_artifact=cm.forensic_artifact)
    # return redirect(url_for("main.data"))  # test code




# # test code
# @bp.route('/data')
# def data():
#     data = [
#         {"name": "Alice", "email": "alice@example.com"},
#         {"name": "Bob", "email": "bob@example.com"},
#         {"name": "Charlie", "email": "charlie@example.com"}
#     ]
#     return render_template("page/home/index.html", data=data)
