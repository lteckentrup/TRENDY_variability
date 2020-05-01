import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

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

fig = plt.figure(figsize=(12,10))

fig.subplots_adjust(hspace=0.20)
fig.subplots_adjust(wspace=0.15)
fig.subplots_adjust(top=0.95)
fig.subplots_adjust(bottom=0.12)
fig.subplots_adjust(right=0.99)
fig.subplots_adjust(left=0.06)

plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = "Helvetica"
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['font.size'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

ax1 = fig.add_subplot(3,3,1)
ax2 = fig.add_subplot(3,3,2)
ax3 = fig.add_subplot(3,3,3)
ax4 = fig.add_subplot(3,3,4)
ax5 = fig.add_subplot(3,3,5)
ax6 = fig.add_subplot(3,3,6)
ax8 = fig.add_subplot(3,3,8)


def mask(var, veg_mask, modelname):
    if var in ('temp', 'prec'):
        DATA = nc.Dataset(pathwayIN+var+'/'+var+
                          '_1901-2015_anomaly_annual_australia.nc')    
        data = DATA.variables[var][60:114,:,:] 

        GRIDAREA = nc.Dataset(pathwayIN+'/prec/gridarea.nc')    
        gridarea = GRIDAREA.variables['cell_area'][:,:]    
        gridarea_masked = np.ma.array(gridarea, 
                                      mask = gridarea*veg_mask[np.newaxis,:,:])
    else:
        DATA = nc.Dataset(pathwayIN+var+'/sh_year/'+modelname+'_S2_'+var+
                          '_anomaly_area_weighted.nc')
        data = DATA.variables[var][60:114,:,:]   
    
    data_masked = np.ma.array(data, mask = data*veg_mask[np.newaxis,:,:])
    
    timeseries_data = []
    
    for i in range(0,54):
        if var in ('temp', 'prec'):
            sum_data = data_masked[i,:,:].sum()
            sum_gridarea = gridarea_masked[:,:].sum()
            mean_data = sum_data/sum_gridarea
            timeseries_data.append(mean_data)
        else:
            sum_data = data_masked[i,:,:].sum()                 
            timeseries_data.append(sum_data)
    
    return(timeseries_data)
 
def regression_magic(met_var, model_var, modelname, veg_mask, ax):
    model = mask(model_var, veg_mask, modelname)
    met = mask(met_var, veg_mask, modelname)
    
    corr, p_value = pearsonr(met, model)
    met = np.array(met).reshape(-1,1)
            
    ### Linear regression    
    reg = LinearRegression()  
    reg.fit(met, model)
    Y_pred = reg.predict(met)
    
    # ### Information about linear regression model
    X2 = sm.add_constant(met)
    est = sm.OLS(model, X2)
    est2 = est.fit()
    # print(est2.summary())
    
    ### Plot
    ax.plot(met.reshape(-1,1), Y_pred.reshape(-1,1), lw=2.0, ls="-")
          
axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax8]
veg_masks = [total_mask, tropics_mask, savanna_mask, warm_temperate_mask, 
             cool_temperate_mask, mediterranean_mask, desert_mask]
titles = ['Total', 'Tropics', 'Savanna', 'Warm temperate', 'Cool temperate', 
          'Mediterranean', 'Desert']

modelz = ['CABLE-POP', 'CLASS-CTEM', 'CLM5.0', 'DLEM', 'ISAM', 'JSBACH', 
               'LPJ', 'LPJ-GUESS', 'LPX', 'OCN', 'ORCHIDEE', 'ORCHIDEE-CNP', 
               'SDGVM', 'SURFEX', 'VISIT']
colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 
           'tab:brown', 'tab:pink', 'tab:grey', 'tab:olive', 'tab:cyan', 
           'coral', 'goldenrod', 'purple', 'navy', 'darkslategrey']  


for a, vm, t in zip(axes, veg_masks, titles):
    for m, c in zip(modelz, colours):
        regression_magic('prec', 'gpp', m, vm, a)
    a.set_title(t)

for ax in (ax4, ax6, ax8):
    ax.set_xlabel('PPT [mm yr-1]')

for ax in (ax1, ax4, ax8):
    ax.set_ylabel('GPP [PgC yr-1]')

ax1.legend(loc='upper center', bbox_to_anchor=(1.55, -2.5), ncol=7)
plt.show()   

# veg_vars = ['gpp', 'nbp', 'ra', 'rh']
# met_vars = ['prec', 'temp']
# veg_labels = ['GPP [PgC yr-1]', 'NBP [PgC yr-1]', 'Ra [PgC yr-1]', 
#               'Rh [PgC yr-1]']
# met_labels = ['PPT [mm yr-1]', 'T [$^\circ$C yr-1]']

# for mv, ml in zip(met_vars, met_labels):
#     for vv, vl in zip(veg_vars, veg_labels):
#         for a, vm, t in zip(axes, veg_masks, titles):
#             for m, c in zip(modelz, colours):
#                 regression_magic('prec', 'gpp', m, vm, a)

        # plt.savefig('regression_annual_australian_anomalies_'+mv+'_'+
        #             vv+'_trendy.png', dpi = 600)
        # plt.clf()

# os.system("convert regression_annual_australian_anomalies_prec_nbp_trendy.png \
#           regression_annual_australian_anomalies_prec_gpp_trendy.png \
#           regression_annual_australian_anomalies_prec_ra_trendy.png \
#           regression_annual_australian_anomalies_prec_rh_trendy.png \
#           regression_anomalies_precipitation.pdf")

# os.system("convert regression_annual_australian_anomalies_temp_nbp_trendy.png \
#           regression_annual_australian_anomalies_temp_gpp_trendy.png \
#           regression_annual_australian_anomalies_temp_ra_trendy.png \
#           regression_annual_australian_anomalies_temp_rh_trendy.png \
#           regression_anomalies_temperature.pdf")
          
# for v in veg_vars:
#     os.remove(regression_annual_australian_anomalies_prec_'+v+'_trendy.png') 
#     os.remove(regression_annual_australian_anomalies_temp_'+v+'_trendy.png') 
