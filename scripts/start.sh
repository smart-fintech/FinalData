cd /home/ubuntu/smartdotcheck

# nohup gunicorn config.wsgi >& /dev/null &
# gunicorn config.wsgi --daemon
nohup gunicorn config.wsgi >& /dev/null &
