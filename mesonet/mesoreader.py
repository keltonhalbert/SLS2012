#! /usr/bin/env python
## Mesonet Data Reader
## (C) Kelton Halbert 2012
import vectors
from thermo import Thermo
import urllib

def MesonetReader( filedate ):
  mesonet = {}
  vars = [ 'TMPC',  'WSPD', 'RELH', 'PRES', 'RAIN' ]
  mesdat = urllib.urlopen( 'http://www.mesonet.org/data/public/mesonet/latest/latest.mdf' )
  #mesdat = open( '201105242000.mdf', 'r' )
  data = mesdat.read().split('\n')
  for n in range(3, 123):
    StationData = data[ n ]
    StationData = StationData.split()
    if len( StationData ) < 16:
      continue
    stn = StationData[0]
   ## Initialize a dictionary of dictionaries for easy data access
    mesonet[ stn ] = {}
   ## Variable names come from the Oklahoma Mesonet Website 
    mesonet[ stn ][ 'RELH' ] = float( StationData[3] )
    mesonet[ stn ][ 'TMPC' ] = float( StationData[4] )
    mesonet[ stn ][ 'WSPD' ] = float( StationData[5] )
    mesonet[ stn ][ 'WVEC' ] = StationData[6]
    mesonet[ stn ][ 'WDIR' ] = StationData[7]
    mesonet[ stn ][ 'WDSD' ] = StationData[8]
    mesonet[ stn ][ 'WSSD' ] = StationData[9]
    mesonet[ stn ][ 'WMAX' ] = StationData[10]
    mesonet[ stn ][ 'RAIN' ] = float( StationData[11] )
    mesonet[ stn ][ 'PRES' ] = float( StationData[12] )
    mesonet[ stn ][ 'SRAD' ] = StationData[13]
    mesonet[ stn ][ 'TA9M' ] = StationData[14]
    mesonet[ stn ][ 'WS2M' ] = StationData[15]
    mesonet[ stn ][ 'TS10' ] = StationData[16]
    mesonet[ stn ][ 'TB10' ] = StationData[17]
    mesonet[ stn ][ 'TS05' ] = StationData[18]
    mesonet[ stn ][ 'TB05' ] = StationData[19]
    mesonet[ stn ][ 'TS30' ] = StationData[20]
    mesonet[ stn ][ 'TR05' ] = StationData[21]
    mesonet[ stn ][ 'TR25' ] = StationData[22]
    mesonet[ stn ][ 'TR60' ] = StationData[23]
   ## Objects that must be calculated separately
    mesonet[ stn ][ 'UWIN' ] = vectors.UWIN( StationData[7], StationData[5] )
    mesonet[ stn ][ 'VWIN' ] = vectors.VWIN( StationData[7], StationData[5] )
    mesonet[ stn ][ 'UMET' ] = vectors.UMET( StationData[7], StationData[5] )
    mesonet[ stn ][ 'VMET' ] = vectors.VMET( StationData[7], StationData[5] )
    mesonet[ stn ][ 'TMPF' ] = Thermo().fahrenheit( StationData[4] )
    mesonet[ stn ][ 'DWPC' ] = Thermo().dewpoint_c( StationData[4], StationData[3] )
    mesonet[ stn ][ 'DWPF' ] = Thermo().dewpoint_f( StationData[4], StationData[3] ) 
  for k in mesonet.keys():
    for var in vars:
      if mesonet[ k ][ var ] == -999.0 or mesonet[ k ][ var ] == -998.0 or mesonet[ k ][ var ] == -997.0 or mesonet[ k ][ var ] == -996.0:
        mesonet[ k ][ var ] = '-999.99'
  return mesonet



if __name__ == '__main__':
  data = MesonetReader( '201105241830.mdf' )
  print data[ 'ADAX' ][ 'UMET' ]
