#! /usr/bin/env python
import matplotlib.delaunay as md 
from pylab import *
from numpy import *
from mpl_toolkits.basemap import Basemap

stations = load('mesonet.npz')
m = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=35,lon_0=-98)
x = []
y = []
for stn in stations.keys():
  x.append( stations[stn][0] )
  y.append( stations[stn][1] )

x,y = m(x,y)
x = array(x)
y = array(y)
centers,edges,tri,neighbors = md.delaunay(x,y)

m.drawstates()
for t in tri:
    t_ext = [t[0], t[1], t[2], t[0]] #add first point to end
    plot(x[t_ext],y[t_ext],'r')

for c in centers:
  cx,cy =  c[0], c[1] 
  plot( cx, cy, 'ro' )

plot(x,y,'*')
show()
