import argparse
from dataclasses import dataclass, field

from app.engine.plugins import PLUGINS
from app.engine.forensic_artifact import ForensicArtifact


@dataclass(kw_only=True)
class CaseManager:
    _artifacts: list = field(default_factory=list)
    forensic_artifacts: ForensicArtifact = field(default_factory=list)
    
    def __post_init__(self):
        for artifact, plugin in PLUGINS.items():
            ForensicArtifact, _ = plugin
            for artifact_entry in self._artifacts:
                if artifact == artifact_entry:
                    self.forensic_artifacts.append(
                        ForensicArtifact(artifact=artifact))
            
    def parse_all(self) -> None:
        for entry in self.forensic_artifacts:
            entry.parse(descending=False)
        

# test code
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--artifact", default=None, help="artifact to parse", dest="artifact")

    args = parser.parse_args()
    
    if args.artifact:
        artifacts = args.artifact.split(',')
    else:
        artifacts = None
        
    case = CaseManager(_artifacts=artifacts)
    case.parse_all()
    print(case.forensic_artifacts[0].result)