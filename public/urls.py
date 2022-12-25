from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

app_name = 'public'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<slug:url>/', (LinkDetail.as_view()), name='link_detail'),
    path('accounts/login/', Login.as_view(), name='login'),
    path('accounts/logout/', Logout.as_view(), name='logout'),
    path('link/add/', login_required(AddLink.as_view()), name='add_link'),
    path('category/<slug:url>/', LinksViewDateCategory.as_view(),
         name='link_category_list'),
    path('link/delete/', login_required(delete_link), name='delete_link'),
    path('link/search/', search_result, name='search'),
    
]
