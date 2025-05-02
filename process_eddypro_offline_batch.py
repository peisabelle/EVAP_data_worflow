# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:26:26 2021

@author: peisa
"""

import process_micromet as pm
from utils import data_loader as dl, dataframe_manager as dfm
import pandas as pd

### Define paths

eddyCovStations =   ["Juvenile_NO","Juvenile_SE","Sapling","Regeneration","Regeneration_CPEC","Canopy","Neige"]

asciiOutDir         = "F:/peisa/FM_Hydromet/Raw_Data/CSV/"
eddyproOutDir       = "F:/peisa/FM_Hydromet/EddyPro/"
eddyproConfigDir    = "./Config/EddyProConfig/"

### Process eddy covariance stations - Batch process EddyPro

dates = {'start': '2024-04-10', 'end': '2025-04-02'}

# # Loop over stations
for iStation in eddyCovStations:
    # Ascii to eddypro
    pm.eddypro.run(iStation,asciiOutDir,eddyproConfigDir,
                   eddyproOutDir,dates)

