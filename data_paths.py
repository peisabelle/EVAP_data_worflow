# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 11:26:23 2025

@author: ANTHI182
"""
from pathlib import Path

rawFileDir          = Path("F:\peisa\FM_Hydromet\Raw_Data\Binary")
reanalysisDir       = Path("D:/Ro2_micromet_raw_data/Data/Reanalysis/")
asciiOutDir         = Path("F:\peisa\FM_Hydromet\Raw_Data\CSV")
miscDataDir         = Path("D:/Ro2_micromet_raw_data/Data/Misc/")
eddyproOutDir       = Path("F:\peisa\FM_Hydromet\Processed_Data\EddyPro")
intermediateOutDir  = Path("D:/Ro2_micromet_processed_data/Data/Intermediate/")
finalOutDir         = Path("D:/Ro2_micromet_processed_data/Final_output/")
varNameExcelSheet   = Path("./Resources/Variable_description_full.xlsx")
eddyproConfigDir    = Path("./Config/EddyProConfig/")
gapfillConfigDir    = Path("./Config/GapFillingConfig/")
filterConfigDir     = Path("./Config/Filtering/")
gasAnalyzerConfigDir    = Path("./Config/Gas_analyzer/")
reanalysisConfigDir = Path("./Config/Reanalysis/")