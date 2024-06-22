Link al video de Youtube donde se ve el funcionamiento de la web.

https://www.youtube.com/watch?v=NsP3uFwcaDw

python -m venv myenv

source myenv/bin/activate  # En macOS y Linux

myenv\Scripts\activate     # En Windows

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver