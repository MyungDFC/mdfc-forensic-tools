from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field

from app.engine.plugins import PLUGINS
from app.engine.forensic_artifact import ForensicArtifact

@dataclass(kw_only=True)
class CaseManager:
    _artifacts: list = field(default_factory=list)
    root_directory: Path
    forensic_artifacts: ForensicArtifact = field(default_factory=list)
    
    def __post_init__(self):
        for artifact, plugin in PLUGINS.items():
            ForensicArtifact, _ = plugin
            for artifact_entry in self._artifacts:
                if artifact == artifact_entry:
                    self.forensic_artifacts.append(
                        ForensicArtifact(artifact=artifact))

    @property
    def session_dir(self) -> Path:
        return self.root_directory
        
    @property
    def session_time(self) -> str:
        return datetime.now().strftime("%Y%m%dT%H%M%S")

    def parse_all(self) -> None:
        for entry in self.forensic_artifacts:
            entry.parse(descending=False)

    def export_all(self) -> list[dict]:
        result_files = []
        for entry in self.forensic_artifacts:
            output_dir = self.session_dir
            result_files.extend(
                entry.export(output_dir=output_dir)
            )
        return self._export_session(result_files=result_files)
            
    def _export_session(self, result_files: list) -> list[dict]:
        session = "[" + ",\n".join(result_files) + "]"
        session_file = self.session_dir / f"session_{self.session_time}.json"
        with open(session_file, 'w+', encoding='utf-8') as f:
            f.write(session)
            