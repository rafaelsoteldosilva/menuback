from ..models import Restaurant, Restaurant_Delivery_Company, Category, Dish
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from django.db.models import F
from typing import Dict, Any
from django.db.models import Q
from .Useful_procedures import Useful_procedures


class Preferences_Editing_Publish_or_Discard:
    def discard_preferences_editing(self, my_restaurant):
        try:
            my_restaurant.private_name = ""
            my_restaurant.private_description = ""
            my_restaurant.private_address = ""
            my_restaurant.private_country = None
            my_restaurant.private_phone = ""
            my_restaurant.private_instagram_url = ""
            my_restaurant.private_facebook_url = ""
            my_restaurant.private_twitter_url = ""
            my_restaurant.private_website_url = ""
            my_restaurant.private_facade_image_id = -1
            my_restaurant.private_logo_image_id = -1
            my_restaurant.private_show_images = False
            my_restaurant.private_show_restaurant_reviews = True
            my_restaurant.private_show_dishes_reviews = True
            my_restaurant.private_currency_symbol = "CLP$"
            my_restaurant.private_show_prices = True
            my_restaurant.private_show_ask_button = True
            my_restaurant.private_monday_close_hour_in_minutes = 0
            my_restaurant.private_tuesday_close_hour_in_minutes = 0
            my_restaurant.private_wednesday_close_hour_in_minutes = 0
            my_restaurant.private_thursday_close_hour_in_minutes = 0
            my_restaurant.private_friday_close_hour_in_minutes = 0
            my_restaurant.private_saturday_close_hour_in_minutes = 0
            my_restaurant.private_sunday_close_hour_in_minutes = 0

            my_restaurant.preferences_edition_is_pending = False

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

    def publish_preferences_editing(self, my_restaurant):
        if my_restaurant.currently_logged_in == -1:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You are not logged in",
            }

        if my_restaurant.dont_allow_further_actions_from_this_user:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You can't perform any actions, please logout",
            }

        if not my_restaurant.preferences_edition_is_pending:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You haven't started the preference edition",
            }

        try:
            if (
                my_restaurant.public_facade_image_id
                != my_restaurant.private_facade_image_id
            ):
                Useful_procedures.procedure_update_image_use_count(
                    my_restaurant.public_facade_image_id,
                    my_restaurant.private_facade_image_id,
                )
            if (
                my_restaurant.public_logo_image_id
                != my_restaurant.private_logo_image_id
            ):
                Useful_procedures.procedure_update_image_use_count(
                    my_restaurant.public_logo_image_id,
                    my_restaurant.private_logo_image_id,
                )
            my_restaurant.public_name = my_restaurant.private_name
            my_restaurant.public_description = my_restaurant.private_description
            my_restaurant.public_address = my_restaurant.private_address
            my_restaurant.public_country = my_restaurant.private_country
            my_restaurant.public_phone = my_restaurant.private_phone
            my_restaurant.public_instagram_url = my_restaurant.private_instagram_url
            my_restaurant.public_facebook_url = my_restaurant.private_facebook_url
            my_restaurant.public_twitter_url = my_restaurant.private_twitter_url
            my_restaurant.public_website_url = my_restaurant.private_website_url
            my_restaurant.public_facade_image_id = my_restaurant.private_facade_image_id
            my_restaurant.public_logo_image_id = my_restaurant.private_logo_image_id
            my_restaurant.public_show_images = my_restaurant.private_show_images
            my_restaurant.public_show_restaurant_reviews = (
                my_restaurant.private_show_restaurant_reviews
            )
            my_restaurant.public_show_dishes_reviews = (
                my_restaurant.private_show_dishes_reviews
            )
            my_restaurant.public_show_prices = my_restaurant.private_show_prices
            my_restaurant.public_show_ask_button = my_restaurant.private_show_ask_button
            my_restaurant.public_monday_open_hour_in_minutes = (
                my_restaurant.private_monday_open_hour_in_minutes
            )
            my_restaurant.public_tuesday_open_hour_in_minutes = (
                my_restaurant.private_tuesday_open_hour_in_minutes
            )
            my_restaurant.public_wednesday_open_hour_in_minutes = (
                my_restaurant.private_wednesday_open_hour_in_minutes
            )
            my_restaurant.public_thursday_open_hour_in_minutes = (
                my_restaurant.private_thursday_open_hour_in_minutes
            )
            my_restaurant.public_friday_open_hour_in_minutes = (
                my_restaurant.private_friday_open_hour_in_minutes
            )
            my_restaurant.public_saturday_open_hour_in_minutes = (
                my_restaurant.private_saturday_open_hour_in_minutes
            )
            my_restaurant.public_sunday_open_hour_in_minutes = (
                my_restaurant.private_sunday_open_hour_in_minutes
            )
            my_restaurant.public_monday_close_hour_in_minutes = (
                my_restaurant.private_monday_close_hour_in_minutes
            )
            my_restaurant.public_tuesday_close_hour_in_minutes = (
                my_restaurant.private_tuesday_close_hour_in_minutes
            )
            my_restaurant.public_wednesday_close_hour_in_minutes = (
                my_restaurant.private_wednesday_close_hour_in_minutes
            )
            my_restaurant.public_thursday_close_hour_in_minutes = (
                my_restaurant.private_thursday_close_hour_in_minutes
            )
            my_restaurant.public_friday_close_hour_in_minutes = (
                my_restaurant.private_friday_close_hour_in_minutes
            )
            my_restaurant.public_saturday_close_hour_in_minutes = (
                my_restaurant.private_saturday_close_hour_in_minutes
            )
            my_restaurant.public_sunday_close_hour_in_minutes = (
                my_restaurant.private_sunday_close_hour_in_minutes
            )
            my_restaurant.private_name = ""
            my_restaurant.private_description = ""
            my_restaurant.private_schedule = ""
            my_restaurant.private_address = ""
            my_restaurant.private_country = None
            my_restaurant.private_phone = ""
            my_restaurant.private_instagram_url = ""
            my_restaurant.private_facebook_url = ""
            my_restaurant.private_twitter_url = ""
            my_restaurant.private_website_url = ""
            my_restaurant.private_facade_image_id = -1
            my_restaurant.private_logo_image_id = -1
            my_restaurant.private_show_images = False
            my_restaurant.private_show_restaurant_reviews = True
            my_restaurant.private_show_dishes_reviews = True
            my_restaurant.private_currency_symbol = "CLP$"
            my_restaurant.private_show_prices = True
            my_restaurant.private_show_ask_button = True
            my_restaurant.private_monday_close_hour_in_minutes = 0
            my_restaurant.private_tuesday_close_hour_in_minutes = 0
            my_restaurant.private_wednesday_close_hour_in_minutes = 0
            my_restaurant.private_thursday_close_hour_in_minutes = 0
            my_restaurant.private_friday_close_hour_in_minutes = 0
            my_restaurant.private_saturday_close_hour_in_minutes = 0
            my_restaurant.private_sunday_close_hour_in_minutes = 0
            my_restaurant.preferences_edition_is_pending = False
            my_restaurant.update_image_uses = True

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
