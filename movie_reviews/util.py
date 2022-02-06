# -----------------------------------------------------------------------------------------------+
# Filename      : util.py                                                                        +
# Creation Date : 20220129                                                                       +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Imports / Functions / Modules                                                                  +
# -----------------------------------------------------------------------------------------------+
import os
import sys

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
def bookmark_it(request, reviews, username):
    """ save or remove the review to the database

    Args:
        request (): request page
        reviews (list): list of reviews in the page
        username (string): username of the current user
    """
    for i in range(10):
        button = "review_{}".format(i)
        remove_button = "reviewr_{}".format(i)
        if button in request.POST:
            b = BookmarkedReviews(user=username, reviews=reviews[i])
            b.save()
        elif remove_button in request.POST:
            b = BookmarkedReviews.objects.filter(user=username).filter(reviews=reviews[i])
            b.delete()

def refresh_bookmarked_list(username):
    """ retrieve the reviews from the bookmark database

    Args:
        username (string): username of the current user

    Returns:
        list : list of reviews in the Bookmarked database
    """
    bookmarked_reviews = list(BookmarkedReviews.objects.all().filter(user=username))
    bookmarked = [review.reviews for review in bookmarked_reviews]
    return bookmarked

# -----------------------------------------------------------------------------------------------+
# Footer                                                                                         +
# -----------------------------------------------------------------------------------------------+