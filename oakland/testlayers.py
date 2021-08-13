#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 09:09:22 2021

@author: katebelisle
"""

fn="/Users/katebelisle/Downloads/CalEnviroScreen_4.0GDB_D1_2021.gdb.zip"
#fn="/Users/katebelisle/Documents/smc/gisdata/customlayers/oakaccesspoints.shp"
oakfn="/Users/katebelisle/Documents/smc/gisdata/customlayers/oakland.geojson"
#fn="/Users/katebelisle/Documents/smc/gisdata/customlayers/oakcorridor.shp"
#fn=   "https://data.oaklandca.gov/api/geospatial/g7vb-tiyh?method=export&format=GeoJSON"

import geopandas as gp
import pandas as pd
import math
oak=gp.read_file(oakfn).to_crs("EPSG:4326")
oak["agency"]="oak"
oak=oak.dissolve(by="agency",aggfunc="first")

ces=gp.read_file(fn).to_crs("EPSG:4326")
ces["ttract"]=[f"{t}" for t in ces["Tract"]]
ces=gp.clip(ces,oak)
ces["score"]=[0 if math.isnan(s) else s for s in ces["CIscoreP"]]
ces["score"]=[math.ceil(s/10) for s in ces["score"]]
ces=ces[ces["score"]>0]
colors=['#a50026','#d73027','#f46d43','#fdae61','#fee08b','#d9ef8b','#a6d96a','#66bd63','#1a9850','#006837']
colors.reverse()
ces["shade"]=[colors[(s-1)] for s in ces["score"]]
#        fn=(GJ_PREFIX+"/%s_%s.geojson" % (layer_name,lang.lower()) )
ces.to_file("/Users/katebelisle/Documents/smc/gisdata/customlayers/calenviro4.geojson",driver="GeoJSON")
