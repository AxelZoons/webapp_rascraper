
from django.urls import path, include

from firstapp.views import home, running

urlpatterns = [
    path('', home, name='home'),
    path('runing', running, name='running')
]
