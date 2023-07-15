from pathlib import Path
from flask import Blueprint, render_template, redirect, url_for

from app.engine.case_manager import CaseManager

bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/loading")
def loading():
    return render_template("page/home/loadingscreen.jinja-html")

@bp.route("/")
def process():

    ROOT_DIRECTORY_NAME = "_myungit"

    artifacts = [
        "Chrome",
        "Edge",
        "RecycleBin",
        "Prefetch",
        "JumpList",
        "LogonEvent",
        "USB(EventLog)",
        "WLAN",
    ]

    temp_dir = Path.home() / "AppData" / "Local" / "Temp"
    root_directory = temp_dir / ROOT_DIRECTORY_NAME
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("home.index"))


# NOTE: This is the main view of the application.
@bp.route("/index")
def index():
    return render_template("page/home/index.jinja-html")
