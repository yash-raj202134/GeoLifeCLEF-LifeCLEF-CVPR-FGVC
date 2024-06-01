import os
import torch
import numpy as np
import pickle

def construct_patch_path(data_path, survey_id):
    """Construct the patch file path based on plot_id as './CD/AB/XXXXABCD.jpeg'"""
    path = data_path
    for d in (str(survey_id)[-2:], str(survey_id)[-4:-2]):
        path = os.path.join(path, d)

    path = os.path.join(path, f"{survey_id}.jpeg")

    return path

def set_seed(seed):
    # Set seed for Python's built-in random number generator
    torch.manual_seed(seed)
    # Set seed for numpy
    np.random.seed(seed)
    # Set seed for CUDA if available
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        # Set cuDNN's random number generator seed for deterministic behavior
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    
    return seed


def save_data_loaders(path,train_loader,val_loader,test_loader):
        with open(path, 'wb') as f:
            pickle.dump({
                'train_loader': train_loader,
                'val_loader': val_loader,
                'test_loader': test_loader
            }, f)


def load_data_loaders(path):
    with open(path, 'rb') as f:
        loaders = pickle.load(f)
        train_loader = loaders['train_loader']
        val_loader = loaders['val_loader']
        test_loader = loaders['test_loader']
    
    return train_loader,val_loader,test_loader