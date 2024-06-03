from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF import logger
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH,num_classes
from src.geoLifeCLEF.components.multi_modal_initialization import Multimodalinitialization


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




        
# if __name__ == '__main__':
    # STAGE_NAME = "Multi modal initialization Stage"
#     # Run the multimodal initialization pipeline
#     try:
#         logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
#         pipeline = multiModalInitializationipeline()
#         pipeline.run()
#         logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logger.exception(e)
#         raise e