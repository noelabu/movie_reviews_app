# -----------------------------------------------------------------------------------------------+
# Filename      : util.py                                                                        +
# Creation Date : 20220129                                                                       +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Imports / Functions / Modules                                                                  +
# -----------------------------------------------------------------------------------------------+
import os
import sys
import json

from django.contrib.auth import get_user_model

from movie_reviews.api.reviews import MovieReviews
from .models import BookmarkedReviews
# -----------------------------------------------------------------------------------------------+
# Global Variables                                                                               +
# -----------------------------------------------------------------------------------------------+


# -----------------------------------------------------------------------------------------------+
# Local Functions                                                                                +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Main Code                                                                                      +
# -----------------------------------------------------------------------------------------------+

def refresh_bookmarked_list(request):
    """ retrieve the reviews from the bookmark database

    Args:
        username (string): username of the current user

    Returns:
        list : list of reviews in the Bookmarked database
    """
    bookmarked_reviews = list(BookmarkedReviews.objects.all().filter(user=request.user))
    bookmarked = [review.reviews for review in bookmarked_reviews]
    return bookmarked

def replace_string_to_json(string):
    """ converts the string to json

    Args:
        string

    Returns:
        json
    """
    try:
        s = string.replace('\t','')
        s = s.replace('\'', '\"')
        s = s.replace('\n','')
        s = s.replace(',}','}')
        s = s.replace(',]',']')
        s = s.replace('None', "null")
        return json.loads(s)
    except:
        return "None"


    
# -----------------------------------------------------------------------------------------------+
# Footer                                                                                         +
# -----------------------------------------------------------------------------------------------+