# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:26:26 2021

@author: peisa
"""

import process_micromet as pm
import data_paths as path
from utils import data_loader as dl, dataframe_manager as dfm
import pandas as pd

### Define stations

eddyCovStations =   ["Juvenile_NO","Juvenile_SE","Sapling","Neige","Regeneration_OPEC","Regeneration_CPEC"]

### Process eddy covariance stations - Batch process EddyPro

dates = {'start': '2026-06-10', 'end': '2026-11-09'}

# # Loop over stations
for iStation in eddyCovStations:
    # Ascii to eddypro
    pm.eddypro.run(iStation,path.asciiOutDir,path.eddyproConfigDir,
                   path.eddyproOutDir,dates)
