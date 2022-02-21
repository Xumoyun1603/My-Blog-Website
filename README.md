## This is my first website:

https://khumoyunblogs.herokuapp.com/

## How to start

Clone repository and install requirements in your virtual environment

```
pip install -r requirements.txt
```

and make migrations

```
python manage.py makemigrations engine
python manage.py migrate engine
```

To adding content you should create a categories but before that, create a superuser

```
python manage.py createsuperuser
```

Then start the site

```
python manage.py runserver
```
