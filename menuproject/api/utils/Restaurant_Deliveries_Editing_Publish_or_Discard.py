from ..models import (
    Restaurant,
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


class Restaurant_Deliveries_Editing_Publish_or_Discard:
    def discard_restaurant_deliveries_editing(self, my_restaurant):
        try:
            all_restaurant_deliveries = Restaurant_Delivery_Company.objects.filter(
                restaurant=my_restaurant.id
            )
            all_restaurant_deliveries.filter(recently_created=True).delete()
            all_restaurant_deliveries = Restaurant_Delivery_Company.objects.filter(
                restaurant=my_restaurant.id
            )
            if all_restaurant_deliveries.exists():
                all_restaurant_deliveries.update(
                    private_token="",
                    recently_created=False,
                    has_been_modified=False,
                    marked_for_deletion=False,
                )

            my_restaurant.restaurant_deliveries_edition_is_pending = False

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

    def publish_restaurant_deliveries_editing(self, my_restaurant):
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
        if not my_restaurant.restaurant_deliveries_edition_is_pending:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You haven't started the edition",
            }

        try:
            # all_restaurant_deliveries = Restaurant_Delivery_Company.objects.filter(
            #     restaurant=my_restaurant.id, private_token=""
            # )
            # if all_restaurant_deliveries.exists():
            #     return {
            #         "return_code": status.HTTP_406_NOT_ACCEPTABLE,
            #         "message": f"There still are elements without a token",
            #     }
            # all_restaurant_deliveries = Restaurant_Delivery_Company.objects.filter(
            #     restaurant=my_restaurant.id, private_token=f"{PROVISIONAL_VALUE}"
            # )
            # if all_restaurant_deliveries.exists():
            #     return {
            #         "return_code": status.HTTP_406_NOT_ACCEPTABLE,
            #         "message": f"There still are elements with a provisional value",
            #     }
            all_restaurant_deliveries = Restaurant_Delivery_Company.objects.filter(
                restaurant=my_restaurant.id
            )
            all_restaurant_deliveries.filter(marked_for_deletion=True).delete()
            all_restaurant_deliveries = Restaurant_Delivery_Company.objects.filter(
                restaurant=my_restaurant.id
            )

            if all_restaurant_deliveries.exists():
                all_restaurant_deliveries.update(
                    public_token=F("private_token"),
                    private_token="",
                    recently_created=False,
                    has_been_modified=False,
                    marked_for_deletion=False,
                )

            my_restaurant.restaurant_deliveries_edition_is_pending = False
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
