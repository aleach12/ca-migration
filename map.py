#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 17:08:57 2019

@author: alanleach
"""

import matplotlib.pyplot as plt

import geopandas as gpd

import dfply

import matplotlib.patheffects as pe

import pandas as pd

##reads in migration summary
ca_sum = pd.read_csv("/Users/alanleach/Desktop/ca-migration/ca-sum.csv")

##retrieves state shapefiles from Tiger Web and merges with ca_sum
geo_state = gpd.read_file("https://www2.census.gov/geo/tiger/TIGER2017/STATE/tl_2017_us_state.zip")

geo_state_cont = geo_state >> dfply.mask(geo_state.NAME != 'Alaska', geo_state.NAME != 'Hawaii')

geo_state_cont['STATEFP'] = geo_state_cont.STATEFP.astype(int)

geo_state_cont = geo_state_cont.merge(ca_sum, on='STATEFP', how='left') 

geo_state_cont = geo_state_cont.dropna()
 
geo_state_cont['emigrants'] = geo_state_cont.emigrants.astype(int)

geo_state_cont = geo_state_cont.to_crs("+proj=cea +lon_0=0 +lat_ts=45 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs")  ##changes projection to gall-peters

##creates a dataframe with polygon centroids for labeling the states
geo_state_points = geo_state_cont.copy()

geo_state_points["center"] = geo_state_points["geometry"].centroid

geo_state_points.set_geometry("center", inplace = True)

geo_state_points['coords'] = geo_state_points['geometry'].apply(lambda x: x.representative_point().coords[:])

geo_state_points['coords'] = [coords[0] for coords in geo_state_points['coords']]

 
## makes plot
ax = plt.figure(figsize=(1, 1))

ax = geo_state_cont.plot(column = 'emigrants', cmap = 'Blues', edgecolor = 'black')


for idx, row in geo_state_points.iterrows():

    plt.annotate(s=row['emigrants'], xy=row['coords'],

                 verticalalignment='bottom',

                 horizontalalignment='center',

                 size = 4,

                 color = 'black',

                 path_effects=[pe.withStroke(linewidth=2, foreground="white")])

ax.set_axis_off()

plt.title('Average Annual California Emigrants to\n Continental United States, 2013-2017', fontdict={'family': 'serif',

                                                                                            'color':  'black',

                                                                                            'weight': 'normal',

                                                                                            'size': 10,

                                                                                            })

plt.style.use('fivethirtyeight')

plt.savefig('/Users/alanleach/Desktop/ca-migration/ca-migrants.png', dpi = 1000)

plt.show()

plt.close()