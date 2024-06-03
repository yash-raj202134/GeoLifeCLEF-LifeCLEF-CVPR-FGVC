from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF import logger


from src.geoLifeCLEF.components.prediction import ModelPrediction
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH

STAGE_NAME = "Model prediction Stage"

class ModelPredictionPipeline():
    def __init__(self):
        pass

    def run(self):
        config = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)
        model_prediction_config = config.get_model_prediction_config()
        model_prediction = ModelPrediction(config = model_prediction_config)
        status = model_prediction.prediction()

        logger.info(status)

