### Comparison with GOSIF-GPP
for model in CABLE-POP OCN ORCHIDEE-CNP ORCHIDEE SDGVM; do
    cdo -b F64 -L -selyear,1901/2017 -remapycon,../fine_grid.txt -invertlat \
         ../../S2/gpp/$model'_'S2_gpp.nc sh_year/$model'_'S2_gpp_1901-2017.nc
done

for model in CLM5.0 SURFEX; do
    cdo -b F64 -L -selyear,1901/2017 -remapycon,../fine_grid.txt \
         ../../S2/gpp/$model'_'S2_gpp.nc sh_year/$model'_'S2_gpp_1901-2017.nc
done

for model in ISAM LPJ LPJ-GUESS LPX; do
    cdo -b F64 -L -selyear,1901/2017 ../../S2/gpp/$model'_'S2_gpp.nc \
    sh_year/$model'_'S2_gpp_1901-2017.nc
done

for model in DLEM VISIT; do
    cdo -b F64 -L -selyear,1901/2017 -invertlat ../../S2/gpp/$model'_'S2_gpp.nc \
    sh_year/$model'_'S2_gpp_1901-2017.nc
done

for model in CABLE-POP CLM5.0 DLEM ISAM LPJ-GUESS LPJ LPX OCN ORCHIDEE-CNP ORCHIDEE SURFEX VISIT; do
    cdo -b F64 -L -divc,1e+12 -yearsum -mulc,86400 -muldpm \
        -settaxis,1901-01-01,00:00,1month -seldate,1901-07-01,2017-06-30 \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 \
        -mul sh_year/$model'_'S2_gpp_1901-2017.nc -gridarea \
        sh_year/$model'_'S2_gpp_1901-2017.nc \
        sh_year/$model'_'S2_gpp_australia_annual_area_weighted.nc
       
    cdo -b F64 -L -divc,1e+12 -mulc,86400 -muldpm \
        -settaxis,1901-01-01,00:00,1month -seldate,1901-07-01,2017-06-30 \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 \
        -mul sh_year/$model'_'S2_gpp_1901-2017.nc -gridarea \
        sh_year/$model'_'S2_gpp_1901-2017.nc \
        sh_year/$model'_'S2_gpp_australia_monthly_area_weighted.nc
done

for model in SDGVM; do
        cdo -b F64 -L -divc,1e+12 -yearsum -mulc,86400 -muldpm \
        -settaxis,1901-01-01,00:00,1month -seldate,1901-07-01,2017-06-30 \
        -sellonlatbox,292.25,333.75,-43.75,-10.25 \
        -mul sh_year/$model'_'S2_gpp_1901-2017.nc -gridarea \
        sh_year/$model'_'S2_gpp_1901-2017.nc \
        sh_year/$model'_'S2_gpp_australia_annual_area_weighted.nc
       
    cdo -b F64 -L -divc,1e+12  -mulc,86400 -muldpm \
        -settaxis,1901-01-01,00:00,1month -seldate,1901-07-01,2017-06-30 \
        -sellonlatbox,292.25,333.75,-43.75,-10.25 \
        -mul sh_year/$model'_'S2_gpp_1901-2017.nc -gridarea \
        sh_year/$model'_'S2_gpp_1901-2017.nc \
        sh_year/$model'_'S2_gpp_australia_monthly_area_weighted.nc
done

module unload cdo
module load cdo/1.6.1

for model in CLASS-CTEM JSBACH; do
    cdo -b F64 -L -selyear,1901/2017 -remapcon,../fine_grid.txt \
         ../../S2/gpp/$model'_'S2_gpp.nc sh_year/$model'_'S2_gpp_1901-2017.nc
done

for model in CLASS-CTEM JSBACH; do
    cdo -b F64 -L -divc,1e+12 -yearsum -mulc,86400 -muldpm \
        -settaxis,1901-01-01,00:00,1month -seldate,1901-07-01,2017-06-30 \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 \
        -mul sh_year/$model'_'S2_gpp_1901-2017.nc -gridarea \
        sh_year/$model'_'S2_gpp_1901-2017.nc \
        sh_year/$model'_'S2_gpp_australia_annual_area_weighted.nc

    cdo -b F64 -L -divc,1e+12 -mulc,86400 -muldpm \
        -settaxis,1901-01-01,00:00,1month -seldate,1901-07-01,2017-06-30 \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 \
        -mul sh_year/$model'_'S2_gpp_1901-2017.nc -gridarea \
        sh_year/$model'_'S2_gpp_1901-2017.nc \
        sh_year/$model'_'S2_gpp_australia_monthly_area_weighted.nc
done

module unload cdo
module load cdo
