from ..models import Restaurant, Category, Dish
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from django.db.models import F
from typing import Dict, Any
from django.db.models import Q


class check_current_user_id_and_random:
    def check_current_user_id_and_random(self, my_restaurant, user_id, user_random) -> bool:
        if not user_id or not user_random:
            return Response(False) # type: ignore

        if (user_id == my_restaurant.currently_logged_in) and (
            user_random == my_restaurant.logged_in_user_random_number
        ):
            return Response(True) # type: ignore
        else:
            return Response(False) # type: ignore
