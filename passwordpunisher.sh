#!/bin/bash
MATRIX="1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*"
LENGTH="$1"

while [ "${n:=1}" -le "$LENGTH" ]
do
    # echo ${VAR:POS:LENGTH}
    PASS="$PASS${MATRIX:$(($RANDOM%${#MATRIX})):1}"
    #${50:5:1}
    let n++
done

echo $PASS
