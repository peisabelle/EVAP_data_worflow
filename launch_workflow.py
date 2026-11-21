import process_micromet as pm
import data_paths as path
from utils import data_loader as dl, dataframe_manager as dfm

# Station names
CampbellStations =  [
    'Juvenile_NO',
    'Juvenile_SE',
    'Juvenile_Sol',
    'Sapling',
    'Sapling_Sol',
    'Regeneration',
    'Regeneration_CPEC',
    'Canopy',
    'Neige',
    ]

eddyCovStations =   [
    'Juvenile_NO',
    'Juvenile_SE',
    'Sapling',
    'Regeneration',
    'Regeneration_CPEC',
    'Canopy',
    'Neige',
    ]

gapfilledStation =  [
    'Juvenile',
    'Sapling',
    'Regeneration',
    'Neige',
    ]

dates = {'start':'2015-09-01','end':'2026-11-11'}

# # Perform ERA5 extraction and handling
# for iStation in gapfilledStation:
#     reanalysis_config = dl.yaml_file(path.reanalysisConfigDir, iStation)
#     pm.reanalysis.retrieve( reanalysis_config['era5-land'], dates, path.reanalysisDir)
#     pm.reanalysis.retrieve( reanalysis_config['era5'], dates, path.reanalysisDir)

for iStation in CampbellStations:

    # Binary to ascii
    unconverted_files = pm.csbinary_to_csv.find_unconverted_files(iStation,
                                path.rawFileDir,path.asciiOutDir)
    pm.csbinary_to_csv.convert(iStation, path.asciiOutDir, unconverted_files)

#     # List slow files
#     slow_files = dfm.list_files(iStation, '*slow.csv', path.asciiOutDir)
#     # Create reference dataframe and merge slow files
#     df = dfm.create(dates)
#     df = dfm.merge_files(df, slow_files, 'TOA5')
#     # Rename and trim slow variables
#     db_name_map = pm.names.map_db_names(iStation, path.varNameExcelSheet, 'cs')
#     df = pm.names.rename_trim(iStation, df, db_name_map)

#     # First filter
#     df = pm.filters.remove_by_variable_and_date(df, path.filterConfigDir, f"{iStation}_erroneous_variables")

#     # Correct raw concentrations
#     if iStation in eddyCovStations:
#         gas_analyzer_info = dl.yaml_file(path.gasAnalyzerConfigDir, f"{iStation}_gas_analyzer")
#         corr_coeff = pm.gas_analyzer.get_correction_coeff(df,gas_analyzer_info,iStation)
#         uncorrected_files = pm.gas_analyzer.find_uncorrected_files(path.asciiOutDir.joinpath(iStation))
#         pm.gas_analyzer.correct_densities(iStation, corr_coeff, uncorrected_files)
#     # Rotate wind
#     if iStation == 'Romaine-2_reservoir_raft':
#         unrotated_files = pm.sonic.find_unrotated_files(path.asciiOutDir.joinpath(iStation))
#         pm.sonic.rotate(iStation,unrotated_files)


#     if iStation in eddyCovStations:
#         # Ascii to eddypro
#         pm.eddypro.run(iStation,path.asciiOutDir,path.eddyproConfigDir,
#                        path.eddyproOutDir,dates)
#         # List EddyPro files
#         eddypro_files = dfm.list_files(iStation, '*full_output*.csv', path.eddyproOutDir)
#         # Create reference dataframe and merge EddyPro files
#         eddy_df = dfm.create(dates)
#         eddy_df = dfm.merge_files(eddy_df,eddypro_files,'EddyPro')
#         # Rename and trim eddy variables
#         db_name_map = pm.names.map_db_names(iStation, path.varNameExcelSheet, 'ep')
#         eddy_df = pm.names.rename_trim(iStation, eddy_df, db_name_map)
#         # Merge slow and eddy data
#         df = dfm.merge(df,eddy_df)

#     dfm.save(df,path.intermediateOutDir,iStation)


# for iStation in CampbellStations:
#     # Load csv
#     df = dl.csv(path.intermediateOutDir.joinpath(iStation))
#     # Filter
#     df = pm.filters.remove_by_variable_and_date(df, path.filterConfigDir, f"{iStation}_erroneous_variables")
#     # Handle exceptions
#     df = pm.handle_exception(iStation,df)
#     # Filter data
#     df = pm.filters.apply_all(iStation,df,path.filterConfigDir,path.intermediateOutDir)
#     # Save to csv
#     dfm.save(df,path.finalOutDir,iStation)
#     # Format reanalysis data
#     pm.reanalysis.netcdf_to_dataframe(dates,iStation,path.filterConfigDir,
#                                       path.reanalysisDir,path.intermediateOutDir)


# for iStation in gapfilledStation:
#     # Merge the eddy covariance together (water/forest)
#     df = pm.merge_eddycov_stations(iStation,path.rawFileDir,
#                                    path.finalOutDir, path.miscDataDir, path.varNameExcelSheet)

#     # Format reanalysis data for gapfilling
#     pm.reanalysis.netcdf_to_dataframe(dates,iStation,path.filterConfigDir,
#                                       path.reanalysisDir,path.intermediateOutDir)

#     # Perform gap filling
#     df = pm.gap_fill_slow_data.gap_fill_meteo(
#         iStation,df,path.intermediateOutDir,path.gapfillConfigDir)
#     df = pm.gap_fill_slow_data.gap_fill_radiation(
#         iStation,df,path.intermediateOutDir,path.gapfillConfigDir)
#     df = pm.gap_fill_slow_data.custom_operation(
#         iStation,df,path.gapfillConfigDir)
#     df = pm.gap_fill_flux.gap_fill_flux(iStation,df,path.gapfillConfigDir)

#     # Compute storage terms
#     df = pm.compute_storage_flux(iStation,df)

#     # Correct for energy balance
#     if iStation == 'Bernard_spruce_moss': # Land type station
#         df = pm.correct_energy_balance(df)
#     else: # Water body type station
#         df = pm.correct_energy_balance(df, 1.34)

#     # Filter data
#     df = pm.filters.apply_all(iStation,df,path.filterConfigDir,path.finalOutDir)

#     # Perform gap filling
#     df = pm.gap_fill_flux.gap_fill_flux(iStation,df,path.gapfillConfigDir)

#     # Save to csv
#     dfm.save(df,path.finalOutDir,iStation)


# for iStation in eddyCovStations:
#     df = dl.csv(path.finalOutDir.joinpath(iStation))
#     fp = pm.footprint.compute(df)
#     pm.footprint.dump(iStation,fp,path.finalOutDir)