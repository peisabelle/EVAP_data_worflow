import pandas as pd
from joblib import Parallel, delayed
import process_micromet as pm

# TODO deal with start/end dates
# TODO add a row for units
# TODO 360-wind_sonic_dir for berge
# TODO clean all data
# TODO clean doc

### Define paths

# allStations     = ["Berge","Foret_ouest","Foret_est","Foret_sol","Reservoir"]
# eddyCovStations = ["Berge","Foret_ouest","Foret_est","Reservoir"]
# gapfilledStation = ["Berge","Foret_ouest","Reservoir"]

rawFileDir          = "D:/E/Ro2_micromet_raw_data/Data"
asciiOutDir         = "D:/E/Ro2_micormet_processed_data/Ascii_data/"
eddyproOutDir       = "D:/E/Ro2_micormet_processed_data/Eddypro_data/"
eddyproConfigDir    = "D:/E/Ro2_data_worflow/Config/EddyProConfig/"
mergedCsvOutDir     = "D:/E/Ro2_micormet_processed_data/Merged_csv/"
gapfillConfigDir    = "D:/E/Ro2_data_worflow/Config/GapFillingConfig/"
varNameExcelTab     = "D:/E/Ro2_data_worflow/Resources/EmpreinteVariableDescription.xlsx"

dates = {'start':'2018-06-01','end':'2020-02-01'}

### Temporary stuff for tests
allStations = ["Foret_ouest","Berge"]
eddyCovStations  = ["Foret_ouest"]
gapfilledStation = ["Foret_ouest"]


def parallel_function_1(iStation, rawFileDir, asciiOutDir, eddyproOutDir,
                        eddyproConfigDir, mergedCsvOutDir, gapfillConfigDir,
                        varNameExcelTab):

    # Binary to ascii
    pm.convert_CSbinary_to_csv(iStation,rawFileDir,asciiOutDir)

    # Merge slow data
    slow_df = pm.merge_slow_csv(iStation,asciiOutDir)

    # Rename and trim slow variables
    slow_df = pm.rename_trim_vars(iStation,varNameExcelTab,slow_df,'cs')

    if iStation in eddyCovStations:

        # # Ascii to eddypro
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


def parallel_function_2(iStation, mergedCsvOutDir, gapfillConfigDir):

    df = pd.read_csv(mergedCsvOutDir+iStation+'.csv', low_memory=False)

    # Handle special cases and errors
    df = pm.handle_exception(iStation, df,mergedCsvOutDir)

    # Perform gap filling
    df = pm.gap_fill(iStation,df,mergedCsvOutDir,gapfillConfigDir)

    # Save to csv
    df.to_csv(mergedCsvOutDir+iStation+'_gf.csv')



########### Process stations ############

# # Merge Hobo TidBit thermistors
# pm.merge_thermistors(dates, rawFileDir, mergedCsvOutDir)

Parallel(n_jobs=len(allStations))(delayed(parallel_function_1)(
        iStation, rawFileDir, asciiOutDir, eddyproOutDir, eddyproConfigDir,
        mergedCsvOutDir, gapfillConfigDir, varNameExcelTab)for iStation in allStations)

Parallel(n_jobs=len(gapfilledStation))(delayed(parallel_function_2)(
        iStation, mergedCsvOutDir, gapfillConfigDir)for iStation in gapfilledStation)