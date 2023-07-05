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
        "RecycleBin",
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
    return redirect(url_for("dashboard.statistics"))


@bp.route("/statistics", methods=["GET"])
def statistics():
    title = "Statistics"
    return render_template(
        "page/dashboard/table_statistics.jinja-html",
        title=title
    )

@bp.route("/Internet", methods=["GET"])
def internet():
    title = "Statistics"
    return render_template(
        "page/dashboard/table_internet.jinja-html",
        title=title
    )

@bp.route("/logon_event", methods=["GET"])
def logon_event():
    title = "Logon History"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        for record in session.get("logon_event", "{}")
    ]

    return render_template(
        "page/dashboard/table_logon_event.jinja-html",
        title = title,
        records=records
    )

@bp.route("/jumplist", methods=["GET"])
def jumplist():
    title = "File History"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        for record in session.get("jumplist", "{}")
    ]

    return render_template(
        "page/dashboard/table_jumplist.jinja-html",
        title = title,
        records=records
    )

@bp.route("/recyclebin", methods=["GET"])
def recyclebin():
    title = "Recyclebin History"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        for record in session.get("recyclebin", "{}")
    ]

    return render_template(
        "page/dashboard/table_recyclebin.jinja-html",
        title = title,
        records=records
    )

@bp.route("/usb_event", methods=["GET"])
def usb_event():
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
        "page/dashboard/table_usb_event.jinja-html",
        title = title,
        records=records
    )

@bp.route("/prefetch", methods=["GET"])
def prefetch():
    title = "Program History"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        for record in session.get("prefetch", "{}")
    ]

    return render_template(
        "page/dashboard/table_prefetch.jinja-html",
        title = title,
        records=records
    )



@bp.route("/wlan_event", methods=["GET"])
def wlan_event():
    title = "Wi-Fi History"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        for record in session.get("wlan_event", "{}")
    ]

    return render_template(
        "page/dashboard/table_wlan_event.jinja-html",
        title = title,
        records=records
    )

