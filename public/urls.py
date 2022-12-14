from django.urls import path

from .views import *

app_name = 'public'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:url>/', (LinkDetail.as_view()), name='link_detail'),
]