import argparse
from dataclasses import dataclass, field

from engine.plugins import PLUGINS
from engine.forensic_artifact import ForensicArtifact


@dataclass(kw_only=True)
class CaseManager:
    _artifacts: list = field(default_factory=list)
    forensic_artifact: ForensicArtifact = field(default_factory=list)
    
    def __post_init__(self):
        for artifact, plugin in PLUGINS.items():
            ForensicArtifact, _ = plugin
            for artifact_entry in self._artifacts:
                if artifact == artifact_entry:
                    self.forensic_artifact.append(
                        ForensicArtifact(artifact=artifact))
            
    def parse_all(self) -> None:
        for entry in self.forensic_artifact:
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
    print(case.forensic_artifact[0].result)