set datafile separator ","

# Komplexitäten
i(x) = a*x**2 + b*x + c
m(x) = d*x*log(x)/log(2) + e*x + f
q(x) = g*x*log(x)/log(2) + h*x + j

# Einstellungen für Plot
set title "Sortierverfahren im Vergleich - Anzahl Vergleiche"
set xrange [0:500]
set yrange [0:70000]
set xlabel "Arraygröße [n]"
set ylabel "# Vergleiche"
set output "sortComparisons.pdf"
set terminal pdf enhanced color

fit i(x) 'counts.txt' using 1:2 via a,b,c
fit m(x) 'counts.txt' using 1:3 via d,e,f
fit q(x) 'counts.txt' using 1:4 via g,h,j

# Plots für Vergleiche
plot 'counts.txt' using 1:2 with lines title 'insertionSort', i(x),\
     'counts.txt' using 1:3 with lines title 'mergeSort', m(x),\
     'counts.txt' using 1:4 with lines title 'quickSort', q(x)

# Einstellungen für Plot
set title "Sortierverfahren im Vergleich - Anzahl Vergleiche"
set xrange [0:500]
set yrange [0:0.02]
set xlabel "Arraygröße [n]"
set ylabel "Laufzeit [ms]"
set output "sortTimes.pdf"
set terminal pdf enhanced color

# Fits für Zetien
fit i(x) 'times.txt' using 1:2 via a,b,c
fit m(x) 'times.txt' using 1:3 via d,e,f
fit q(x) 'times.txt' using 1:4 via g,h,j

# Plots für Zeiten
plot 'times.txt' using 1:2 with lines title 'insertionSort', i(x),\
     'times.txt' using 1:3 with lines title 'mergeSort', m(x),\
     'times.txt' using 1:4 with lines title 'quickSort', q(x)
