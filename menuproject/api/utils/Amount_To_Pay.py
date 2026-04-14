#
from datetime import datetime, date
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal, ROUND_HALF_UP
from ..models import Global_Price, Country, Restaurant
from .Constants_and_strings import *
import calendar
from rest_framework.decorators import api_view

def app_total_cost(price_type):
    try:
        global_price: Global_Price = Global_Price.objects.get(id=1)
    except Global_Price.DoesNotExist:
        return -1
    
    if price_type == FULL_PRICE:
        payment_value = global_price.full_price or 0  # Ensure it's not None
    elif price_type == MINIMUM_PRICE:
        payment_value = global_price.minimum_price or 0  # Ensure it's not None
    else:
        return -1
    
    return Decimal(payment_value)

def converted_app_total_cost(price_type, my_country):   
    payment_value = Decimal(app_total_cost(price_type))
    converted_value = 0
    if (payment_value != None):
        converted_value = payment_value * (
            my_country.exchange_rate 
            if my_country and my_country.exchange_rate is not None 
            else Decimal('1.0')
        )
    return Decimal(converted_value)
    
def app_total_cost_existing_restaurant(my_restaurant):  
    return app_total_cost(my_restaurant.price_type)

def converted_app_total_cost_existing_restaurant(my_restaurant):
    try:
        my_country = Country.objects.get(pk=my_restaurant.public_country.id) # type: ignore
    except Country.DoesNotExist:
        return -1
        
    return converted_app_total_cost(my_restaurant.price_type, my_country)

def converted_app_total_cost_non_existing_restaurant(price_type, country_name):   
    try:
        my_country = Country.objects.get(name=country_name) # type: ignore
    except Country.DoesNotExist:
        return -1
    return converted_app_total_cost(price_type, my_country)

def app_total_cost_non_existing_restaurant(price_type):
    return app_total_cost(price_type)