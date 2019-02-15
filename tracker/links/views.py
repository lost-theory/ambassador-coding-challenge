from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render

from rest_framework import viewsets

from .serializers import LinkSerializer
from .models import Link, Click

class LinkViewSet(viewsets.ModelViewSet):
    """
    REST API endpoint for links.
    """
    queryset = Link.objects.all().order_by('-creation_date')
    serializer_class = LinkSerializer

def redirect_referral(request, title):
    link = Link.objects.get(title=title)
    ip = request.META['REMOTE_ADDR'] # XXX: should use something like this in prod: https://pypi.org/project/django-xff/
    Click.objects.create(link=link, ip=ip)
    return HttpResponseRedirect(link.url)

def landing(request):
    link = request.GET.get('link')
    templates = ['links/landing_default.html']
    if link and link.isalnum() and Link.objects.filter(title=link):
        templates.insert(0, 'links/landing_{}.html'.format(link))
    return render(request, templates, {
        'link_title': link or 'Things',
    })
