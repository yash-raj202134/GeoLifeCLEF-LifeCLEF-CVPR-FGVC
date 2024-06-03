from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF import logger

from src.geoLifeCLEF.components.model_validation import ModelValidation
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH

STAGE_NAME = "Model validation Stage"

class ModelValidationPipeline():
    def __init__(self):
        pass

    def run(self):
        config = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)
        model_validation_config = config.get_model_validation_config()
        model_validation = ModelValidation(config = model_validation_config)
        status = model_validation.validate()
        
        logger.info(status)



# if __name__ == '__main__':
    # STAGE_NAME = "Model validation Stage"
#     # Run the model validation pipeline
#     try:
#         logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
#         pipeline = ModelValidationPipeline()
#         pipeline.run()
#         logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logger.exception(e)
#         raise e