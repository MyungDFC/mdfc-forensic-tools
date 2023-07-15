import argparse
from pathlib import Path

from app.engine.case_manager import CaseManager

ROOT_DIRECTORY_NAME = "_myungit"

# test code
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--artifact", default=None, help="artifact to parse", dest="artifact")
    parser.add_argument("-o", "--out", default=None, help="output directory", dest="out")

    args = parser.parse_args()
    
    if args.artifact:
        artifacts = args.artifact.split(',')
    else:
        artifacts = None

    if args.out:
        root_directory = Path(args.out) / ROOT_DIRECTORY_NAME
    else:
        temp_dir = Path.home() / "AppData" / "Local" / "Temp"
        root_directory = temp_dir / ROOT_DIRECTORY_NAME
    

    case = CaseManager(
        _artifacts=artifacts,
        root_directory=root_directory
    )
    case.parse_all()
    session = case.export_all()

    print(case.forensic_artifacts[0].result)