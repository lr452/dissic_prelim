import iris 
import numpy as np
import iris.quickplot as qplt
import matplotlib.pyplot as plt
from iris.coord_categorisation import *
from scipy.stats.mstats import *

cube = iris.load_cube('/disk2/lr452/Downloads/DISSIC_FIX/S_OCEAN/S_Ocean.dissic_Omon_MIROC-ES2L_historical_r1i1p1f2_gn_199401-201412_landmask.nc','dissic')

print(cube.shape)

average_across_time = cube.collapsed(['time'],iris.analysis.MEAN)

average_across_depth = average_across_time.collapsed(['ocean sigma over z coordinate'],iris.analysis.MEAN)

variable1 = cube[2]
variable2 = average_across_depth

print(variable1.shape)
print(variable2.shape)

slope,intercept,r_value,p_value,std_err = linregress(variable1, variable2)
show()
