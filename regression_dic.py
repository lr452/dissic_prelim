import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *
from scipy.stats.mstats import *

cube = iris.load_cube('/disk2/lr452/Downloads/dissic_data/dissic_Omon_CESM2-FV2_historical_r1i1p1f1_gn_199401-201412.rg.yr.so.fix.mask.nc','dissic')

print(cube) 
print(cube.shape)


#Taking the mean value across the 20 years
average_across_time = cube.collapsed(['time'],iris.analysis.MEAN)

#Averaging across depth
max_depth = 100.0
indexes = np.where(average_across_time.coord('lev').points <= max_depth)[0]
average_across_time = average_across_time[indexes]
average_across_depth = average_across_time.collapsed(['lev'],iris.analysis.MEAN)

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

variable1 = global_average_variable.coord('latitude').points
variable2 = global_average_variable.data

print(variable1.shape)
print(variable2.shape)

slope,intercept,r_value,p_value,std_err = linregress(variable1, variable2)

print(slope)

plt.scatter(variable1,variable2)
plt.plot(variable1,(slope*variable1)+intercept)
plt.xlabel('latitude')
plt.ylabel('DIC concentration')
plt.show()
