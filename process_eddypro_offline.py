# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:26:26 2021

@author: peisa
"""

import pandas as pd
import process_micromet as pm

### Define paths

allStations     = ["Sapling","Juvenile_NO","Juvenile_SE","Canopy","CanopyCR5000"]
eddyCovStations = ["Sapling","Juvenile_NO","Juvenile_SE","Canopy"]

asciiOutDir         = "E:/EVAP/Data_EVAP/Raw_Data/ASCII/"
eddyproOutDir       = "E:/EVAP/Data_EVAP/Processed_Data/EddyPro_FM/"
eddyproConfigDir    = "./Config/EddyProConfig/"

### Process eddy covariance stations - Batch process EddyPro
dates = {'start':'2015-10-28','end':'2016-01-01'}

# Ascii to eddypro
for iStation in allStations:
    
    if iStation in eddyCovStations:

        #Ascii to eddypro
        pm.batch_process_eddypro('Sapling',asciiOutDir,eddyproConfigDir,eddyproOutDir,dates)