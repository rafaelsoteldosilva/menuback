from datetime import datetime, date
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal, ROUND_HALF_UP
from ..models import Global_Price
from .Constants_and_strings import *
from .Amount_To_Pay import converted_app_total_cost_non_existing_restaurant, app_total_cost_non_existing_restaurant
import calendar
from rest_framework.decorators import api_view


def days_left_in_current_month():
    today = date.today()  # Using 'date' class to get today's date
    # Get the first day of the next month
    if today.month == 12:  # Handle December edge case
        first_day_next_month = date(today.year + 1, 1, 1)
    else:
        first_day_next_month = date(today.year, today.month + 1, 1)
    # Calculate the number of days left
    days_left = (first_day_next_month - today).days
    return days_left

def Converted_First_Month_Amount_To_Pay(price_type, country_name):
    payment_value = converted_app_total_cost_non_existing_restaurant(price_type, country_name)

    if payment_value == -1:
        return 0

    # Ensure payment_value is a Decimal
    payment_value = Decimal(payment_value)

    # Get the current date and the number of days in the current month
    current_date = datetime.now()  # Using 'datetime' class to get the current date and time
    _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
    # with '_' I'm ignoring the day of the week of the first day of the month, returned by the function

    # Calculate the remaining days in the month
    days_left = days_left_in_current_month()

    # Calculate the daily payment based on the total days in the current month
    daily_payment_value = payment_value / Decimal(days_in_month)

    # Calculate the amount to pay based on the remaining days
    remaining_payment_value = daily_payment_value * Decimal(days_left)

    # Round to two decimal places
    remaining_payment_value = remaining_payment_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return remaining_payment_value


@api_view(["GET"])
def get_converted_first_month_amount_to_pay(request, price_type, country_name):
    remaining_payment_value = Converted_First_Month_Amount_To_Pay(price_type, country_name)
    
    return Response({"value_to_pay": f"{remaining_payment_value}"}, status=status.HTTP_200_OK)

def First_Month_Amount_To_Pay(price_type):
    payment_value = app_total_cost_non_existing_restaurant(price_type)

    if payment_value == -1:
        return 0

    # Ensure payment_value is a Decimal
    payment_value = Decimal(payment_value)

    # Get the current date and the number of days in the current month
    current_date = datetime.now()  # Using 'datetime' class to get the current date and time
    _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
    # with '_' I'm ignoring the day of the week of the first day of the month, returned by the function

    # Calculate the remaining days in the month
    days_left = days_left_in_current_month()

    # Calculate the daily payment based on the total days in the current month
    daily_payment_value = payment_value / Decimal(days_in_month)

    # Calculate the amount to pay based on the remaining days
    remaining_payment_value = daily_payment_value * Decimal(days_left)

    # Round to two decimal places
    remaining_payment_value = remaining_payment_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return remaining_payment_value


@api_view(["GET"])
def get_first_month_amount_to_pay(request, price_type):
    remaining_payment_value = First_Month_Amount_To_Pay(price_type)
    
    return Response({"value_to_pay": f"{remaining_payment_value}"}, status=status.HTTP_200_OK)