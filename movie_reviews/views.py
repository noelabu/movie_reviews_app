# -----------------------------------------------------------------------------------------------+
# Filename      : views.py                                                                        +
# Creation Date : 20220131                                                                       +                                                                  +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Imports / Functions / Modules                                                                  +
# -----------------------------------------------------------------------------------------------+
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect

# Django authentication and login imports
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Forms imports
from .forms import LoginForm, SignUpForm, SearchForm

# Database imports
from .models import BookmarkedReviews

# Class for Reviews retrieval using NYT Movie Reviews API
from movie_reviews.api.reviews import MovieReviews

# Application Functions imports
from movie_reviews.util import bookmark_it, refresh_bookmarked_list
# -----------------------------------------------------------------------------------------------+
# Global Variables                                                                               +
# -----------------------------------------------------------------------------------------------+
page = 0
# -----------------------------------------------------------------------------------------------+
# Local Functions                                                                                +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Main Code                                                                                      +
# -----------------------------------------------------------------------------------------------+
def user_login(request):
    # Login form
    form = LoginForm(request.POST or None)

    # Message
    msg = None

    if request.method == "POST":

        if form.is_valid():
            # Retrieve username and password
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Authentice user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})

def register(request):
    #Messages
    msg = None
    success = False
    if request.method == "POST":
        # Signup form
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Retrive username, email and passwords
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")

            # Authenticate user
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True

            return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

@login_required(login_url="/login/")
def index(request):

    # Initial variables
    global page 
    offset = (page) * 10 
    msg = None

    # Retrieve the reviews from the NYT API
    mv_reviews = MovieReviews()
    reviews = mv_reviews.load_reviews(offset)

    # Get the current user
    current_user = request.user

    # Search Form
    form = SearchForm(request.POST or None)

    if request.method == "POST":
        if request.POST.get("reviews_form") == "Search":
            if form.is_valid():
                # Retrieve searh/keyword in the form
                search_keywords = form.cleaned_data.get("search")
                return redirect('search', search_keywords=search_keywords)
            else:
                msg = "Keyword is not valid!"
        
        elif request.POST.get("reviews_form") == ">>":
            offset = (page + 1) * 10 
            page += 1

        # Bookmark reviews
        bookmark_it(request, reviews, current_user.username)
    # Retrieve additional reviews
    reviews = mv_reviews.load_reviews(offset)
    #Retrieve the reviews from thr Bookmarked database
    bookmarked = refresh_bookmarked_list(current_user.username)
    return render(request, "home/index.html", {"form":form, "reviews": reviews[:10], "bookmarked": bookmarked, "page": page})


@login_required(login_url="/login")
def search(request, search_keywords):
    # Search Form
    form = SearchForm(request.POST or None)
    msg = None

    # Get the current user
    current_user = request.user

    # Retrieve reviews from NYT Movie Reviews Search API
    mv_reviews = MovieReviews()
    reviews = mv_reviews.search(search_keywords)
    if request.method == "POST":
        if request.POST.get("reviews_form") == "Search":
            if form.is_valid():
                # Retrieve searh/keyword in the form
                search_keywords = form.cleaned_data.get("search")
                return redirect('search', search_keywords=search_keywords)
            else:
                msg = "Keyword is not valid!"
    
        # Bookmark reviews
        bookmark_it(request, reviews, current_user.username)
    # Retrieve the reviews from the Bookmarked Database
    bookmarked = refresh_bookmarked_list(current_user.username)
    return render(request, "home/search.html", {"form":form, "reviews": reviews, "bookmarked": bookmarked})

@login_required(login_url="/login/")
def bookmarks(request):
    msg = None
    # Retrieve current user
    current_user = request.user

    # Retriece bookmarked reviews from the database
    bookmarked = refresh_bookmarked_list(current_user.username)
    
    # Bookmark reviews
    bookmark_it(request, bookmarked, current_user.username)
    
     # Retrieve the reviews from the Bookmarked Database
    bookmarked = refresh_bookmarked_list(current_user.username)
    return render(request, "home/bookmarks.html", { "bookmarked":bookmarked })

# -----------------------------------------------------------------------------------------------+
# Footer                                                                                         +
# -----------------------------------------------------------------------------------------------+