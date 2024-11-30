# reformattemps.awk - script to reformat the temperature data
# emitted by scrapeecobee.py.
# This needed due to an oddity of the Ecobee website, which 
# does not always present the thermostats in the same order.
# Sample input line:
# 2024-11-30 09:20:08,Downstairs,68,68,kalika,63,66,Upstairs,65,65
# Sample output line:
# 2024-11-30 09:20:08,kalika,63,66,Upstairs,65,65,Downstairs,68,68
#
# Usage: awk -f reformattemps.awk temps.csv > reformatted_temps.csv
#
# MRR 2024-11-30 partly by GitHub Copilot

BEGIN { FS = OFS = "," }

{
    if(length($0) > 24 ) {
        timestamp = $1
        kalika = ""
        upstairs = ""
        downstairs = ""

        for (i = 2; i <= NF; i += 3) {
            if ($i == "kalika") {
                kalika = $i OFS $(i+1) OFS $(i+2)
            } else if ($i == "Upstairs") {
                upstairs = $i OFS $(i+1) OFS $(i+2)
            } else if ($i == "Downstairs") {
                downstairs = $i OFS $(i+1) OFS $(i+2)
            }
        }

        print timestamp, kalika, upstairs, downstairs
    } else { 
        #print $0
        ignored++
    }
}

END {
    print "Ignored " ignored " lines" > "/dev/stderr"
}
