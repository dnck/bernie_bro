#!/usr/bin/env bash

set -e


echo $PATH >> /home/dnck/bernie_bro/log.log

PATH=$PATH:/usr/local/bin

source /home/dnck/bernie_bro/bin/activate

echo $PATH >> /home/dnck/bernie_bro/log.log

python /home/dnck/bernie_bro/bernie_bro.py

deactivate
