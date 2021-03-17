#!/bin/bash

this_file=`basename $0 .sh`

if [[ $# != 1 ]]; then
   echo ""
   echo "Usage: "
   echo "   $this_file.sh <<monitor-interval>>"
   echo ""
   echo "Where"
   echo "   monitor-interval      How frequent the device should be monitored in seconds"
   echo ""
   exit
fi

watch -n $1 -d "nmap -vv -n -sn -iL monitor-host.txt 2>/dev/null | 
    grep -i 'Nmap scan report for' | 
    cut -d ' ' -f 5-"

