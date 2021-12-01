cd /home/ubuntu/smartdotcheck

pkill gunicorn
pkill -P1 gunicorn

# install depedency
pip3 install -r requirements.txt

# Download config
aws s3 cp s3://intelligere-configs/production/production.env .env

python3 manage.py makemigrations
python3 manage.py migrate



