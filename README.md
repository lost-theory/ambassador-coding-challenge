# My submission

This is for the "back-end track" solution. I chose Python 3, the latest version of Django and DRF, and psycopg2 and gunicorn for running the app on Heroku.

I chose to implement the links & click tracking using Link and Click models (see [models.py](https://github.com/lost-theory/ambassador-coding-challenge/blob/master/tracker/links/models.py)). Each new click is recorded as a separate row in the clicks table, storing the user's IP address and potentially other request metadata in the future. This will scale better than trying to keep a counter on a single row in the links table (which introduces write lock contention for that one row). To scale beyond this you could use a [distributed or sharded counter](https://cloud.google.com/appengine/articles/sharding_counters) (if counts need to be close to real-time), or use an [event logging](https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying) model where counts are calculated periodically using an [ETL process](https://en.wikipedia.org/wiki/Extract%2C_transform%2C_load).

The REST and user-facing views (see [views.py](https://github.com/lost-theory/ambassador-coding-challenge/blob/master/tracker/links/views.py)) are pretty straightforward, the only tricky part was writing custom SQL to pull in the counts and a custom [serializer](https://github.com/lost-theory/ambassador-coding-challenge/blob/master/tracker/links/serializers.py) to render them in the REST API.

I wrote a [test suite](https://github.com/lost-theory/ambassador-coding-challenge/blob/master/tracker/links/tests.py) covering three areas: the model layer, the REST views, and the user-facing views.

How to run and test the Django application locally (with some example output):

```bash
# Initial setup
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

The app is running on Heroku here:

* https://amb-exercise.herokuapp.com/
* API browser for the link resource: https://amb-exercise.herokuapp.com/links/
* Example redirect: https://amb-exercise.herokuapp.com/wolverines/ (visiting this URL will cause the click count to go up by one)
* Example of a custom landing page: https://amb-exercise.herokuapp.com/landing/?link=wolverines
* Example of a default landing page: https://amb-exercise.herokuapp.com/landing/?link=lions

Original README is here:

* https://github.com/GetAmbassador/coding-challenge/blob/master/README.md
