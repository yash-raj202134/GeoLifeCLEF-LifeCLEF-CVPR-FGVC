
from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF.components.data_ingestion import DataIngestion

from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH
from src.geoLifeCLEF import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionPipeline:
    def __init__(self):
        """
        Initialize the DataIngestionPipeline.
        """
        self.config_manager = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)



    def main(self):
        """
        Main method to handle data ingestion.
        """
        try:
            data_ingestion_configs = self.config_manager.get_data_ingestion_config()

            for config in data_ingestion_configs:
                data_ingestion = DataIngestion(config=config)
                data_ingestion.download_datasets()
                data_ingestion.extract_datasets()


        except Exception as e:
            # Handle exceptions and log the error
            logger.exception("Error during data ingestion pipeline", exc_info=True)
            raise e


# if __name__ == '__main__':
#     # Run the data ingestion pipeline
#     try:
#         logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
#         pipeline = DataIngestionPipeline()
#         pipeline.main()
#         logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
#     except Exception as e:
#         logger.exception(e)
#         raise e