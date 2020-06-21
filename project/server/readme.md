The project is tournament system, implementing "all vs. all" tournament approach. The winner is the contestant with most wins.

Project is written in Django 3.
To run, you need to install requirements:
```
pip install -r requirements.txt
```

and install PostgreSQL, then configure database according to [database_setup.md](database_setup.md).

In `server/settings.py` you need to place key to Google Map API, and SMTP server and account credentials.

Then, prepare database by running:
```
python manage.py makemigrations
python manage.py migrate
```

and run the server using:
```
python manage.py runserver
```

the site should be available under [http://127.0.0.1:8000](http://127.0.0.1:8000).