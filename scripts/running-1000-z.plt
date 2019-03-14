#!/usr/local/bin/gnuplot -persist
set terminal pdf
set output "../running-1000-z.pdf"

set datafile separator ","
set key autotitle columnhead
set xrange [0:1010]
set yrange [-8000:4000]
set xlabel 'Time Unit'
set ylabel '4.8mm/s^2'
plot '../data/running-1000.csv' u 4 w l title 'az-value'
