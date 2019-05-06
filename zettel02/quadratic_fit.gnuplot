# Input options
set datafile separator ","

# Fitting a quadratic function
f(x) = a*x**2 + b*x + c
fit f(x) 'quadratic.txt' using 1:2 via a,b,c

plot  'quadratic.txt' using 1:2 title 'data', f(x) title "fit"

# Output options
set title "Quadratic function :)"
set xrange [-110:110]
set yrange [-10:21000]
set xlabel "x"
set ylabel "y"
set output "quadratic_fit.pdf"
set terminal pdf enhanced color
replot
