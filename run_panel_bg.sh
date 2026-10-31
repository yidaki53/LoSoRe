#!/bin/bash
cd "/home/robin/OneDrive/University and such/LoSoRe"
nohup python3 tools/pascal/e6_match.py --target stickman --panel --attempts 2 > panel_run.log 2>&1 &
echo "PID: $!"
echo "Started panel in background"
