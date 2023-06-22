import json
from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect
from app.engine.case_manager import CaseManager

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route("/", methods=["GET"])
def timeline():
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
                    "page/dashboard/table_usb.jinja-html",
                    artifact_name=artifact_name,
                    records=records,
                )
            elif forensic_artifact.artifact == "WLAN":
                return render_template(
                    "page/results/table_wlan.html",
                    artifact_name=artifact_name,
                    records=records,
                )

@bp.route("/usb", methods=["GET"])
def usb():
    artifacts = [
        "USB(EventLog)",
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
            
            if forensic_artifact.artifact == "USB(EventLog)":
                title = "USB 연결정보"
                return render_template(
                    "page/dashboard/table_usb.jinja-html",
                    title = title,
                    artifact_name=artifact_name,
                    records=records,
                )