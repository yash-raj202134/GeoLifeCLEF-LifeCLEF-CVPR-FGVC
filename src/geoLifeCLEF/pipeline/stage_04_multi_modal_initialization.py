from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF import logger
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH,num_classes
from src.geoLifeCLEF.components.multi_modal_initialization import Multimodalinitialization
import torch
import os
from src.geoLifeCLEF import logger

STAGE_NAME = "Multi modal initialization Stage"

class multiModalInitializationipeline:
    def __init__(self) -> None:
        pass
    

    def run(self):
        config = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)
        multi_modal_initialization_config = config.get_initialize_multimodal_config()
        multi_modal = Multimodalinitialization(config=multi_modal_initialization_config)
        status = multi_modal.get_multimodal_ensemble_model()
        logger.info(status)




        
