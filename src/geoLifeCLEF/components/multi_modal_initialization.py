# Imports
import os
import torch # type: ignore
import torch.nn as nn # type: ignore
import torchvision.models as models # type: ignore
import pandas as pd # type: ignore
from src.geoLifeCLEF.constants import *
from src.geoLifeCLEF.entity.config_entity import Multimodalconfig


class Multimodalinitialization():
    def __init__(self,config:Multimodalconfig) -> None:
        self.config = config
        pass

    def get_multimodal_ensemble_model(self):
        # Check if cuda is available
        device = torch.device("cpu")
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("DEVICE = CUDA")
        
        model = MultimodalEnsemble(num_classes=num_classes).to(device)
        torch.save(model.state_dict(),os.path.join(self.config.root_dir,"multimodal_ensemble_model.pth"))
        return True
    

class MultimodalEnsemble(nn.Module):
    def __init__(self,num_classes):

        super(MultimodalEnsemble, self).__init__()
        train_tab = pd.read_csv("artifacts/data_loader/train_tab.csv")
        features = list(train_tab.columns)[1:]
        self.tab_norm = nn.LayerNorm([len(features)])
        self.tab_model = nn.Sequential(nn.Linear(len(features),128),
                                       nn.ReLU(),
                                       nn.Linear(128,128),
                                       nn.ReLU(),
                                       nn.Linear(128,32),
                                      )
        
        self.landsat_norm = nn.LayerNorm([6,4,21])
        self.landsat_model = models.resnet18(weights=None)
        # Modify the first convolutional layer to accept 6 channels instead of 3
        self.landsat_model.conv1 = nn.Conv2d(6, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.landsat_model.maxpool = nn.Identity()
        
        self.bioclim_norm = nn.LayerNorm([4,19,12])
        self.bioclim_model = models.resnet18(weights=None)
        # Modify the first convolutional layer to accept 4 channels instead of 3
        self.bioclim_model.conv1 = nn.Conv2d(4, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bioclim_model.maxpool = nn.Identity()
        
        self.sentinel_model = models.swin_t(weights="IMAGENET1K_V1")
        # Modify the first layer to accept 4 channels instead of 3
        self.sentinel_model.features[0][0] = nn.Conv2d(4, 96, kernel_size=(4, 4), stride=(4, 4))
        self.sentinel_model.head = nn.Identity()
        
        self.ln0 = nn.LayerNorm(32)
        self.ln1 = nn.LayerNorm(1000)
        self.ln2 = nn.LayerNorm(1000)
        self.ln3 = nn.LayerNorm(768)
        
        self.fc1 = nn.Linear(2768+32, 1024)
        self.fc2 = nn.Linear(1024, num_classes)
        
        self.dropout = nn.Dropout(p=0.15)
        
    def forward(self, t, x, y, z):
        t = self.tab_norm(t)
        t = self.tab_model(t)
        t = self.ln0(t)
        t = self.dropout(t)
        
        x = self.landsat_norm(x)
        x = self.landsat_model(x)
        x = self.ln1(x)
        x = self.dropout(x)
        
        y = self.bioclim_norm(y)
        y = self.bioclim_model(y)
        y = self.ln2(y)
        y = self.dropout(y)
        
        z = self.sentinel_model(z)
        z = self.ln3(z)
        z = self.dropout(z)
        
        txyz = torch.cat((t, x, y, z), dim=1)
        
        txyz = self.fc1(txyz).relu()
        txyz = self.dropout(txyz)
        
        out = self.fc2(txyz)
        return out