import pysftp as sftp

pathwayLOCAL = '/srv/ccrc/data02/z5227845/research/TRENDY/'
def sftpgrab(var, exp):
    s = sftp.Connection(xxx, username=yyy, password=zzz)
   
    remotepath_cable='/output/CABLE-POP/'+exp+'/CABLE-POP_'+exp+'_'+var+'.nc.gz'
    remotepath_class_ctem='/output/CLASS-CTEM/'+exp+'/CLASS-CTEM_'+exp+'_monthly_'+var+'.nc'   
    remotepath_clm='/output/CLM5.0/'+exp+'/CLM5.0_'+exp+'_'+var+'.nc'
    remotepath_dlem='/output/DLEM/'+exp+'/DLEM_'+exp+'_'+var+'.nc'
    remotepath_isam='/output/ISAM/'+exp+'/ISAM_'+exp+'_'+var+'.nc.gz'
    remotepath_jsbach='/output/JSBACH/'+exp+'/JSBACH_'+exp+'_'+var+'.nc'
    remotepath_jules='/output/JULES/'+exp+'/JULES_'+exp+'_'+var+'.nc.bz2'
    remotepath_lpj='/output/LPJ/'+exp+'/LPJ_'+exp+'_'+var+'.nc'
    remotepath_lpj_guess='/output/LPJ-GUESS/'+exp+'/LPJ-GUESS_'+exp+'_'+var+'.nc'
    remotepath_lpx='/output/LPX-Bern/'+exp+'/LPX_'+exp+'_'+var+'.nc'
    remotepath_ocn='/output/OCN/'+exp+'/OCN_'+exp+'_'+var+'.nc'
    remotepath_orchidee='/output/ORCHIDEE/'+exp+'/ORCHIDEE_'+exp+'_'+var+'.nc'
    remotepath_orchidee_cnp='/output/ORCHIDEE-CNP/'+exp+'/ORCHIDEE-CNP_'+exp+'_'+var+'.nc'
    remotepath_sdgvm='/output/SDGVM/'+exp+'/SDGVM_'+exp+'_'+var+'.nc.gz'
    remotepath_surfex='/output/SURFEX/'+exp+'/SURFEX_'+exp+'_'+var+'.nc'
    remotepath_visit='/output/VISIT/'+exp+'/VISIT_'+exp+'_'+var+'.nc.gz'
        
    localpath_cable=pathwayLOCAL+exp+'/'+var+'/CABLE-POP_'+exp+'_'+var+'.nc.gz'  
    localpath_class_ctem=pathwayLOCAL+exp+'/'+var+'/CLASS-CTEM_'+exp+'_'+var+'.nc'  
    localpath_clm=pathwayLOCAL+exp+'/'+var+'/CLM5.0_'+exp+'_'+var+'.nc'   
    localpath_dlem=pathwayLOCAL+exp+'/'+var+'/DLEM_'+exp+'_'+var+'.nc'
    localpath_isam=pathwayLOCAL+exp+'/'+var+'/ISAM_'+exp+'_'+var+'.nc.gz'
    localpath_jsbach=pathwayLOCAL+exp+'/'+var+'/JSBACH_'+exp+'_'+var+'.nc'
    localpath_jules=pathwayLOCAL+exp+'/'+var+'/JULES_'+exp+'_'+var+'.nc.bz2'
    localpath_lpj=pathwayLOCAL+exp+'/'+var+'/LPJ_'+exp+'_'+var+'.nc'
    localpath_lpj_guess=pathwayLOCAL+exp+'/'+var+'/LPJ-GUESS_'+exp+'_'+var+'.nc'
    localpath_lpx=pathwayLOCAL+exp+'/'+var+'/LPX_'+exp+'_'+var+'.nc'
    localpath_ocn=pathwayLOCAL+exp+'/'+var+'/OCN_'+exp+'_'+var+'.nc'
    localpath_orchidee=pathwayLOCAL+exp+'/'+var+'/ORCHIDEE_'+exp+'_'+var+'.nc'
    localpath_orchidee_cnp=pathwayLOCAL+exp+'/'+var+'/ORCHIDEE-CNP_'+exp+'_'+var+'.nc'
    localpath_sdgvm=pathwayLOCAL+exp+'/'+var+'/SDGVM_'+exp+'_'+var+'.nc.gz'
    localpath_surfex=pathwayLOCAL+exp+'/'+var+'/SURFEX_'+exp+'_'+var+'.nc'
    localpath_visit=pathwayLOCAL+exp+'/'+var+'/VISIT_'+exp+'_'+var+'.nc.gz'
    
    rem_paths = (remotepath_cable, remotepath_class_ctem, remotepath_clm, 
                 remotepath_dlem, remotepath_isam, remotepath_jsbach, 
                 remotepath_jules, remotepath_lpj, remotepath_lpj_guess, 
                 remotepath_lpx, remotepath_ocn, remotepath_orchidee, 
                 remotepath_orchidee_cnp, remotepath_sdgvm, remotepath_surfex, 
                 remotepath_visit)

    loc_paths = (localpath_cable, localpath_class_ctem, localpath_clm, 
                 localpath_dlem, localpath_isam, localpath_jsbach, 
                 localpath_jules, localpath_lpj, localpath_lpj_guess, 
                 localpath_lpx, localpath_ocn, localpath_orchidee, 
                 localpath_orchidee_cnp, localpath_sdgvm, localpath_surfex, 
                 localpath_visit)
    
    for r,l in zip(rem_paths, loc_paths):
        try:
            s.get(r,l, preserve_mtime=True)
        except (NameError, FileNotFoundError):
            print(r+' not found')
  
    s.close()

sftpgrab('mrso', 'S2')
