#!/usr/bin/env python

#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sys
#from awids import decoder as dc
from mesoreader import MesonetReader as mred
from Projection import Projection as proj
import gridmaker
import Barbs as b
import time as gmtime

## Get the cycle hour to be used for plotting
if len(sys.argv) >= 2:
  datestring = sys.argv[1]
else:
  gmt = gmtime.gmtime()
  year = str( gmt[0] )
  month = str( gmt[1] ).zfill( 2 )
  day = str( gmt[2] ).zfill( 2 )
  hour = str( gmt[3] ).zfill( 2 )
  datestring = year[-2:] + month  + day + hour

## Get the cycle hour three hours prior to the initial hour;
## Fix the date for hours after 00Z
cycle_hour = datestring
if cycle_hour[-2:] == '00':
  ymd = int(cycle_hour)-3
  three_hour = str(ymd)[:-2] + '21'
elif cycle_hour[-2:] == '01':
  ymd = int(cycle_hour)-3
  three_hour = str(ymd)[:-2] + '22'
elif cycle_hour[-2:] == '02':
  ymd = int(cycle_hour)-3
  three_hour = str(ymd)[:-2] + '23'
else:
  three_hour = int(cycle_hour)-3
  three_hour = str(three_hour).zfill(2)

## Download the METAR data
print 'Loading Mesonet Data...'
DataDict = mred( '201105242000.mdf' )
TendDict = mred( '201105242000.mdf' )
## Lists/Dictionaries for plotting functions
syntax = []
plotvar = {}
uservars = []
print 'Plot Variables:\n  PFUNC = \n  WIND = \ntype "exit" to exit\ntype "run" or "r" to run'

while True:
  while True:
    vars = raw_input('==> ')
    if vars.upper() == 'R' or vars.upper() == 'RUN' or vars.upper() == 'EXIT':
      break
    else:
      syntax.append( vars.upper() )
      plt.close()
  if vars.upper() == 'EXIT':
    break
  else:
    for d in syntax:
      if not d:
        raise PlotErr, 'No Plot Functions'
        sys.exit()
      newlist = d.split( ' ' )
      plotvar[ newlist[0] ] = newlist[-1]
  ## Draw the map 
  pmap = proj( area='OK', stationdict=np.load('mesonet.npz') )
  m = pmap.proj()
  m.drawcoastlines()
  m.drawcountries()
  m.drawstates()
  ## Contour the data grids
  gmaker = gridmaker.GRIDMAKER( area='OK', datdict=DataDict, tenddict=TendDict, StationDict=np.load('mesonet.npz') )
  if plotvar[ 'PFUNC' ].startswith( '3' ):
    grid = gmaker.grid_3hr( datatype=plotvar[ 'PFUNC' ] )
  elif plotvar[ 'PFUNC' ] == 'VORT' or plotvar[ 'PFUNC' ] == 'DIVR':
    grid = gmaker.VectorGrid( datatype=plotvar[ 'PFUNC' ] )
  elif plotvar[ 'PFUNC' ] == 'TPFA' or plotvar[ 'PFUNC' ] == 'TPCA' or plotvar[ 'PFUNC' ] == 'MXRA' or plotvar[ 'PFUNC' ] == 'THEA':
    grid =gmaker.AdvectionGrid( datatype=plotvar[ 'PFUNC' ] )
  else: 
    grid = gmaker.grid( datatype=plotvar[ 'PFUNC' ] )
  m.contourf( grid[0], grid[1], grid[2], grid[3], cmap=grid[4] )
  ## Plot the wind barbs
  if plotvar['WIND'] == 'GRID':
    barbplot = b.PlotBarbs( area='OK', DatDict=DataDict, StationDict=np.load('mesonet.npz') )
    barb = barbplot.GridBarbs()
  if plotvar['WIND'] == 'BARB':
    barbplot = b.PlotBarbs( area='OK', DatDict=DataDict, StationDict=np.load('mesonet.npz') )
    barb = barbplot.StnBarbs()
  plt.colorbar(orientation='horizontal', fraction=.05)
  plt.title(grid[5])
  plt.xlabel(datestring[2:4] + '/' + datestring[4:6] + '/' + datestring[:2] + '    ' + datestring[-2:] + 'Z' + '\n' + '(C) AWIDS')
  plt.savefig(plotvar['PFUNC'] + '_' + 'OK' + '_' + datestring + '.pdf',bbox_inches='tight')
 # plt.show()
  
