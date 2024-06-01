
# Imports:
import os
import torch # type: ignore
import numpy as np
import pandas as pd # type: ignore
import torchvision.models as models # type: ignore
import torchvision.transforms as transforms # type: ignore
from torch.utils.data import Dataset, DataLoader, random_split # type: ignore
from PIL import Image # type: ignore
from src.geoLifeCLEF.utils import construct_patch_path , set_seed, save_data_loaders
from src.geoLifeCLEF.entity.config_entity import DataLoadingandTransformationConfig
from src.geoLifeCLEF.constants import *



class DataLoadingandTransformation():
    def __init__(self,config:DataLoadingandTransformationConfig):
        self.config = config
        # self._prepare_data()
    
    def prepare_data(self):
        # Load training data
        train_landcover = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/LandCover/GLC24-PA-train-landcover.csv")
        train_solidgrids = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/SoilGrids/GLC24-PA-train-soilgrids.csv")
        train_humanfootprint = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/Human Footprint/GLC24-PA-train-human_footprint.csv")
        train_elevation = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/Elevation/GLC24-PA-train-elevation.csv")
        train_climate = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/Climate/Average 1981-2010/GLC24-PA-train-bioclimatic.csv")

        train_tab = train_climate.merge(train_elevation,on="surveyId").merge(train_humanfootprint,on="surveyId").merge(train_solidgrids,on="surveyId").merge(train_landcover,on="surveyId")
        global features  # Ensure features are accessible within Dataset classes
        features = list(train_tab.columns)[1:]
        train_tab = train_tab.fillna(-1).replace(np.inf, -1).replace(-np.inf, -1)

        # Load test data
        test_landcover = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/LandCover/GLC24-PA-test-landcover.csv")
        test_solidgrids = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/SoilGrids/GLC24-PA-test-soilgrids.csv")
        test_humanfootprint = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/Human Footprint/GLC24-PA-test-human_footprint.csv")
        test_elevation = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/Elevation/GLC24-PA-test-elevation.csv")
        test_climate = pd.read_csv(self.config.dataset+"/EnvironmentalRasters/EnvironmentalRasters/Climate/Average 1981-2010/GLC24-PA-test-bioclimatic.csv")

        test_tab = test_climate.merge(test_elevation,on="surveyId").merge(test_humanfootprint,on="surveyId").merge(test_solidgrids,on="surveyId").merge(test_landcover,on="surveyId")
        test_tab = test_tab.fillna(-1).replace(np.inf, -1).replace(-np.inf, -1)
        
        # Define transform
        batch_size = 128
        transform = transforms.Compose([
            transforms.ToTensor()
        ])
        
        # Load training metadata
        train_landsat_data_path = self.config.dataset+"/TimeSeries-Cubes/TimeSeries-Cubes/GLC24-PA-train-landsat_time_series/"
        train_bioclim_data_path = self.config.dataset+"/TimeSeries-Cubes/TimeSeries-Cubes/GLC24-PA-train-bioclimatic_monthly/"
        train_sentinel_data_path = self.config.dataset+"/PA_Train_SatellitePatches_RGB/pa_train_patches_rgb/"
        train_metadata_path = self.config.dataset+"/GLC24_PA_metadata_train.csv"

        train_metadata = pd.read_csv(train_metadata_path)
        seed = 151
        seed = set_seed(seed)

        # Create train datasets
        self.train_dataset = TrainDataset(train_tab, train_bioclim_data_path,train_landsat_data_path,train_sentinel_data_path, train_metadata, transform=transform)

        # Split train dataset into training and validation sets
        self.training_dataset, self.validation_dataset = random_split(self.train_dataset,
                                                                      [int(len(self.train_dataset) * 0.85), len(self.train_dataset) - int(len(self.train_dataset) * 0.85)],
                                                                      generator=torch.Generator().manual_seed(seed))

        # Create data loaders
        self.train_loader = DataLoader(self.training_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
        self.val_loader = DataLoader(self.validation_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

        # Load Test metadata
        test_landsat_data_path = self.config.dataset+"/TimeSeries-Cubes/TimeSeries-Cubes/GLC24-PA-test-landsat_time_series/"
        test_bioclim_data_path = self.config.dataset+"/TimeSeries-Cubes/TimeSeries-Cubes/GLC24-PA-test-bioclimatic_monthly/"
        test_sentinel_data_path = self.config.dataset+"/PA_Test_SatellitePatches_RGB/pa_test_patches_rgb/"
        test_metadata_path = self.config.dataset+"/GLC24_PA_metadata_test.csv"

        test_metadata = pd.read_csv(test_metadata_path)

        # create test dataset
        test_dataset = TestDataset(test_tab, test_bioclim_data_path, test_landsat_data_path, test_sentinel_data_path, test_metadata, transform=transform)
        self.test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
        
        # saving the output files
        status = save_data_loaders(self.config.save_data,self.train_loader,self.val_loader,self.test_loader)
        train_tab.to_csv(os.path.join(self.config.root_dir,"train_tab.csv"))
        test_tab.to_csv(os.path.join(self.config.root_dir,"test_tab.csv"))

        return status


    def get_data_loaders(self):
        return self.train_loader, self.val_loader, self.test_loader




class TrainDataset(Dataset):
    def __init__(self, tab, bioclim_data_dir, landsat_data_dir, sentinel_data_dir, metadata, transform=None):
        self.tab = tab
        self.transform = transform
        self.sentinel_transform = transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5, 0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5, 0.5)),
        ])
      
        self.bioclim_data_dir = bioclim_data_dir
        self.landsat_data_dir = landsat_data_dir
        self.sentinel_data_dir = sentinel_data_dir
        self.metadata = metadata
        self.metadata = self.metadata.dropna(subset="speciesId").reset_index(drop=True)
        self.metadata['speciesId'] = self.metadata['speciesId'].astype(int)
        self.label_dict = self.metadata.groupby('surveyId')['speciesId'].apply(list).to_dict()
        
        self.metadata = self.metadata.drop_duplicates(subset="surveyId").reset_index(drop=True)

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        
        survey_id = self.metadata.surveyId[idx]
        tab = torch.Tensor(self.tab[self.tab["surveyId"]==survey_id][features].values[0])
        landsat_sample = torch.nan_to_num(torch.load(os.path.join(self.landsat_data_dir, f"GLC24-PA-train-landsat-time-series_{survey_id}_cube.pt")))
        bioclim_sample = torch.nan_to_num(torch.load(os.path.join(self.bioclim_data_dir, f"GLC24-PA-train-bioclimatic_monthly_{survey_id}_cube.pt")))

        rgb_sample = np.array(Image.open(construct_patch_path(self.sentinel_data_dir, survey_id)))
        nir_sample = np.array(Image.open(construct_patch_path(self.sentinel_data_dir.replace("rgb", "nir").replace("RGB", "NIR"), survey_id)))
        sentinel_sample = np.concatenate((rgb_sample, nir_sample[...,None]), axis=2)

        species_ids = self.label_dict.get(survey_id, [])  # Get list of species IDs for the survey ID
        label = torch.zeros(num_classes)  # Initialize label tensor
        for species_id in species_ids:
            label_id = species_id
            label[label_id] = 1  # Set the corresponding class index to 1 for each species
        
        if isinstance(landsat_sample, torch.Tensor):
            landsat_sample = landsat_sample.permute(1, 2, 0)  # Change tensor shape from (C, H, W) to (H, W, C)
            landsat_sample = landsat_sample.numpy()  # Convert tensor to numpy array
            
        if isinstance(bioclim_sample, torch.Tensor):
            bioclim_sample = bioclim_sample.permute(1, 2, 0)  # Change tensor shape from (C, H, W) to (H, W, C)
            bioclim_sample = bioclim_sample.numpy()  # Convert tensor to numpy array   
        
        if self.transform:
            landsat_sample = self.transform(landsat_sample)
            bioclim_sample = self.transform(bioclim_sample)
            sentinel_sample = self.sentinel_transform(sentinel_sample)

        return tab, landsat_sample, bioclim_sample, sentinel_sample, label, survey_id


class TestDataset(TrainDataset):
    def __init__(self, tab, bioclim_data_dir, landsat_data_dir, sentinel_data_dir, metadata, transform=None):
        self.tab = tab
        self.transform = transform
        self.sentinel_transform = transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5, 0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5, 0.5)),
        ])
      
        self.bioclim_data_dir = bioclim_data_dir
        self.landsat_data_dir = landsat_data_dir
        self.sentinel_data_dir = sentinel_data_dir
        self.metadata = metadata
        
    def __getitem__(self, idx):
        
        survey_id = self.metadata.surveyId[idx]
        tab = torch.Tensor(self.tab[self.tab["surveyId"]==survey_id][features].values[0])
        landsat_sample = torch.nan_to_num(torch.load(os.path.join(self.landsat_data_dir, f"GLC24-PA-test-landsat_time_series_{survey_id}_cube.pt")))
        bioclim_sample = torch.nan_to_num(torch.load(os.path.join(self.bioclim_data_dir, f"GLC24-PA-test-bioclimatic_monthly_{survey_id}_cube.pt")))
        
        rgb_sample = np.array(Image.open(construct_patch_path(self.sentinel_data_dir, survey_id)))
        nir_sample = np.array(Image.open(construct_patch_path(self.sentinel_data_dir.replace("rgb", "nir").replace("RGB", "NIR"), survey_id)))
        sentinel_sample = np.concatenate((rgb_sample, nir_sample[...,None]), axis=2)

        if isinstance(landsat_sample, torch.Tensor):
            landsat_sample = landsat_sample.permute(1, 2, 0)  # Change tensor shape from (C, H, W) to (H, W, C)
            landsat_sample = landsat_sample.numpy()  # Convert tensor to numpy array
            
        if isinstance(bioclim_sample, torch.Tensor):
            bioclim_sample = bioclim_sample.permute(1, 2, 0)  # Change tensor shape from (C, H, W) to (H, W, C)
            bioclim_sample = bioclim_sample.numpy()  # Convert tensor to numpy array   
        
        if self.transform:
            landsat_sample = self.transform(landsat_sample)
            bioclim_sample = self.transform(bioclim_sample)
            sentinel_sample = self.sentinel_transform(sentinel_sample)

        return tab, landsat_sample, bioclim_sample, sentinel_sample, survey_id
    
