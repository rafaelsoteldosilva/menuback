from ..models import Restaurant, Category, Dish
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from django.db.models import F
from typing import Dict, Any
from django.db.models import Q


class Menu_Sort_Editing_Publish_or_Discard:
    def discard_menu_sort_editing(self, my_restaurant):
        try:
            all_categories = Category.objects.filter(restaurant=my_restaurant.id)
            if all_categories.exists():
                all_categories.update(
                    private_name="",
                    private_description="",
                    private_image_id=-1,
                    private_view_order=None,
                    has_been_modified=False,
                )
                all_dishes = Dish.objects.filter(category__in=all_categories)
                if all_dishes.exists():
                    all_dishes.update(
                        private_name="",
                        private_description="",
                        private_image_id=-1,
                        private_price=0.0,
                        private_view_order=None,
                        has_been_modified=False,
                    )

            my_restaurant.menu_sorting_is_pending = False
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

    def publish_menu_sort_editing(self, my_restaurant):
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
        if not my_restaurant.menu_sorting_is_pending:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You haven't started the sorting",
            }

        try:
            # categories will have all the Restaurant's categories
            all_categories = Category.objects.filter(restaurant=my_restaurant.id)

            # Proceed with the rest
            all_categories.filter().update(
                private_name="",
                private_description="",
                private_image_id=-1,
                public_view_order=F("private_view_order"),
            )

            all_categories.filter().update(
                private_view_order=None, has_been_modified=False
            )

            # all_dishes will have all_categories dishes
            all_dishes = Dish.objects.filter(category__in=all_categories)

            # Proceed with the rest
            all_dishes.filter().update(
                private_name="",
                private_description="",
                private_image_id=-1,
                private_price=0.0,
                public_view_order=F("private_view_order"),
            )

            all_dishes.filter().update(private_view_order=None, has_been_modified=False)

            my_restaurant.menu_sorting_is_pending = False
            my_restaurant.save()
            return {
                "return_code": status.HTTP_200_OK,
                "message": f"Your sort was performed succesfully",
            }

        except Exception as e:
            # If any exception occurs, the transaction is rolled back automatically
            return {
                "return_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }
