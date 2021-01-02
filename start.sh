#!/bin/bash
nohup python start.py &
python -m flask run --host=0.0.0.0
