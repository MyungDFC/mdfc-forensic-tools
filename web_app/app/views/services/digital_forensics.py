import re
import json
import math
from collections import namedtuple
from pathlib import Path
from datetime import datetime

from flask import Blueprint, render_template, session, request, redirect, url_for

from app.engine.case_manager import CaseManager

bp = Blueprint("artifact", __name__, url_prefix="/dashboard/digital_forensics")

ArtifactCategory = namedtuple("ArtifactCategory", ["title", "icon_html"])


icon_html_red = "<i class='bg-danger'></i>"
icon_html_yellow = "<i class='bg-warning'></i>"
icon_html_green = "<i class='bg-success'></i>"
icon_html_pink = "<i class='bg-tertiary'></i>"

artifact_category = {
    "internet_visits": ArtifactCategory(title="인터넷 사용기록", icon_html=icon_html_yellow),
    "internet_downloads": ArtifactCategory(title="인터넷 사용기록", icon_html=icon_html_yellow),
    "internet_keyword_search_terms": ArtifactCategory(title="인터넷 사용기록", icon_html=icon_html_yellow),
    "logon_event": ArtifactCategory(title="사용자 활동", icon_html=icon_html_green),
    "jumplist": ArtifactCategory(title="사용자 활동", icon_html=icon_html_green),
    "jumplist_external": ArtifactCategory(title="데이터 유출", icon_html=icon_html_red),
    "recyclebin": ArtifactCategory(title="데이터 삭제", icon_html=icon_html_pink),
    "usb_event": ArtifactCategory(title="데이터 유출", icon_html=icon_html_red),
    "prefetch": ArtifactCategory(title="사용자 활동", icon_html=icon_html_green),
    "wlan_event": ArtifactCategory(title="사용자 활동", icon_html=icon_html_green),
}

## Template Filters
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


@bp.app_template_filter("format_count")
def format_count(count):
    return format(int(count), ",d")


## Pagination
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


## Internet Visits
@bp.route("/internet_visits", methods=["GET"])
def internet_visits():
    title = "웹사이트 방문 기록"
    artifact_icon_html = """
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-unlock" viewBox="0 0 16 16">
    <path d="M11 1a2 2 0 0 0-2 2v4a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h5V3a3 3 0 0 1 6 0v4a.5.5 0 0 1-1 0V3a2 2 0 0 0-2-2zM3 8a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1H3z"/>
    </svg>
    """
    category = artifact_category.get("internet_visits", None)
    artifact_page = "artifact.internet_visits"
    edge_path = Path(session.get("root_directory", None)) / "edge_history.json"
    chrome_path = Path(session.get("root_directory", None)) / "chrome_history.json"

    with open(edge_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Pagination variables
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_internet_visits.jinja-html",
        title = title,
        category=category,
        artifact_icon_html=artifact_icon_html,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        reload_url=url_for("artifact.internet_visits_reload"),
    )

@bp.route("/internet_visits/reload", methods=["GET"])
def internet_visits_reload():
    artifacts = ["Chrome", "Edge"]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("artifact.internet_visits")) 


## Internet Downloads
@bp.route("/internet_downloads", methods=["GET"])
def internet_downloads():
    title = "파일 다운로드 기록"
    artifact_icon_html = """
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-unlock" viewBox="0 0 16 16">
    <path d="M11 1a2 2 0 0 0-2 2v4a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h5V3a3 3 0 0 1 6 0v4a.5.5 0 0 1-1 0V3a2 2 0 0 0-2-2zM3 8a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1H3z"/>
    </svg>
    """
    category = artifact_category.get("internet_downloads", None)
    artifact_page = "artifact.internet_downloads"
    edge_downloads_path = Path(session.get("root_directory", None)) / "edge_downloads.json"
    chrome_downloads_path = Path(session.get("root_directory", None)) / "chrome_downloads.json"

    with open(edge_downloads_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Pagination variables
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_internet_downloads.jinja-html",
        title = title,
        category=category,
        artifact_icon_html=artifact_icon_html,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        reload_url=url_for("artifact.internet_downloads_reload"),
    )

@bp.route("/internet_downloads/reload", methods=["GET"])
def internet_downloads_reload():
    artifacts = ["Chrome", "Edge"]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("artifact.internet_downloads")) 


## Internet keyword search terms
@bp.route("/internet_keyword_search_terms", methods=["GET"])
def internet_keyword_search_terms():
    title = "인터넷 키워드 검색 목록"
    artifact_icon_html = """
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-unlock" viewBox="0 0 16 16">
    <path d="M11 1a2 2 0 0 0-2 2v4a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h5V3a3 3 0 0 1 6 0v4a.5.5 0 0 1-1 0V3a2 2 0 0 0-2-2zM3 8a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1H3z"/>
    </svg>
    """
    category = artifact_category.get("internet_keyword_search_terms", None)
    artifact_page = "artifact.internet_keyword_search_terms"
    edge_keyword_search_terms_path = Path(session.get("root_directory", None)) / "edge_keyword_search_terms.json"
    chrome_keyword_search_terms_path = Path(session.get("root_directory", None)) / "chrome_keyword_search_terms.json"

    with open(edge_keyword_search_terms_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Pagination variables
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_internet_keyword_search_terms.jinja-html",
        title = title,
        category=category,
        artifact_icon_html=artifact_icon_html,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        reload_url=url_for("artifact.internet_keyword_search_terms_reload"),
    )

@bp.route("/internet_keyword_search_terms/reload", methods=["GET"])
def internet_keyword_search_terms_reload():
    artifacts = ["Chrome", "Edge"]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("artifact.internet_keyword_search_terms")) 



## LogonEvent
@bp.route("/logon_event", methods=["GET"])
def logon_event():
    title = "사용자 로그온 기록"
    artifact_icon_html = """
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" class="bi bi-unlock" viewBox="0 0 16 16">
    <path d="M11 1a2 2 0 0 0-2 2v4a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h5V3a3 3 0 0 1 6 0v4a.5.5 0 0 1-1 0V3a2 2 0 0 0-2-2zM3 8a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1H3z"/>
    </svg>
    """
    category = artifact_category.get("logon_event", None)
    artifact_page = "artifact.logon_event"
    artifact_path = Path(session.get("root_directory", None)) / "logon_event.json"

    with open(artifact_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Pagination variables
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_logon_event.jinja-html",
        title = title,
        category=category,
        artifact_icon_html=artifact_icon_html,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        reload_url=url_for("artifact.logon_event_reload"),
    )

@bp.route("/logon_event/reload", methods=["GET"])
def logon_event_reload():
    artifacts = ["LogonEvent",]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("artifact.logon_event")) 

## JumpList
@bp.route("/jumplist", methods=["GET"])
def jumplist():
    title = "파일/폴더 열람 기록"
    artifact_icon_html = """
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="bi bi-folder2-open" viewBox="0 0 16 16">
    <path d="M1 3.5A1.5 1.5 0 0 1 2.5 2h2.764c.958 0 1.76.56 2.311 1.184C7.985 3.648 8.48 4 9 4h4.5A1.5 1.5 0 0 1 15 5.5v.64c.57.265.94.876.856 1.546l-.64 5.124A2.5 2.5 0 0 1 12.733 15H3.266a2.5 2.5 0 0 1-2.481-2.19l-.64-5.124A1.5 1.5 0 0 1 1 6.14V3.5zM2 6h12v-.5a.5.5 0 0 0-.5-.5H9c-.964 0-1.71-.629-2.174-1.154C6.374 3.334 5.82 3 5.264 3H2.5a.5.5 0 0 0-.5.5V6zm-.367 1a.5.5 0 0 0-.496.562l.64 5.124A1.5 1.5 0 0 0 3.266 14h9.468a1.5 1.5 0 0 0 1.489-1.314l.64-5.124A.5.5 0 0 0 14.367 7H1.633z"/>
    </svg>
    """
    category = artifact_category.get("jumplist", None)
    artifact_page = "artifact.jumplist"
    artifact_path = Path(session.get("root_directory", None)) / "jumplist.json"

    with open(artifact_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    drive_pattern = r"^[A-Z]:\\"

    records = [record for record in records if re.match(drive_pattern, record["path"])]

    # Pagination variables
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_jumplist.jinja-html",
        title = title,
        category=category,
        artifact_icon_html=artifact_icon_html,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        reload_url=url_for("artifact.jumplist_reload"),
    )

@bp.route("/jumplist/reload", methods=["GET"])
def jumplist_reload():
    artifacts = ["JumpList",]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("artifact.jumplist")) 


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

## RecycleBin
@bp.route("/recyclebin", methods=["GET"])
def recyclebin():
    title = "휴지통 분석 기록"
    artifact_icon_html = """
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                        style="fill: rgba(0, 0, 0, 1);transform: ;msFilter:;">
                        <path
                          d="m21.224 15.543-.813-1.464-1.748.972.812 1.461c.048.085.082.173.104.264a1.024 1.024 0 0 1-.014.5.988.988 0 0 1-.104.235 1 1 0 0 1-.347.352.978.978 0 0 1-.513.137H14v-2l-4 3 4 3v-2h4.601c.278 0 .552-.037.811-.109a2.948 2.948 0 0 0 1.319-.776c.178-.179.332-.38.456-.593a2.992 2.992 0 0 0 .336-2.215 3.163 3.163 0 0 0-.299-.764zM5.862 11.039l-2.31 4.62a3.06 3.06 0 0 0-.261.755 2.997 2.997 0 0 0 .851 2.735c.178.174.376.326.595.453A3.022 3.022 0 0 0 6.236 20H8v-2H6.236a1.016 1.016 0 0 1-.5-.13.974.974 0 0 1-.353-.349 1 1 0 0 1-.149-.468.933.933 0 0 1 .018-.245c.018-.087.048-.173.089-.256l2.256-4.512 1.599.923L8.598 8 4 9.964l1.862 1.075zm12.736 1.925L19.196 8l-1.638.945-2.843-5.117a2.95 2.95 0 0 0-1.913-1.459 3.227 3.227 0 0 0-.772-.083 3.003 3.003 0 0 0-1.498.433A2.967 2.967 0 0 0 9.41 3.944l-.732 1.464 1.789.895.732-1.465c.045-.09.101-.171.166-.242a.933.933 0 0 1 .443-.27 1.053 1.053 0 0 1 .53-.011.963.963 0 0 1 .63.485l2.858 5.146L14 11l4.598 1.964z">
                        </path>
                      </svg>
                      """
    category = artifact_category.get("recyclebin", None)
    artifact_page = "artifact.recyclebin"
    artifact_path = Path(session.get("root_directory", None)) / "recyclebin.json"

    with open(artifact_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Pagination variables
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_recyclebin.jinja-html",
        title = title,
        category=category,
        artifact_icon_html=artifact_icon_html,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        reload_url=url_for("artifact.recyclebin_reload"),
    )

@bp.route("/recyclebin/reload", methods=["GET"])
def recyclebin_reload():
    artifacts = ["RecycleBin",]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("artifact.recyclebin"))    


## USB(EventLog)
@bp.route("/usb_event", methods=["GET"])
def usb_event():
    title = "USB 연결 이벤트"
    artifact_icon_html = """
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                        style="fill: rgba(0, 0, 0, 1);transform: ;msFilter:;">
                        <path
                          d="M16 10h1v2h-4V6h2l-3-4-3 4h2v8H7v-2.277c.596-.347 1-.985 1-1.723a2 2 0 0 0-4 0c0 .738.404 1.376 1 1.723V14c0 1.103.897 2 2 2h4v2.277A1.99 1.99 0 0 0 10 20a2 2 0 0 0 4 0c0-.738-.404-1.376-1-1.723V14h4c1.103 0 2-.897 2-2v-2h1V6h-4v4z">
                        </path>
                      </svg>
                      """
    category = artifact_category.get("usb_event", None)
    artifact_page = "artifact.usb_event"
    artifact_path = Path(session.get("root_directory", None)) / "usb_event.json"

    with open(artifact_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Pagination variables
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_usb_event.jinja-html",
        title = title,
        category=category,
        artifact_icon_html=artifact_icon_html,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        reload_url=url_for("artifact.usb_event_reload"),
    )

@bp.route("/usb_event/reload", methods=["GET"])
def usb_event_reload():
    artifacts = ["USB(EventLog)",]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("artifact.usb_event"))  


## Prefetch
@bp.route("/prefetch", methods=["GET"])
def prefetch():
    title = "프로그램 실행 기록"
    artifact_icon_html = """
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="bi bi-terminal" viewBox="0 0 16 16">
    <path d="M6 9a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3A.5.5 0 0 1 6 9zM3.854 4.146a.5.5 0 1 0-.708.708L4.793 6.5 3.146 8.146a.5.5 0 1 0 .708.708l2-2a.5.5 0 0 0 0-.708l-2-2z"/>
    <path d="M2 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h12z"/>
    </svg>
    """
    category = artifact_category.get("prefetch", None)
    artifact_page = "artifact.prefetch"
    artifact_path = Path(session.get("root_directory", None)) / "prefetch.json"

    with open(artifact_path, "r", encoding="utf-8") as f:
        records = json.load(f)

    # Pagination variables
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Pagination
    items_on_page, total, last_page, block_start, block_end = pagination(records, page, per_page)

    return render_template(
        "page/services/digital_forensics/table_prefetch.jinja-html",
        title = title,
        category=category,
        artifact_icon_html=artifact_icon_html,
        artifact_page=artifact_page,
        records=items_on_page,
        page=page,
        per_page=per_page,
        total=total,
        last_page=last_page,
        block_start=block_start,
        block_end=block_end,
        reload_url=url_for("artifact.prefetch_reload"),
    )

@bp.route("/prefetch/reload", methods=["GET"])
def prefetch_reload():
    artifacts = ["Prefetch",]
    root_directory = Path(session.get("root_directory", None))
    
    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    case.export_all()
    
    return redirect(url_for("artifact.prefetch"))


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

