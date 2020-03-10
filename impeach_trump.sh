#!/usr/bin/env bash

set -e

PATH=$PATH:/usr/local/bin

source /home/dnck/bernie_bro/bin/activate

python /home/dnck/bernie_bro/bernie_bro.py trump

deactivate
