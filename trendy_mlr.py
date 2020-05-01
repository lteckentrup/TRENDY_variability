import numpy as np
import pandas as pd
import netCDF4 as nc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

pathwayIN = '../../TRENDY/IOD_detrend_new/'

data_vegetation_mask = nc.Dataset('../IOD_detrend_new/vegetation_mask.nc')
vegetation_mask = data_vegetation_mask.variables['land_cover'][:,:]

tropics_mask = vegetation_mask != 1
savanna_mask = vegetation_mask != 2
warm_temperate_mask = vegetation_mask != 3
cool_temperate_mask = vegetation_mask != 4
mediterranean_mask = vegetation_mask !=5
desert_mask = vegetation_mask !=6
total_mask = vegetation_mask > 6
total_mask = total_mask < 0

def mask(var, veg_mask, modelname, time_res, scaled):
    if var in ('temp', 'prec'):
        GRIDAREA = nc.Dataset(pathwayIN+'/prec/gridarea.nc')    
        gridarea = GRIDAREA.variables['cell_area'][:,:]    
        gridarea_masked = np.ma.array(gridarea, 
                                      mask = gridarea*veg_mask[np.newaxis,:,:])
        
        if scaled == True:
            DATA = nc.Dataset(pathwayIN+var+'/'+var+
                              '_1901-2015_'+time_res+'_australia.nc')  
        else:
            DATA = nc.Dataset(pathwayIN+var+'/'+var+
                              '_1901-2015_anomaly_'+time_res+'_australia.nc')            
        
    else:
        if scaled == True:
            DATA = nc.Dataset(pathwayIN+var+'/sh_year/'+modelname+'_S2_'+var+
                              '_australia_'+time_res+'_area_weighted.nc')
        else:
            DATA = nc.Dataset(pathwayIN+var+'/sh_year/'+modelname+'_S2_'+var+
                              '_australia_anomaly_'+time_res+'_area_weighted.nc')
    
    timeseries_data = []
    if time_res == 'annual': 
        data = DATA.variables[var][60:114,:,:]   
        data_masked = np.ma.array(data, mask = data*veg_mask[np.newaxis,:,:])        
        for i in range(0,54):
            if var in ('temp', 'prec'):
                sum_data = data_masked[i,:,:].sum()
                sum_gridarea = gridarea_masked[:,:].sum()
                mean_data = sum_data/sum_gridarea
                timeseries_data.append(mean_data)
            else:
                sum_data = data_masked[i,:,:].sum()                 
                timeseries_data.append(sum_data)
    else:
        for i in range(0,648):
            data = DATA.variables[var][720:1368,:,:]   
            data_masked = np.ma.array(data, mask = data*veg_mask[np.newaxis,:,:]) 
            if var in ('temp', 'prec'):
                sum_data = data_masked[i,:,:].sum()
                sum_gridarea = gridarea_masked[:,:].sum()
                mean_data = sum_data/sum_gridarea
                timeseries_data.append(mean_data)
            else:
                sum_data = data_masked[i,:,:].sum()                 
                timeseries_data.append(sum_data)
                
    if scaled == True:
        timeseries_data_scaled = (timeseries_data - min(timeseries_data))/ \
                                 (max(timeseries_data) - min(timeseries_data))
        return(timeseries_data_scaled)
    else:
        return(timeseries_data)
    
# Predictors
PPT = mask('prec', total_mask, 'CABLE-POP', 'annual', True)
TEMP = mask('temp', total_mask, 'CABLE-POP', 'annual', True)

df_clim = pd.DataFrame(TEMP, columns=['temp'])
df_clim['prec'] = PPT

# Target values in separate dataframe
GPP = mask('gpp', total_mask, 'CABLE-POP', 'annual', True)
NBP = mask('nbp', total_mask, 'CABLE-POP', 'annual', True)
RA = mask('ra', total_mask, 'CABLE-POP', 'annual', True)
RH = mask('rh', total_mask, 'CABLE-POP', 'annual', True)

df_carbon = pd.DataFrame(GPP, columns=['gpp'])
df_carbon['nbp'] = NBP
df_carbon['ra'] = RA
df_carbon['rh'] = RH

x = df_clim
y = df_carbon['rh']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, 
                                                    random_state=9)

lin_reg_mod = LinearRegression()
model = lin_reg_mod.fit(x_train, y_train)
pred = lin_reg_mod.predict(x_test)

print(model.score(x,y))
print(model.coef_)
