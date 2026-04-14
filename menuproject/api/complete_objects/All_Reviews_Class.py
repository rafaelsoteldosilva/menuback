import datetime
from django.utils import timezone
import random
from django.db import models
from django.db.models import Avg
from ..models import (
    Restaurant,
    Review_Rejection,
    Review,
)
from ..serializer import (
    Review_Rejection_Serializer_For_All_Reviews,
    Review_Serializer,
)
from rest_framework import status

from ..utils.Useful_procedures import Useful_procedures


class All_Reviews_Class:
    def __init__(self):
        self.reviews = {}
        self.restaurant_was_read = True

    def Load_Reviews_And_Rejections_if_any(self, restaurant_id):
        try:
            my_restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            self.restaurant_was_read = False
        else:
            restaurant_reviews = Review.objects.filter(
                restaurant=restaurant_id
            ).order_by("-creation_date")

            reviews_data = []
            for review in restaurant_reviews:
                review_serializer = Review_Serializer(review)
                review_data = {"review": review_serializer.data}

                review_rejection = Review_Rejection.objects.filter(
                    review=review
                ).first()

                if review_rejection:
                    review_rejection_data = Review_Rejection_Serializer_For_All_Reviews(
                        review_rejection
                    ).data
                else:
                    review_rejection_data = {}

                review_data["review_rejection"] = review_rejection_data
                reviews_data.append(review_data)

            self.reviews["reviews"] = reviews_data
