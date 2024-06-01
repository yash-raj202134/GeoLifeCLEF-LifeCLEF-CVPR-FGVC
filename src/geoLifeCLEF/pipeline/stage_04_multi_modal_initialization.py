from src.geoLifeCLEF.config.configuration import ConfigurationManager
from src.geoLifeCLEF import logger
from src.geoLifeCLEF.constants import CONFIG_FILE_PATH,PARAMS_FILE_PATH,num_classes
from src.geoLifeCLEF.components.multi_modal_initialization import MultimodalEnsemble
import torch
import os

STAGE_NAME = "Multi modal initialization Stage"

class multiModalInitializationipeline:
    def __init__(self) -> None:
        pass
    

    def run(self):
        config = ConfigurationManager(config_filepath=CONFIG_FILE_PATH,params_filepath=PARAMS_FILE_PATH)
        multi_modal_initialization_config = config.get_initialize_multimodal_config()

        # Check if cuda is available
        device = torch.device("cpu")
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("DEVICE = CUDA")
        
        multi_modal = MultimodalEnsemble(config=multi_modal_initialization_config,num_classes=num_classes).to(device)
        
        # saving the model
        torch.save(multi_modal.state_dict(),os.path.join(multi_modal_initialization_config.root_dir,"multimodal_ensemble_model.pth"))

        
