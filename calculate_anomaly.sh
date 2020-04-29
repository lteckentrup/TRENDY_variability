for model in CLASS-CTEM CLM5.0 ISAM JSBACH JULES LPJ-GUESS LPJ LPX SURFEX; do
    cdo -b F64 -L -ymonmean -selyear,1960/2017 \
         ../../S2_new/gpp/$model'_'S2_gpp.nc \
        $model'_'S2_gpp_climatology.nc
    cdo selyear,1901/2017 ../../S2_new/gpp/$model'_'S2_gpp.nc \
        $model'_'S2_gpp_1901-2017.nc

    cdo -b F64 sub $model'_'S2_gpp_1901-2017.nc $model'_'S2_gpp_climatology.nc  \
        $model'_'S2_gpp_anomaly_trend.nc
    cdo -b F64 detrend $model'_'S2_gpp_anomaly_trend.nc \
        $model'_'S2_gpp_anomaly.nc
    rm $model'_'S2_gpp_anomaly_trend.nc
done

for model in CABLE-POP DLEM OCN ORCHIDEE-CNP ORCHIDEE VISIT; do
    cdo -b F64 -L -invertlat -ymonmean -selyear,1960/2017 \
        ../../S2_new/gpp/$model'_'S2_gpp.nc \
        $model'_'S2_gpp_climatology.nc
    cdo -b F64 -L -invertlat -selyear,1901/2017 \
        ../../S2_new/gpp/$model'_'S2_gpp.nc $model'_'S2_gpp.nc

    cdo -b F64 sub $model'_'S2_gpp.nc $model'_'S2_gpp_climatology.nc  \
        $model'_'S2_gpp_anomaly_trend.nc
    cdo -b F64 detrend $model'_'S2_gpp_anomaly_trend.nc \
        $model'_'S2_gpp_anomaly.nc
    rm $model'_'S2_gpp_anomaly_trend.nc
done

for model in CABLE-POP CLM5.0 OCN ORCHIDEE-CNP ORCHIDEE SURFEX; do
    mv $model'_'S2_gpp_anomaly.nc $model'_'S2_gpp_anomaly_original.nc
    cdo -b F64 remapycon,../fine_grid.txt $model'_'S2_gpp_anomaly_original.nc \
        $model'_'S2_gpp_anomaly.nc
done

for model in CABLE-POP CLM5.0 DLEM ISAM LPJ LPJ-GUESS LPX OCN ORCHIDEE-CNP ORCHIDEE SURFEX VISIT; do
        cdo -b F64 -L -divc,1e+12 -yearsum -settaxis,1901-01-01,00:00,1month \
        -seldate,1901-07-16,2017-06-16 \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 -mulc,86400 -muldpm \
        -mul $model'_'S2_gpp_anomaly.nc -gridarea \
        $model'_'S2_gpp_anomaly.nc \
        sh_year/$model'_'S2_gpp_anomaly_area_weighted.nc
done

module unload cdo
module load cdo/1.6.1

for model in CLASS-CTEM JSBACH; do
    mv $model'_'S2_gpp_anomaly.nc $model'_'S2_gpp_anomaly_original.nc
    cdo -b F64 remapcon,../fine_grid.txt $model'_'S2_gpp_anomaly_original.nc \
        $model'_'S2_gpp_anomaly.nc
done

for model in CLASS-CTEM JSBACH; do
        cdo -b F64 -L -divc,1e+12 -yearsum -settaxis,1901-01-01,00:00,1month \
        -seldate,1901-07-16,2017-06-16 \
        -sellonlatbox,112.25,153.75,-43.75,-10.25 -mulc,86400 -muldpm \
        -mul $model'_'S2_gpp_anomaly.nc -gridarea \
        $model'_'S2_gpp_anomaly.nc \
        sh_year/$model'_'S2_gpp_anomaly_area_weighted.nc
done

module unload cdo
module load cdo
