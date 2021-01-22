import pandas as pd
import process_micromet as pm

# TODO add a row for units
# TODO add a fluxnet name format
# TODO consider storage effects between instruments and ground
# TODO deal with the periods where turbulent fluxes largely violated the energy budget (i.e., H+λE > 5Rn) were discarded
# TODO Cap shortwave downwelling radiation with maximum theoretical values calculated following -- Whiteman and Allwine (1986).
# TODO Cap humidity values using temperature-dependent relations
# TODO Account for energy storage in soil above flux plates to include it in G
# TODO Acconut for LE and H storage between ground and flux instrument ? How without several temperature sensors ?
# TODO implement energy balance correction
# TODO add script to average/sum minute to half-hour for slow data
# TODO create script to merge and interpolate governement stations data
# TODO add fix_timelapse to workflow
# TODO check if units are converted when needed
# TODO create precipitation series precip_FM
# TODO create theoretical radiation series and calculate diffuse fraction

### Define paths

allStations     = ["Sapling","Juvenile_NO","Juvenile_SE","Canopy","Trees","Juvenile_Geonor"]
eddyCovStations = ["Sapling","Juvenile_NO","Juvenile_SE","Canopy"]
gapfilledStation = ["Sapling","Juvenile_NO","Juvenile_SE"]

rawFileDir          = "E:/EVAP/Data_EVAP/Raw_Data/Binary/"
asciiOutDir         = "E:/EVAP/Data_EVAP/Raw_Data/Test/"
eddyproOutDir       = "E:/EVAP/Data_EVAP/Processed_Data/EddyPro_FM"
eddyproConfigDir    = "./Config/EddyProConfig/"
externalDataDir     = "D:/E/Ro2_micromet_raw_data/Data/External_data/"
varNameExcelTab     = "./Resources/FMVariableDescription.xlsx"
mergedCsvOutDir     = "E:/EVAP/Data_EVAP/Processed_Data/Merged_CSV/"
gapfillConfigDir    = "./Config/GapFillingConfig/"

dates = {'start':'2015-10-22','end':'2016-01-01'}

### Process external data

# Merge Tree Heat thermistors


# Merge ECCC station data


# Merge MDDELCC station data


### Process eddy covariance stations
for iStation in allStations:

    # Binary to ascii
    pm.convert_CSbinary_to_csv(iStation,rawFileDir,asciiOutDir)

    # Merge slow data
    slow_df = pm.merge_slow_csv(iStation,asciiOutDir)

    # Rename and trim slow variables
    slow_df = pm.rename_trim_vars(iStation,varNameExcelTab,slow_df,'cs')

    if iStation in eddyCovStations:

        # Ascii to eddypro
        pm.batch_process_eddypro(iStation,asciiOutDir,eddyproConfigDir,eddyproOutDir,dates)

        # Load eddypro file
        eddy_df = pm.load_eddypro_file(iStation,eddyproOutDir)

        # Rename and trim eddy variables
        eddy_df = pm.rename_trim_vars(iStation,varNameExcelTab,eddy_df,'eddypro')

        # Merge slow and eddy data
        df = pm.merge_slow_csv_and_eddypro(iStation, slow_df, eddy_df, mergedCsvOutDir)

        # Save to csv
        df.to_csv(mergedCsvOutDir+iStation+'.csv', index=False)

    else:

        # Save to csv
        slow_df.to_csv(mergedCsvOutDir+iStation+'.csv', index=False)


for iStation in gapfilledStation:

    # Merge the eddy covariance together (water/forest), or simply load data
    df = pm.merge_eddycov_stations(iStation, mergedCsvOutDir, varNameExcelTab)

    # Handle special cases and errors
    df = pm.handle_exception(iStation, df,mergedCsvOutDir, varNameExcelTab)

    # # Perform gap filling
    df = pm.gap_fill(iStation,df,mergedCsvOutDir,gapfillConfigDir)

    # # Save to csv
    df.to_csv(mergedCsvOutDir+iStation+'_gf.csv')

