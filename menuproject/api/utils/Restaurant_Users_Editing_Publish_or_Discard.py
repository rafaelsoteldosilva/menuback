from ..models import Restaurant, Category, Dish, Restaurant_User
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from django.db.models import F
from typing import Dict, Any
from django.db.models import Q
from .Useful_procedures import Useful_procedures


# methods should receive the restaurant object, not just the id


class Restaurant_Users_Editing_Publish_or_Discard:
    def discard_restaurant_users_editing(self, my_restaurant):
        try:
            all_users = Restaurant_User.objects.filter(restaurant=my_restaurant.id)
            all_users.filter(recently_created=True).delete()
            all_users = Restaurant_User.objects.filter(restaurant=my_restaurant.id)
            if all_users.exists():
                all_users.update(
                    private_name="",
                    # private_phone="",
                    private_image_id=-1,
                    private_password="",
                    private_email="",
                    private_email_validated=False,
                    # private_phone_validated=False,
                    marked_for_deletion=False,
                    recently_created=False,
                    has_been_modified=False,
                )

            my_restaurant.users_edition_is_pending = False

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

    def publish_restaurant_users_editing(self, my_restaurant):
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
        if not my_restaurant.users_edition_is_pending:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You haven't started the edition",
            }

        try:
            all_users = Restaurant_User.objects.filter(restaurant=my_restaurant.id)
            all_users.filter(marked_for_deletion=True).delete()
            all_users = Restaurant_User.objects.filter(restaurant=my_restaurant.id)
            if all_users.exists():
                for user in all_users:
                    # Check if public_image_id is being updated
                    if user.public_image_id != user.private_image_id:
                        # Update image use count for old and new public_image_id
                        Useful_procedures.procedure_update_image_use_count(
                            user.public_image_id, user.private_image_id
                        )
                all_users.update(
                    public_name=F("private_name"),
                    # public_phone=F("private_phone"),
                    public_image_id=F("private_image_id"),
                    public_password=F("private_password"),
                    public_email=F("private_email"),
                    public_email_validated=F("private_email_validated"),
                    # public_phone_validated=F("private_phone_validated"),
                    private_name="",
                    # private_phone="",
                    private_image_id=-1,
                    private_password="",
                    private_email="",
                    private_email_validated=False,
                    # private_phone_validated=False,
                    marked_for_deletion=False,
                    recently_created=False,
                    has_been_modified=False,
                )

            my_restaurant.users_edition_is_pending = False
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
