from src.geoLifeCLEF import logger
from src.geoLifeCLEF.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from src.geoLifeCLEF.pipeline.stage_02_data_validation import DataValidationPipeline
from src.geoLifeCLEF.pipeline.stage_03_data_loading_and_transformation import DataLoadingandTransformationPipeline
from src.geoLifeCLEF.pipeline.stage_04_multi_modal_initialization import multiModalInitializationipeline
from src.geoLifeCLEF.pipeline.stage_05_model_training import ModelTrainerPipeline
from src.geoLifeCLEF.utils import load_data_loaders

def main():

    # STAGE_NAME = "DATA INGESTION"
    # logger.info("test log 2")
    # Run the data ingestion pipeline
    # try:
    #     logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    #     pipeline = DataIngestionPipeline()
    #     pipeline.run()
    #     logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
    # except Exception as e:
    #     logger.exception(e)
    #     raise e
    

    # STAGE_NAME = "DATA VALIDATION"   
    # try:
    #     logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    #     pipeline = DataValidationPipeline()
    #     pipeline.run()
    #     logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
    # except Exception as e:
    #     logger.exception(e)
    #     raise e


    # STAGE_NAME = "DATA LOADING STAGE"
    # try:
    #     logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    #     pipeline = DataLoadingandTransformationPipeline()
    #     pipeline.run()
    #     logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
    # except Exception as e:
    #     logger.exception(e)
    #     raise e
    

    # STAGE_NAME = "MULTI MODAL INITIALIZATION STAGE"
    # try:
    #     logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    #     pipeline = multiModalInitializationipeline()
    #     pipeline.run()
    #     logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
    # except Exception as e:
    #     logger.exception(e)
    #     raise e


    STAGE_NAME = "MODEL TRAINER STAGE"
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        pipeline = ModelTrainerPipeline()
        pipeline.run()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
    pass





if __name__ =="__main__":

    main()
    # train_loader,val_loader,test_loader = load_data_loaders("artifacts/data_loader/geolifeclef-2024")
    # print(type(test_loader))

