import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd
from pylab import text

pathwayIN_trendy = '../../TRENDY/IOD_detrend_new/'
pathwayIN_gosif = ''

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

fig = plt.figure(figsize=(18,10))

fig.subplots_adjust(hspace=0.20)
fig.subplots_adjust(wspace=0.13)
fig.subplots_adjust(top=0.95)
fig.subplots_adjust(bottom=0.12)
fig.subplots_adjust(right=0.99)
fig.subplots_adjust(left=0.05)

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
                                '_australia_monthly_area_weighted_test.nc')
        model = data_model.variables['Band1'][:,:,:]
    elif modelname =='prec':
        data_model = nc.Dataset(pathwayIN_trendy+
                                'prec/obs/prec_australia_monthly_area_weighted.nc')
        model = data_model.variables['prec'][:,:,:]
    else:
        data_model = nc.Dataset(pathwayIN_trendy+'nbp/obs/'+modelname+'_S2_'+
                                var+'_australia_monthly_area_weighted.nc')
        model = data_model.variables[var][:,:,:]

    model_masked = np.ma.array(model,
                                mask = model*veg_mask[np.newaxis,:,:])

    timeseries_model = []

    for i in range(0,215):
        sum_model = model_masked[i,:,:].sum()
        timeseries_model.append(sum_model)

    return(timeseries_model)

model_names = ['CABLE-POP', 'CLASS-CTEM', 'CLM5.0', 'DLEM', 'ISAM', 'JSBACH',
                'LPJ', 'LPX', 'OCN', 'ORCHIDEE', 'ORCHIDEE-CNP',
                'SDGVM', 'SURFEX', 'VISIT']
colours = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
            'tab:brown', 'tab:pink', 'tab:olive', 'tab:cyan',
            'coral', 'gold', 'purple', 'navy', 'darkslategrey']

titles = ['Total', 'Tropics', 'Savanna', 'Warm temperate', 'Cool temperate',
          'Mediterranean', 'Desert']
veg_masks = [total_mask, tropics_mask, savanna_mask, warm_temperate_mask,
              cool_temperate_mask, mediterranean_mask, desert_mask]

axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax8]

time = np.arange(0,215)

for vegm, ax, t in zip(veg_masks, axes, titles):
    for mn, c in zip(model_names, colours):
        annual = mask('nbp', vegm, mn)
        ax.plot(time[89:126], np.cumsum(np.array(annual)[89:126])[:],
                color = c, lw = 2.0, linestyle = '--')
        # ax.set_xlim(106,130)
        ax.axhline(linewidth=1, color='k', alpha = 0.5)
        ax.set_title(t)

for vegm, ax, t in zip(veg_masks, axes, titles):
    for mn, c in zip(model_names, colours):
        annual = mask('nbp', vegm, mn)
        ax.plot(time[125:162], np.cumsum(np.array(annual)[125:162])[:],
                color = c, lw = 2.0, label = mn)
        # ax.set_xlim(106,130)
        ax.axhline(linewidth=1, color='k', alpha = 0.5)
        ax.set_title(t)

for ax in axes:
    ax.axvspan(125, 146, facecolor='tab:blue', alpha=0.5)
    ax.axvspan(89, 125, facecolor='tab:orange', alpha=0.5)
    ax.axvline(x=125, linewidth=2, color='k', alpha = 0.5)
    text(0.27, 0.85,'End of \n Millenium drought', ha='center', va='center',
         transform=ax.transAxes)
    text(0.62, 0.85,'2010-2012 \n'r'La Ni$\mathrm{\tilde{n}}$a', ha='center', va='center',
         transform=ax.transAxes)
for vegm, ax, t in zip(veg_masks, axes, titles):
    annual_prec = mask('prec', vegm, 'prec')

#xlabels = ['', '01/2010', '07/2010', '01/2011', '07/2011', '01/2012', '07/2012']
#xlabels = ['', '07/\'07', '01/\'08', '07/\'09', '01/\'10', '07/\'10', '01/\'11',
#           '07/\'11', '01/\'12', '07/\'12', '01/\'13', '07/\'13']
xlabels = ['', '07/\'07', '05/\'08', '03/\'09', '01/\'10', '11/\'10', '09/\'11',
           '07/\'12', '05/\'13']
for ax in (ax4, ax6, ax8):
    ax.set_xticklabels(xlabels)
for ax in (ax1, ax2, ax3, ax5):
    ax.set_xticklabels([])


ax1.set_ylabel('Cumulative NBP [PgC]')
ax4.set_ylabel('Cumulative NBP [PgC]')
ax8.set_ylabel('Cumulative NBP [PgC]')


ax1.legend(loc='upper center', bbox_to_anchor=(1.62, -2.6), ncol=7)
#plt.subplot_tool()
#plt.show()

plt.savefig('post_extreme_events.pdf')
