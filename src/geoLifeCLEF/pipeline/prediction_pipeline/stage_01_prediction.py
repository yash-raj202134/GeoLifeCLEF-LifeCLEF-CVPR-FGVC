from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF import logger


from src.geoLifeCLEF.components.prediction import ModelPrediction
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
import sys

STAGE_NAME = "Model prediction Stage"

class ModelPredictionPipeline():
    def __init__(self):
        self.config = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)

    def run(self):
        try:

            model_prediction_config = self.config.get_model_prediction_config()
            model_prediction = ModelPrediction(config = model_prediction_config)
            status = model_prediction.prediction()

            logger.info(status)
        except Exception as e:
            logger.exception(e,sys)



# if __name__ == '__main__':
    # STAGE_NAME = "Model prediction Stage"
#     try:
#         logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
#         pipeline = ModelPredictionPipeline()
#         pipeline.run()
#         logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logger.exception(e)
#         raise e