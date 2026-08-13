#!/bin/bash

FILE="Backup-`date +%d-%m-%y-%H:%M:%S`"

tar -cvf /home/vkp/Desktop/bash/$FILE /home/vkp/Desktop/bash/

scp /home/vkp/Desktop/bash/$FILE vkp@192.168.43.64:/home/vkp/backups
