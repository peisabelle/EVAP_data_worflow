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
study_years = {'2015': {'start': '2015-10-28', 'end': '2016-01-01'}, 
               '2016': {'start': '2016-01-01', 'end': '2017-01-01'},
               '2017': {'start': '2017-01-01', 'end': '2018-01-01'},
               '2018': {'start': '2018-01-01', 'end': '2019-01-01'},
               '2019': {'start': '2019-01-01', 'end': '2020-01-01'},
               '2020': {'start': '2020-01-01', 'end': '2020-10-01'}}


# Loop over study years
for iYear in study_years:
    dates = study_years[iYear]
    
    # Loop over stations
    for iStation in eddyCovStations:

        #Ascii to eddypro
        pm.batch_process_eddypro(iStation,asciiOutDir,eddyproConfigDir,eddyproOutDir,dates)