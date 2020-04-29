for var in gpp lai rh ra nbp; do
    ncatted -O -a bounds,time,d,, $var'/'CLM5.0_S2_$var'_'original.nc \
                                  $var'/'CLM5.0_S2_$var'.'nc
    ncks -x -v latitude,longitude $var'/'CABLE-POP_S2_$var'_'original.nc \
                                  $var'/'test.nc
    ncrename -v x,lon -vy,lat $var'/'test.nc $var'/'test1.nc
    ncap2 -s 'time@calendar="standard"' $var'/'test1.nc \
                                        $var'/'CABLE-POP_S2_$var'.'nc
    rm $var'/'test.nc
    rm $var'/'test1.nc
done
