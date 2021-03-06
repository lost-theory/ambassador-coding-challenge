import json

import django.db.utils
from django.test import TestCase
from django.urls import reverse

from .models import Link, Click

def make_link(title):
    url = "http://127.0.0.1:8000/landing/?link={}".format(title)
    return Link.objects.create(title=title, url=url)

class LinksModelTests(TestCase):
    def test_create_link(self):
        l = make_link('wolverines')
        assert l.title == 'wolverines'

    def test_create_link_uniqueness(self):
        l1 = make_link('wolverines')
        with self.assertRaises(django.db.utils.IntegrityError):
            l2 = make_link('wolverines')

    def test_create_click(self):
        l = make_link('wolverines')
        c = Click.objects.create(link=l, ip='127.0.0.1')
        assert c.link == l

class LinksViewTests(TestCase):
    def test_redirect(self):
        l = make_link('wolverines')
        res = self.client.get(reverse('redirect_referral', args=(l.title,)))
        assert res.status_code == 302
        assert res.url == l.url

    def test_redirect_causes_click_creation(self):
        l = make_link('wolverines')
        num_clicks = 10
        for i in range(num_clicks):
            self.client.get(reverse('redirect_referral', args=(l.title,)))
        clicks = Click.objects.all()
        assert len(clicks) == num_clicks
        assert all(c.link == l for c in clicks)

    def test_default_landing(self):
        l = make_link('lions')
        res = self.client.get(reverse('landing'), {'link': l.title})
        assert res.status_code == 200
        assert b"Lions are awesome" in res.content

    def test_custom_template_landing(self):
        l = make_link('wolverines')
        res = self.client.get(reverse('landing'), {'link': l.title})
        assert b"wolverines.jpg" in res.content

class LinksRestTests(TestCase):
    def test_list(self):
        l1 = make_link('wolverines')
        l2 = make_link('lions')
        res = self.client.get('/links/').json()
        assert len(res) == 2
        assert res[0]['title'] == l1.title
        assert res[0]['clicks'] == res[1]['clicks'] == 0
        assert res[1]['url'] == l2.url

    def test_list_with_clicks(self):
        l = make_link('wolverines')
        num_clicks = 3
        for i in range(num_clicks):
            Click.objects.create(link=l, ip='127.0.0.1')
        res = self.client.get('/links/').json()
        assert res[0]['clicks'] == num_clicks

    def test_create(self):
        res = self.client.post('/links/', json.dumps(dict(title='wings', url='https://www.nhl.com/redwings/')), content_type='application/json')
        assert res.status_code == 201
        assert res.json()['title'] == 'wings'

    def test_create_url_validation_failure(self):
        res = self.client.post('/links/', json.dumps(dict(title='wings', url='zzz')), content_type='application/json')
        assert res.status_code == 400
        assert 'Enter a valid URL.' in res.json()['url']
