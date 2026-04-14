from ..models import Restaurant, Category, Dish, Review, Review_Rejection
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from django.db.models import F
from typing import Dict, Any
from django.db.models import Q


class Reviews_Editing_Publish_or_Discard:
    def discard_reviews_editing(self, my_restaurant):
        try:
            all_reviews = Review.objects.filter(restaurant=my_restaurant)
        except Review.DoesNotExist:
            pass
        else:
            for review in all_reviews:
                if not review.public_rejected:
                    try:
                        review_rejection = Review_Rejection.objects.get(review=review)
                    except Review_Rejection.DoesNotExist:
                        pass
                    else:
                        review_rejection.delete()
            all_reviews.update(
                private_rejected=False, rejection_status_just_changed=False
            )

        my_restaurant.reviews_updates_are_pending = False
        my_restaurant.save()
        return {
            "return_code": status.HTTP_200_OK,
            "message": f"You have discarded changes",
        }

    def publish_reviews_editing(self, my_restaurant):
        if my_restaurant.currently_logged_in == -1:
            # No one is logged in
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "Nobody is logged in !!!",
            }

        if my_restaurant.dont_allow_further_actions_from_this_user:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You can't perform any action, please logout",
            }
        if not my_restaurant.reviews_updates_are_pending:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You didn't start updating reviews",
            }

        try:
            all_reviews = Review.objects.filter(restaurant=my_restaurant.id)

            if all_reviews.exists():
                all_reviews.update(
                    public_rejected=F("private_rejected"),
                )
                for review in all_reviews:
                    if not review.public_rejected:
                        try:
                            corresponding_rejection = Review_Rejection.objects.get(
                                review=review
                            )
                        except Review_Rejection.DoesNotExist:
                            pass
                        else:
                            corresponding_rejection.delete()

            all_reviews.update(
                private_rejected=False, rejection_status_just_changed=False
            )

            my_restaurant.reviews_updates_are_pending = False
            my_restaurant.save()
            return {
                "return_code": status.HTTP_200_OK,
                "message": f"Your revisions were performed succesfully",
            }

        except Exception as e:
            # If any exception occurs, the transaction is rolled back automatically
            print(f"{str(e)}")
            return {
                "return_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }
