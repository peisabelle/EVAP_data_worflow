# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 16:42:15 2021

@author: ANTHI182
"""
import os
import netCDF4 as ncdf
import pandas as pd
import numpy as np

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, f= nan_helper(y)
        >>> y[nans]= np.interp(f(nans), f(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]


def daily_decumulate(x):
    """Decumulate the daily meteorological variables and linearly interpolate
    the missing values.

    Parameters
    ----------
    x : Pandas series

    Returns
    -------
    x : Pandas series

    """

    # Reshape values by day
    n_rows = len(x)//48
    x_arr = np.reshape(x.values, (n_rows, 48) )

    # Add a 0 value at the beginning of each day for decumulation
    x_arr = np.concatenate(
        ( np.zeros( (n_rows,1) ), x_arr ),
        axis=1)

    # Interpolate over missing half hours
    for i_row in range(0,n_rows):
        nans, f = nan_helper(x_arr[i_row, :])
        x_arr[i_row, nans]= np.interp(f(nans), f(~nans), x_arr[i_row, ~nans])

    # Convert back the array to its original shape (n_time_step,)
    x[:] = np.reshape(np.diff(x_arr,axis=1), x.shape)

    return x


def handle_netcdf(dates, data_folder, dest_folder):
    """ Organize the ERA5 land reanalysis into a pandas dataframe


    Parameters
    ----------
    dates : dictionnary that contains a 'start' and 'end' dates
        Example: dates{'start': '2018-06-01', 'end': '2020-02-01'}
    dest_folder : string
        Path to folder where netcdf files are saved
    dest_folder : string
        Path to folder where results are saved

    Returns
    -------
    None. Inputs are saved as .csv file in dest_folder

    """
    variables = {
        ### Instantaneous vars ###

        # Lake variables
        'lake_mix_layer_temperature':
            {'short_name': 'lmlt', 'db_name': 'water_mix_layer_temp', 'unit_conv': lambda x : x - 273.15},

        # Snow variables
        'snow_cover':
            {'short_name': 'snowc', 'db_name': 'snow_cover_frac', 'unit_conv': lambda x : x},
        'snow_density':
            {'short_name': 'rsn', 'db_name': 'snow_density', 'unit_conv': lambda x : x},
        'snow_depth':
            {'short_name': 'sde', 'db_name': 'snow_depth', 'unit_conv': lambda x : x * 1000},
        'snow_depth_water_equivalent':
            {'short_name': 'sd', 'db_name': 'swe', 'unit_conv': lambda x : x * 1000},
        'snowmelt':
            {'short_name': 'smlt', 'db_name': 'snowmelt', 'unit_conv': lambda x : x * 1000},

        # Standard meteorological variables
        '10m_u_component_of_wind':
            {'short_name': 'u10', 'db_name': 'wind_speed_u', 'unit_conv': lambda x : x },
        '10m_v_component_of_wind':
            {'short_name': 'v10', 'db_name': 'wind_speed_v', 'unit_conv': lambda x : x },
        '2m_temperature':
            {'short_name': 't2m', 'db_name': 'air_temp', 'unit_conv': lambda x : x - 273.15},
        'soil_temperature_level_1':
            {'short_name': 'stl1', 'db_name': 'soil_temp_surface', 'unit_conv': lambda x : x - 273.15},
        'soil_temperature_level_2':
            {'short_name': 'stl2', 'db_name': 'soil_temp_20cm', 'unit_conv': lambda x : x - 273.15},
        'surface_pressure':
            {'short_name': 'sp', 'db_name': 'air_press', 'unit_conv': lambda x : x / 1000},

        ### Cumulated vars ###

        # Snow variables
        'snowfall':
            {'short_name': 'sf', 'db_name': 'snowfall', 'unit_conv': lambda x : daily_decumulate(x) * 1000},

        # Radiation variables
        'surface_solar_radiation_downwards':
            {'short_name': 'ssrd', 'db_name': 'rad_shortwave_down', 'unit_conv': lambda x : daily_decumulate(x) / 3600},
        'surface_thermal_radiation_downwards':
            {'short_name': 'strd', 'db_name': 'rad_longwave_down', 'unit_conv': lambda x : daily_decumulate(x) / 3600},
        'surface_net_solar_radiation':
            {'short_name': 'ssr', 'db_name': 'rad_short_net', 'unit_conv': lambda x : daily_decumulate(x) / 3600},
        'surface_net_thermal_radiation':
            {'short_name': 'str', 'db_name': 'rad_long_net', 'unit_conv': lambda x : daily_decumulate(x) / 3600},

        # Precipitation
        'total_precipitation':
            {'short_name': 'tp', 'db_name': 'precipitation', 'unit_conv': lambda x : daily_decumulate(x) * 1000},

        # Fluxes
        'surface_sensible_heat_flux':
            {'short_name': 'sshf', 'db_name': 'H', 'unit_conv': lambda x : -1 * daily_decumulate(x) / 3600},
        'surface_latent_heat_flux':
            {'short_name': 'slhf', 'db_name': 'LE', 'unit_conv': lambda x : -1 * daily_decumulate(x) / 3600},
        'total_evaporation':
            {'short_name': 'e', 'db_name': 'evap', 'unit_conv': lambda x : -1 * daily_decumulate(x) * 1000},
        'potential_evaporation':
            {'short_name': 'pev', 'db_name': 'potential_evap', 'unit_conv': lambda x : -1 * daily_decumulate(x) * 1000},
        'evaporation_from_open_water_surfaces_excluding_oceans':
            {'short_name': 'evaow', 'db_name': 'water_evap', 'unit_conv': lambda x : -1 * daily_decumulate(x) * 1000},
        'evaporation_from_vegetation_transpiration':
            {'short_name': 'evavt', 'db_name': 'plant_evap', 'unit_conv': lambda x : -1 * daily_decumulate(x) * 1000},
              }

    station_coord = {'Water_stations': [-63.2494011, 50.6889992],
                     'Forest_station': [-63.4051018, 50.9020996]}


    for iStation in station_coord:

        # Initialize reference dataframe
        d_start = pd.to_datetime(dates['start']).strftime('%Y-%m-%d') + ' 00:30:00'
        d_end = pd.to_datetime(dates['end']).strftime('%Y-%m-%d')
        df = pd.DataFrame( index=pd.date_range(start=d_start, end=d_end, freq='30min') )

        # Expected list of ERA5 land files (dates)
        datelist = pd.date_range(start=dates['start'], end=dates['end'], freq='M')

        for iDate in datelist:
            if os.path.isfile(os.path.join(
                    data_folder,'ERA5','ERA5L_{}.nc'.format(iDate.strftime('%Y%m')))):

                # Open netcdf file
                rootgrp = ncdf.Dataset(os.path.join(
                    data_folder,'ERA5','ERA5L_{}.nc'.format(iDate.strftime('%Y%m'))), "r")

                # Retrieve dates and find matching entries in reference Dataframe
                ncdf_time = rootgrp['time']
                f_date = ncdf.num2date(ncdf_time, ncdf_time.units,
                                       ncdf_time.calendar, only_use_cftime_datetimes=False)

                # Initialize temporary dataframe that will contain netcdf data
                f_date = pd.to_datetime(f_date)
                id_tmp_in_df = f_date.isin(df.index)
                id_df_in_tmp = df.index.isin(f_date)

                # Handle coordinates
                id_long = np.argmin( np.abs(
                    (rootgrp['longitude'][:] - station_coord[iStation][0]) ) )
                id_lat = np.argmin( np.abs(
                    (rootgrp['latitude'][:] - station_coord[iStation][1]) ) )

                for iVar in variables:
                    df.loc[id_df_in_tmp, iVar] = rootgrp[
                        variables[iVar]['short_name']][id_tmp_in_df,id_lat,id_long]

            else:
                print('ERA5L_{}.nc not available yet'.format(iDate.strftime('%Y%m')))

        # Convert units / decumulate / (interpolate for cumulated vars)
        for iConv in variables:
            df[iConv] = variables[iConv]['unit_conv'](df[iConv])

        # Interpolate for remaining variables
        df = df.interpolate(method='linear', limit=1)

        # Compute wind speed
        df['wind_speed'] = np.sqrt(df['10m_u_component_of_wind']**2 +
                                   df['10m_v_component_of_wind']**2)

        # Save
        df.insert(0, 'timestamp', df.index)
        df.to_csv(os.path.join(dest_folder,'ERA5_'+iStation+'.csv'), index=False)