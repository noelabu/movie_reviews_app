from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from movie_reviews import views


urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('search/', views.search, name="search"),
    path('logout/', LogoutView.as_view(), name="logout")
    
]