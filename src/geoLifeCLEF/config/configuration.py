# Import necessary modules and classes
from pathlib import Path
from typing import List

from src.geoLifeCLEF.utils.common import read_yaml,create_directories

from src.geoLifeCLEF.entity.config_entity import (DataIngestionConfig,
                                                  DataValidationConfig,
                                                  DataLoadingandTransformationConfig,
                                                  Multimodalconfig,
                                                  ModelTrainerConfig)


class ConfigurationManager:
    def __init__(self, config_filepath: Path, params_filepath: Path = None):
        # Load configuration files
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath) if params_filepath else None

        # Create necessary directories
        # create_directories([self.config['artifacts_root']])

    def get_data_ingestion_config(self) -> List[DataIngestionConfig]:
        """
        Create and return a list of DataIngestionConfig instances based on the data_ingestion section
        in the config.yaml file.

        Returns:
            List[DataIngestionConfig]: A list of DataIngestionConfig instances.
        """
        data_ingestion = self.config['data_ingestion']
        root_dir = Path(data_ingestion['root_dir'])
        datasets_config = data_ingestion['datasets']

        # Create a list to hold DataIngestionConfig instances
        data_ingestion_configs = []

        # If datasets_config is a list, iterate through it, otherwise handle it as a single dataset.
        if isinstance(datasets_config, list):
            # Iterate through each dataset in the config file
            for dataset in datasets_config:
                # Create a DataIngestionConfig instance for each dataset
                data_ingestion_config = DataIngestionConfig(
                    root_dir=root_dir,
                    source_URL=dataset['source_URL'],
                    type=dataset['type'],
                    local_data_file=Path(dataset['local_data_file']),
                    unzip_dir=Path(dataset['unzip_dir'])
                )
                # Append the instance to the list
                data_ingestion_configs.append(data_ingestion_config)
        else:
            # Handle single dataset
            data_ingestion_config = DataIngestionConfig(
                root_dir=root_dir,
                source_URL=datasets_config['source_URL'],
                type=datasets_config['type'],
                local_data_file=Path(datasets_config['local_data_file']),
                unzip_dir=Path(datasets_config['unzip_dir'])
            )
            # Append the instance to the list
            data_ingestion_configs.append(data_ingestion_config)

        return data_ingestion_configs

    def get_data_validation_config(self)->DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            STATUS_FILE = config.STATUS_FILE,
            ALL_REQUIRED_FOLDERS = config.ALL_REQUIRED_FOLDERS,
            # ALL_REQUIRED_FOLDERS=[Path(folder) for folder in config['ALL_REQUIRED_FOLDERS']],
            # ALL_REQUIRED_FILES=[Path(file) for file in config['ALL_REQUIRED_FILES']]
            ALL_REQUIRED_FILES= config.ALL_REQUIRED_FILES

        )

        return data_validation_config
    
    def get_data_loader_and_transformer_config(self)-> DataLoadingandTransformationConfig:
        config = self.config.data_loading_and_transformation

        create_directories([config.root_dir])

        data_loader_and_transformer_config = DataLoadingandTransformationConfig(
            root_dir = config.root_dir,
            dataset = config.dataset,
            save_data= config.save_data
        )

        return data_loader_and_transformer_config
    
    def get_initialize_multimodal_config(self)-> Multimodalconfig:
        config = self.config.initialize_multimodal

        create_directories([config.root_dir])

        multi_modal_config = Multimodalconfig(
            root_dir = config.root_dir,
            data_loader_path = config.data_loader_path

        )
        return multi_modal_config
    

    def get_model_trainer_config(self)-> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.TrainingParameters

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            multimodal = config.multimodal,
            learning_rate = params.learning_rate,
            num_epochs = params.num_epochs,
            debug = params.debug,
            positive_weigh_factor =  params.positive_weigh_factor

        )
        return model_trainer_config

    



# class ConfigurationManager:
#     def __init__(self, config_filepath:Path, params_filepath:Path):
      
#         # Load configuration files
#         self.config = read_yaml(config_filepath)
#         self.params = read_yaml(params_filepath) if params_filepath else None

#         # Create necessary directories
#         # create_directories([self.config['artifacts_root']])

    
#     def get_data_ingestion_config(self) -> List[DataIngestionConfig]:
#         """
#         Create and return a list of DataIngestionConfig instances based on the data_ingestion section
#         in the config.yaml file.

#         Returns:
#             List[DataIngestionConfig]: A list of DataIngestionConfig instances.
#         """
#         data_ingestion = self.config['data_ingestion']
#         root_dir = Path(data_ingestion['root_dir'])
#         # datasets_config = data_ingestion_section['datasets']

#         # # Create directories for each dataset if they don't already exist
#         # for dataset in datasets_config:
#         #     create_directories([dataset['unzip_dir']])

#         # Create a list to hold DataIngestionConfig instances
#         data_ingestion_configs = []

#         # Iterate through each dataset in the config file
#         for dataset in data_ingestion['datasets']:
#             # Create a DataIngestionConfig instance for each dataset
#             data_ingestion_config = DataIngestionConfig(
#                 root_dir=root_dir,
#                 source_URL=dataset['source_URL'],
#                 type = dataset['type'],
#                 local_data_file=Path(dataset['local_data_file']),
#                 unzip_dir=Path(dataset['unzip_dir'])
#             )
#             # Append the instance to the list
#             data_ingestion_configs.append(data_ingestion_config)

#         return data_ingestion_configs

