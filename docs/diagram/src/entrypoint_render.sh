#!/bin/sh
set -eu

eval "$(fixuid -q)"

eval d2  --omit-version -c --pad 0 init-diagram/lambda-init.d2 init-diagram/lambda-init.svg 
eval d2  --omit-version --animate-interval=3000 -c --pad 0 run-diagram/lambda-run.d2 run-diagram/lambda-run.svg 
