import iris 
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *
from scipy.stats.mstats import *

cube = iris.load_cube('/disk2/lr452/Downloads/dissic_data/S_Ocean.dissic_Omon_MIROC-ES2L_historical_r1i1p1f2_gn_199401-201412_landmask.nc','dissic')


print(cube.shape)
 

#Taking the mean value across the 20 years
average_across_time = cube.collapsed(['time'],iris.analysis.MEAN)

#Averaging across depth, here I want to change this to the average over the 0-1000m rather than the average across all depth levels
average_across_depth = average_across_time.collapsed(['ocean sigma over z coordinate'],iris.analysis.MEAN)

#Extracting a region (Indian, Atlantic, or Pacific)
west = 40
east = 120
south = -65
north = -40
temporary_cube = average_across_depth.intersection(longitude = (west, east))
cube_region = temporary_cube.intersection(latitude = (south,north))

#Averaging across longitude
cube_region.coord('latitude').guess_bounds()
cube_region.coord('longitude').guess_bounds()
grid_areas = iris.analysis.cartography.area_weights(cube_region)
global_average_variable = cube_region.collapsed(['longitude'],iris.analysis.MEAN,weights=grid_areas)

variable1 = #the latitude data 
variable2 = global_average_variable 

#print(variable1.shape)
print(variable2.shape)

slope,intercept,r_value,p_value,std_err = linregress(variable1, variable2)
show()
