import json
from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from app.engine.case_manager import CaseManager

bp = Blueprint("main", __name__, url_prefix="/")

# NOTE: This is the main view of the application.
@bp.route("/")
def home():
    return render_template("page/home/index.jinja-html")
    # return render_template("page/home/index.html")

@bp.route("/dashboard")
def dashboard():
    return render_template("page/about/index.html")

@bp.route("/dashboard")
def index():
    artifacts = [
        # "Chrome",
        # "Edge",
        # "RecycleBin",
        # "Prefetch",
        # "JumpList",
        # "LogonEvent",
        # "USB(EventLog)",
        "WLAN",
    ]
    cm = CaseManager(_artifacts=artifacts)
    cm.parse_all()

    for forensic_artifact in cm.forensic_artifacts:
        for artifact_name, records in forensic_artifact.result.items():
            """
                records variable is list of str(json), which is a result of 'json.dumps'.
                So, we need to convert it to list of dict(json) using 'json.loads'.
            """
            records = [
                json.loads(record) for record in records
            ]
            
            if forensic_artifact.artifact == "Chrome":
                return render_template(
                    "page/results/table_chrome.html",
                    artifact_name=artifact_name,
                    records=records,
                )
            # elif forensic_artifact.artifact == "Edge":
            #     return render_template(
            #         "page/results/table_edge.html",
            #         artifact_name=artifact_name,
            #         records=records,
            #     )
            elif forensic_artifact.artifact == "RecycleBin":
                return render_template(
                    "page/results/table_recyclebin.html",
                    artifact_name=artifact_name,
                    records=records,
                )
            elif forensic_artifact.artifact == "Prefetch":
                return render_template(
                    "page/results/table_prefetch.html",
                    artifact_name=artifact_name,
                    records=records,
                )
            elif forensic_artifact.artifact == "JumpList":
                return render_template(
                    "page/results/table_jumplist.html",
                    artifact_name=artifact_name,
                    records=records,
                )
            elif forensic_artifact.artifact == "LogonEvent":
                return render_template(
                    "page/results/table_logonevent.html",
                    artifact_name=artifact_name,
                    records=records,
                )
            elif forensic_artifact.artifact == "USB(EventLog)":
                return render_template(
                    "page/results/table_usb.html",
                    artifact_name=artifact_name,
                    records=records,
                )
            elif forensic_artifact.artifact == "WLAN":
                return render_template(
                    "page/results/table_wlan.html",
                    artifact_name=artifact_name,
                    records=records,
                )
