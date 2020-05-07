import numpy as np
from netCDF4 import Dataset as open_ncfile
import pandas as pd
import netCDF4 as nc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.basemap import Basemap
import numpy.ma as ma
import statsmodels.formula.api as smf

pathwayIN = '../../TRENDY/IOD_detrend_new/'

TEMP = nc.Dataset(pathwayIN+'temp/temp_1901-2015_anomaly_annual_australia_test.nc')  
PREC = nc.Dataset(pathwayIN+'prec/prec_1901-2015_anomaly_annual_australia_test.nc')  

temp = TEMP.variables['temp'][60:,4:,:]
prec = PREC.variables['prec'][60:,4:,:]

def regression_map(model, position, met_var, met_var_name):
    GPP = nc.Dataset(pathwayIN+'gpp/sh_year/'+model+
                     '_S2_gpp_anomaly_area_weighted.nc') 

    if model in ('ISAM', 'LPX'):
        lat = GPP.variables['latitude'][4:]
        lon = GPP.variables['longitude'][:]
    else:   
        lat = GPP.variables['lat'][4:]
        lon = GPP.variables['lon'][:]
        
    gpp = GPP.variables['gpp'][60:-2,4:,:]*1000
    
    matrix_gpp = [[0 for i in range(len(lon))] for j in range(len(lat))]
    
    for x in range(len(lat)):
        for y in range(len(lon)):   
            df_clim = pd.DataFrame(temp[:,x,y],columns=['temp'])
            df_clim['prec'] = pd.DataFrame(prec[:,x,y],columns=['prec'])
            df_clim['gpp'] = pd.DataFrame(gpp[:,x,y],columns=['gpp'])
    
            X = df_clim[['temp', 'prec']]
            Y = df_clim['gpp']
    
            try:
                # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, 
                #                                                     test_size = 0.2, 
                #                                                     random_state=0)
                # lin_reg_mod = LinearRegression()
                # model = lin_reg_mod.fit(X_train, Y_train)
                # pred = lin_reg_mod.predict(X_test)
                lm1 = smf.ols(formula='gpp ~ prec + temp', data=df_clim).fit()
                if lm1.pvalues[met_var] < 0.05:
                    # matrix_gpp[x][y] = lin_reg_mod.coef_[1]
                    matrix_gpp[x][y] = lm1.params[met_var]
                else:
                    matrix_gpp[x][y] = np.nan
    
            except (ValueError):
                nanibert = 0
                matrix_gpp[x][y] = nanibert
    
        matrix_gpp = np.squeeze(np.asarray(matrix_gpp))
    
    try:
        matrix_gpp[matrix_gpp == 0] = np.nan
    except ValueError:
        pass
       
    map = Basemap(projection='cyl',llcrnrlat= -44.75,urcrnrlat=-10.25,\
                  resolution='c',  llcrnrlon=110.,urcrnrlon=160.)
    
    map.drawcoastlines(linewidth=0.6)
    x, y = map(*np.meshgrid(lon, lat))
    cut_data = matrix_gpp[:-1, :-1]*1000
    
    plt.subplot(4, 4, position)
    plt.subplots_adjust(top=0.98, left=0.02, right=0.98, bottom=0.08, 
                        wspace=0.03, hspace=0.08)
    cmap = plt.cm.gist_rainbow
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    levels = np.arange(0,2.2,0.2)
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    cnplot = map.pcolormesh(x, y, cut_data, cmap=cmap, norm=norm)
    cax = plt.axes([0.2, 0.06, 0.6, 0.02])
    cbar=fig.colorbar(cnplot, orientation='horizontal', cax=cax)
    cbar.ax.tick_params(labelsize=11)
    plt.colorbar(ticks = levels, cax=cax, 
                  orientation='horizontal')
    cbar.set_label(met_var_name,fontsize=11)
    plt.title(model)

fig, ax = plt.subplots(figsize=(8,8))

modelz = ['CABLE-POP', 'CLASS-CTEM', 'CLM5.0', 'DLEM', 'ISAM', 'JSBACH', 
          'LPJ', 'LPJ-GUESS', 'LPX', 'OCN', 'ORCHIDEE', 'ORCHIDEE-CNP', 
          'SDGVM', 'SURFEX', 'VISIT']
positions = [1, 2, 3, 4, 5, 6, 7 ,8 , 9, 10, 11, 12, 13, 14, 15]

for m, p in zip(modelz, positions):
    regression_map(m, p, 0, 'Temperature')
    # regression_map(m, p, 1, 'Precipitation')
