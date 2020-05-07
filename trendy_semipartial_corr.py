import numpy as np
import pandas as pd
import netCDF4 as nc
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.basemap import Basemap
import pingouin as pg

pathwayIN = '../../TRENDY/IOD_detrend_new/'

TEMP = nc.Dataset(pathwayIN+'temp/temp_1901-2015_anomaly_annual_australia.nc')  
PREC = nc.Dataset(pathwayIN+'prec/prec_1901-2015_anomaly_annual_australia.nc')  

temp = TEMP.variables['temp'][60:,:,:]
prec = PREC.variables['prec'][60:,:,:]

def semipart_corr(model, met_var, trendy_var, position, title):
    GPP = nc.Dataset(pathwayIN+'gpp/sh_year/'+model+'_S2_'+trendy_var+
                     '_anomaly_area_weighted.nc') 
    gpp = GPP.variables['gpp'][60:,:,:]*1000
    
    if model in ('ISAM', 'LPX'):
        lat = GPP.variables['latitude'][:]
        lon = GPP.variables['longitude'][:]
    else:   
        lat = GPP.variables['lat'][:]
        lon = GPP.variables['lon'][:]

    matrix = np.zeros((len(lat), len(lon)))    
    for x in range(len(lat)):
        for y in range(len(lon)):  
            try:
                df_clim = pd.DataFrame(temp[:,x,y],columns=['temp'])           
                df_clim['prec'] = pd.DataFrame(prec[:,x,y],columns=['prec'])           
                df_clim['gpp'] = pd.DataFrame(gpp[:,x,y],columns=['gpp'])
                
                if met_var == 'prec':
                    corr = pg.partial_corr(data=df_clim, x='prec', y=trendy_var, 
                                           x_covar=['temp'], method='spearman')
                elif met_var == 'temp':
                    corr = pg.partial_corr(data=df_clim, x='temp', y=trendy_var, 
                                           x_covar=['prec'], method='spearman')                    
    
                if corr['p-val'][0] < 0.05:
                    matrix[x,y] = corr['r'][0] 
                else:
                    matrix[x,y] = np.nan   
    
            except (np.linalg.LinAlgError, AssertionError):
                matrix[x,y] = np.nan
    
    plt.subplot(3, 5, position)
    if model == 'SDGVM':
        lon = lon + 180
    else:
        pass
    
    map = Basemap(projection='cyl',llcrnrlat= -44.75,urcrnrlat=-10.25,\
                  resolution='c',  llcrnrlon=110.,urcrnrlon=160.)
    
    map.drawcoastlines()
    x, y = map(*np.meshgrid(lon, lat))
    cut_data = matrix[:-1, :-1]
    
    plt.title(model)
    plt.subplots_adjust(top=0.95, left=0.02, right=0.98, bottom=0.10, 
                        wspace=0.03, hspace=0.15)
    cmap = plt.cm.BrBG
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    levels = np.arange(-1,1.2,0.2)
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    cnplot = map.pcolormesh(x, y, cut_data, cmap=cmap, norm=norm)
    cax = plt.axes([0.2, 0.06, 0.6, 0.02])
    cbar=fig.colorbar(cnplot, orientation='horizontal', cax=cax)
    cbar.ax.tick_params(labelsize=11)
    plt.colorbar(ticks = levels, cax=cax, 
                  orientation='horizontal')
    cbar.set_label(title,fontsize=11)

fig, ax = plt.subplots(figsize=(14,7.5))

modelz = ['CABLE-POP', 'CLASS-CTEM', 'CLM5.0', 'DLEM', 'ISAM', 'JSBACH', 
          'LPJ', 'LPJ-GUESS', 'LPX', 'OCN', 'ORCHIDEE', 'ORCHIDEE-CNP', 
          'SDGVM', 'SURFEX', 'VISIT']
positions = [1, 2, 3, 4, 5, 6, 7 ,8 , 9, 10, 11, 12, 13, 14, 15]

for m, p in zip(modelz, positions):
    # semipart_corr(m, 'prec', 'gpp', p, r'$\sigma_P$')  
    semipart_corr(m, 'temp', 'gpp', p, r'$\sigma_T$')  
# plt.show()  
plt.savefig('semipart_corr_gpp_temp_anomaly_map.png', dpi = 600)     
