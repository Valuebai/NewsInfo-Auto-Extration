
# nohup python3 -u  run.py > nohup.log 2>&1 &
nohup gunicorn -w 4 -b 0.0.0.0:8088 run:app > gunicorn.log 2>&1 &