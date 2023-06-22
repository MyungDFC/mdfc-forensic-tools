import json
from flask import Blueprint, render_template, url_for, session
from werkzeug.utils import redirect
from app.engine.case_manager import CaseManager

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route("/", methods=["GET"])
def process():
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
                'records' variable is already serialized by 'json.dumps()'
                type: list[json]
            """
            session[artifact_name] = records 

            # if forensic_artifact.artifact == "Chrome":
            #     session["artifact_name"] = records
            #     return render_template(
            #         "page/results/table_chrome.html",
            #         artifact_name=artifact_name,
            #         records=records,
            #     )
            # elif forensic_artifact.artifact == "Edge":
            #     return render_template(
            #         "page/results/table_edge.html",
            #         artifact_name=artifact_name,
            #         records=records,
            #     )
            # elif forensic_artifact.artifact == "RecycleBin":
            #     return render_template(
            #         "page/results/table_recyclebin.html",
            #         artifact_name=artifact_name,
            #         records=records,
            #     )
            # elif forensic_artifact.artifact == "Prefetch":
            #     return render_template(
            #         "page/results/table_prefetch.html",
            #         artifact_name=artifact_name,
            #         records=records,
            #     )
            # elif forensic_artifact.artifact == "JumpList":
            #     return render_template(
            #         "page/results/table_jumplist.html",
            #         artifact_name=artifact_name,
            #         records=records,
            #     )
            # elif forensic_artifact.artifact == "LogonEvent":
            #     return render_template(
            #         "page/results/table_logonevent.html",
            #         artifact_name=artifact_name,
            #         records=records,
            #     )
            # if forensic_artifact.artifact == "USB(EventLog)":
            #     session["artifact_name"] = records
            # elif forensic_artifact.artifact == "WLAN":
            #     session["artifact_name"] = records
                
    return redirect(url_for("dashboard.statistics"))


@bp.route("/statistics", methods=["GET"])
def statistics():
    return render_template("page/dashboard/table_statistics.jinja-html")



@bp.route("/usb", methods=["GET"])
def usb():
    title = "USB History"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        for record in session.get("usb_event", "{}")
    ]

    return render_template(
        "page/dashboard/table_usb.jinja-html",
        title = title,
        records=records
    )