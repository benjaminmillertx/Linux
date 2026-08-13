#!/bin/bash

# Server load monitoring script

trigger=1.00

load=`cat /proc/loadavg | awk '{print $1}'`

response=`echo | awk -v T=$trigger L=$load 'BEGIN{if ( L > T ){ print "Greater"}}'`

if [[ $response = "Greater" ]]
then
    sar -q | mail -s "High server load - [ $load ]" benjaminmillerdev@gmail.com
fi
