from src.geoLifeCLEF import logger
from src.geoLifeCLEF.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from src.geoLifeCLEF.pipeline.stage_02_data_validation import DataValidationPipeline


def main():
    # STAGE_NAME = "DATA INGESTION"
    # # logger.info("test log 2")
    # # Run the data ingestion pipeline
    # try:
    #     logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    #     pipeline = DataIngestionPipeline()
    #     pipeline.main()
    #     logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
    # except Exception as e:
    #     logger.exception(e)
    #     raise e
    


    STAGE_NAME = "DATA VALIDATION"   
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        pipeline = DataValidationPipeline()
        pipeline.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e





if __name__ =="__main__":
    main()
