#! /usr/bin/env python

import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sys
#from awids import decoder as dc
from awids.mesoreader import MesonetReader as mred
from awids.Projection import Projection as proj
from awids import gridmaker
from awids import Barbs as b
import time as gmtime
import os
import datetime

plotvar = {}


plotvar['PFUNC'] = sys.argv[1]
plotvar['WIND'] = 'BARB'

dirList = os.listdir( os.path.dirname(__file__) )
dirList = sorted( dirList )
flist = []
count = 0
t = int( sys.argv[2] )
pmap = proj( area='MESONET' )
m = pmap.proj()
gmaker = gridmaker.GRIDMAKER( area='MESONET', StationDict='mesonet.npz', GridFile='mesonet_oa.npz', RoI=40000 )

if plotvar['WIND'] == 'GRID':
  barbplot = b.PlotBarbs( area='MESONET', StationDict='mesonet.npz' )
if plotvar['WIND'] == 'BARB':
  barbplot = b.PlotBarbs( area='MESONET', StationDict='mesonet.npz', GridFile='mesonet_oa.npz' )

for fname in dirList:
  if fname[-4:] == '.mdf':
    ## convert the filenames to dates
    fname = fname[:-4]
    flist.append( fname )

for fname in flist:
  year = int( fname[:4] )
  month = int( fname[4:6] )
  day = int( fname[6:8] )
  hour = int( fname[8:10] )
  minute = int( fname[10:] )

  ## do date math
  tendency = datetime.datetime( year, month, day, hour, minute )
  interval = datetime.timedelta( minutes=t )
  initial = interval + tendency
  ## convert dates back to strings
  initial = str( initial )
  tendency = str( tendency )
  initial = initial.replace( '-', '').replace( ':', '' ).replace( ' ', '' )
  tendency = tendency.replace( '-', '').replace( ':', '' ).replace( ' ', '' )
  filename = initial[:-2]
  tendency = tendency[:-2]
  print filename, tendency
  
  ## Download the METAR data
  print 'Loading Mesonet Data...'
  try:
    DataDict = mred( filename )
    TendDict = mred( tendency )
  except:
    pass
  gridname = {}
  while True:
    ## Draw the map 
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    ## Contour the data grids
    if plotvar[ 'PFUNC' ].startswith( '3' ):
      grid = gmaker.grid_3hr( datatype=plotvar[ 'PFUNC' ], datdict=DataDict, tenddict=TendDict )
    elif plotvar[ 'PFUNC' ] == 'VORT' or plotvar[ 'PFUNC' ] == 'DIVR':
      grid = gmaker.TriangulateKinematics( datatype=plotvar[ 'PFUNC' ], datdict=DataDict )
    elif plotvar[ 'PFUNC' ] == 'TPFA' or plotvar[ 'PFUNC' ] == 'TPCA' or plotvar[ 'PFUNC' ] == 'MXRA' or plotvar[ 'PFUNC' ] == 'THEA':
      grid = gmaker.AdvectionGrid( datatype=plotvar[ 'PFUNC' ] )
    else: 
      grid = gmaker.grid( datatype=plotvar[ 'PFUNC' ], datdict=DataDict )
    m.contourf( grid[0], grid[1], grid[2], grid[3], cmap=grid[4], extend='both' )
    gridname[ filename ] = grid[2]
    if plotvar['PFUNC'] == '3DIV':
      np.savez( sys.argv[2] + 'DIV_' + filename, **gridname )
    else:
      np.savez( plotvar['PFUNC'] + '_' + filename + '.npz', **gridname )
    ## Plot the wind barbs
    if plotvar['WIND'] == 'GRID':
      barb = barbplot.GridBarbs( DatDict=DataDict )
    if plotvar['WIND'] == 'BARB':
      barb = barbplot.StnBarbs( DatDict=DataDict )
    plt.colorbar(orientation='horizontal', fraction=.05)
    if plotvar['PFUNC'] == '3DIV':
      plt.title( sys.argv[2] + r' Minute Surface Divergence ($S^{-1}*{10^5}$) Tendency' )
    else:
      plt.title( grid[5] )
    plt.xlabel(filename[4:6] + '/' + filename[6:8] + '/' + filename[:4] + '     ' + filename[8:10] + ':' + filename[10:] + 'Z' + '\n' + '(C) AWIDS')
    if plotvar['PFUNC'] == '3DIV':
      nm = sys.argv[2] + 'DIV'
    else:
      nm = plotvar['PFUNC']
    plt.savefig(nm + '_' + 'OK' + '_' + filename + '.png',bbox_inches='tight')
    #plt.show()
    plt.close()
    break
if plotvar['PFUNC'] == '3DIV':
  np.savez( sys.argv[2] + 'DIV.npz', **gridname )
else:
  np.savez( plotvar['PFUNC'] + '.npz', **gridname )

    



