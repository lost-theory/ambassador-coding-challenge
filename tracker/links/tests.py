import django.db.utils
from django.test import TestCase
from django.urls import reverse

from .models import Link, Click

class LinksModelTests(TestCase):
    def test_create_link(self):
        l = Link.objects.create(title="wolverines", url="http://127.0.0.1:8000/wolverines/")
        assert l.title == 'wolverines'

    def test_create_link_uniqueness(self):
        l1 = Link.objects.create(title="wolverines", url="http://127.0.0.1:8000/wolverines/")
        with self.assertRaises(django.db.utils.IntegrityError):
            l2 = Link.objects.create(title="wolverines", url="http://127.0.0.1:8000/wolverines/")

    def test_create_click(self):
        l = Link.objects.create(title="wolverines", url="http://127.0.0.1:8000/wolverines/")
        c = Click.objects.create(link=l, ip='127.0.0.1')
        assert c.link == l

class LinksViewTests(TestCase):
    def test_redirect(self):
        l = Link.objects.create(title="wolverines", url="http://127.0.0.1:8000/wolverines/")
        res = self.client.get(reverse('redirect_referral', args=(l.title,)))
        assert res.status_code == 302
        assert res.url == l.url
