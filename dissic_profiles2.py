import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *

cube = iris.load_cube('/disk2/lr452/Downloads/DISSIC_FIX/S_OCEAN/S_Ocean.dissic_Omon_NorESM2-LM_historical_r1i1p1f1_gr_199401-201412_landmask.nc','dissic')


add_month_number(cube, 'time', name='month_number')
cube2 = cube[np.where((cube.coord('month_number').points == 6) | (cube.coord('month_number') == 7) | (cube.coord('month_number') == 8))]

#then to average this by each year, so that you have the December-Jan for each year add the 'season year', i.e. a number of each 'season'
add_season_year(cube2, 'time', name='season_year')

#then average by the season year:
cube3 = cube2.aggregated_by(['season_year'], iris.analysis.MEAN)

#average all of the data together along the time axis
cube4 = cube3.collapsed('time',iris.analysis.MEAN)

#extracting a geographical region
west = 40
east = 120
south = -65
north = -40
temporary_cube = cube4.intersection(longitude = (west, east))
cube4_region = temporary_cube.intersection(latitude = (south,north))

#averaging across longitudes
cube4_region.coord('latitude').guess_bounds()
cube4_region.coord('longitude').guess_bounds()
grid_areas = iris.analysis.cartography.area_weights(cube4_region)
global_average_variable = cube4_region.collapsed(['longitude'],iris.analysis.MEAN,weights=grid_areas)

qplt.pcolormesh(global_average_variable,vmin = 2.1, vmax = 2.35)
plt.ylim(1000,0)
plt.show()
