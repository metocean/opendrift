import numpy as np
from datetime import timedelta, datetime
from opendrift.readers import reader_global_landmask
from opendrift.models.oceandrift import OceanDrift
from opendrift.readers import reader_schism_datamesh_cons

###############################
# MODEL
###############################
o = OceanDrift(loglevel=0)  # Set loglevel to 0 for debug information
###############################
# READERS
###############################
# Creating and adding reader using a native SCHISM netcdf output file
# SCHISM reader
reader_landmask = reader_global_landmask.Reader() 

# >> ideally we would use the boundary/islands polygons here ? 

# NZTM proj4 string found at https://spatialreference.org/ref/epsg/nzgd2000-new-zealand-transverse-mercator-2000/
proj4str_nztm = '+proj=tmerc +lat_0=0 +lon_0=173 +k=0.9996 +x_0=1600000 +y_0=10000000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'

schism_datamesh_cons = reader_schism_datamesh_cons.Reader(
	filename = 'calypso-tidalcons-hauraki-v1',)  # native coordinate system is lon/lat
	# proj4 = proj4str_nztm, 
	# use_3d = True)

# schism_native.plot_mesh()
o.add_reader([reader_landmask,schism_datamesh_cons])
o.set_config('general:use_auto_landmask', False) # prevent opendrift from making a new dynamical landmask with global_landmask
o.set_config('general:coastline_action', 'previous') # prevent particles stranding
o.set_config('drift:horizontal_diffusivity', 0.1) # Switch on horizontal diffusivity. Set this at 0.1 m2/s (https://journals.ametsoc.org/view/journals/atot/22/9/jtech1794_1.xml)

# time_run = [datetime.utcnow(), datetime.utcnow() + timedelta(hours=12)]
time_run = [datetime(2024,1,1), datetime(2024,1,1) + timedelta(hours=12)]

# Seed elements at defined positions, depth and time
o.seed_elements(lon=175.0060864, 
                lat=-36.5267795, 
                radius=250, 
                number=100,
                z=np.linspace(0,-10, 100), 
                time=time_run) # this will be a continuous release over that time vector



# Running model
o.run(stop_on_error = True,
      time_step=600, 
	  end_time = time_run[-1],
      time_step_output = 1800.)
	  # outfile='schism_native_output.nc')
import pdb;pdb.set_trace()
o.plot(fast=True,filename='test_schism_datamesh_cons.png')
o.animation(fast=True,filename='test_schism_datamesh_cons.gif')

# ax,_=o.plot(fast=True, corners=MapCorners, filename='particle_map.png')

# MapCorners=[173.5,174.0,-42.5,-42.0] # Specify map corners
# # Print and plot results
# print(o)
# ax,_=o.plot(fast=True, corners=MapCorners, filename='particle_map.png')