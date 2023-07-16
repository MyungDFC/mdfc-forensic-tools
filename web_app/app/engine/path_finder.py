from collections import namedtuple


ArtifactPath = namedtuple("ArtifactPath", ["directory", "entry"])

## BROWSER
ARTIFACT_DIRECTORY_CHROME = [
    "%USER%/AppData/Local/Google/Chrome/User Data/Default",
    "%USER%/AppData/Local/Google/Chrome/continuousUpdates/User Data/Default",
    "%USER%/Local Settings/Application Data/Google/Chrome/User Data/Default",
    "%USER%/AppData/local/Google/Chromium/User Data/Default",
    "%USER%/snap/chromium/common/chromium/Default",
]
ARTIFACT_DIRECTORY_EDGE = [
    "%USER%/AppData/Local/Microsoft/Edge/User Data/Default",
    "%USER%/Library/Application Support/Microsoft Edge/Default",
]

## WINDOWS
ARTIFACT_DIRECTORY_RECYCLEBIN = [
    "%ROOT%/$recycle.bin",
]
ARTIFACT_DIRECTORY_PREFETCH = [
    "%ROOT%/windows/prefetch",
]
ARTIFACT_DIRECTORY_JUMPLIST = [
    "%USER%/AppData/Roaming/Microsoft/Windows/Recent/AutomaticDestinations",
    "%USER%/AppData/Roaming/Microsoft/Windows/Recent/CustomDestinations",
]
ARTIFACT_DIRECTORY_EVENTLOG = [
    "%ROOT%/Windows/System32/winevt/Logs"
]


ARTIFACT_PATH = {
    "Chrome": ArtifactPath(directory=ARTIFACT_DIRECTORY_CHROME, entry=None),  # Browser
    "Edge": ArtifactPath(directory=ARTIFACT_DIRECTORY_EDGE, entry=None),
    "RecycleBin": ArtifactPath(directory=ARTIFACT_DIRECTORY_RECYCLEBIN, entry="$I*"),  # Windows
    "Prefetch": ArtifactPath(directory=ARTIFACT_DIRECTORY_PREFETCH, entry="*.pf"),
    "JumpList": ArtifactPath(directory=ARTIFACT_DIRECTORY_JUMPLIST, entry="*.automaticDestinations-ms"),
    "LogonEvent": ArtifactPath(directory=ARTIFACT_DIRECTORY_EVENTLOG, entry=None),  # EventLog
    "USB(EventLog)": ArtifactPath(directory=ARTIFACT_DIRECTORY_EVENTLOG, entry=None),
    "WLAN": ArtifactPath(directory=ARTIFACT_DIRECTORY_EVENTLOG, entry=None),    
}