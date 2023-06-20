from pathlib import Path
from datetime import timedelta, timezone
from typing import Generator
from dataclasses import dataclass, field

from app.engine.path_finder import ARTIFACT_PATH
from app.engine.util.ts import TimeStamp


@dataclass(kw_only=True)
class ForensicArtifact:
    artifact: str
    directory: list[str] = field(init=False)
    entry: str = field(init=False)
    result: dict = field(default_factory=dict)

    def __post_init__(self):
        self.directory, self.entry = ARTIFACT_PATH.get(self.artifact)
        
    @property
    def ts(self) -> TimeStamp:
        bias: timedelta = timedelta(hours=9)  # KST(+09:00)
        return TimeStamp(tzinfo=timezone(bias))

    def _iter_directory(self) -> Generator[Path, None, None]:
        for dir in self.directory:
            if dir.startswith("%ROOT%"):
                if (dir:=Path(dir.replace("%ROOT%", "C:"))).exists():
                    yield dir

            elif dir.startswith("%USER%"):
                if (dir:=Path(dir.replace("%USER%", str(Path.home())))).exists():
                    yield dir

    def _iter_entry(self, name: str = None, recurse: bool = False) -> Generator[Path, None, None]:
        if name == None:
            entry = self.entry
        else:
            entry = name
            
        for dir in self._iter_directory():
            if recurse == True:
                yield from dir.rglob(entry)
            else:
                yield from dir.glob(entry)

    def parse(self, descending: bool = False) -> None:
        """Parse artifact and update 'self.result' variable.

        Args:
            descending (bool, optional)
                - sort parsed results by descending/ascending order. Defaults to False.

        Returns: None

        # 'json.dumps' returned a string(<class 'str'>).
        # The JSON string can then be written to a file or
        # sent over a network connection.
        # It can be parsed back into a Python object using the 'json.loads()'.
        """
        raise NotImplementedError