import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt

pathwayIN_trendy = '../../TRENDY/IOD_detrend_new/gpp/obs/'
pathwayIN_gosif = '/srv/ccrc/data02/z5227845/research/SIF/Australia/'
 
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
fig.subplots_adjust(wspace=0.19)
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
    if modelname in ('GOSIF-GPP', 'GOSIF-GPP_SD'):
        data_model = nc.Dataset(pathwayIN_gosif+'GOSIF_'+var+
                                '_australia_climatology_area_weighted.nc')        
        model = data_model.variables['Band1'][:,:,:]   
    else:
        data_model = nc.Dataset(pathwayIN_trendy+modelname+'_S2_'+var+
                            '_australia_climatology_area_weighted.nc')
        model = data_model.variables[var][:,:,:]   
       
    model_masked = np.ma.array(model, 
                                mask = model*veg_mask[np.newaxis,:,:])
    
    timeseries_model = []
    
    for i in range(0,12):
        sum_model = model_masked[i,:,:].sum()                 
        timeseries_model.append(sum_model)
    
    return(timeseries_model)
          
model_names = ['CABLE-POP', 'CLASS-CTEM', 'CLM5.0', 'DLEM', 'ISAM', 'JSBACH', 
               'LPJ', 'LPJ-GUESS', 'LPX', 'OCN', 'ORCHIDEE', 'ORCHIDEE-CNP', 
               'SURFEX', 'VISIT']
colours = ['teal', 'coral', 'green', 'crimson', 'orchid', 'sienna', 'aqua', 
           'grey', 'plum', 'blue', 'goldenrod', 'purple', 'navy', 'yellowgreen'] 

titles = ['Total', 'Tropics', 'Savanna', 'Warm temperate', 'Cool temperate', 
          'Mediterranean', 'Desert']
veg_masks = [total_mask, tropics_mask, savanna_mask, warm_temperate_mask, 
             cool_temperate_mask, mediterranean_mask, desert_mask]

axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax8]

time = np.arange(1,13)
idx = [6,7,8,9,10,11,0,1,2,3,4,5]  

for vegm, ax in zip(veg_masks, axes):     
    for mn, c in zip(model_names, colours):
        annual = mask('gpp', vegm, mn)
        ax.plot(time, np.array(annual)[idx], color = c, lw = 2.0, label = mn)

for vegm, ax, t in zip(veg_masks, axes, titles):     
    annual_gosif = mask('GPP', vegm, 'GOSIF-GPP')
    annual_gosif_sd = mask('GPP_SD', vegm, 'GOSIF-GPP_SD')
    
    annual_upper = np.array(annual_gosif) + np.array(annual_gosif_sd)
    annual_lower = np.array(annual_gosif) - np.array(annual_gosif_sd)

    ax.plot(time, np.array(annual_gosif)[idx], color = 'k', lw = 4.0, 
            label = 'GOSIF-GPP')
    ax.fill_between(time, annual_upper[idx], annual_lower[idx], color = 'k', 
                    alpha = 0.3)
    ax.set_xticks(time)
    ax.set_title(t)

xlabels = ['J', 'A', 'S', 'O', 'N', 'D', 'J', 'F', 'M', 'A','M', 'J']    
for ax in (ax4, ax6, ax8):
    ax.set_xticklabels(xlabels)   
for ax in (ax1, ax2, ax3, ax5):
    ax.set_xticklabels([])

ax1.set_ylabel('GPP [PgC mon-1]')
ax4.set_ylabel('GPP [PgC mon-1]')
ax8.set_ylabel('GPP [PgC mon-1]')

ax1.legend(loc='upper center', bbox_to_anchor=(1.55, -2.5), ncol=7)
plt.show()   

# plt.savefig('seasonal_GPP_australia_trendy.png', dpi = 400)   
