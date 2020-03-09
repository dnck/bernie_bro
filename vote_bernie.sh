#!/usr/bin/env bash

set -e

echo $PATH >> /home/<user>/bernie_bro/log.log

PATH=$PATH:/usr/local/bin

source /home/dnck/<user>/bin/activate

echo $PATH >> /home/<user>/bernie_bro/log.log

python /home/<user>/bernie_bro/bernie_bro.py

deactivate