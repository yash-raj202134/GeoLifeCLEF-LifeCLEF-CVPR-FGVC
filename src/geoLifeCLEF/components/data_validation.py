import os 
import sys
from src.geoLifeCLEF import logger

from src.geoLifeCLEF.entity.config_entity import DataValidationConfig



class DataValidation:
    def __init__(self,config:DataValidationConfig) -> None:
        self.config = config
        
    
    def validate_all_folders_exist(self)-> bool:
        try:
            validation_status = True

            # Validate folders
            for folder in self.config.ALL_REQUIRED_FOLDERS:
                if not os.path.exists(folder):

                    validation_status = False
                    break

            # Validate files
            if validation_status:
                for file in self.config.ALL_REQUIRED_FILES:
                    if not os.path.isfile(file):
                        validation_status = False
                        break

            with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Validation status: {validation_status}")
                
            return validation_status
        
        except Exception as e:
            raise logger.exception(e,sys)