import iris
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *

cubea = iris.load_cube('/disk2/lr452/Downloads/DISSIC_FIX/S_OCEAN/S_Ocean.dissic_Omon_NorESM2-LM_historical_r1i1p1f1_gr_199401-201412_depthregrid.nc','dissic')


add_month_number(cubea, 'time', name='month_number')
cube2a = cubea[np.where((cubea.coord('month_number').points == 6) | (cubea.coord('month_number') == 7) | (cubea.coord('month_number') == 8))]

#then to average this by each year, so that you have the December-Jan for each year add the 'season year', i.e. a number of each 'season'
add_season_year(cube2a, 'time', name='season_year')

#then average by the season year:
cube3a = cube2a.aggregated_by(['season_year'], iris.analysis.MEAN)

#average all of the data together along the time axis
cube4a = cube3a.collapsed('time',iris.analysis.MEAN)

#extracting a geographical region
west = 40
east = 120
south = -60
north = -40
temporary_cubea = cube4a.intersection(longitude = (west, east))
cube4a_region = temporary_cubea.intersection(latitude = (south,north))

#averaging across longitudes
cube4a_region.coord('latitude').guess_bounds()
cube4a_region.coord('longitude').guess_bounds()
grid_areas = iris.analysis.cartography.area_weights(cube4a_region)
global_average_variablea = cube4a_region.collapsed(['longitude'],iris.analysis.MEAN,weights=grid_areas)


cubeb = iris.load_cube('/disk2/lr452/Downloads/DISSIC_FIX/S_OCEAN/S_Ocean.dissic_Omon_GFDL-CM4_historical_r1i1p1f1_gr_199401-201412_depthregrid.nc','dissic')

add_month_number(cubeb, 'time', name='month_number')
cube2b = cubeb[np.where((cubeb.coord('month_number').points == 6) | (cubeb.coord('month_number') == 7) | (cubeb.coord('month_number') == 8))]

#then to average this by each year, so that you have the December-Jan for each year add the 'season year', i.e. a number of each 'season'
add_season_year(cube2b, 'time', name='season_year')

#then average by the season year:
cube3b = cube2b.aggregated_by(['season_year'], iris.analysis.MEAN)

#average all of the data together along the time axis
cube4b = cube3b.collapsed('time',iris.analysis.MEAN)

#extracting a geographical region
west = 40
east = 120
south = -60
north = -40
temporary_cubeb = cube4b.intersection(longitude = (west, east))
cube4b_region = temporary_cubeb.intersection(latitude = (south,north))

#averaging across longitudes
cube4b_region.coord('latitude').guess_bounds()
cube4b_region.coord('longitude').guess_bounds()
grid_areas = iris.analysis.cartography.area_weights(cube4b_region)
global_average_variableb = cube4b_region.collapsed(['longitude'],iris.analysis.MEAN,weights=grid_areas)

global_average_variablea_copy = global_average_variablea.copy()
global_average_variablea_copy.data = global_average_variableb.data 

diff_cube = global_average_variablea - global_average_variablea_copy
                                                   
qplt.pcolormesh(diff_cube)
plt.show()
