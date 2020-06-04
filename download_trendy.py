import pysftp as sftp

pathwayLOCAL = '/srv/ccrc/data02/z5227845/research/TRENDY/'
def sftpgrab(var, exp, model, suffix):
    s = sftp.Connection(server, username=xxx, 
                        password=yyy)
    if model == 'CLASS-CTEM':
        if var == 'lai':
            remotepath='/output/'+model+'/'+exp+'/'+model+'_'+exp+'_monthly_perpft_'+var+suffix
            localpath=pathwayLOCAL+exp+'/'+var+'/'+model+'_'+exp+'_'+var+suffix
        else:
            remotepath='/output/'+model+'/'+exp+'/'+model+'_'+exp+'_monthly_'+var+suffix
            localpath=pathwayLOCAL+exp+'/'+var+'/'+model+'_'+exp+'_'+var+suffix
    elif model == 'LPX':
        remotepath='/output/'+model+'-Bern/'+exp+'/'+model+'_'+exp+'_'+var+suffix
        localpath=pathwayLOCAL+exp+'/'+var+'/'+model+'_'+exp+'_'+var+suffix
    elif model == 'ORCHIDEE-CNP':
        remotepath='/output/'+model+'/'+exp+'_new/'+model+'_'+exp+'_'+var+suffix
        localpath=pathwayLOCAL+exp+'/'+var+'/'+model+'_'+exp+'_'+var+suffix
    elif var == 'lai':
        if model in ('JSBACH', 'LPJ-GUESS'):
            remotepath='/output/'+model+'/'+exp+'/'+model+'_'+exp+'_'+var+'pft'+suffix
            localpath=pathwayLOCAL+exp+'/'+var+'/'+model+'_'+exp+'_'+var+suffix
        else:
            remotepath='/output/'+model+'/'+exp+'/'+model+'_'+exp+'_'+var+suffix
            localpath=pathwayLOCAL+exp+'/'+var+'/'+model+'_'+exp+'_'+var+suffix
    else:
        remotepath='/output/'+model+'/'+exp+'/'+model+'_'+exp+'_'+var+suffix
        localpath=pathwayLOCAL+exp+'/'+var+'/'+model+'_'+exp+'_'+var+suffix

    rem_paths = (remotepath)
    loc_paths = (localpath)
    
    try:
        s.get(rem_paths,loc_paths, preserve_mtime=True)
    except (NameError, FileNotFoundError):
        print(rem_paths+' not found')
  
    s.close()
    
modelz=['CABLE-POP', 'CLASS-CTEM', 'CLM5.0', 'DLEM', 'ISAM', 'JSBACH', 'JULES',
        'LPJ', 'LPJ-GUESS', 'LPX', 'OCN', 'ORCHIDEE', 'ORCHIDEE-CNP', 'SDGVM',
        'SURFEX', 'VISIT']
suffices=['.nc.gz', '.nc' , '.nc', '.nc', '.nc.gz', '.nc', '.nc.bz2', '.nc',
          '.nc', '.nc', '.nc', '.nc', '.nc', '.nc.gz', '.nc', '.nc.gz']

for m, s in zip(modelz, suffices):
    sftpgrab('mrso', 'S2', m, s)
