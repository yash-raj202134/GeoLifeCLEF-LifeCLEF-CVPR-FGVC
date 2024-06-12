from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF.components.data_loading_and_transformation import DataLoadingandTransformation

from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.geoLifeCLEF import logger
import sys

STAGE_NAME = "Data loading and transformation Stage"


class DataLoadingandTransformationPipeline:
    def __init__(self) -> None:
        self.config_manager = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)

    def run(self):
        try:
            data_loading_and_transformation_config = self.config_manager.get_data_loader_and_transformer_config()
            data_loading_and_transformation = DataLoadingandTransformation(config=data_loading_and_transformation_config)
            status = data_loading_and_transformation.prepare_data()
            logger.info(status)
        except Exception as e:
            logger.exception(e,sys)
        



# if __name__ == '__main__':
#     # Run the data loading and transformation pipeline
#     try:
#         logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
#         pipeline = DataLoadingandTransformationPipeline()
#         pipeline.run()
#         logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logger.exception(e)
#         raise e