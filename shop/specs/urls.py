from django.urls import path

from .views import BaseSpecView


urlpatterns = [
    path('', BaseSpecView.as_view(), name='base-spec'),
]
