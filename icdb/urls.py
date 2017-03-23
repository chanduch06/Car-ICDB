"""
URLs for the icdb project.
"""
from django.conf.urls import patterns, include,url

from cars.views import CarView

urlpatterns = patterns('',
   url(r'^cars/', include('cars.urls')),

)

