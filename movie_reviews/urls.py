
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

import re
from movie_reviews import views


urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('nextpage/', views.nextpage, name='nextpage'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('search/<search_keywords>/', views.search, name="search"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('addbookmark/', views.addbookmark, name="addbookmark")
    
]