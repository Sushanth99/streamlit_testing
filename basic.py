
## Author: Sushanth Reddy Kamaram
## Email: ksushanthreddy0605@gmail.com

import os
import sys
import yaml

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')
from utilities import *
import streamlit as st



# params_file = sys.argv[1]
# print(params_file)

@st.cache_data
def generate_figure(params_file):
    with open(params_file, 'r') as f:
        params = yaml.safe_load(f)


    TAG = params['data']['TAG']
    path = params['data']['path']

    tmin = params['selection']['tmin']
    tmax = params['selection']['tmax']
    flux_ratio = params['selection']['flux_ratio']
    index_ratio = params['selection']['index_ratio']
    min_ts = params['selection']['min_ts']

    fig_width = params['plot']['fig_width']
    fig_height = params['plot']['fig_height']
    dpi = params['plot']['dpi']
    label = params['plot']['label']
    plot_titles = {TAG: params['plot']['plot_title']}
    plot_name = params['plot']['plot_name']
    save_dir = params['plot']['save_dir']
    save_figure = params['plot']['save_figure']

    source = Source(path)
    source.filter_data(flux_ratio=flux_ratio, index_ratio=index_ratio, min_ts=min_ts)
    if tmin is None and tmax is None:
        df = source.df
    elif tmin is None:
        df = source.df.loc[:tmax]
    elif tmax is None:
        df = source.df.loc[tmin:]
    else:
        df = source.df.loc[tmin:tmax]


    figsize = (fig_width, fig_height)
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    FACTOR = 1e6
    params = dict(fmt='.-', color='blue', ecolor='green', label=label, lw=2)
    ax.errorbar(df.index, df['flux']*FACTOR, 
                yerr=df['flux_error']*FACTOR, 
                **params)
    
    fontsize = 30; labelsize=30
    ax.legend(fontsize=fontsize)
    # ax.set_ylim(0, 5e-6)
    ax.set_xlabel('MJD', fontsize=fontsize)
    ax.set_ylabel('Photon Flux ($ 10^{-6} \; \mathrm{ph \; cm^{-2} \; s^{-1}}$)', fontsize=fontsize)
    ax.set_title(f'{plot_titles[TAG]} (TS > {min_ts}) (MJD: {min(df.index):.2f}-{max(df.index):.2f})', fontsize=25)
    ax.tick_params(axis='both', which='both', direction='in', length=10, labelsize=labelsize)
    if save_figure:
        plt.savefig(f'{os.path.join(save_dir, plot_name)}')

        try:
            print(f'Plot saved to {os.path.join(save_dir, plot_name)}') 
        except:
            print(f'Plot saved to {os.path.join(os.getcwd(), plot_name)}')
    
    st.line_chart(data=df, y='flux')
    return fig

option = st.multiselect('Choose source:', ['4C +01.02', 'PKS 0903-57', 'S4 0954+65'])
fig = generate_figure('params_sourceA_task2.yaml')
st.pyplot(fig)
