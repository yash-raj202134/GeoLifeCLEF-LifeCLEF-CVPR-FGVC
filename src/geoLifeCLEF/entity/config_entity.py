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


@dataclass
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    ALL_REQUIRED_FOLDERS: List[Path]
    ALL_REQUIRED_FILES: List[Path]


@dataclass
class DataLoadingandTransformationConfig:
    root_dir: Path
    dataset: Path
    save_data: Path

@dataclass
class Multimodalconfig:
    root_dir : Path
    data_loader_path: Path


@dataclass
class ModelTrainerConfig:
    root_dir: Path
    multimodal: str

    # parameters
    learning_rate: float
    num_epochs: int
    debug: bool
    positive_weigh_factor: float
