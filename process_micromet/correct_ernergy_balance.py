# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 12:00:48 2022

@author: ANTHI182
"""

def correct_energy_balance(df):
    """ Correct latent and sensible heat flux according to Mauder 2017

    Parameters
    ----------
    df : Pandas DataFrame
        Dataset that contains columns
            - LE_gf_mds
            - H_gf_mds
            - LE_strg
            - H_strg
            - net_rad_CNR4
            - G

    Returns
    -------
    df : Pandas DataFrame
        Dataset with additional columns:
            - LE_corr
            - H_corr

    References
    ----------
    Mauder, M, Genzel, S, Fu, J, et al. Evaluation of energy balance closure
    adjustment methods by independent evapotranspiration estimates from
    lysimeters and hydrological simulations. Hydrological Processes.
    2018; 32: 39– 50. https://doi.org/10.1002/hyp.11397

    """

    df['LE_corr'] = df['LE_gf_mds']
    df['H_corr'] = df['H_gf_mds']

    for i in range(0,df.shape[0],48):
        idx_bol = df.loc[i:i+48,'daytime'] == 1
        if not (sum(idx_bol) == 0):
            idx = idx_bol[idx_bol].index
            C = (df.loc[idx,'H_gf_mds'].sum() + df.loc[idx,'LE_gf_mds'].sum()) / \
                (df.loc[idx,'rad_net_CNR4'].sum() + df.loc[idx,'G'].sum() + df.loc[idx,'LE_strg'] + df.loc[idx,'H_strg'])
            df.loc[idx,'LE_corr'] = df.loc[idx,'LE_corr'] * 1/C
            df.loc[idx,'H_corr']  = df.loc[idx,'H_corr'] * 1/C

    return df