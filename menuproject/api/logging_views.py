import os

from django.template import Template, Context
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from dateutil.parser import parse
from babel.dates import format_datetime
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import transaction
from django.db.models import F
import difflib
import random
from django.utils import timezone
from django.views.decorators.cache import never_cache

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("DJANGO_APP_NAME")

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL")

import cloudinary
import cloudinary.uploader
import cloudinary.api

config = cloudinary.config(
    cloud_name=os.environ["CLOUDINARY_NAME"],
    api_key=os.environ["CLOUDINARY_API_KEY"],
    api_secret=os.environ["CLOUDINARY_API_SECRET"],
    secure=True,
)

from .utils.Menu_Editing_Publish_or_Discard import Menu_Editing_Publish_or_Discard
from .utils.Menu_Sort_Editing_Publish_or_Discard import (
    Menu_Sort_Editing_Publish_or_Discard,
)
from .utils.Reviews_Editing_Publish_or_Discard import Reviews_Editing_Publish_or_Discard

from .utils.Preferences_Editing_Publish_or_Discard import (
    Preferences_Editing_Publish_or_Discard,
)

from .utils.Restaurant_Users_Editing_Publish_or_Discard import Restaurant_Users_Editing_Publish_or_Discard
from .utils.Restaurant_Deliveries_Editing_Publish_or_Discard import (
    Restaurant_Deliveries_Editing_Publish_or_Discard,
)
from .utils.Promotions_Editing_Publish_or_Discard import (
    Promotions_Editing_Publish_or_Discard,
)
from .utils.check_current_user_id_and_random import check_current_user_id_and_random
from .authorization_views import check_authorization

from .complete_objects.Menu_Class import Menu_Class
from .complete_objects.All_Reviews_Class import All_Reviews_Class
from .models import (
    Help_Atonn,
    Country,
    Delivery_Company,
    Payment_Option,
    Restaurant_Delivery_Company,
    Promotion,
    Restaurant,
    Category,
    Dish,
    Super_User,
    Restaurant_User,
    Review,
    Image,
    Rejection_Reason,
    Review_Rejection,
)
from .serializer import (
    Delivery_Company_Serializer,
    Payment_Option_Serializer,
    Restaurant_Delivery_Company_Serializer,
    Promotion_Serializer,
    Restaurant_Serializer,
    Category_Serializer,
    Dish_Serializer,
    Restaurant_User_Retrieve_Serializer,
    Restaurant_User_Update_or_Create_Serializer,
    Super_User_Serializer,
    Review_Serializer,
    Image_Serializer,
)

from .utils.Constants_and_strings import *


def Discard_all_editings(my_restaurant):

    performer = Menu_Editing_Publish_or_Discard()
    result = performer.discard_menu_editing(my_restaurant)

    performer = Menu_Sort_Editing_Publish_or_Discard()
    result = performer.discard_menu_sort_editing(my_restaurant)

    my_performer = Reviews_Editing_Publish_or_Discard()
    result = my_performer.discard_reviews_editing(my_restaurant)

    my_performer = Preferences_Editing_Publish_or_Discard()
    result = my_performer.discard_preferences_editing(my_restaurant)

    my_performer = Restaurant_Users_Editing_Publish_or_Discard()
    result = my_performer.discard_restaurant_users_editing(my_restaurant)

    my_performer = Restaurant_Deliveries_Editing_Publish_or_Discard()
    result = my_performer.discard_restaurant_deliveries_editing(my_restaurant)

    my_performer = Promotions_Editing_Publish_or_Discard()
    result = my_performer.discard_promotions_editing(my_restaurant)


# @csrf_protect
@never_cache 
@api_view(["PATCH"])
@transaction.atomic
def try_to_login_into_the_admin_area(
    request, restaurant_id
):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
        
    new_user_name = request.data['userName']
    new_user_password = request.data['userPassword']
    new_user_is_super = True
    new_user_id = -1
    super_user_password = ""
    user_password = ""
    current_user_name = ""
    if (new_user_name != "_____ Rafael Y Elsy _____") or (new_user_password != 'Chile.17'):
        new_user_is_super = False
    new_user_is_main = False
    if not new_user_is_super:
        my_restaurant_user = Restaurant_User.objects.filter(restaurant=my_restaurant, public_name=new_user_name)
        if not my_restaurant_user.exists():
            print(f"{USER_DOES_NOT_EXIST}")
            return Response(
                {"error": f"{USER_DOES_NOT_EXIST}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            my_restaurant_user = my_restaurant_user.first()
            new_user_is_main = my_restaurant_user.main_user # type: ignore
            new_user_id = my_restaurant_user.id # type: ignore
            user_password = my_restaurant_user.get_decrypted_public_password() # type: ignore
    print(f"new_user_password, user_password:: {new_user_password}, {user_password}")
    if (new_user_password == user_password) or (
        (new_user_password == super_user_password) and (new_user_is_super)
    ):
        if my_restaurant.currently_logged_in == -1:  # Nobody logged in
            return Response(
                {
                    "somebody_in": False,
                    "current_user_name": "",
                    "new_user_id": new_user_id,
                    "new_user_is_main": new_user_is_main,
                    "new_user_is_super": new_user_is_super,
                    "message": "",
                    "new_token": check_authorization_result["new_token"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            # my_restaurant.currently_logged_in != -1, then somebody is already logged in
            if my_restaurant.currently_logged_in != -10:
                my_current_user = Restaurant_User.objects.get(
                    id=my_restaurant.currently_logged_in
                )
                current_user_name = my_current_user.public_name
            else:
                current_user_name = APP_NAME
            if new_user_is_super:
                new_user_name = APP_NAME
            else:
                my_new_user = Restaurant_User.objects.get(id=new_user_id)
                new_user_name = my_new_user.public_name
            return Response(
                {
                    "somebody_in": True,
                    "current_user_name": current_user_name,
                    "new_user_id": new_user_id,
                    "new_user_is_main": new_user_is_main,
                    "new_user_is_super": new_user_is_super,
                    "message": "",
                    "new_token": check_authorization_result["new_token"],
                },
                status=status.HTTP_200_OK,
            )
    else:
        print(f"{BAD_CREDENTIALS}")
        return Response(
            {"error": f"{BAD_CREDENTIALS}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def Login(my_restaurant, new_user_id):
    try:
        new_user_id = int(new_user_id)
    except ValueError:
        print(f"Invalid new_user_id value: {new_user_id} (not an integer)")
        return Response(
            {"error": "Invalid new_user_id format"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    if new_user_id != -10:
        try:
            my_restaurant_user = Restaurant_User.objects.get(pk=new_user_id)
        except Restaurant_User.DoesNotExist:
            print(f"Restaurant_User with ID {new_user_id} does not exist")
            return Response(
                {"error": f"{USER_DOES_NOT_EXIST}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"Exception occurred while fetching Restaurant_User: {e}")
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    # The following code runs regardless of the new_user_id check
    current_time = timezone.now()
    my_restaurant.currently_logged_in = new_user_id
    my_restaurant.logged_in_time = timezone.localtime(current_time).strftime(
        "%Y-%m-%d:%H:%M:%S"
    )

    my_restaurant.logged_out_time = ""
    my_restaurant.logged_in_user_random_number = random.randint(1, 100000)

    # Only if new_user_id > -1
    if new_user_id > -1:
        my_restaurant_user.logged_in = True # type: ignore
        my_restaurant_user.last_logged_in = timezone.localtime(current_time).strftime( # type: ignore
            "%Y-%m-%d:%H:%M:%S"
        ) 
        my_restaurant_user.last_logged_out = "" # type: ignore
        my_restaurant_user.save() # type: ignore
        


# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def login_normally(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    new_user_id = request.data['newUserId']

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    Login(my_restaurant, new_user_id)
    my_restaurant.dont_allow_further_actions_from_this_user = False
    my_restaurant.save()
    return Response(
        {
            "message": f"{YOU_ARE_LOGGED_INTO_ADMIN_AREA}",
            "new_token": check_authorization_result["new_token"],
        },
        status=status.HTTP_200_OK,
    )


# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def login_no_further_actions(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    new_user_id = request.data['newUserId']

    Login(my_restaurant, new_user_id)

    my_restaurant.dont_allow_further_actions_from_this_user = True

    my_restaurant.save()

    return Response(
        {
            "message": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}",
            "new_token": check_authorization_result["new_token"],
        },
        status=status.HTTP_200_OK,
    )


@api_view(["PATCH"])
@transaction.atomic
def logout_from_admin_area(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    current_time = timezone.now()

    if my_restaurant.currently_logged_in == -1:
        return Response(
            {"message": f"{NO_USER_TO_LOGOUT}"},
            status=status.HTTP_200_OK,
        )

    if my_restaurant.currently_logged_in > -1:
        my_current_user = Restaurant_User.objects.get(
            pk=my_restaurant.currently_logged_in
        )
        my_current_user.logged_in = False
        my_current_user.last_logged_out = timezone.localtime(current_time).strftime(
            "%Y-%m-%d:%H:%M:%S"
        )
        my_current_user.save()

    my_restaurant.currently_logged_in = -1
    my_restaurant.logged_in_user_random_number = -1

    Discard_all_editings(my_restaurant)  # <--------------------- logging out

    my_restaurant.logged_out_time = timezone.localtime(current_time).strftime(
        "%Y-%m-%d:%H:%M:%S"
    )

    my_restaurant.dont_allow_further_actions_from_this_user = False

    my_restaurant.save()

    return Response(
        {
            "message": f"{CURRENT_LOGGED_IN_USER_WAS_LOGGED_OUT}",
            "new_token": check_authorization_result["new_token"],
        },
        status=status.HTTP_200_OK,
    )
