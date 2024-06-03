
import os
import torch  # type: ignore
from tqdm import tqdm # type: ignore
from copy import deepcopy
import numpy as np
import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import json
from src.geoLifeCLEF.entity.config_entity import ModelValidationConfig
from src.geoLifeCLEF.constants import *
from src.geoLifeCLEF import logger
from src.geoLifeCLEF.utils import load_data_loaders
from src.geoLifeCLEF.components.multi_modal_initialization import MultimodalEnsemble




class ModelValidation():
    
    def __init__(self,config:ModelValidationConfig) -> None:
        self.config = config


    def eval_pred(self,pred,gt):

        list_f1 = []
        for p,g in zip(pred,gt):
            sp = set(p)
            sg = set(g)
            TP = len(list(sp.intersection(sg)))
            FP = len(list(sp-sg))
            FN = len(list(sg-sp))
            f1 = TP/(TP + (FP+FN)/2)
            list_f1.append(f1)

        return np.mean(list_f1)
    

    
    def validate(self):
        # Check if cuda is available
        device = torch.device("cpu")

        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("DEVICE = CUDA")

        model = MultimodalEnsemble(num_classes).to(device)
        model.load_state_dict(torch.load(self.config.last_model,map_location=device))
        model.eval()

        train_loader,val_loader,test_loader = load_data_loaders("artifacts/data_loader/geolifeclef-2024")

        with torch.no_grad():
            all_predictions = []
            all_surveyID = []
            for batch_idx, (data0, data1, data2, data3, targets, surveyID) in enumerate(tqdm(val_loader)):
                data0 = data0.to(device)
                data1 = data1.to(device)
                data2 = data2.to(device)
                data3 = data3.to(device)
                targets = targets.to(device)

                outputs = model(data0, data1, data2, data3)
                predictions = torch.sigmoid(outputs).cpu().numpy()

                all_predictions.extend(predictions)
                all_surveyID.extend(surveyID.numpy())
                
        all_predictions = np.array(all_predictions)
        all_surveyID = np.array(all_surveyID)


        train_pa = pd.read_csv("artifacts/data_ingestion/geolifeclef-2024/GLC24_PA_metadata_train.csv")
        gt = []

        for surveyId in tqdm(all_surveyID):
            gt.append(train_pa[train_pa["surveyId"]==surveyId].speciesId.values.astype(int).tolist())
        

        pred_sorted = np.argsort(-all_predictions, axis=1)
        best_top_k = 1
        best_score = 0
        f1_scores = []
        for k in tqdm(range(1,100)):
            top_k = pred_sorted[:, :k].tolist()
            score = self.eval_pred(top_k,gt)
            f1_scores.append(score)
            if score > best_score :
                best_score = score
                best_top_k = k
                
        print(f'best score {best_score:.5f} @ top {best_top_k}')

        validations = {
            'best_score' : best_score,
            'best_top_k' : best_top_k,
        }
        with open(os.path.join(self.config.root_dir, "validation_result.json"), 'w') as file:
            json.dump(validations, file)



        # saving the Plots results

        # Plot F1 score vs. top-k
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, 100), f1_scores, marker='o')
        plt.xlabel('Top-K')
        plt.ylabel('F1 Score')
        plt.title('F1 Score vs. Top-K')
        plt.savefig(os.path.join(self.config.root_dir, 'f1_score_vs_top_k.png'))


        return True
    