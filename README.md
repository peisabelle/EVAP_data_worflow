# EVAP_data_worflow
Workflow to process the raw binary data from the Campbell Scientific dataloggers. 

Processing steps:

- Process external data
- Convert Campbell Scientific binary data to ASCII files
- Merge slow frequency data, rename variables
- Batch process high-frequency data into EddyPro
- Merge Eddypro variables with slow frequency variables, rename variables
- Combine all data sources.
- Perform gap-filling.