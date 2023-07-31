import json
from pathlib import Path

from flask import Blueprint, render_template, session, jsonify, request

from app.engine.case_manager import CaseManager


bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.app_template_filter("format_count")
def format_count(count):
    return format(int(count), ",d")

@bp.route("/digital_forensics", methods=["GET"])
def digital_forensics():
    root_directory = Path(session.get("root_directory", None))
    
    usb_event_path = root_directory / "usb_event.json"
    logon_event_path = root_directory / "logon_event.json"
    jumplist_path = root_directory / "jumplist.json"
    prefetch_path = root_directory / "prefetch.json"
    recyclebin_path = root_directory / "recyclebin.json"

    with open(usb_event_path, "r", encoding="utf-8") as f:
        usb_event_records = json.load(f)

    with open(logon_event_path, "r", encoding="utf-8") as f:
        logon_event_records = json.load(f)
        
    with open(jumplist_path, "r", encoding="utf-8") as f:
        jumplist_records = json.load(f)
    
    with open(prefetch_path, "r", encoding="utf-8") as f:
        prefetch_records = json.load(f)
    
    with open(recyclebin_path, "r", encoding="utf-8") as f:
        recyclebin_records = json.load(f)
    
    usb_event_total = len(usb_event_records)
    logon_event_total = len(logon_event_records)
    jumplist_total = len(jumplist_records)
    prefetch_total = len(prefetch_records)
    recyclebin_total = len(recyclebin_records)

    return render_template(
        "page/services/digital_forensics/dashboard.jinja-html",
        usb_event_total=usb_event_total,
        logon_event_total=logon_event_total,
        jumplist_total=jumplist_total,
        prefetch_total=prefetch_total,
        recyclebin_total=recyclebin_total,
    )

@bp.route("/data_recovery", methods=["GET"])
def data_recovery():
    return render_template("page/services/data_recovery/dashboard.jinja-html")


@bp.route("/usb_event_reload", methods=["GET"])
def usb_event_reload():
    artifacts = ["USB(EventLog)",]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()

    usb_event_path = root_directory / "usb_event.json"

    with open(usb_event_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    usb_event_total = len(records)

    return jsonify({"usb_event_total": usb_event_total,})

@bp.route("/recyclebin_reload", methods=["GET"])
def recyclebin_reload():
    artifacts = ["Recyclebin",]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()

    usb_event_path = root_directory / "recyclebin.json"

    with open(usb_event_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    recyclebin_total = len(records)

    return jsonify({"recyclebin_total": recyclebin_total,})