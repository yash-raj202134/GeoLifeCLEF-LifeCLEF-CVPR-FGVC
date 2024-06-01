from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF.components.data_loading_and_transformation import DataLoadingandTransformation

from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.geoLifeCLEF import logger


STAGE_NAME = "Data loading and transformation Stage"


class DataLoadingandTransformationPipeline:
    def __init__(self) -> None:
        
        pass

    def run(self):
        config = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)
        data_loading_and_transformation_config = config.get_data_loader_and_transformer_config()
        data_loading_and_transformation = DataLoadingandTransformation(config=data_loading_and_transformation_config)
        data_loading_and_transformation.prepare_data()
        



# if __name__ == '__main__':
#     # Run the data validation pipeline
#     try:
#         logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
#         pipeline = DataLoadingandTransformationPipeline()
#         pipeline.run()
#         logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logger.exception(e)
#         raise e