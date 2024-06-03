
import os
import torch  # type: ignore
from tqdm import tqdm # type: ignore
from copy import deepcopy
import numpy as np

from src.geoLifeCLEF.entity.config_entity import ModelTrainerConfig
from src.geoLifeCLEF.constants import *
from src.geoLifeCLEF import logger
from src.geoLifeCLEF.utils import load_data_loaders
from src.geoLifeCLEF.components.multi_modal_initialization import MultimodalEnsemble


class ModelTrainer():
    def __init__(self,config:ModelTrainerConfig) -> None:

        self.config = config

    
    def train(self):
        # Check if cuda is available
        device = torch.device("cpu")

        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("DEVICE = CUDA")

        model = MultimodalEnsemble(num_classes=num_classes).to(device)

        # print(type(self.config.learning_rate))
        # print(self.config.learning_rate)
        # print(float(self.config.learning_rate))

        model.load_state_dict(torch.load(self.config.multimodal, map_location=device))
        optimizer = torch.optim.AdamW(model.parameters(), lr = float(self.config.learning_rate))
        # model = torch.load(self.config.multimodal, map_location=device)
        print(type(model))
        # optimizer = torch.optim.AdamW(model.parameters(), lr=self.config.learning_rate)
        criterion = torch.nn.BCEWithLogitsLoss()


        logger.info(f"Training for {self.config.num_epochs} epochs started.")

        best_val = None
        best_model = deepcopy(model)
        train_loader,val_loader,test_loader = load_data_loaders("artifacts/data_loader/geolifeclef-2024")

        for epoch in range(self.config.num_epochs):
            # training 
            total = 0
            total_loss = 0
            model.train()
            for batch_idx, (data0, data1, data2, data3, targets, _) in enumerate(tqdm(train_loader)):
                data0 = data0.to(device)
                data1 = data1.to(device)
                data2 = data2.to(device)
                data3 = data3.to(device)
                targets = targets.to(device)


                        # Mixup
                if np.random.rand() < 0.4:
                    lam = torch.tensor(np.random.beta(0.4, 0.4)).to(device)
                    rand_index = torch.randperm(data0.size()[0]).to(device)
                    mixed_data0 = lam * data0 + (1 - lam) * data0[rand_index]
                    mixed_data1 = lam * data1 + (1 - lam) * data1[rand_index]
                    mixed_data2 = lam * data2 + (1 - lam) * data2[rand_index]
                    mixed_data3 = lam * data3 + (1 - lam) * data3[rand_index]
                    targets_a, targets_b = targets, targets[rand_index]
                    mixed_targets = lam * targets_a + (1 - lam) * targets_b
                    outputs = model(mixed_data0, mixed_data1, mixed_data2, mixed_data3)
                    loss = criterion(outputs, mixed_targets)
                else:
                    outputs = model(data0, data1, data2, data3)
                    loss = criterion(outputs, targets)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                total += data1.shape[0]
                total_loss += loss.item() * data1.shape[0]
                
                if DEBUG and batch_idx > 50:
                    break
            
            total_loss /= total

            if epoch % 2 == 0:
                # validation 
                vtotal = 0
                vtotal_loss = 0
                model.eval()
                with torch.no_grad():
                    for batch_idx, (data0, data1, data2, data3, targets, _) in enumerate(val_loader):
                        data0 = data0.to(device)
                        data1 = data1.to(device)
                        data2 = data2.to(device)
                        data3 = data3.to(device)
                        targets = targets.to(device)

                        outputs = model(data0, data1, data2, data3)

                        loss = criterion(outputs, targets)

                        vtotal += data1.shape[0]
                        vtotal_loss += loss.item() * data1.shape[0]

                        if DEBUG and batch_idx > 50:
                            break

                vtotal_loss /= vtotal

                print(f'Epoch {epoch} : train_loss {total_loss:.5f} | val_loss {vtotal_loss:.5f}')

                if best_val is None or vtotal_loss < best_val:
                    best_val = vtotal_loss
                    best_model = deepcopy(model)

        # Save the trained model
        model.eval()
        torch.save(model.state_dict(),os.path.join(self.config.root_dir,"last.pth"))
        best_model.eval()
        torch.save(best_model.state_dict(), os.path.join(self.config.root_dir,"best.pth"))

        return True




