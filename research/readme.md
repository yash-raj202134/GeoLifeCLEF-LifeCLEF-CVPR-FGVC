<!-- Readme file  -->
# Species Distribution Modeling Using Multimodal Data

## Project Overview

This project aims to develop a sophisticated multimodal model capable of predicting species distribution across diverse geographical regions using a variety of environmental data sources. The model leverages tabular data, Landsat cubes, bioclimatic cubes, and Sentinel image patches, integrating these disparate modalities through a carefully designed neural network architecture.

## Table of Contents
1. [Introduction](#introduction)
2. [Dataset](#dataset)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Model Architecture](#model-architecture)
6. [Training and Evaluation](#training-and-evaluation)
7. [Challenges](#challenges)
8. [Conclusion](#conclusion)
9. [Future Scope](#future-scope)
10. [Contributing](#contributing)
11. [License](#license)

## Introduction

The goal of this project is to predict species distribution using a multimodal approach that integrates multiple data sources. This approach helps capture the complex environmental factors influencing species distribution more effectively than single-modality models.

## Dataset

The project utilizes several datasets, including:

1. **Satellite Image Patches**
   - RGB and NIR patches centered at the observation geolocation.
   - Format: 128x128 JPEG images.
   - Resolution: 10 meters per pixel.
   - Source: Sentinel2 remote sensing data.

2. **Satellite Time Series**
   - Time series of satellite median point values over each season since the winter of 1999 for six satellite bands (R, G, B, NIR, SWIR1, and SWIR2).
   - Format: CSV files and 3D tensors.
   - Resolution: 30 meters per pixel.
   - Source: Landsat remote sensing data.

3. **Monthly Climatic Rasters**
   - Climatic variables computed monthly (mean, minimum and maximum temperature, and total precipitation) from January 2000 to December 2019.
   - Format: CSV files and 3D tensors.
   - Resolution: 1 kilometer.
   - Source: Chelsa.

4. **Environmental Rasters**
   - Additional environmental data such as GeoTIFF rasters and scalar values (e.g., bioclimatic, soil, elevation, land cover, and human footprint).
   - Source: Various environmental datasets.

## Installation

To set up the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yash-raj202134/GeoLifeCLEF-LifeCLEF-CVPR-FGVC.git
   ```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the main script:
```bash
python main.py
```
## Usage

The main script will automatically start ingesting the data and start executing the pipelines one by one.

In order to execute the pipelines manually navigate to the pipeline folder.
```bash
cd src/geoLifeCLEF/pipeline
```

## Model Architecture
The multimodal model integrates multiple data sources to enhance species classification accuracy. Key components include:

- **Tabular Data Encoder**: Processes tabular features through a feed-forward neural network.
- **Landsat Data Encoder**: Utilizes a modified ResNet18 architecture for Landsat cubes.
- **Bioclimatic Data Encoder**: Adopts a modified ResNet18 for bioclimatic data.
- **Sentinel Image Encoder**: Employs a modified Swin Transformer (Swin-v2-t) for Sentinel image patches.
- **Fusion Layer**: Concatenates outputs from all encoders for final classification.

## Training and Evaluation
The model is trained using the AdamW optimizer and Binary Cross Entropy (BCE) loss function. Key steps include:

- Data preprocessing
- Forward propagation
- Loss calculation
- Backpropagation and optimization
- Hyperparameters include a learning rate of 3e-4, 3 epochs for debugging, and 15 epochs for full training. The model's performance is evaluated using metrics such as F1-score and validation loss.

## Challenges
Several challenges were encountered during the project, including:

- Multi-Label Learning from Single Positive Labels: Requires sophisticated techniques to generalize well.
- Strong Class Imbalance: Necessitates specialized loss functions and resampling techniques.
- Multi-Modal Learning: Ensuring effective integration of diverse data types.
- Large-Scale Data Handling: Requires substantial computational resources and efficient data management strategies.
## Conclusion
This project demonstrates the potential of a multimodal approach for species distribution modeling, integrating diverse environmental data sources to achieve high predictive accuracy. The insights gained provide a solid foundation for future research in this area.

## Future Scope
Future work can focus on:

Improvement in Model Architecture and Techniques
- Advanced deep learning architectures
- ncorporation of attention mechanisms
- Ensemble methods
- Enhanced Data Utilization
- Inclusion of additional data modalities
- Longitudinal data analysis
- Higher resolution data
- Scalability and Real-Time Applications
- Scalability to larger datasets
- Real-time species distribution monitoring
- Improved Model Interpretability and User Interfaces
- Model interpretability
- User-friendly interfaces
- Application to Conservation and Management
- Conservation planning and policy making
- Collaboration with ecologists and conservationists

## Contributing
We welcome contributions to improve this project! Please fork the repository and submit a pull request. For major changes, please open an issue to discuss what you would like to change.
for further discussion feel free to contact me @[ yashraj3376@gmail.com ]

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
