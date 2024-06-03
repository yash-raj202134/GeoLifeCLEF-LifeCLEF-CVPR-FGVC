from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF import logger

from src.geoLifeCLEF.components.model_trainer import ModelTrainer
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH,num_classes
import os

STAGE_NAME = "Model trainer Stage"


class ModelTrainerPipeline():

    def __init__(self)-> None:
        pass
    
    def run(self):
        config = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        status = model_trainer.train()
        logger.info(status)




# if __name__ == '__main__':
    # STAGE_NAME = "Model trainer Stage"
#     # Run the model trainer pipeline
#     try:
#         logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
#         pipeline = ModelTrainerPipeline()
#         pipeline.run()
#         logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logger.exception(e)
#         raise e