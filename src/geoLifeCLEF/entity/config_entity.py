# Entity
from dataclasses import dataclass , field
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    type: str
    local_data_file: Path
    unzip_dir: Path

