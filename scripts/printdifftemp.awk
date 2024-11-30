# printdifftemp.awk - given a file of thermostat data, print a line
# if the temperature setpoint changes from the previous line.
# MRR  2024-11-30  mostly by GitHub Copilot
# awk -f printdifftemp.awk thermostats.csv
BEGIN { FS = "," }
NR == 1 { prev = $9; print; next } 
$9 != prev { print; prev = $9 }
