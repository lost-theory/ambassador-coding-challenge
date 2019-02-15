# My submission

This is for the "back-end track" solution.

How to run and test the Django application (with some example output):

```bash
$ python3 -mvenv env
$ env/bin/pip install -r requirements.txt
$ cd tracker
$ ../env/bin/python manage.py migrate
$ ../env/bin/python manage.py createsuperuser --email admin@example.com --username admin
$ ../env/bin/python manage.py runserver
Starting development server at http://127.0.0.1:8000/

# Making requests to the REST API:
$ curl -s http://127.0.0.1:8000/links/ -d'{"title": "wolverines", "url": "http://127.0.0.1:8000/wolverines"}' -H "Content-type: application/json"
{"title":"wolverines","url":"http://127.0.0.1:8000/wolverines","creation_date":"2019-02-15T22:28:22.340138Z","last_modified_date":"2019-02-15T22:28:22.340180Z"}
$ curl -s http://127.0.0.1:8000/links/
[{"title":"wolverines","url":"http://127.0.0.1:8000/wolverines","creation_date":"2019-02-15T22:28:22.340138Z","last_modified_date":"2019-02-15T22:28:22.340180Z","clicks":0}]

# Running tests:
$ ../env/bin/python manage.py test
...........
----------------------------------------------------------------------
Ran 11 tests in 0.217s

OK
```

Original README is here:

https://github.com/GetAmbassador/coding-challenge/blob/master/README.md
