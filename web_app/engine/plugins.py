from collections import namedtuple

from engine.artifacts.windows.recyclebin import RecycleBin
from engine.artifacts.windows.prefetch import Prefetch
from engine.artifacts.windows.jumplist import JumpList
from engine.artifacts.windows.eventlog import ForensicEvent
from engine.artifacts.browsers.chrome import Chrome
from engine.artifacts.browsers.edge import Edge


Plugin = namedtuple("Plugin", ["artifact", "category"])

CATEGORY_APPLICATION_EXECUTION = "Application Execution"
CATEGORY_FILE_FOLDER_OPENING = "File and Folder Opening"
CATEGORY_DELETED_ITEMS_FILE_EXISTENCE = "Deleted Items and File Existence"
CATEGORY_BROWSER_ACTIVITY = "Browser Activity"
CATEGORY_CLOUD_STORAGE = "Cloud Storage"
CATEGORY_ACCOUNT_USAGE = "Account Usage"
CATEGORY_NETWORK_ACTIVITY_PHYSICAL_LOCATION = "Network Activity"
CATEGORY_SYSTEM_INFORMATION = "System Information"
CATEGORY_EXTERNAL_DEVICE_USB_USAGE = "External Device And USB Usage"

PLUGINS = {
    "Chrome": Plugin(artifact=Chrome, category=CATEGORY_BROWSER_ACTIVITY),  # Browser
    "Edge": Plugin(artifact=Edge, category=CATEGORY_BROWSER_ACTIVITY),
    "RecycleBin": Plugin(artifact=RecycleBin, category=CATEGORY_DELETED_ITEMS_FILE_EXISTENCE),  # Windows
    "Prefetch": Plugin(artifact=Prefetch, category=CATEGORY_APPLICATION_EXECUTION),
    "JumpList": Plugin(artifact=JumpList, category=CATEGORY_FILE_FOLDER_OPENING),
    "LogonEvent": Plugin(artifact=ForensicEvent, category=CATEGORY_ACCOUNT_USAGE),  # EventLog
    "USB(EventLog)": Plugin(artifact=ForensicEvent, category=CATEGORY_EXTERNAL_DEVICE_USB_USAGE),
    "WLAN": Plugin(artifact=ForensicEvent, category=CATEGORY_NETWORK_ACTIVITY_PHYSICAL_LOCATION),
}