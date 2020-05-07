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

TEMP = nc.Dataset(pathwayIN+'temp/temp_1901-2015_anomaly_annual_australia.nc')  
PREC = nc.Dataset(pathwayIN+'prec/prec_1901-2015_anomaly_annual_australia.nc')  

temp_original = TEMP.variables['temp'][60:,4:,:]
prec_original = PREC.variables['prec'][60:,4:,:]

def regression_map(model, position, met_var, met_var_name):
    GPP = nc.Dataset(pathwayIN+'gpp/sh_year/'+model+
                     '_S2_gpp_anomaly_area_weighted.nc') 

    if model in ('ISAM', 'LPX'):
        lat = GPP.variables['latitude'][4:]
        lon = GPP.variables['longitude'][:]
    else:   
        lat = GPP.variables['lat'][4:]
        lon = GPP.variables['lon'][:]
        
    gpp_original = GPP.variables['gpp'][60:,4:,:]*1000
    
    matrix_gpp = [[0 for i in range(len(lon))] for j in range(len(lat))]
    
    for x in range(len(lat)):
        for y in range(len(lon)):   
            temp = (temp_original[:,x,y] - min(temp_original[:,x,y]))/ \
                   (max(temp_original[:,x,y]) - min(temp_original[:,x,y])) 
            prec = (prec_original[:,x,y] - min(prec_original[:,x,y]))/ \
                   (max(prec_original[:,x,y]) - min(prec_original[:,x,y]))
            gpp = (gpp_original[:,x,y] - min(gpp_original[:,x,y]))/ \
                  (max(gpp_original[:,x,y]) - min(gpp_original[:,x,y]))

            df_clim = pd.DataFrame(temp,columns=['temp'])
            df_clim['prec'] = pd.DataFrame(prec,columns=['prec'])
            df_clim['gpp'] = pd.DataFrame(gpp,columns=['gpp'])
#            df_clim = df_clim[(df_clim[['temp','prec']] != 0).all(axis=1)]
    
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
                print(lm1.params[met_var])
                # print(gpp)
                # print(prec)
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

    plt.subplot(4, 4, position)
    if model == 'SDGVM':
        lon = lon + 180
    else:
        pass
    
    map = Basemap(projection='cyl',llcrnrlat= -44.75,urcrnrlat=-10.25,\
                  resolution='c',  llcrnrlon=110.,urcrnrlon=160.)
    
    map.drawcoastlines()
    x, y = map(*np.meshgrid(lon, lat))
    cut_data = matrix_gpp[:-1, :-1]
    
    plt.title(model)
    plt.subplots_adjust(top=0.98, left=0.02, right=0.98, bottom=0.08, 
                        wspace=0.03, hspace=0.08)
    cmap = plt.cm.gist_rainbow
    # cmap = plt.cm.seismic
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    levels = np.arange(0,1.1,0.1)
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    cnplot = map.pcolormesh(x, y, cut_data, cmap=cmap, norm=norm)
    cax = plt.axes([0.2, 0.06, 0.6, 0.02])
    cbar=fig.colorbar(cnplot, orientation='horizontal', cax=cax)
    cbar.ax.tick_params(labelsize=11)
    plt.colorbar(ticks = levels, cax=cax, 
                  orientation='horizontal')
    cbar.set_label(met_var_name,fontsize=11)
    
fig, ax = plt.subplots(figsize=(8,8))

modelz = ['CABLE-POP', 'CLASS-CTEM', 'CLM5.0', 'DLEM', 'ISAM', 'JSBACH', 
          'LPJ', 'LPJ-GUESS', 'LPX', 'OCN', 'ORCHIDEE', 'ORCHIDEE-CNP', 
          'SDGVM', 'SURFEX', 'VISIT']
positions = [1, 2, 3, 4, 5, 6, 7 ,8 , 9, 10, 11, 12, 13, 14, 15]

# regression_map('SDGVM', 1, 1, 'Precipitation')
# regression_map('SDGVM', 1, 0, 'Temperature')
for m, p in zip(modelz, positions):
    regression_map(m, p, 0, 'Temperature')
    # regression_map(m, p, 1, 'Precipitation')
    
plt.show()
# plt.savefig('regression_gpp_temp_anomaly_map.png', dpi = 600)     
