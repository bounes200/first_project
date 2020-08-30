import pandas as pd
import datetime

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

# Each tab is drawn by one script
from scripts.cambar import bar_cam
from scripts.time_series import time_series


# read the data

sni = pd.read_csv(join(dirname(__file__), 'data', 'statsSNI.csv'),
                  sep=';', encoding='latin-1', parse_dates=['Arrete', 'date'])
sni['NVF'].replace(to_replace=[8], value=7, inplace=True)
sni['NVF'] = sni['NVF'].astype(str)
sni['NSY'] = sni['NSY'].astype(str)
sni.drop(['code_agence', 'Nom_Agence', 'Creer par', 'NOR', 'NOV'], axis = 1, inplace = True)

# data for bar charts
sni_sub = sni[['CAMR', 'Tiers', 'NVF']]
sni_gsub = sni_sub.groupby(['CAMR', 'NVF']).count().reset_index()
sni_gsub.columns = ['CAMR', 'NVF', 'Count']

# data for time series
grouper = sni[['date','CAMR','NVF']].set_index('date').groupby([pd.Grouper(freq = '1M'), 'CAMR']).count().reset_index()


# create tabs
tab1 = bar_cam(sni_gsub)
tab2 = time_series(grouper)
tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)

