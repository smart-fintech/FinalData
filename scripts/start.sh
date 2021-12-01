cd /home/ubuntu/smartdotcheck

# Download config
aws s3 cp s3://intelligere-configs/production/production.env .env

# nohup gunicorn config.wsgi >& /dev/null &
# gunicorn config.wsgi --daemon
nohup gunicorn config.wsgi >& /dev/null &
