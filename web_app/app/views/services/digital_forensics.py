import re
import json
import math
from pathlib import Path
from datetime import datetime
from flask import Blueprint, render_template, session, request

from app.engine.case_manager import CaseManager

bp = Blueprint("artifact", __name__, url_prefix="/dashboard/digital_forensics")

@bp.app_template_filter("format_datetime")
def format_datetime(value):
    # Parsing the string into a datetime object
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        return value

    # Formatting the datetime object into a string with the desired format
    formatted_time_str = dt.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_time_str

def pagination(records: list[dict], page: int, per_page: int):
    """
        This function returns a list of dict(json) data for the current page.
        :param records: list of dict(json) data
        :param page: current page number
        :param per_page: number of items per page
    """
    BLOCK_SIZE = 5  # number of pages in the navigation block

    # Pagination
    start = (page - 1) * per_page  # first item to display on this page
    end = start + per_page  # last item to display on this page
    items_on_page = records[start:end]  # items to display on this page

    total = len(records)  # total number of items in the list
    last_page = math.ceil(total / per_page)  # last page number

    block_num = int((page - 1) / BLOCK_SIZE)  # current block number
    block_start = int((BLOCK_SIZE * block_num) + 1)  # first page number in the block (1, 6, 11, ...
    block_end = math.ceil(block_start + (BLOCK_SIZE - 1))  # last page number in the block

    if block_end > last_page:
        block_end = last_page

    return items_on_page, total, last_page, block_start, block_end

@bp.route("/internet", methods=["GET"])
def internet():
    title = "인터넷 사용기록"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        # for record in session.get("logon_event", "{}")
        for record in session.get("recyclebin", "{}")
    ]

    return render_template(
        "page/services/digital_forensics/table_internet.jinja-html",
        title = title,
        records=records
    )

@bp.route("/logon_event", methods=["GET"])
def logon_event():
    title = "사용자 로그온 기록"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        # for record in session.get("logon_event", "{}")
        for record in session.get("recyclebin", "{}")
    ]

    return render_template(
        "page/services/digital_forensics/table_logon_event.jinja-html",
        title = title,
        records=records
    )

@bp.route("/jumplist", methods=["GET"])
def jumplist():
    title = "파일 열람기록"
    artifact_page = "artifact.jumplist"
    artifact_path = Path(session.get("root_directory", None)) / "jumplist.json"

    with open(artifact_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    drive_pattern = r"^[A-Z]:\\"

    records = [record for record in records if re.match(drive_pattern, record["path"])]

    # Pagination variables
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_jumplist.jinja-html",
        title = title,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
    )

@bp.route("/jumplist_external", methods=["GET"])
def jumplist_external():
    title = "외부 데이터 열람기록"
    
    artifact_path = Path(session.get("root_directory", None)) / "jumplist.json"

    with open(artifact_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    drive_pattern = r"^[A-Z]:\\"

    records = [record for record in records if re.match(drive_pattern, record["path"])]
    records = [record for record in records if re.match(drive_pattern, record["path"])]


    # Fixed (Hard disk)

    return render_template(
        "page/services/digital_forensics/table_jumplist_external.jinja-html",
        title = title,
        records=records
    )

@bp.route("/recyclebin", methods=["GET"])
def recyclebin():
    title = '휴지통 데이터 목록'
    artifact_page = "artifact.recyclebin"
    artifact_path = Path(session.get("root_directory", None)) / "recyclebin.json"

    with open(artifact_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Pagination variables
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_recyclebin.jinja-html",
        title = title,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
    )

@bp.route("/usb_event", methods=["GET"])
def usb_event():
    title = "USB 연결 이벤트"
    """
        'records' variable is list of str(json), which is a result of 'json.dumps()'.
        So, you have to convert it to list of dict(json) using 'json.loads'.
    """
    records = [
        json.loads(record)
        # for record in session.get("usb_event", "{}")
        for record in session.get("recyclebin", "{}")
    ]

    return render_template(
        "page/services/digital_forensics/table_usb_event.jinja-html",
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
        for record in session.get("recyclebin", "{}")
        # for record in session.get("prefetch", "{}")
    ]

    return render_template(
        "page/services/digital_forensics/table_prefetch.jinja-html",
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

