### Comparison with GOSIF-GPP
for model in CABLE-POP OCN ORCHIDEE-CNP ORCHIDEE SDGVM; do
    cdo -b F64 -L -selyear,2000/2017 -remapycon,../fine_grid.txt -invertlat \
         ../../S2_new/gpp/$model'_'S2_gpp.nc obs/$model'_'S2_gpp_2000-2017.nc
done

for model in CLM5.0 SURFEX; do
    cdo -b F64 -L -selyear,2000/2017 -remapycon,../fine_grid.txt \
         ../../S2_new/gpp/$model'_'S2_gpp.nc obs/$model'_'S2_gpp_2000-2017.nc
done

for model in ISAM LPJ LPJ-GUESS LPX; do
    cdo -b F64 -L -selyear,2000/2017 ../../S2_new/gpp/$model'_'S2_gpp.nc \
    obs/$model'_'S2_gpp_2000-2017.nc
done

for model in DLEM VISIT; do
    cdo -b F64 -L -selyear,2000/2017 -invertlat ../../S2_new/gpp/$model'_'S2_gpp.nc \
    obs/$model'_'S2_gpp_2000-2017.nc
done

for model in CABLE-POP CLM5.0 DLEM ISAM LPJ-GUESS LPJ LPX OCN ORCHIDEE-CNP ORCHIDEE SURFEX VISIT; do
    cdo -b F64 -L -divc,1e+12 -ymonmean -selyear,2001/2017 -mulc,86400 -muldpm \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 \
        -mul obs/$model'_'S2_gpp_2000-2017.nc -gridarea \
        obs/$model'_'S2_gpp_2000-2017.nc \
        obs/$model'_'S2_gpp_australia_climatology_area_weighted.nc

    cdo -b F64 -L -divc,1e+12 -yearsum -mulc,86400 -muldpm \
        -settaxis,2000-01-01,00:00,1month -seldate,2000-07-16,2017-06-16 \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 \
        -mul obs/$model'_'S2_gpp_2000-2017.nc -gridarea \
        obs/$model'_'S2_gpp_2000-2017.nc \
        obs/$model'_'S2_gpp_australia_area_weighted.nc
done

module unload cdo
module load cdo/1.6.1

for model in CLASS-CTEM JSBACH; do
    cdo -b F64 -L -selyear,2000/2017 -remapcon,../fine_grid.txt \
         ../../S2_new/gpp/$model'_'S2_gpp.nc obs/$model'_'S2_gpp_2000-2017.nc
done

for model in CLASS-CTEM JSBACH; do
    cdo -b F64 -L -divc,1e+12 -ymonmean -selyear,2001/2017 -mulc,86400 -muldpm \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 \
        -mul obs/$model'_'S2_gpp_2000-2017.nc -gridarea \
        obs/$model'_'S2_gpp_2000-2017.nc \
        obs/$model'_'S2_gpp_australia_climatology_area_weighted.nc

    cdo -b F64 -L -divc,1e+12 -yearsum -mulc,86400 -muldpm \
        -settaxis,2000-01-01,00:00,1month -seldate,2000-07-16,2017-06-16 \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 \
        -mul obs/$model'_'S2_gpp_2000-2017.nc -gridarea \
        obs/$model'_'S2_gpp_2000-2017.nc \
        obs/$model'_'S2_gpp_australia_area_weighted.nc
done

module unload cdo
module load cdo
