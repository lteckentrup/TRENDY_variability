import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import netCDF4 as nc
import os

nino_years = [1965,1968,1969,1972,1976,1977,1982,1986,1987,1991,1994,1997,
              2002,2004,2006,2009,2015]

nina_years = [1964,1970,1973,1974,1975,1988,1989,1993,1998,1999,2000,2007,2008,
              2010,2011,2015] 

pIOD = [1961, 1963, 1972, 1982, 1983, 1995, 1997, 2002, 2006, 2012, 2015]
nIOD = [1960, 1964, 1974, 1981, 1989, 1992, 1996, 1998, 2010, 2014]
pathwayIN = '../../TRENDY/IOD_detrend_new/'

fig = plt.figure(figsize=(9, 11.5))

fig.subplots_adjust(hspace=0.20)
fig.subplots_adjust(wspace=0.18)
# fig.subplots_adjust(left =0.3)
fig.subplots_adjust(right= 0.99)
fig.subplots_adjust(bottom=0.15)
fig.subplots_adjust(top=0.93)

plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = "Helvetica"
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['font.size'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

ax1 = fig.add_subplot(4,2,1)
ax2 = fig.add_subplot(4,2,2)
ax3 = fig.add_subplot(4,2,3)
ax4 = fig.add_subplot(4,2,4)
ax5 = fig.add_subplot(4,2,5)
ax6 = fig.add_subplot(4,2,6)
ax7 = fig.add_subplot(4,2,7)
ax8 = fig.add_subplot(4,2,8)

data_prec = nc.Dataset('../../lpj_guess/runs/IOD_detrend/prec/sh_year/prec_1901-2015_anomaly_annual_australia.nc')    
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
    
def mask(var, veg_mask, modelname):
    data_model = nc.Dataset(pathwayIN+var+'/sh_year/'+modelname+'_S2_'+var+
                        '_anomaly_area_weighted.nc')

    model = data_model.variables[var][60:,:,:]    
       
    model_masked = np.ma.array(model, 
                               mask = model*veg_mask[np.newaxis,:,:])
    
    annual_model = []
    
    for i in range(0,56):
        year_model = model_masked[i,:,:].sum()                 
        annual_model.append(year_model)
    
    return(annual_model)
    
def boxplot(var, season, title, vegetation):
    
    annual_cable = mask(var, total_mask, 'CABLE-POP')
    annual_class_ctem = mask(var, total_mask, 'CLASS-CTEM')
    annual_clm = mask(var, total_mask, 'CLM5.0')
    annual_dlem = mask(var, total_mask, 'DLEM')
    annual_isam = mask(var, total_mask, 'ISAM')
    annual_jsbach = mask(var, total_mask, 'JSBACH')
    annual_lpj = mask(var, total_mask, 'LPJ')
    annual_lpj_guess = mask(var, total_mask, 'LPJ-GUESS')
    annual_lpx = mask(var, total_mask, 'LPX')
    annual_ocn = mask(var, total_mask, 'OCN')
    annual_orchidee = mask(var, total_mask, 'ORCHIDEE')
    annual_orchidee_cnp = mask(var, total_mask, 'ORCHIDEE-CNP')
    annual_surfex = mask(var, total_mask, 'SURFEX')
    annual_visit = mask(var, total_mask, 'VISIT')

    df = pd.DataFrame(annual_cable, columns = ['cable'])
    df['class_ctem'] = annual_class_ctem
    df['clm'] = annual_clm
    df['dlem'] = annual_dlem
    df['isam'] = annual_isam
    df['jsbach'] = annual_jsbach
    df['lpj_guess'] = annual_lpj_guess
    df['lpj'] = annual_lpj
    df['lpx'] = annual_lpx
    df['ocn'] = annual_ocn
    df['orchidee'] = annual_orchidee
    df['orchidee_cnp'] = annual_orchidee_cnp
    df['surfex'] = annual_surfex
    df['visit'] = annual_visit
    df['year'] = np.arange(1961,2017)
     
    df_prec = pd.DataFrame(data_prec.variables['prec'][60:,0,0], 
                           columns = ['prec'])
    df_prec['year'] = np.arange(1961,2015)
    df_prec_dry = df_prec.nsmallest(10, 'prec')
    dry_years = df_prec_dry['year'].tolist()
    
    df_prec_wet = df_prec.nlargest(10, 'prec')
    wet_years = df_prec_wet['year'].tolist()
        
    df_pIOD = df[df.year.isin(pIOD)]
    df_nIOD = df[df.year.isin(nIOD)]
    df_nino = df[df.year.isin(nino_years)]
    df_nina = df[df.year.isin(nina_years)]
    df_dry = df[df.year.isin(dry_years)]
    df_wet = df[df.year.isin(wet_years)]
    
    df_positive = df.mask(df <= 0, np.nan)
    df_negative = df.mask(df >= 0, np.nan)

    df_not_pIOD = df_negative[~df_negative.year.isin(pIOD)]
    df_neg = df_not_pIOD[~df_not_pIOD.year.isin(nino_years)]   
    
    df_not_nIOD = df_positive[~df_positive.year.isin(nIOD)]  
    df_pos = df_not_nIOD[~df_not_nIOD.year.isin(nina_years)]
          
    axes = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]   
    dataframes = [df_pIOD, df_nIOD, df_nino, df_nina, df_dry, df_wet, 
                  df_neg, df_pos]
    titles = ['pIOD', 'nIOD', 'El Nino', 'La Nina', 'Driest years', 
              'Wettest years', 'other negative', 'other positive']
    
    modelz = ['CABLE-POP', 'CLASS-CTEM', 'CLM', 'DLEM', 'ISAM', 'JSBACH', 
              'LPJ-GUESS', 'LPJ', 'LPX', 'OCN', 'ORCHIDEE', 'ORCHIDEE-CNP', 
              'SURFEX', 'VISIT']
    for a, d, t in zip(axes, dataframes, titles):
          boxplots = a.boxplot([d['cable'].dropna(), d['class_ctem'].dropna(), 
                                d['clm'].dropna(), d['dlem'].dropna(), 
                                d['isam'].dropna(), d['jsbach'].dropna(), 
                                d['lpj_guess'].dropna(), d['lpj'].dropna(),
                                d['lpx'].dropna(), d['ocn'].dropna(), 
                                d['orchidee'].dropna(), 
                                d['orchidee_cnp'].dropna(), 
                                d['surfex'].dropna(), d['visit'].dropna()],
                                  labels=modelz,
                                  widths = .7, patch_artist=True,                                  
                                  medianprops = dict(linestyle='-', linewidth=2, 
                                                    color='Yellow'),
                                  boxprops = dict(linestyle='--', linewidth=2, 
                                                  color='Black', 
                                                  facecolor='green', alpha=.7))
          a.set_title(t)
          a.axhline(linewidth=1, color='k', alpha = 0.5)
          
          boxplot1 = boxplots['boxes'][0]
          boxplot1.set_facecolor('teal')   
          boxplot2 = boxplots['boxes'][1]
          boxplot2.set_facecolor('coral')
          boxplot3 = boxplots['boxes'][2]
          boxplot3.set_facecolor('green')
          boxplot4 = boxplots['boxes'][3]
          boxplot4.set_facecolor('crimson')
          boxplot5 = boxplots['boxes'][4]        
          boxplot5.set_facecolor('orchid')
          boxplot6 = boxplots['boxes'][5]
          boxplot6.set_facecolor('sienna')
          boxplot7 = boxplots['boxes'][6]
          boxplot7.set_facecolor('aqua')
          boxplot8 = boxplots['boxes'][7]
          boxplot8.set_facecolor('grey')
          boxplot9 = boxplots['boxes'][8]
          boxplot9.set_facecolor('plum')
          boxplot10 = boxplots['boxes'][9]
          boxplot10.set_facecolor('blue')
          boxplot11 = boxplots['boxes'][10]
          boxplot11.set_facecolor('goldenrod')
          boxplot12 = boxplots['boxes'][11]
          boxplot12.set_facecolor('purple')
          boxplot13 = boxplots['boxes'][12]
          boxplot13.set_facecolor('navy')
          boxplot14 = boxplots['boxes'][13]
          boxplot14.set_facecolor('yellowgreen')
  
    ax1.set_xticklabels([])
    ax2.set_xticklabels([])
    ax3.set_xticklabels([])
    ax4.set_xticklabels([])
    ax5.set_xticklabels([])
    ax6.set_xticklabels([])
    ax7.set_xticklabels(labels=modelz, 
    		    rotation=90, ha='center')
    ax8.set_xticklabels(labels=modelz, 
    		    rotation=90, ha='center')
    
    ax1.set_ylabel(title)
    ax3.set_ylabel(title)
    ax5.set_ylabel(title)  
    ax7.set_ylabel(title)  
    
# boxplot('gpp', '', '', '')
# boxplot('ra', 'mra', '', '', '')
# boxplot('rh', '', '', '')
# boxplot('nbp', 'mnee', '', 'NEE anomaly [gC yr-1]', '')
# boxplot('gpp', 'mgpp', '', 'GPP anomaly [gC yr-1]', '')
# boxplot('ra', 'mra', '', 'Ra anomaly [gC yr-1]', '')
# boxplot('nbp', 'mnee', '', 'NEE anomaly [gC yr-1]', 'tropics_')
# boxplot('nbp', 'mnee', '', 'NEE anomaly [gC yr-1]', 'savanna_')
# boxplot('nbp', 'mnee', '', 'NEE anomaly [gC yr-1]', 'warm_temperate_')
# boxplot('nbp', 'mnee', '', 'NEE anomaly [gC yr-1]', 'cool_temperate_')
# boxplot('nbp', 'mnee', '', 'NEE anomaly [gC yr-1]', 'mediterranean_')
# boxplot('nbp', 'mnee', '', 'NEE anomaly [gC yr-1]', 'desert_')
# boxplot('gpp', '', '', 'tropics_')
# boxplot('gpp', '', '', 'savanna_')
# boxplot('gpp', '', '', 'warm_temperate_')
# boxplot('gpp', '', '', 'cool_temperate_')
# boxplot('gpp', '', '', 'mediterranean_')
# boxplot('gpp', '', '', 'desert_')

# plt.subplot_tool()
# plt.show()
vars_lpj = ['mgpp', 'mra', 'mrh', 'mnee']
vars_trendy = ['gpp', 'ra', 'rh', 'nbp']
titles = ['GPP anomaly [PgC yr-1]', 'Ra anomaly [PgC yr-1]', 
          'Rh anomaly [PgC yr-1]', 'NBP anomaly [PgC yr-1']

boxplot('gpp', 'annual', 'GPP anomaly \n [PgC yr-1]', '')
plt.suptitle('Australia')
plt.show()
# plt.savefig('boxplot_trendy_v7.png', dpi = 300)
# veg_types = ['', 'tropics_', 'savanna_', 'warm_temperate', 'cool_temperate',
#              'mediterranean_', 'desert_']
# veg_types_titles = ['Australia', 'Savanna', 'Warm Temperate', 'Cool temperate',
#                     'Mediterranean', 'Desert']

# veg_types = ['mediterranean_', 'desert_']
# veg_types_titles = ['Mediterranean', 'Desert']
# for vtypes, vtypest in zip(veg_types, veg_types_titles):
#     for vl, vt, t in zip(vars_lpj, vars_trendy, titles):
#         boxplot(vt, vl, 'annual', t, '')
#         plt.suptitle(vtypest)
#         plt.savefig(vt+'_'+vtypes+'anomaly_boxplot_trendy.png', dpi = 300)
#         plt.clf()
    
# os.system("convert mgpp_anomaly_boxplot_trendy.png \
#           mra_anomaly_boxplot_trendy.png \
#           mrh_anomaly_boxplot_trendy.png\
#           boxplot_trendy.pdf")
          
# for v in ('mgpp', 'mra', 'mrh', 'prec'):
#     os.remove(v+'_anomaly_boxplot.png') 
