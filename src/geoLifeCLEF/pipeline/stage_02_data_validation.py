
from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF.components.data_validation import DataValidation
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.geoLifeCLEF import logger


STAGE_NAME = "Data Validation Stage"

class DataValidationPipeline:
    def __init__(self):
        pass

    def run(self):
        
        config = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config = data_validation_config)
        status = data_validation.validate_all_folders_exist()
        logger.info(status)




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