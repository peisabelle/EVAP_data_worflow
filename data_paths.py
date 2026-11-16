# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 11:26:23 2025

@author: ANTHI182
"""
from pathlib import Path

rawFileDir          = Path("D:/Ro2_micromet_raw_data/Data/Raw_data/Data")
reanalysisDir       = Path("D:/Ro2_micromet_raw_data/Data/Reanalysis/")
asciiOutDir         = Path("E:/EVAP/Data_EVAP/Raw_Data/ASCII/")
miscDataDir         = Path("D:/Ro2_micromet_raw_data/Data/Misc/")
eddyproOutDir       = Path("E:/EVAP/Data_EVAP/Processed_Data/EddyPro_FM/")
intermediateOutDir  = Path("D:/Ro2_micromet_processed_data/Data/Intermediate/")
finalOutDir         = Path("D:/Ro2_micromet_processed_data/Final_output/")
varNameExcelSheet   = Path("./Resources/Variable_description_full.xlsx")
eddyproConfigDir    = Path("./Config/EddyProConfig/")
gapfillConfigDir    = Path("./Config/GapFillingConfig/")
filterConfigDir     = Path("./Config/Filtering/")
gasAnalyzerConfigDir    = Path("./Config/Gas_analyzer/")
reanalysisConfigDir = Path("./Config/Reanalysis/")