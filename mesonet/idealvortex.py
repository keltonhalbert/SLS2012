#! /usr/bin/env python
import numpy as np
from Projection import Projection as P
import matplotlib.pyplot as plt
import gridmaker
import Barbs as b
import matplotlib as mpl

c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
cmap = mycm


stations = np.load('mesonet.npz')
datadict = {}

m = P( area='OK' ).proj()
m.drawstates()

file = open('data.mdf', 'r')
text = file.read().split('\n')
for line in text:
  line = line.split()
  if len( line ) > 2:
    stn = line[0]
    datadict[ stn ] = {}
    datadict[ stn ]['UMET'] = float( line[1] )
    datadict[ stn ]['VMET'] = float( line[2] )
    datadict[ stn ]['UWIN'] = float( line[1] )
    datadict[ stn ]['VWIN'] = float( line[2] )

gmaker = gridmaker.GRIDMAKER( area='OK', StationDict=stations, datdict=datadict )
grid = gmaker.TriangulateKinematics( datdict=datadict, datatype='DIVR' )
#grid = gmaker.VectorGrid( datdict=datadict, datatype='VORT' )
#m.contourf( grid[0], grid[1], grid[2], np.arange(-0.0001, 0.000125, .000025), cmap=mycm )
m.contourf( grid[0], grid[1], grid[2],np.arange(0, 0.0012, 0.00004), cmap=plt.cm.gist_heat_r )
#CS = m.contour( grid[0], grid[1], grid[2] )
#plt.clabel( CS, inline=1 )

for idx, p in enumerate( grid[2] ):
  print grid[2][idx]

for stn in datadict.keys():
  U = datadict[ stn ]['UMET']
  V = datadict[ stn ]['VMET']
  X = stations[ stn ][0]
  Y = stations[ stn ][1]
  X,Y = m( X,Y )
  m.barbs( X,Y,U,V )

#barbplot = b.PlotBarbs( area='OK', DatDict=datadict, StationDict=np.load('mesonet.npz') )
#barb = barbplot.GridBarbs()
plt.colorbar(orientation='horizontal', fraction=.05)
plt.show()
