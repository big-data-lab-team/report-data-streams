#!/usr/local/bin/gnuplot -persist
set terminal pdf
set output "../energy-measure-plot.pdf"

set datafile separator ","
set key autotitle columnhead
set xlabel '500 ms'
set ylabel 'mA'
plot for[i=1:14] '../data/EnergyUsageMeasure.csv' u i w l t columnhead(i)
