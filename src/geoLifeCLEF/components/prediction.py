
import os
import torch  # type: ignore
from tqdm import tqdm # type: ignore
from copy import deepcopy
import numpy as np
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import json
from src.geoLifeCLEF.entity.config_entity import ModelPredictionConfig
from src.geoLifeCLEF.constants import *
from src.geoLifeCLEF import logger
from src.geoLifeCLEF.utils import load_data_loaders
from src.geoLifeCLEF.components.multi_modal_initialization import MultimodalEnsemble


class ModelPrediction:
    def __init__(self,config:ModelPredictionConfig)->None:
        self.config = config
    
    def prediction(self):
        device = torch.device("cpu")

        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("DEVICE = CUDA")
        
        model = MultimodalEnsemble(num_classes).to(device)
        model.load_state_dict(torch.load(self.config.last_model,map_location=device))
        model.eval()

        with open(os.path.join(self.config.validation_result,"validation_result.json"), 'r') as file:
            validations = json.load(file)
        
        best_top_k = validations.get('best_top_k')

        with torch.no_grad():
            surveys = []
            top_k_indices = None
            _ , _ , test_loader = load_data_loaders("artifacts/data_loader/geolifeclef-2024")
            for batch_idx, (data0, data1, data2, data3, surveyID) in enumerate(tqdm(test_loader)):
                data0 = data0.to(device)
                data1 = data1.to(device)
                data2 = data2.to(device)
                data3 = data3.to(device)
                targets = targets.to(device)

                outputs = model(data0, data1, data2, data3)
                predictions = torch.sigmoid(outputs).cpu().numpy()

                # Sellect top-k values as predictions
                top_k = np.argsort(-predictions, axis=1)[:, :best_top_k] 
                if top_k_indices is None:
                    top_k_indices = top_k
                else:
                    top_k_indices = np.concatenate((top_k_indices, top_k), axis=0)

                surveys.extend(surveyID.cpu().numpy())
        

        ## Save prediction file!
        logger.info("saving the prediction file output as csv")
        data_concatenated = [' '.join(map(str, row)) for row in top_k_indices]

        pd.DataFrame({'surveyId': surveys,
                    'predictions': data_concatenated,
        }).to_csv("outputs/main_output.csv", index = False)

        return True
    






