cd /home/ubuntu/smartdotcheck

pkill gunicorn
pkill -P1 gunicorn

# install depedency
pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate



