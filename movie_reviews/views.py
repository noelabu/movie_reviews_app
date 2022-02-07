# -----------------------------------------------------------------------------------------------+
# Filename      : views.py                                                                        +
# Creation Date : 20220131                                                                       +                                                                  +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Imports / Functions / Modules                                                                  +
# -----------------------------------------------------------------------------------------------+
import json

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
from .forms import LoginForm, SignUpForm, SearchForm, BookmarkForm

# Database imports
from .models import BookmarkedReviews

# Class for Reviews retrieval using NYT Movie Reviews API
from movie_reviews.api.reviews import MovieReviews

# Application Functions imports
from movie_reviews.util import refresh_bookmarked_list, replace_string_to_json
# -----------------------------------------------------------------------------------------------+
# Global Variables                                                                               +
# -----------------------------------------------------------------------------------------------+

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
    
    msg = None
    page = 0
    # Retrieve the reviews from the NYT API
    mv_reviews = MovieReviews()
    reviews = mv_reviews.load_reviews()

    # Get the current user
    current_user = request.user

    # Search Form
    form = SearchForm(request.POST or None)
    bookmark_form = BookmarkForm(request.POST or None)

    if request.method == "POST":
        if request.POST.get("reviews_form") == "Search":
            if form.is_valid():
                # Retrieve searh/keyword in the form
                search_keywords = form.cleaned_data.get("search")
                return redirect('search', search_keywords=search_keywords)
            else:
                msg = "Keyword is not valid!"

    #Retrieve the reviews from thr Bookmarked database
    bookmarked = refresh_bookmarked_list(request)
    return render(request, "home/index.html", {"form":form,"bookmark_form":bookmark_form, "reviews": reviews[:10], "bookmarked": bookmarked, "page": page})

@login_required(login_url="/login/")
def nextpage(request):
    # Search Form
    search_form = SearchForm(request.POST or None)

    # Bookmark Form
    bookmark_form = BookmarkForm(request.POST or None)

    # Page
    page = request.GET.get('page')
    page = int(page) + 1
    offset = (page*10)

    # Retrieve the reviews from the NYT API
    try:
        mv_reviews = MovieReviews()
        reviews = mv_reviews.load_reviews(offset)[:10]
    except KeyError:
        reviews = []
    
    if request.method == "POST":
        if request.POST.get("reviews_form") == "Search":
            if search_form.is_valid():
                # Retrieve searh/keyword in the form
                search_keywords = form.cleaned_data.get("search")
                return redirect('search', search_keywords=search_keywords)
            else:
                msg = "Keyword is not valid!"

    #Retrieve the reviews from thr Bookmarked database
    bookmarked = refresh_bookmarked_list(request)
    return render(request, "home/index.html", {"form":search_form,"bookmark_form":bookmark_form, "reviews": reviews, "bookmarked": bookmarked, "page": page})

@login_required(login_url="/login/")
def addbookmark(request):
    
    # Determine if remove or add bookmark
    button_type = request.GET.get('type')

    # Selected review
    review = request.GET.get('review')

    if request.method == "POST":

        # Bookmark Form
        bookmark_form = BookmarkForm(request.POST)

        if bookmark_form.is_valid():
            # get foldername
            foldername = bookmark_form.cleaned_data.get('foldername')
        else:
            # default foldername
            foldername = "Favorites"

    if button_type == "add_bookmark":

        # convert string to json
        review = replace_string_to_json(review)

        if review is not None:

            # Add review in Bookmarked Table
            b = BookmarkedReviews(user=request.user,folder=foldername, reviews=review)
            b.save()
    else:

        # convert string to json
        review = replace_string_to_json(review)

        if review is not None:

            # Remove review in Bookmarked Table
            b = BookmarkedReviews.objects.filter(user=request.user).filter(reviews=review)
            b.delete()

    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="/login")
def search(request, search_keywords):

    # Search Form
    form = SearchForm(request.POST or None)
    bookmark_form = BookmarkForm(request.POST or None)
    
    # Message 
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
    
    # Retrieve the reviews from the Bookmarked Database
    bookmarked = refresh_bookmarked_list(request)

    return render(request, "home/search.html", {"form":form,"bookmark_form":bookmark_form, "reviews": reviews, "bookmarked": bookmarked})

@login_required(login_url="/login/")
def bookmarks(request):

    # Retrieve current user
    current_user = request.user

    # Retrive distinct folder names
    folders = BookmarkedReviews.objects.order_by().values_list('folder', flat=True).distinct()
    folders = list(folders)
    bookmarked = {}

    for folder in sorted(folders, key=str.lower):
        bookmarked_reviews= list(BookmarkedReviews.objects.all().filter(user=request.user, folder=folder).exclude(reviews='None'))
        bookmarked[folder] = [review.reviews for review in bookmarked_reviews if review.reviews != 'None']
    
    bookmarked = {k:v for k,v in bookmarked.items() if len(v) != 0}
    return render(request, "home/bookmarks.html", {"folders":folders, "bookmarked":bookmarked })

# -----------------------------------------------------------------------------------------------+
# Footer                                                                                         +
# -----------------------------------------------------------------------------------------------+