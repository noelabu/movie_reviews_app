# -----------------------------------------------------------------------------------------------+
# Filename      : reviews.py                                                                     +
# Creation Date : 20220129                                                                       +
# Description   : This file contains the classes for the use of movie reviews API.               +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Imports / Functions / Modules                                                                  +
# -----------------------------------------------------------------------------------------------+
import os
import requests
import json

import pandas as pd
from decouple import config
# -----------------------------------------------------------------------------------------------+
# Global Variables                                                                               +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Local Functions                                                                                +
# -----------------------------------------------------------------------------------------------+

# -----------------------------------------------------------------------------------------------+
# Main Code                                                                                      +
# -----------------------------------------------------------------------------------------------+

class MovieReviews():

    def load_reviews(self, offset=0):
        """ load the reviews from the NYT Movie Reviews API using requests

        Args:
            offset (int, optional). Defaults to 20.

        Returns:
            list : list of reviews loaded from the ApI
        """
        url = "https://api.nytimes.com/svc/movies/v2/reviews/all.json"
        headers = {
        "Accept": "application/json"
        }
        data = {
            "offset": offset,
            "api-key" : config('API_KEY')
        }

        response = requests.get(url, headers=headers, params=data)
        report = response.json()
        return report["results"]

    def search (self, keyword):
        """loads the reviews from the Movie Reviews API given a certain keywordd

        Args:
            keyword (string): keyword to filter the reviews

        Returns:
            list : list of reviews loaded from the API
        """
        url = "https://api.nytimes.com/svc/movies/v2/reviews/search.json"
        headers = {
        "Accept": "application/json"
        }
        data = {
            "query" : keyword,
            "api-key" : config('API_KEY')
        }

        response = requests.get(url, headers=headers, params=data)
        report = response.json()
        return report["results"]



# -----------------------------------------------------------------------------------------------+
# Footer                                                                                         +
# -----------------------------------------------------------------------------------------------+