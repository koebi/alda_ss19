set datafile separator ","
plot  'quadratic.txt' using 1:2 title 'data'

set title "Quadratic data?"
set xrange [-110:110]
set yrange [-10:21000]
set xlabel "x"
set ylabel "y"
set output "quadratic.pdf"
set terminal pdf enhanced color
replot
