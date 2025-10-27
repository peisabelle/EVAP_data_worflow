# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:26:26 2021

@author: peisa
"""

import process_micromet as pm
from utils import data_loader as dl, dataframe_manager as dfm
import pandas as pd

### Define paths

eddyCovStations =   ["Juvenile_NO","Juvenile_SE","Sapling","Neige","Regeneration","Regeneration_CPEC"]

asciiOutDir         = "E:/EVAP/Data_EVAP/Raw_Data/ASCII/"
eddyproOutDir       = "E:/EVAP/Data_EVAP/Processed_Data/EddyPro_FM/"
eddyproConfigDir    = "./Config/EddyProConfig/"

### Process eddy covariance stations - Batch process EddyPro

dates = {'start': '2025-05-14', 'end': '2025-09-30'}

# # Loop over stations
for iStation in eddyCovStations:
    # Ascii to eddypro
    pm.eddypro.run(iStation,asciiOutDir,eddyproConfigDir,
                   eddyproOutDir,dates)

