# linelengths.awk: Count the number of lines of each length in a file
# MRR (and GitHub Copilot) 2024-11-30
{
    line_lengths[length($0)]++
    if(length($0) < 24) print NR ": " $0
}

END {
    for (len in line_lengths) {
        print "Length " len ": " line_lengths[len] " lines"
    }
}
