from ..models import (
    Restaurant,
    Promotion,
    Category,
    Dish,
    Restaurant_User,
    Restaurant_Delivery_Company,
)
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from django.db.models import F
from typing import Dict, Any
from django.db.models import Q

from .Constants_and_strings import *

# methods should receive the restaurant object, not just the id


class Promotions_Editing_Publish_or_Discard:
    def discard_promotions_editing(self, my_restaurant):
        try:
            promotions = Promotion.objects.filter(restaurant=my_restaurant.id)
            promotions.filter(recently_created=True).delete()
            promotions = Promotion.objects.filter(restaurant=my_restaurant.id)
            if promotions.exists():
                promotions.update(
                    private_name="",
                    private_attractor_text="",
                    private_promotion_text="",
                    recently_created=False,
                    has_been_modified=False,
                    marked_for_deletion=False,
                )

            my_restaurant.promotions_edition_is_pending = False

            my_restaurant.save()
            return {
                "return_code": status.HTTP_200_OK,
                "message": f"You have discarded changes",
            }

        except Exception as e:
            return {
                "return_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }

    def publish_promotions_editing(self, my_restaurant):
        if my_restaurant.currently_logged_in == -1:
            # No one is logged in
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You are not logged in",
            }

        if my_restaurant.dont_allow_further_actions_from_this_user:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You can't perform any actions, please logout",
            }
        if not my_restaurant.promotions_edition_is_pending:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You haven't started the edition",
            }

        try:
            promotions = Promotion.objects.filter(restaurant=my_restaurant.id)
            promotions.filter(marked_for_deletion=True).delete()
            promotions = Promotion.objects.filter(restaurant=my_restaurant.id)

            if promotions.exists():
                promotions.update(
                    public_name=F("private_name"),
                    private_name="",
                    public_attractor_text=F("private_attractor_text"),
                    private_attractor_text="",
                    public_promotion_text=F("private_promotion_text"),
                    private_promotion_text="",
                    recently_created=False,
                    has_been_modified=False,
                    marked_for_deletion=False,
                )

            my_restaurant.promotions_edition_is_pending = False
            my_restaurant.save()
            return {
                "return_code": status.HTTP_200_OK,
                "message": f"Your updates were performed succesfully",
            }

        except Exception as e:
            # If any exception occurs, the transaction is rolled back automatically
            return {
                "return_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }
