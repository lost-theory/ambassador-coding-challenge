from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'links', views.LinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('landing/', views.landing, name='landing'),
    path('<str:title>/', views.redirect_referral, name='redirect_referral'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
