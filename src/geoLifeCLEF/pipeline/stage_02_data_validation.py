
from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF.components.data_validation import DataValidation
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.geoLifeCLEF import logger
import sys

STAGE_NAME = "Data Validation Stage"

class DataValidationPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)

    def run(self):
        try:
            data_validation_config = self.config_manager.get_data_validation_config()
            data_validation = DataValidation(config = data_validation_config)
            status = data_validation.validate_all_folders_exist()
            logger.info(status)

        except Exception as e:
            logger.exception(e,sys)




# if __name__ == '__main__':
#     # Run the data validation pipeline
#     try:
#         logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
#         pipeline = DataValidationPipeline()
#         pipeline.run()
#         logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logger.exception(e)
#         raise e