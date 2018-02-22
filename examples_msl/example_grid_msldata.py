#!/usr/bin/env python

#  This script is based on https://github.com/OpenDrift/opendrift/tree/master/examples/example_grid.py
#  The aim is to test the use of reader_netCDF_MetOcean which allows using MetOcean data in OpenDrift
#   
#  This is also used as a reference case to compare Opendrift trajectories with ERcore trajectories
# 

import numpy as np
from datetime import datetime, timedelta
from opendrift.readers import reader_basemap_landmask
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.readers import reader_netCDF_MetOcean
from opendrift.models.oceandrift import OceanDrift

o = OceanDrift(loglevel=0)  # Set loglevel to 0 for debug information

# Norkyst
# reader_norkyst = reader_netCDF_CF_generic.Reader(o.test_data_folder() + '16Nov2015_NorKyst_z_surface/norkyst800_subset_16Nov2015.nc')

# reader_roms_cnz = reader_netCDF_MetOcean.Reader('C:\metocean\cnz19800801_00z_surf.nc') # this file has several u,v variable which confuses which to use - to fix by specifying which variables to use ? 
reader_roms_cnz = reader_netCDF_MetOcean.Reader('C:\metocean\cnz_surf_res200401.nc') # only uso,vso in this one - seems to be recognized ok 

# Making customised landmask (Basemap)

# reader_basemap = reader_basemap_landmask.Reader(
#                     llcrnrlon=3.5, llcrnrlat=59.9,
#                     urcrnrlon=5.5, urcrnrlat=61.2,
#                     resolution='h', projection='merc')

# o.add_reader([reader_basemap, reader_norkyst])
o.add_reader([reader_roms_cnz])

# Seeding some particles
# lons = np.linspace(3.5, 5.0, 100)
# lats = np.linspace(60, 61, 100)
# 
#  Point release
lon = 174.5133; lat = -41.2348; 
#  Rectangle release
lons = np.linspace(170.0,170.5, 100) 
lats = np.linspace(-39.5,-39.0, 100)
lons, lats = np.meshgrid(lons, lats)
lons = lons.ravel()
lats = lats.ravel()
#

# Seed oil elements at defined position and time

# o.seed_elements(lons, lats, radius=0, number=10000,
#                 time=reader_roms_cnz.start_time)

o.seed_elements(lon, lat, radius=0, number=1000,
                time=datetime(2004,1,1) ) #

# o.set_config('drift:current_uncertainty', .1)

# import pdb;pdb.set_trace()

# Running model (until end of driver data)
o.run(time_step=1800, end_time = datetime(2004,1,4), outfile='opendrift.nc',time_step_output = 1800)  
# the start time is define by seed_elements, the end_time is defined by either steps=number of step, duration = timedelta, or end_time= datetime

# Print and plot results
print o


o.animation()
o.plot()
