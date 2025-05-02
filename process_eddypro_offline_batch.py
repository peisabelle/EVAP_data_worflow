# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:26:26 2021

@author: peisa
"""

import pandas as pd
import process_micromet as pm

### Define paths

eddyCovStations = ["Juvenile_NO","Juvenile_SE","Sapling"]

asciiOutDir         = "E:/EVAP/Data_EVAP/Raw_Data/ASCII/"
eddyproOutDir       = "E:/EVAP/Data_EVAP/Processed_Data/EddyPro_FM/"
eddyproConfigDir    = "./Config/EddyProConfig/No_Filter/"

### Process eddy covariance stations - Batch process EddyPro

dates = {'start': '2024-04-10', 'end': '2025-04-02'}

# # Loop over stations
for iStation in eddyCovStations:
    # Ascii to eddypro
    pm.eddypro.run(iStation,asciiOutDir,eddyproConfigDir,
                   eddyproOutDir,dates)

