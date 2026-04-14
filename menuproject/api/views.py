# Transbank

import random
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction as WebpayTransaction
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions

# end

from asyncio import constants
import os
import smtplib
import urllib.parse
import pytz
from babel import Locale, UnknownLocaleError

from django.template import Template, Context
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import unquote
from django.db.models import Q

from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Country
from .serializer import Country_Serializer
from .authorization_views import check_authorization  # Assuming you have this utility function

import traceback
import requests
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

import re
import json

from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from dateutil.parser import parse
from babel.dates import format_datetime
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from django.db.models import F
import difflib
import qrcode
from io import BytesIO
from django.utils.timezone import now
import calendar
from datetime import date, datetime, timedelta
import locale
from dateutil.relativedelta import relativedelta
from decimal import Decimal, ROUND_HALF_UP
from rest_framework import status
from .utils.Useful_procedures import Useful_procedures
import calendar
from django.http import HttpResponseBadRequest
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .utils.Encryption import decrypt_value, encrypt_value

from .utils.First_Month_Amount_To_Pay import Converted_First_Month_Amount_To_Pay

from .utils.Amount_To_Pay import converted_app_total_cost_existing_restaurant, converted_app_total_cost_non_existing_restaurant

from dotenv import load_dotenv

load_dotenv()

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL")

REACT_BASE_URL = os.getenv("DJANGO_REACT_BASE_URL")
HTTPS_BASE_URL = os.getenv("DJANGO_HTTPS")
CATEGORIES_PATH = os.getenv("DJANGO_CATEGORIES_PATH")

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

from .logging_views import Discard_all_editings
import logging

logger = logging.getLogger(__name__)

from .models import (
    Help_Atonn,
    Global_Price,
    Country,
    Delivery_Company,
    Payment_Option,
    Restaurant_Delivery_Company,
    Promotion,
    New_Restaurant_Data,
    BuyOrderSessionID,
    Restaurant,
    ReactivatedDate,
    CuttingServiceDate,
    Category,
    Dish,
    Restaurant_User,
    Review,
    Image,
    Rejection_Reason,
    Review_Rejection,
    Accessing_Devices,
)
from .serializer import (
    Country_Serializer,
    Delivery_Company_Serializer,
    Payment_Option_Serializer,
    Restaurant_Delivery_Company_Serializer,
    Promotion_Serializer,
    Restaurant_Serializer,
    Restaurant_User_Retrieve_Serializer,
    Restaurant_User_Update_or_Create_Serializer,
    Category_Serializer,
    Dish_Serializer,
    Review_Serializer,
    Image_Serializer,
    Accessing_Devices_Serializer
)

from .utils.Constants_and_strings import *

@api_view(["GET"])
def access_backend_view(request):
    # print(f"[{datetime.now()}] in access_backend_view - {request.META.get('HTTP_USER_AGENT')}")
    print(f"in access_backend_view")
    try:
        new_country_data = Country.objects.get(pk=1)
        return JsonResponse({"message": f"Exito mi chinita linda, el pais es {new_country_data.flag_image_url}"})
    except Country.DoesNotExist:
        print("access_backend_view:: a Country was not found")
        return Response({"error": "a Country was not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

# Useful Procedures ----------------------------------

def create_restaurant(restaurant_rut):
    try:
        new_restaurant_data = New_Restaurant_Data.objects.get(rut=restaurant_rut)
    except New_Restaurant_Data.DoesNotExist:
        return Response({"error": "New restaurant data not found"}, status=status.HTTP_404_NOT_FOUND)

    # Extract values from the New_Restaurant_Data object
    restaurant_rut = new_restaurant_data.rut
    restaurant_country_id = new_restaurant_data.country_id
    restaurant_price_type = new_restaurant_data.price_type
    user_name = new_restaurant_data.user_name
    user_password = new_restaurant_data.user_password
    user_email = new_restaurant_data.user_email
    
    new_restaurant_data.delete()
    
    try:
        my_country = Country.objects.get(pk=restaurant_country_id)
    except Country.DoesNotExist:
        print(f'{COUNTRY_DOES_NOT_EXIST}')
        return f'{COUNTRY_DOES_NOT_EXIST}'

    try:
        # Check if a restaurant with the same rut exists
        restaurant_same_rut = Restaurant.objects.get(rut=restaurant_rut)
        return f"{RESTAURANT_ALREADY_EXISTS}"
    except Restaurant.DoesNotExist:
        pass

    my_restaurant = None
        # Create the restaurant with explicit field mapping
    try:
        my_restaurant = Restaurant.objects.create(
            rut=restaurant_rut,
            public_country=my_country,
            price_type=restaurant_price_type,
            last_payment_date=now()
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        
    try:
        my_restaurant_user = Restaurant_User.objects.create(
            public_name=user_name,
            public_password=user_password,
            public_email=user_email,
            public_email_validated=True,
            recently_created=False,
            main_user=True,
            restaurant=my_restaurant
        )
        my_restaurant.main_user_id = my_restaurant_user.id  # type: ignore
        my_restaurant.save() # type: ignore
        # send_qr_code_via_email_and_link_to_atonna(my_restaurant.id, user_email, restaurant_rut, REACT_BASE_URL, CATEGORIES_PATH) # type: ignore
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return {"id": my_restaurant.id} # type: ignore

def extract_request_data_func_with_user_id_and_user_random(request):
    if request.method == 'GET':
        # For GET requests, typically you don't need to extract request body data
        data = {}
    else:
        # For POST, PATCH, DELETE requests, extract from request data
        data = request.data.copy()  # Make a copy to avoid mutating the original request data
    
    # Extract desired fields
    extracted_data = {
        "restaurant_id": data.get("restaurant_id"), # type: ignore
        "user_id": data.get("user_id"),
        "user_random": data.get("user_random"),
    }
       
    return extracted_data

def replace_placeholder_for_sending_emails(match):
    placeholder = match.group(1)  # Extract the placeholder name without the ***

    # Try to get the value from the imported constants using globals()
    # If the constant exists, return its value; otherwise, return the original placeholder
    return globals().get(placeholder, match.group(0))


def format_currency(amount, country):
    """Formats the currency based on the country's locale and currency symbol."""
    try:
        amount = Decimal(amount)  # Ensure it's a decimal
        locale.setlocale(locale.LC_ALL, country.locale)  # Set locale
        formatted_amount = f"{country.currency_symbol}{amount:,.0f}".replace(",", ".")  # Format with dots
        return formatted_amount
    except (ValueError, locale.Error):
        return f"{country.currency_symbol}{amount}"  # Fallback

def format_transaction_date(transaction_date, country):
    """Converts UTC date to the restaurant's local timezone and formats it."""
    try:
        # Remove 'Z' and parse ISO format (handles both 3-digit and 6-digit milliseconds)
        transaction_date = transaction_date.rstrip("Z")  # Remove the trailing "Z"
        dt_utc = datetime.fromisoformat(transaction_date)  # Automatically parses different decimal places

        # Ensure it's UTC
        dt_utc = dt_utc.replace(tzinfo=pytz.utc)

        # Get the timezone from the country object
        timezone_str = getattr(country, "timezone", "UTC")
        local_tz = pytz.timezone(timezone_str)

        # Convert time to local time
        dt_local = dt_utc.astimezone(local_tz)

        # Manually format the date
        formatted_date = dt_local.strftime("%A, %d de %B de %Y %H:%M:%S")

        return formatted_date

    except (ValueError, pytz.UnknownTimeZoneError) as e:
        print(f"Error formatting transaction date: {e}")
        return transaction_date  # Fallback to raw format if conversion fails

def send_webpay_plus_payment_done(data, main_user_email, restaurant_rut, other_user_email=None):
    subject = INITIAL_MENU_LOAD_PAYMENT_CONFIRMATION + restaurant_rut
    from_email = FROM_EMAIL
    recipient_list = ["rafael.soteldo@gmail.com"] 

    # Get restaurant country for formatting
    try:
        my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
        country = my_restaurant.public_country
    except Restaurant.DoesNotExist:
        country = None

    print(f"country.name:: {country.name}") # type: ignore
    # Get values from data
    status = data.get("status", "Desconocido")
    amount = format_currency(data.get("amount", "0"), country) if country else data.get("amount", "0")
    response_code = data.get("response_code", "N/A")
    buy_order = data.get("buy_order", "N/A")
    session_id = data.get("session_id", "N/A")
    transaction_date = format_transaction_date(data.get("transaction_date", "N/A"), country) if country else data.get("transaction_date", "N/A")
    print(f"transaction_date:: {transaction_date}")
    authorization_code = data.get("authorization_code", "N/A")
    card_number = data.get("card_detail", {}).get("card_number", "N/A")

    # Mask card number if full number is returned
    if len(card_number) > 4:
        card_number = f"**** **** **** {card_number[-4:]}"

    # Email template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Pago para Carga de Menu Inicial Realizado</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
            .receipt {{ max-width: 600px; margin: 20px auto; background: white; padding: 20px; border: 1px solid #ddd; text-align: center; }}
            .header img {{ max-width: 150px; }}
            .details p {{ margin: 5px 0; text-align: left; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="receipt">
            <div class="header">
                <img src="cid:logo" alt="Application Logo">
                <h1>El pago para la solicitud de una carga inicial fue realizado</h1>
            </div>
            <h2>Detalles de la Transacción</h2>
            <p><strong>Monto:</strong> {amount}</p>
            <p><strong>Fecha de Transacción:</strong> {transaction_date}</p>
            <p><strong>RUT del Restaurante:</strong> {restaurant_rut}</p>
        </div>
    </body>
    </html>
    """

    # Create email
    msg = EmailMultiAlternatives(
        subject=subject,
        body="Recibo de pago - Pago realizado con Webpay Plus",
        from_email=from_email,
        to=recipient_list,
    )
    msg.attach_alternative(html_template, "text/html")

    # Fetch the logo from Cloudinary
    image_url = settings.CLOUDINARY_LOGO_URL
    response = requests.get(image_url)
    if response.status_code == 200:
        logo = MIMEImage(response.content)
        logo.add_header("Content-ID", "<logo>")
        msg.attach(logo)  # type: ignore

    # Send email
    msg.send()

def send_webpayplus_payment_confirmation_via_email(data, main_user_email, restaurant_rut, action, other_user_email=None):
    subject = PAYMENT_CONFIRMATION
    from_email = FROM_EMAIL
    recipient_list = [main_user_email] + ([other_user_email] if other_user_email else [])

    # Get restaurant country for formatting
    try:
        my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
        country = my_restaurant.public_country
    except Restaurant.DoesNotExist:
        country = None

    print(f"country.name:: {country.name}")  # type: ignore
    # Get values from data
    status = data.get("status", "Desconocido")
    amount = format_currency(data.get("amount", "0"), country) if country else data.get("amount", "0")
    response_code = data.get("response_code", "N/A")
    buy_order = data.get("buy_order", "N/A")
    session_id = data.get("session_id", "N/A")
    transaction_date = format_transaction_date(data.get("transaction_date", "N/A"), country) if country else data.get("transaction_date", "N/A")
    print(f"transaction_date:: {transaction_date}")
    authorization_code = data.get("authorization_code", "N/A")
    card_number = data.get("card_detail", {}).get("card_number", "N/A")
    
    # Define the message based on the action
    messages = {
        CREATING: "Su restaurant ha sido registrado",
        REACTIVATING: "Su restaurant ha sido reactivado",
        PAYINGNORMALFEE: "Usted ha pagado un mes de servicio",
        INITIALMENULOAD: "Usted ha pagado la solicitud de carga inicial de su menú en ATONNA",
    }
    message = messages.get(action, "")

    # Mask card number if full number is returned
    if len(card_number) > 4:
        card_number = f"**** **** **** {card_number[-4:]}"

    # Email template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Recibo de Pago</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
            .receipt {{ max-width: 600px; margin: 20px auto; background: white; padding: 20px; border: 1px solid #ddd; text-align: center; }}
            .header img {{ max-width: 150px; }}
            .details p {{ margin: 5px 0; text-align: left; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="receipt">
            <div class="header">
                <img src="cid:logo" alt="Application Logo">
                <h1>Recibo de pago - Pago realizado con Webpay Plus</h1>
                <h3>Por favor, no responda este mensaje</h3>
            </div>
            <h2>Detalles de la Transacción</h2>
            <p><strong>Estado:</strong> {status}</p>
            <p><strong>Monto:</strong> {amount}</p>
            <p><strong>Código de Respuesta:</strong> {response_code}</p>
            <p><strong>Orden de Compra:</strong> {buy_order}</p>
            <p><strong>ID de Sesión:</strong> {session_id}</p>
            <p><strong>Fecha de Transacción:</strong> {transaction_date}</p>
            <p><strong>Código de Autorización:</strong> {authorization_code}</p>
            <p><strong>Número de Tarjeta:</strong> {card_number}</p>
            <p><strong>RUT del Restaurante:</strong> {restaurant_rut}</p>
            <p><strong>Mensaje:</strong> {message}</p>
            <div class="footer">
                <p>Gracias por su pago.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create email
    msg = EmailMultiAlternatives(
        subject=subject,
        body="Recibo de pago - Pago realizado con Webpay Plus",
        from_email=from_email,
        to=recipient_list,
    )
    msg.attach_alternative(html_template, "text/html")

    # Fetch the logo from Cloudinary
    image_url = settings.CLOUDINARY_LOGO_URL
    response = requests.get(image_url)
    if response.status_code == 200:
        logo = MIMEImage(response.content)
        logo.add_header("Content-ID", "<logo>")
        msg.attach(logo)  # type: ignore

    # Send email
    msg.send()


def send_notification_for_payment_via_email_func(my_restaurant):
    my_main_restaurant_user = Restaurant_User.objects.get(pk=my_restaurant.main_user_id)

    my_restaurant_user = None
    if (my_restaurant.currently_logged_in != -1) and (my_restaurant.currently_logged_in != my_restaurant.main_user_id):
        my_restaurant_user = Restaurant_User.objects.get(pk=my_restaurant.currently_logged_in)

    subject = GRACE_PERIOD_ACTIVATED
    from_email = FROM_EMAIL
    recipient_list = [my_main_restaurant_user.public_email]
    
    if (my_restaurant_user is not None) and (my_restaurant.currently_logged_in != my_restaurant.main_user_id) and (my_restaurant_user.public_email_validated):
        recipient_list.append(my_restaurant_user.public_email)

    # Define the notification message based on the number of reminders sent
    if my_restaurant.number_of_sent_payment_reminders == 0:
        text_content = FIRST_PAYMENT_NOTIFICATION
    elif my_restaurant.number_of_sent_payment_reminders == 1:
        text_content = SECOND_PAYMENT_NOTIFICATION
    else:
        return f"{NO_PAYMENT_NOTIFICATION_SENT}"

    # HTML email template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>PERIODO DE GRACIA PARA EL PAGO ACTIVADO</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                width: 100%;
                padding: 20px;
                box-sizing: border-box;
            }
            .content {
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border: 1px solid #dddddd;
                padding: 20px;
                box-sizing: border-box;
            }
            .header {
                text-align: center;
                margin-bottom: 20px;
            }
            .header img {
                max-width: 150px;
            }
            .footer {
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #666666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <div class="header">
                    <img src="cid:logo" alt="Application Logo">
                    <h3>Por favor, no responda este mensaje</h3>
                </div>
                <h1>PERIODO DE GRACIA PARA EL PAGO ACTIVADO</h1>
                <p>{text_content}</p>
                <p>GRACIAS DE ANTEMANO</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Render the HTML content with the provided context
    html_template = html_template.replace("{text_content}", text_content)

    # Create the email
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Plain text content
        from_email=from_email,
        to=recipient_list,
    )
    msg.attach_alternative(html_template, "text/html")

    # Fetch the logo from Cloudinary
    image_url = settings.CLOUDINARY_LOGO_URL
    response = requests.get(image_url)
    
    if response.status_code == 200:
        logo = MIMEImage(response.content)
        logo.add_header("Content-ID", "<logo>")
        msg.attach(logo)  # type: ignore

    # Send email
    msg.send()
    
    return f"{PAYMENT_NOTIFICATION_SENT}"


@api_view(["PATCH"])
def send_key_via_email(request, email_address, four_digits_key, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    # Get Cloudinary image URL from settings
    image_url = settings.CLOUDINARY_LOGO_URL
    
    # Fetch the image from Cloudinary
    response = requests.get(image_url)
    if response.status_code != 200:
        print("Error fetching image from Cloudinary")
        return Response({"error": "Failed to fetch logo image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_can_go_on = True

    if int(restaurant_id) != -1:
        if (int(restaurant_id) != int(extracted_data.get("restaurant_id") or 0) and extracted_data["restaurant_id"] is not None):
            print(f"{RESTAURANT_ID_DOES_NOT_MATCH}")
            return Response({"error": f"{RESTAURANT_ID_DOES_NOT_MATCH}"}, status=status.HTTP_400_BAD_REQUEST)

        restaurant_id = extracted_data["restaurant_id"]
        user_id = extracted_data["user_id"]
        user_random = extracted_data["user_random"]

        if not restaurant_id or not user_id or not user_random:
            print("restaurant_id or user_id or user_random not provided")
            return Response({"error": "restaurant_id or user_id or user_random not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            my_restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            print(f"{RESTAURANT_DOES_NOT_EXIST}")
            return Response({"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)

        performer = check_current_user_id_and_random()  # type: ignore
        user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)

    if user_can_go_on:
        subject = YOUR_ATONNA_VERIFICATION_KEY
        from_email = FROM_EMAIL
        recipient_list = [email_address]

        constants = {
            "VERIFICATION_KEY": VERIFICATION_KEY,
            "YOUR_FOUR_DIGITS_KEY_IS": YOUR_FOUR_DIGITS_KEY_IS,
            "USE_THIS_KEY_TO_COMPLETE_EMAIL_VERIFICATION_PROCESS": USE_THIS_KEY_TO_COMPLETE_EMAIL_VERIFICATION_PROCESS,
        }

        text_content = f"""
        {VERIFICATION_KEY}

        {YOUR_FOUR_DIGITS_KEY_IS}: '{four_digits_key}'

        {USE_THIS_KEY_TO_COMPLETE_EMAIL_VERIFICATION_PROCESS}
        """
        text_content = text_content.format(**constants)

        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>CLAVE DE VERIFICACIÓN DE EMAIL</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                .container {
                    width: 100%;
                    padding: 20px;
                    box-sizing: border-box;
                }
                .content {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    border: 1px solid #dddddd;
                    padding: 20px;
                    box-sizing: border-box;
                }
                .header {
                    text-align: center;
                    margin-bottom: 20px;
                }
                .header img {
                    max-width: 150px;
                }
                .key {
                    text-align: center;
                    margin-top: 20px;
                    font-size: 24px;
                    font-weight: bold;
                }
                .footer {
                    text-align: center;
                    margin-top: 20px;
                    font-size: 12px;
                    color: #666666;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <div class="header">
                        <img src="cid:logo" alt="Application Logo">
                        <h1>Clave de verificación de EMail</h1>
                        <h3>Por favor, no responda este mensaje</h3>
                    </div>
                    <div class="key">
                        Su clave de verificación de cuatro dígitos: {{ key }}
                    </div>
                    <div class="footer">
                        <p>Use esta clave para completar el proceso de verificación</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        html_template = re.sub(r'\*\*\*(.*?)\*\*\*', replace_placeholder_for_sending_emails, html_template)
        
        # Render the HTML content with the provided context
        template = Template(html_template)
        context = Context({"key": four_digits_key})
        html_content = template.render(context)

        # Create the email
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,  # Plain text content
            from_email=from_email,
            to=recipient_list,
        )

        msg.attach_alternative(html_content, "text/html")  # Attach HTML content as an alternative

        # Attach the image fetched from Cloudinary
        logo = MIMEImage(response.content)
        logo.add_header("Content-ID", "<logo>")
        msg.attach(logo)  # type: ignore

        msg.send()

        return Response({"message": f"{KEY_SENT}"}, status=status.HTTP_200_OK)
    
    else:
        print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
        return Response({"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"}, status=status.HTTP_400_BAD_REQUEST)
                       
@api_view(["PATCH"])
def send_qr_code_via_email(request):
    print('in send_qr_code_via_email')
    # Check authorization
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Extract JSON data from the request body
    try:
        data = json.loads(request.body)
        email_address = data.get("email_address")
        react_base_url = data.get("react_base_url")
        categories_path = data.get("categories_path")
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)

    print(f"📧 Email: {email_address}, 🌍 Base URL: {react_base_url}, 📂 Path: {categories_path}")
    
    print(f"send_qr_code_via_email:: HTTPS_BASE_URL:: {HTTPS_BASE_URL}")
    print(f"send_qr_code_via_email:: react_base_url:: {react_base_url}")
    print(f"send_qr_code_via_email:: categories_path:: {categories_path}")
    
    # Extract data from request
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    restaurant_id = extracted_data["restaurant_id"]
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    if not restaurant_id or not user_id or not user_random:
        return Response(
            {"error": "restaurant_id, user_id, or user_random not provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": "Restaurant does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )
        
    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)

    if not user_can_go_on:
        return Response(
            {"error": "User cannot perform further actions"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # type: ignore
        box_size=10,
        border=4,
    )
    qr.add_data(f"{react_base_url}/{categories_path}/{restaurant_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to a BytesIO object
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")  # type: ignore
    img_buffer.seek(0)

    # Prepare email details
    subject = YOUR_QR_CODE_FOR_ENTERING_ATONNA
    from_email = FROM_EMAIL
    recipient_list = [email_address]

    constants = {
        "QR_CODE": QR_CODE,
        "YOUR_QR_CODE_IS_IN_THE_ATTACHMENT": YOUR_QR_CODE_IS_IN_THE_ATTACHMENT
    }
    text_content = """
    {QR_CODE}

    {YOUR_QR_CODE_IS_IN_THE_ATTACHMENT}
    """
    text_content = text_content.format(**constants)

    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>***QR_CODE***</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                width: 100%;
                padding: 20px;
                box-sizing: border-box;
            }
            .content {
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border: 1px solid #dddddd;
                padding: 20px;
                box-sizing: border-box;
            }
            .header {
                text-align: center;
                margin-bottom: 20px;
            }
            .header img {
                max-width: 150px;
            }
            .qr-code {
                text-align: center;
                margin-top: 20px;
            }
            .footer {
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #666666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <div class="header">
                    <img src="cid:logo" alt="Application Logo">
                    <h1>***QR_CODE***</h1>
                    <h3>Por favor, no responda este mensaje</h3>
                </div>
                <div class="qr-code">
                    <p>SU CÓDIGO QR ESTÁ EN EL ATTACHMENT</p>
                </div>
                <div class="footer">
                    <p>GRACIAS POR USAR NUESTRO SERVICIO</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    html_template = re.sub(r'\*\*\*(.*?)\*\*\*', replace_placeholder_for_sending_emails, html_template)
    
    # Render the HTML content
    template = Template(html_template)
    context = Context({})
    html_content = template.render(context)
    
    # Fetch the Cloudinary image
    image_url = settings.CLOUDINARY_LOGO_URL  # Cloudinary URL stored in Django settings
    response = requests.get(image_url)
    if response.status_code != 200:
        return Response({"error": "Failed to download the logo from Cloudinary"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    logo_image = MIMEImage(response.content)
    logo_image.add_header("Content-ID", "<logo>")

    # Create the email
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Plain text content
        from_email=from_email,
        to=recipient_list,
    )

    msg.attach_alternative(html_content, "text/html")  # Attach HTML content as an alternative

    # Attach the QR code image
    qr_image = MIMEImage(img_buffer.read(), _subtype="png")
    qr_image.add_header("Content-ID", "<qr_code>")
    qr_image.add_header("Content-Disposition", "inline", filename="qrcode.png")
    msg.attach(qr_image)  # type: ignore

    # Attach the Cloudinary logo
    msg.attach(logo_image)  # type: ignore

    # Send the email
    msg.send()

    return Response({"message": "Código QR enviado exitosamente"}, status=status.HTTP_200_OK)

from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import os

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def send_support_request_via_email(request):
    # Get the list of image files
    image_files = request.FILES.getlist("image_files[]")
    
    # Check if all files are images
    for image_file in image_files:
        if not image_file.content_type.startswith("image/"):
            return Response({"error": "Invalid file type. Only images are allowed."}, status=status.HTTP_400_BAD_REQUEST)

    # Get required fields
    phone_number = request.data.get("phone_number")
    email = request.data.get("email")
    name = request.data.get("name")
    restaurant_rut = request.data.get("restaurant_rut")
    support_question = request.data.get("support_question")

    if not phone_number or not email or not support_question:
        return Response({"error": "Phone number, email, and support question are required."}, status=status.HTTP_400_BAD_REQUEST)

    recipient_email = "rafael.soteldo@gmail.com"
    subject = f"Support Request - {restaurant_rut}"
    from_email = "rafael.soteldo@gmail.com"
    recipient_list = [recipient_email]

    text_content = f"""
    Support request details:

    Name: {name}
    Phone Number: {phone_number}
    Email: {email}
    Restaurant RUT: {restaurant_rut}
    Support Question: {support_question}
    """

    html_content = f"""
    <html>
        <body>
            <div style="text-align: center;">
                <img src="cid:logo" alt="Logo" style="max-width: 150px;"/>
                <h2>Support Request</h2>
                <p><strong>Restaurant RUT:</strong> {restaurant_rut}</p>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Phone Number:</strong> {phone_number}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Support Question:</strong> {support_question}</p>
                <p>Thank you!</p>
            </div>
        </body>
    </html>
    """

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=recipient_list,
    )
    msg.attach_alternative(html_content, "text/html")

    # Attach each uploaded image file
    for image_file in image_files:
        msg.attach(image_file.name, image_file.read(), image_file.content_type)

    # Fetch the logo from Cloudinary
    image_url = settings.CLOUDINARY_LOGO_URL
    response = requests.get(image_url)

    if response.status_code == 200:
        logo = MIMEImage(response.content)
        logo.add_header("Content-ID", "<logo>")
        msg.attach(logo)  # type: ignore

    # Send email
    msg.send()

    return Response({"message": "Requerimiento de soporte enviado exitosamente."}, status=status.HTTP_200_OK)



@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def send_pdf_via_email(request):
    # Check if at least one file is included
    if "pdfFiles" not in request.FILES:
        return Response({"error": "No PDF files provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    pdf_files = request.FILES.getlist("pdfFiles")  # Retrieve all uploaded files

    # Validate file types
    for pdf_file in pdf_files:
        if pdf_file.content_type != "application/pdf":
            return Response({"error": f"Invalid file type: {pdf_file.name}. Only PDFs are allowed."},
                            status=status.HTTP_400_BAD_REQUEST)

    # Get phone number and email from request data
    phone_number = request.data.get("phoneNumber")
    email = request.data.get("email")
    name = request.data.get("name")
    restaurant_rut = request.data.get("restaurant_rut")

    if not phone_number or not email:
        return Response({"error": "Phone number and email are required."}, status=status.HTTP_400_BAD_REQUEST)

    recipient_email = "rafael.soteldo@gmail.com"  # Change as needed
    subject = f"Menús en PDF - {restaurant_rut}"
    from_email = "rafael.soteldo@gmail.com"
    recipient_list = [recipient_email]

    text_content = f"""
    Please find the attached PDF files.

    Name: {name}
    Phone Number: {phone_number}
    Email: {email}
    Restaurant RUT: {restaurant_rut}
    """

    # HTML email with Cloudinary logo
    html_content = f"""
    <html>
        <body>
            <div style="text-align: center;">
                <img src="{settings.CLOUDINARY_LOGO_URL}" alt="Logo" style="max-width: 150px;"/>
                <h2>PDF Attachments</h2>
                <p>Hello,</p>
                <p>The Menu PDFs are attached, please load them to ATONNA.</p>
                <p><strong>Restaurant RUT:</strong> {restaurant_rut}</p>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Phone Number:</strong> {phone_number}</p>
                <p><strong>Email:</strong> {email}</p>
                <p>Thank you!</p>
            </div>
        </body>
    </html>
    """

    # Create the email
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=recipient_list,
    )
    msg.attach_alternative(html_content, "text/html")

    # Attach multiple PDFs
    for pdf_file in pdf_files:
        msg.attach(pdf_file.name, pdf_file.read(), "application/pdf")

    # Send the email
    msg.send()

    return Response({"message": "Los PDFs fueron enviados correctamente, ahora esperamos por su pago. Gracias."},
                    status=status.HTTP_200_OK)


def send_link_to_atonna(restaurant_id, email_address, restaurant_RUT, react_base_url, categories_path):
    # Prepare email details
    subject = "Felicitaciones, ahora puede continuar disfrutando de ATONNA"
    from_email = FROM_EMAIL
    recipient_list = [email_address]

    text_content = f"""
    Felicitaciones, ahora puede continuar disfrutando de ATONNA

    Este es el link a ATONNA: {react_base_url}/{categories_path}/{restaurant_id}
    RUT del restaurante: {restaurant_RUT}
    """

    # Use Cloudinary logo instead of a local file
    logo_url = settings.CLOUDINARY_LOGO_URL

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Bienvenido a Atonna</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
                box-sizing: border-box;
            }}
            .content {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border: 1px solid #dddddd;
                padding: 20px;
                box-sizing: border-box;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header img {{
                max-width: 150px;
            }}
            .link-container {{
                text-align: center;
                margin-top: 20px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #666666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <div class="header">
                    <img src="{logo_url}" alt="Application Logo">
                    <h1>Felicitaciones, ahora puede seguir disfrutando de ATONNA</h1>
                    <h3><strong>Por favor, no responda este mensaje</strong></h3>
                </div>
                <div class="link-container">
                    <p>Este es el link a ATONNA: <a href="{react_base_url}/{categories_path}/{restaurant_id}">ATONNA</a></p>
                    <p>RUT del restaurante: <strong>{restaurant_RUT}</strong></p>
                </div>
                <div class="footer">
                    <p>Gracias por usar nuestro servicio</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    # Render the HTML content
    template = Template(html_template)
    context = Context({})
    html_content = template.render(context)

    # Create the email
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Plain text content
        from_email=from_email,
        to=recipient_list,
    )
    msg.attach_alternative(html_content, "text/html")  # Attach HTML content as an alternative

    # Send the email
    msg.send()

    print("Email enviado exitosamente")
    return "Email enviado exitosamente"


def send_qr_code_via_email_and_link_to_atonna(restaurant_id, email_address, restaurant_RUT, react_base_url, categories_path):
    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # type: ignore
        box_size=10,
        border=4,
    )
    
    qr.add_data(f"{react_base_url}/{categories_path}/{restaurant_id}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code image to a BytesIO object
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")  # type: ignore
    img_buffer.seek(0)

    # Prepare email details
    subject = "Felicitaciones, ahora puede comenzar a disfrutar de ATONNA"
    from_email = FROM_EMAIL
    recipient_list = [email_address]

    constants = {
        "QR_CODE": QR_CODE,
        "YOUR_QR_CODE_IS_IN_THE_ATTACHMENT": "Su código QR está en el attachment"
    }
    text_content = """
    {QR_CODE}

    {YOUR_QR_CODE_IS_IN_THE_ATTACHMENT}
    """
    text_content = text_content.format(**constants)

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>QR Code</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
                box-sizing: border-box;
            }}
            .content {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border: 1px solid #dddddd;
                padding: 20px;
                box-sizing: border-box;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header img {{
                max-width: 150px;
            }}
            .qr-code {{
                text-align: center;
                margin-top: 20px;
            }}
            .link-container {{
                text-align: center;
                margin-top: 20px;
            }}
            .remember {{
                text-align: center;
                margin-top: 20px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 12px;
                color: #666666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <div class="header">
                    <img src="cid:logo" alt="Application Logo">
                    <h1>Felicitaciones, ahora puede comenzar a disfrutar de ATONNA</h1>
                    <h3>Por favor, no responda este mensaje</h3>
                </div>
                <div class="qr-code">
                    <p>Para propósitos de soporte use el RUT del restaurant {restaurant_RUT}</p>
                </div>
                <div class="link-container">
                    <p>Puede acceder a ATONNA con este link: <a href="{react_base_url}/{categories_path}/{restaurant_id}">ATONNA</a></p>
                </div>
                <div class="remember">                    
                    <p>Recuerde, cuando entre a ATONNA estará vacía, haga login con las credenciales que introdujo al registrarse, una vez en el área administratiuva, puede crear Categorías, Platos, darle un nombre al restaurant, etc..</p>
                    <p>ATONNA le provee de videos de ayuda en todas partes, de manera que usted estará guiado en todo momento</p>
                    <p>Comience a disfrutar de las características que ofrece ATONNA. Este es el inicio de una era de expansión para su restaurant</p>
               </div>
                <div class="footer">
                    <p>Gracias por usar nuestros servicios</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    html_template = re.sub(r'\*\*\*(.*?)\*\*\*', replace_placeholder_for_sending_emails, html_template)
    
    # Render the HTML content
    template = Template(html_template)
    context = Context({})
    html_content = template.render(context)

    # Fetch the Cloudinary image
    image_url = settings.CLOUDINARY_LOGO_URL  # Cloudinary URL stored in Django settings
    response = requests.get(image_url)
    if response.status_code != 200:
        return Response({"error": "Failed to download the logo from Cloudinary"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    logo_image = MIMEImage(response.content)
    logo_image.add_header("Content-ID", "<logo>")

    # Create the email
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Plain text content
        from_email=from_email,
        to=recipient_list,
    )

    msg.attach_alternative(html_content, "text/html")  # Attach HTML content as an alternative

    # Attach the QR code image
    qr_image = MIMEImage(img_buffer.read(), _subtype="png")
    qr_image.add_header("Content-ID", "<qr_code>")
    qr_image.add_header("Content-Disposition", "inline", filename="qrcode.png")
    msg.attach(qr_image)  # type: ignore

    # Attach the Cloudinary logo
    msg.attach(logo_image)  # type: ignore

    # Send the email
    msg.send()
    
    print("Código QR enviado exitosamente")
    return "Código QR enviado exitosamente"

@api_view(["GET"])
def get_datetime_from_backend(request):
    return Response({"now": now()}, status=status.HTTP_200_OK)

@api_view(["GET"])
def load_countries(request):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        countries = Country.objects.all()  # Get all countries from the database
    except Country.DoesNotExist:
        return Response({"error": "No countries found"}, status=status.HTTP_404_NOT_FOUND)
    # Serialize the countries queryset
    serializer = Country_Serializer(countries, many=True)
    
    # Return the serialized data in the response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def public_or_private(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND
        )

    return Response(my_restaurant.currently_logged_in, status=status.HTTP_200_OK)

@api_view(["GET"])
def is_restaurant_blocked(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND
        )

    result = my_restaurant.payment_state = RESTAURANT_BLOCKED_DUE_TO_PAYMENT
    return Response(result, status=status.HTTP_200_OK)
# Cloudinary ----------------------------------------------

@api_view(["DELETE"])
@transaction.atomic
def delete_cloudinary_resource(request, public_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    restaurant_id = extracted_data["restaurant_id"]
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND
        )
    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        result = cloudinary.api.delete_resources(public_id)
        if result["deleted"] != {f"{public_id}": "not_found"}:
            return Response(
                {
                    "message": f"{IMAGE_DELETED}",
                    "new_token": check_authorization_result["new_token"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": f"{IMAGE_NOT_FOUND}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

@api_view(["DELETE"])
@transaction.atomic
def delete_cloudinary_resource_and_image(request, restaurant_id, image_id, public_id):
    public_id_decoded = unquote(public_id)

    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND
        )
    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        try:
            my_image = Image.objects.get(
                pk=image_id
            )  # deletes the image from the database
            if my_image.use_count == 0:

                my_image.delete()

                result = cloudinary.api.delete_resources(
                    public_id_decoded
                )  # deletes the cloudinary resource
                return Response(
                    {
                        "message": f"{IMAGE_DELETED}",
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": f"{IMAGE_IS_BEING_USED}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Image.DoesNotExist:
            return Response(
                {"error": f"{IMAGE_DOES_NOT_EXIST}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            print(f"error: {e}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"message": f"{RESOURCE_AND_IMAGE_DELETED}"}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# whole Menu ---------------------------------------------------

def payment_period_start_func():  
    payment_period_start = Useful_procedures.get_period_start_date()
    return payment_period_start

# @csrf_protect
@api_view(["GET"])
def payment_period(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    date_a = payment_period_start_func()
    
    if not isinstance(date_a, (date, datetime)):
        return Response({"error": "Invalid date returned from payment_period_start_func"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"payment_start": date_a, "payment_end": date_a + timedelta(days=GRACE_PERIOD_LENGTH_IN_DAYS)}, status=status.HTTP_200_OK) # type: ignore

# @csrf_protect
@api_view(["GET"])
def service_period(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
          
    date_a = payment_period_start_func()
    date_b = date(date_a.year, date_a.month, calendar.monthrange(date_a.year, date_a.month)[1])
    
    if not isinstance(date_a, (date, datetime)):
        return Response({"error": "Invalid date returned from payment_period_start_func"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"service_start": date_a, "service_end": date_b}, status=status.HTTP_200_OK) # type: ignore

def get_next_payment_date_func(my_restaurant) -> date:
    if my_restaurant.restaurant_recently_created:
        # Add free months to the current date and set to the 1st of the resulting month
        next_payment_date = (
            my_restaurant.restaurant_current_date.replace(day=1) +
            relativedelta(months=my_restaurant.number_of_pending_free_months)
        )
    else:
        # Calculate next payment based on the last payment date
        next_payment_date = (
            my_restaurant.last_payment_date.replace(day=1) +
            relativedelta(months=1)
        )

    # Ensure the next payment date is not earlier than the current date
    if next_payment_date < my_restaurant.restaurant_current_date:
        next_payment_date = my_restaurant.restaurant_current_date.replace(day=1)
        
    return next_payment_date

def check_restaurant_payment_state_ok_func(my_restaurant) -> bool:
    return True
    if (my_restaurant.payment_state == RESTAURANT_NOT_BLOCKED_DUE_TO_PAYMENT):
        current_date = now().date()
        if (my_restaurant.last_payment_date.year == current_date.year and
            my_restaurant.last_payment_date.month == current_date.month):
            do_saving = False
            if (my_restaurant.active_month_number > 1):
                # in the current month and year has been already checked
                if (my_restaurant.last_payment_date.day > NUMBER_OF_DAYS_OK_TO_PAY):
                    my_restaurant.payment_state = RESTAURANT_BLOCKED_DUE_TO_PAYMENT
                    cutting_service_date = CuttingServiceDate.objects.create(restaurant=my_restaurant)
                    do_saving = True
            if (my_restaurant.number_of_pending_free_months == 0) and (not my_restaurant.payment_state == RESTAURANT_BLOCKED_DUE_TO_PAYMENT): 
                if (my_restaurant.restaurant_current_date.day in range(1, NUMBER_OF_DAYS_OK_TO_PAY // 2)): # example:: range(3, 16) => 1 is included and 16 is excluded
                    if (my_restaurant.number_of_sent_payment_reminders == 0):
                        send_notification_for_payment_via_email_func(my_restaurant)
                        my_restaurant.number_of_sent_payment_reminders += 1
                        do_saving = True
                elif (my_restaurant.restaurant_current_date.day in range(NUMBER_OF_DAYS_OK_TO_PAY // 2 + 1, NUMBER_OF_DAYS_OK_TO_PAY)):
                    if (my_restaurant.number_of_sent_payment_reminders == 1):
                        send_notification_for_payment_via_email_func(my_restaurant)
                        my_restaurant.number_of_sent_payment_reminders += 1
                        do_saving = True
                elif my_restaurant.restaurant_current_date.day > NUMBER_OF_DAYS_OK_TO_PAY:
                    if (my_restaurant.number_of_sent_payment_reminders > 0):
                        my_restaurant.number_of_sent_payment_reminders = 0
                        do_saving = True
            if do_saving:
                my_restaurant.save()
            return True       
        else:
            if (my_restaurant.number_of_pending_free_months == 0):
                # objects.create creates and saves automatically
                cutting_service_date = CuttingServiceDate.objects.create(restaurant=my_restaurant)
                print(f"cutting_service_date:: {cutting_service_date}")
                my_restaurant.payment_state = RESTAURANT_BLOCKED_DUE_TO_PAYMENT
                my_restaurant.save()
            return False
    else:
        return False

# @csrf_protect
@api_view(["GET"])
def does_the_restaurant_have_to_pay(request, restaurant_id):
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
    
    next_payment_date = get_next_payment_date_func(my_restaurant)
    if (my_restaurant.restaurant_current_date.month == next_payment_date.month) and (my_restaurant.restaurant_current_date.year == next_payment_date.year):
        if (my_restaurant.number_of_pending_free_months == 0):
            return Response(False, status=status.HTTP_200_OK)
        else:
            return Response(True, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_200_OK)
              
    
# @csrf_protect
@api_view(["GET"])
def get_amount_to_be_paid(request, restaurant_id):
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id) # type: ignore
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
        
    converted_value = converted_app_total_cost_existing_restaurant(my_restaurant)

    print(f"converted_value:: {converted_value}")
    
    return Response(
        {
            "value": str(converted_value),  # Convert Decimal to string
            "currency": my_restaurant.public_country.currency_symbol if my_restaurant.public_country else "",
            "locale": my_restaurant.public_country.locale if my_restaurant.public_country else "",
            "minimum_fraction_digits": my_restaurant.public_country.minimum_fraction_digits if my_restaurant.public_country else 0,
            "maximum_fraction_digits": my_restaurant.public_country.maximum_fraction_digits if my_restaurant.public_country else 0,
            "price_type": my_restaurant.price_type if my_restaurant.price_type else ""
        },
        status=status.HTTP_200_OK,
    )
# comment

@api_view(["GET"])
def get_app_total_cost(request, price_type, country_name):
    price_type = urllib.parse.unquote(price_type)
    
    try:
        my_country = Country.objects.get(name=country_name) 
    except Country.DoesNotExist:
        return Response(
            {"error": f"{COUNTRY_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    converted_value = converted_app_total_cost_non_existing_restaurant(price_type, country_name)
    return Response(
        {
            "value": str(converted_value),  # Convert Decimal to string
            "currency": my_country.currency_symbol,
            "locale": my_country.locale,
            "minimum_fraction_digits": my_country.minimum_fraction_digits,
            "maximum_fraction_digits": my_country.maximum_fraction_digits,
        },
        status=status.HTTP_200_OK,
    )
    
@api_view(["GET"])
def get_menu_load_cost(request, country_name):
    try:
        my_global_price = Global_Price.objects.get(pk=1) 
    except Global_Price.DoesNotExist:
        return Response(
            {"error": f"{GLOBAL_PRICE_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    try:
        my_country = Country.objects.get(name=country_name) 
    except Country.DoesNotExist:
        return Response(
            {"error": f"{COUNTRY_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    final_value = (my_global_price.initial_menu_load or Decimal(0)) * (my_country.exchange_rate or Decimal(0))
    
    return Response(
        {
            "value": str(final_value),  # Convert Decimal to string
            "currency": my_country.currency_symbol,
            "locale": my_country.locale,
            "minimum_fraction_digits": my_country.minimum_fraction_digits,
            "maximum_fraction_digits": my_country.maximum_fraction_digits,
        },
        status=status.HTTP_200_OK,
    )
    
    
# @csrf_protect
@api_view(["GET"])
def whole_menu(request, restaurant_id):
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
    if (check_restaurant_payment_state_ok_func(my_restaurant)):
        menu = Menu_Class()
        menu.Load_Restaurant(my_restaurant)
        menu.Load_Countries()
        menu.Load_Restaurant_Reviews(my_restaurant)
        menu.Load_Restaurant_Delivery_Companies(my_restaurant)
        menu.Load_Promotions(my_restaurant)
        menu.Load_Restaurant_User_Images_And_Names(my_restaurant)
        menu.Load_Rejection_Reasons() 
        menu.Load_Whole_Rest_Of_Menu(my_restaurant)
        menu.Update_Accesses(my_restaurant)
        return JsonResponse(menu.menu, status=status.HTTP_200_OK, safe=True)
    else:
        return Response({"error": f"{PAYMENT_REQUIRED}"}, status=status.HTTP_402_PAYMENT_REQUIRED)

# Connection --------------------------------------

@api_view(["GET"])
def check_for_connection(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(-1, status=status.HTTP_200_OK)
    return Response(1, status=status.HTTP_200_OK)

# Help --------------------------------------------------

@api_view(["GET"])
def get_help_video_url(request, video_name):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "GET":
        try:
            my_help_atonn = Help_Atonn.objects.get(video_name=video_name)
            return Response(
                {"video_url": my_help_atonn.video_url}, status=status.HTTP_200_OK
            )
        except Help_Atonn.DoesNotExist:
            return Response(
                {"error": f"{HELP_ATONN_DOES_NOT_EXIST}"},
                status=status.HTTP_404_NOT_FOUND,
            )

# Deliveries -----------------------------------------------
# Restaurant Delivery -----------------------------------------------
        
@api_view(['PATCH', 'POST'])
@transaction.atomic
def restaurant_delivery_company(request, restaurant_delivery_company_id, delivery_selected_id=None):
    # For creation restaurant_delivery_company_id must be -1
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    if int(restaurant_delivery_company_id) == -1 and (delivery_selected_id is None or int(delivery_selected_id) <= 0):
        print("When creating, delivery selected must be a positive number")
        return Response({"error": "When creating, delivery selected must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)

    updating_restaurant_delivery = int(restaurant_delivery_company_id) > -1
    
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data.get("user_id")  # don't rename it as request_user_id
    user_random = extracted_data.get("user_random")
    restaurant_id = extracted_data.get("restaurant_id")
    # restaurant_id has to always be sent in the request

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        print(f"{RESTAURANT_DOES_NOT_EXIST}")
        return Response({"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)

    # check_current_user_id_and_random checks for user_id or user_random not being None
    performer = check_current_user_id_and_random()
    if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
        return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)

    if my_restaurant.restaurant_deliveries_edition_is_pending and not my_restaurant.dont_allow_further_actions_from_this_user:
        # Prepare data for serializer, removing unnecessary fields
        request_data = request.data.copy()
        request_data.pop("restaurant_id", None)
        request_data.pop("user_id", None)
        request_data.pop("user_random", None)

        if updating_restaurant_delivery:
            # Update existing restaurant delivery
            try:
                my_restaurant_delivery = Restaurant_Delivery_Company.objects.get(pk=int(restaurant_delivery_company_id))
            except Restaurant_Delivery_Company.DoesNotExist:
                print(f'{RESTAURANT_DELIVERY_COMPANY_DOES_NOT_EXIST}')
                return Response({'error': f"{RESTAURANT_DELIVERY_COMPANY_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)

            serializer = Restaurant_Delivery_Company_Serializer(
                my_restaurant_delivery,
                data=request_data,
                partial=True,
                context={'include_details': True} 
            )
        else:

            request_data['restaurant'] = my_restaurant.id # type: ignore
            request_data['delivery_company'] = int(delivery_selected_id) # type: ignore
            
            serializer = Restaurant_Delivery_Company_Serializer(
                data=request_data,
                context={'include_details': True}  # Adjust context as needed
            )

        if serializer.is_valid():
            instance = serializer.save()
            if updating_restaurant_delivery:
                return Response({'message': f"{RESTAURANT_DELIVERY_COMPANY_UPDATED}"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f"{RESTAURANT_DELIVERY_COMPANY_CREATED}", 'id': instance.id}, status=status.HTTP_201_CREATED) # type: ignore
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        if not my_restaurant.restaurant_deliveries_edition_is_pending:
            print(f"{YOU_HAVE_TO_START_EDITING_RESTAURANT_DELIVERIES_FIRST}")
            return Response({"error": f"{YOU_HAVE_TO_START_EDITING_RESTAURANT_DELIVERIES_FIRST}"}, status=status.HTTP_403_FORBIDDEN)
        else:
            print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
            return Response({"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"}, status=status.HTTP_403_FORBIDDEN)
       
# @csrf_protect
@api_view(["POST"])
@transaction.atomic
def start_restaurant_deliveries_editing(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]
    
    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if (my_restaurant.currently_logged_in > -1) or (
            my_restaurant.currently_logged_in == -10
        ):
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                if my_restaurant.currently_logged_in != -10:
                    try:
                        my_restaurant_user = Restaurant_User.objects.get(
                            pk=my_restaurant.currently_logged_in
                        )
                    except Restaurant_User.DoesNotExist:
                        return Response(
                            {"error": f"{USER_DOES_NOT_EXIST}"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )
                try:
                    my_restaurant.restaurant_deliveries_edition_is_pending = True
                    my_restaurant.save()

                    my_restaurant_delivery_companies = (
                        Restaurant_Delivery_Company.objects.filter(
                            restaurant=my_restaurant.id # type: ignore
                        )
                    )

                    if my_restaurant_delivery_companies.exists():
                        my_restaurant_delivery_companies.update(
                            private_token=F("public_token"),
                            recently_created=False,
                            has_been_modified=False,
                            marked_for_deletion=False,
                        )

                    return Response(
                        {
                            "message": f"{YOU_MAY_START_EDITING_RESTAURANT_DELIVERIES}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )

                except Exception as e:
                    return Response(
                        {"error": f"{ERROR_OCURRED_WITH_UPDATES_OR_FILTER}"},
                        status=status.HTTP_410_GONE,
                    )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_LOGIN_FIRST}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# @csrf_protect
@api_view(["POST"])
@transaction.atomic
def publish_restaurant_deliveries_editing(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.restaurant_deliveries_edition_is_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                performer = Restaurant_Deliveries_Editing_Publish_or_Discard()
                result = performer.publish_restaurant_deliveries_editing(my_restaurant)
                return Response(
                    {
                        "message": f"{result['message']}", # type: ignore
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=int(result["return_code"]), # type: ignore
                )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_START_EDITING_RESTAURANT_DELIVERIES_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
@api_view(["GET"])
def load_delivery_companies(request, restaurant_id):
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

    delivery_company = Delivery_Company.objects.filter(
        country=my_restaurant.public_country.id # type: ignore
    )
    serializer = Delivery_Company_Serializer(delivery_company, many=True)
    data = [{"delivery_company": item} for item in serializer.data]
    return Response(data, status=status.HTTP_200_OK)

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def discard_restaurant_deliveries_editing(request, restaurant_id):
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
    performer = Restaurant_Deliveries_Editing_Publish_or_Discard()
    result = performer.discard_restaurant_deliveries_editing(my_restaurant)
    return Response(
        {
            "message": f"{result['message']}", # type: ignore
            "new_token": check_authorization_result["new_token"],
        },
        status=int(result["return_code"]), # type: ignore
    )

# Promotions -----------------------------------------------
       
@api_view(['PATCH', 'POST'])
@transaction.atomic
def promotion(request, promotion_id):
    # For creation promotion_id must be -1
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # I'll be using updating_user for knowing if it is creating (promotion_id = -1) or updating
    # promotion_id is a str since it comes from a regular expression
    # re_path(r'^promotion/(?P<promotion_id>-?\d+)/$', promotion)
    
    updating_promotion = int(promotion_id) > -1
    
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data.get("user_id")  # don't rename it as request_user_id
    user_random = extracted_data.get("user_random")
    restaurant_id = extracted_data.get("restaurant_id")
    # restaurant_id has to always be sent in the request
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)
    
    # check_current_user_id_and_random checks for user_id or user_random not being None
    performer = check_current_user_id_and_random()
    if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
        return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)
    
    if my_restaurant.promotions_edition_is_pending and not my_restaurant.dont_allow_further_actions_from_this_user:
        # Get rid of the extra fields before passing request.data to the serializer
        request.data.pop("restaurant_id", None)
        request.data.pop("user_id", None)
        request.data.pop("user_random", None)
        
        if updating_promotion:
            # Update existing promotion
            try:
                my_promotion = Promotion.objects.get(pk=int(promotion_id))
            except Promotion.DoesNotExist:
                return Response({'error': 'promotion not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = Promotion_Serializer(my_promotion, data=request.data, partial=True)
        else:
            # Create new promotion
            new_promotion_data = request.data.copy()
            # This is needed when we're creating based on the serializer
            new_promotion_data['restaurant'] = my_restaurant.id # type: ignore
            serializer = Promotion_Serializer(data=new_promotion_data)
            
        if serializer.is_valid():
            instance = serializer.save()
            if updating_promotion:
                return Response({'message': f"{PROMOTION_UPDATED}"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f"{PROMOTION_CREATED}", 'id': instance.id}, status=status.HTTP_201_CREATED) # type: ignore
        else:
            print('serializer is not valid')
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Please leave these questions there
        if not my_restaurant.promotions_edition_is_pending:
            print(f"{START_EDITING_PROMOTIONS_FIRST}")
            return Response({"error": f"{START_EDITING_PROMOTIONS_FIRST}"}, status=status.HTTP_403_FORBIDDEN)
        else:
            print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
            return Response({"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"}, status=status.HTTP_403_FORBIDDEN)

        
# @csrf_protect
@api_view(["POST"])
@transaction.atomic
def start_promotions_editing(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if (my_restaurant.currently_logged_in > -1) or (
            my_restaurant.currently_logged_in == -10
        ):
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                if my_restaurant.currently_logged_in != -10:
                    try:
                        my_restaurant_user = Restaurant_User.objects.get(
                            pk=my_restaurant.currently_logged_in
                        )
                    except Restaurant_User.DoesNotExist:
                        return Response(
                            {"error": f"{USER_DOES_NOT_EXIST}"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )
                try:
                    my_restaurant.promotions_edition_is_pending = True
                    my_restaurant.save()

                    my_promotions = Promotion.objects.filter(
                        restaurant=my_restaurant.id # type: ignore
                    )

                    if my_promotions.exists():
                        my_promotions.update(
                            private_name=F("public_name"),
                            private_attractor_text=F("public_attractor_text"),
                            private_promotion_text=F("public_promotion_text"),
                            recently_created=False,
                            has_been_modified=False,
                            marked_for_deletion=False,
                        )

                    return Response(
                        {
                            "message": f"{YOU_MAY_START_EDITING_PROMOTIONS}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )

                except Exception as e:
                    return Response(
                        {"error": f"{ERROR_OCURRED_WITH_UPDATES_OR_FILTER}"},
                        status=status.HTTP_410_GONE,
                    )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_LOGIN_FIRST}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def discard_promotions_editing(request, restaurant_id):
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
    performer = Promotions_Editing_Publish_or_Discard()
    result = performer.discard_promotions_editing(my_restaurant)
    return Response(
        {
            "message": f"{result['message']}", # type: ignore
            "new_token": check_authorization_result["new_token"],
        },
        status=int(result["return_code"]), # type: ignore
    )
    
# @csrf_protect
@api_view(["POST"])
@transaction.atomic
def publish_promotions_editing(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.promotions_edition_is_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                performer = Promotions_Editing_Publish_or_Discard()
                result = performer.publish_promotions_editing(my_restaurant)
                return Response(
                    {
                        "message": f"{result['message']}", # type: ignore
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=int(result["return_code"]), # type: ignore
                )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_START_EDITING_PROMOTIONS_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# Restaurant ---------------------------------------------------
# Preferences --------------------------------------------------

@api_view(["GET"])
def check_restaurant_existence(request, pk):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        my_restaurant = Restaurant.objects.get(pk=pk)
    except Restaurant.DoesNotExist:
        return Response(-1, status=status.HTTP_200_OK)
    
    return Response(1, status=status.HTTP_200_OK)

@api_view(["GET"])
def check_restaurant_rut_existence(request, rut):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_restaurant = Restaurant.objects.get(rut=rut)
        print(f'the restaurant with rut {rut} does not exist')
    except Restaurant.DoesNotExist:
        print(f'the restaurant with rut {rut} already exists')
        return Response(False, status=status.HTTP_200_OK)
    
    return Response(True, status=status.HTTP_200_OK)

# @api_view(["GET"])
# def did_data_change(request, restaurant_id):
#     check_authorization_result = check_authorization(request)
#     if not check_authorization_result["valid"]:
#         return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
#     try:
#         my_restaurant = Restaurant.objects.get(pk=restaurant_id)
#     except Restaurant.DoesNotExist:
#         print(f'the restaurant does not exist')
#         return Response(False, status=status.HTTP_200_OK)
    
#     return Response(my_restaurant.data_changed, status=status.HTTP_200_OK)

# @api_view(["POST"])
# @transaction.atomic
# def set_data_changed(request, restaurant_id):
#     check_authorization_result = check_authorization(request)
#     if not check_authorization_result["valid"]:
#         return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
#     try:
#         my_restaurant = Restaurant.objects.get(pk=restaurant_id)
#     except Restaurant.DoesNotExist:
#         print(f'the restaurant does not exist')
#         return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
    
#     # Set data_changed to True
#     my_restaurant.data_changed = True
#     my_restaurant.save()  # Save the change to the database
    
#     return Response({"message": "Data changed successfully"}, status=status.HTTP_200_OK)
  
@api_view(["GET"])
def get_country_by_name(request, country_name):
    # Check for authorization
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Query the country
        country = Country.objects.get(name=country_name)
        country_serializer = Country_Serializer(country)

        return Response(
            {
                "country": country_serializer.data,
                "new_token": check_authorization_result["new_token"],  # Optional: Return refreshed token
            },
            status=status.HTTP_200_OK,
        )
    except Country.DoesNotExist:
        return Response(
            {"error": f"Country with name '{country_name}' does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"error": f"An error occurred while retrieving the country: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@api_view(["GET"])
def get_country_by_id(request, country_id):
    # Check for authorization
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        # Query the country
        country = Country.objects.get(pk=country_id)
        country_serializer = Country_Serializer(country)

        return Response(
            {
                "country": country_serializer.data,
                "new_token": check_authorization_result["new_token"],  # Optional: Return refreshed token
            },
            status=status.HTTP_200_OK,
        )
    except Country.DoesNotExist:
        return Response(
            {"error": f"Country with id '{country_id}' does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response(
            {"error": f"An error occurred while retrieving the country: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
   
@api_view(["PATCH", "POST"])
@transaction.atomic
def restaurant(request, create=0):
    # if create == -1 it is taken as true
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    updating_restaurant = int(create) > -1

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data.get("user_id")  # don't rename it as request_category_id
    user_random = extracted_data.get("user_random")
    restaurant_id = extracted_data.get("restaurant_id")

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        print(f'{RESTAURANT_DOES_NOT_EXIST}')
        return Response({"error": f'{RESTAURANT_DOES_NOT_EXIST}'}, status=status.HTTP_404_NOT_FOUND)

    performer = check_current_user_id_and_random()
    if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
        return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)

    if my_restaurant.preferences_edition_is_pending and not my_restaurant.dont_allow_further_actions_from_this_user:
        # Get rid of the extra fields before passing request.data to the serializer
        request.data.pop("restaurant_id", None)
        request.data.pop("user_id", None)
        request.data.pop("user_random", None)
        if updating_restaurant:
            serializer = Restaurant_Serializer(my_restaurant, data=request.data, partial=True)
        else:
            new_restaurant_data = request.data.copy()
            serializer = Restaurant_Serializer(data=new_restaurant_data)
        if serializer.is_valid():
            instance = serializer.save()
            if updating_restaurant:
                return Response({'message': f"{RESTAURANT_UPDATED}"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f"{RESTAURANT_CREATED}", 'id': instance.id}, status=status.HTTP_201_CREATED) # type: ignore
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        if not my_restaurant.preferences_edition_is_pending:
            return Response({"error": f"{START_EDITING_PREFERENCES_FIRST}"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"}, status=status.HTTP_403_FORBIDDEN)

@api_view(["PATCH"])
@transaction.atomic
def restaurant_basic_data(request):
    # Check authorization
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        data = json.loads(request.body)  # Load JSON data
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    print(f"Extracted data: {data}")  # Debugging

    restaurant_id = data.get("restaurant_id")

    if not restaurant_id:
        return JsonResponse({"error": "Restaurant ID is required"}, status=400)

    try:
        restaurant_id = int(restaurant_id)
    except ValueError:
        return JsonResponse({"error": "Invalid Restaurant ID"}, status=400)

    # Get restaurant
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    print(f"restaurant.id:: {restaurant.id}") # type: ignore

    # Update fields
    rut = data.get("rut")
    next_price_type = data.get("next_price_type")

    print(f"rut:: {rut}")
    print(f"next_price_type:: {next_price_type}")

    if rut is not None:
        restaurant.rut = rut
    if next_price_type is not None:
        restaurant.next_price_type = next_price_type

    restaurant.save()

    print("Restaurant updated successfully")
    return JsonResponse({"message": "Restaurant updated successfully"}, status=200)

        
@api_view(["GET"])
def get_restaurant_from_rut(request, restaurant_rut):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result.get("valid", False):
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
    except Restaurant.DoesNotExist:
        print(f"{RESTAURANT_DOES_NOT_EXIST}")
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = Restaurant_Serializer(my_restaurant)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_restaurant_main_user_email(request, restaurant_id):
    restaurant_id = int(restaurant_id)
    check_authorization_result = check_authorization(request)
    if not check_authorization_result.get("valid", False):
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        restaurant_rut = None
        if restaurant_id == -1:
            restaurant_rut = request.GET.get("restaurant_rut")
        if restaurant_rut:  # Check if restaurant_id is -1 and restaurant_rut is provided
            my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
        else:
            my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        print(f"{RESTAURANT_DOES_NOT_EXIST}; restaurant_id, restaurant_rut:: {restaurant_id}, {restaurant_rut}") # type: ignore
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
        
    try:
        my_restaurant_main_user = Restaurant_User.objects.get(id=my_restaurant.main_user_id)
    except Restaurant_User.DoesNotExist:
        return Response(
            {"error": f"{MAIN_USER_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {"main_user_email": f"{my_restaurant_main_user.public_email}"},
        status=status.HTTP_200_OK,
    )
    
@api_view(["PUT"])
def update_restaurant_user_name_and_password(request, user_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result.get("valid", False):
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        restaurant_user = Restaurant_User.objects.get(id=user_id)
    except Restaurant_User.DoesNotExist:
        return Response(
            {"error": "User does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    data = request.data
    new_name = data.get("public_name", "").strip()
    new_password = data.get("public_password", "").strip()
    
    if not new_name:
        return Response({"error": "Public name is required"}, status=status.HTTP_400_BAD_REQUEST)
    if not new_password:
        return Response({"error": "Public password is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Encrypt password before saving
    restaurant_user.public_name = new_name
    restaurant_user.public_password = encrypt_value(new_password)
    restaurant_user.save()
    
    return Response(
        {"message": "User updated successfully"},
        status=status.HTTP_200_OK,
    )

    
@api_view(["GET"])
def get_restaurant_main_user_data(request, restaurant_id):
    restaurant_id = int(restaurant_id)
    check_authorization_result = check_authorization(request)
    if not check_authorization_result.get("valid", False):
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        restaurant_rut = None
        if restaurant_id == -1:
            restaurant_rut = request.GET.get("restaurant_rut")
        if restaurant_rut:  # Check if restaurant_id is -1 and restaurant_rut is provided
            my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
        else:
            my_restaurant = Restaurant.objects.get(pk=restaurant_id)
            
    except Restaurant.DoesNotExist:
        print(f"{RESTAURANT_DOES_NOT_EXIST}; restaurant_id, restaurant_rut:: {restaurant_id}, {restaurant_rut}") # type: ignore
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    try:
        my_restaurant_main_user = Restaurant_User.objects.get(id=my_restaurant.main_user_id)
    except Restaurant_User.DoesNotExist:
        return Response(
            {"error": f"{USER_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
        
    return Response(
        {
            "main_user_id": my_restaurant_main_user.id, # type: ignore
            "main_user_email": my_restaurant_main_user.public_email,
            "main_user_name": my_restaurant_main_user.public_name,  
        },
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@transaction.atomic
def save_new_restaurant_data(request):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result.get("valid", False):
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    # Extract and validate input data
    required_fields = ["document_value", "country_id", "price_type", "user_name", "user_password", "user_email"]
    for field in required_fields:
        if field not in request.data:
            return Response({"error": f"Missing {field}"}, status=status.HTTP_400_BAD_REQUEST)
    new_restaurant_rut = request.data["document_value"]
    new_restaurant_country_id = request.data["country_id"]
    new_restaurant_price_type = request.data["price_type"]
    new_restaurant_user_name = request.data["user_name"]
    new_restaurant_user_password = request.data["user_password"]
    new_restaurant_user_email = request.data["user_email"]
    try:
        # Encrypt the password
        new_restaurant_encrypted_password = encrypt_value(new_restaurant_user_password)
    except Exception as e:
        return Response({"error": f"Password encryption failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    existing_restaurant_data = New_Restaurant_Data.objects.filter(rut=new_restaurant_rut)
    existing_restaurant_data.delete()
    
    # if existing_restaurant_data:
    #     # Check if the `created_at` field is more than a day old
    #     if existing_restaurant_data.created_at < now() - timedelta(days=1):
    #         # Delete the old record
    #         existing_restaurant_data.delete()
    #     else:
    #         # Return an error if the record is less than a day old
    #         return Response({"error": "A restaurant with this RUT is already being created"}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        my_new_restaurant_data = New_Restaurant_Data.objects.create(
            rut=new_restaurant_rut,
            country_id=new_restaurant_country_id,
            price_type=new_restaurant_price_type,
            user_name=new_restaurant_user_name,
            user_password=new_restaurant_encrypted_password,
            user_email=new_restaurant_user_email
        )
    except Exception as e:
        print(f"Failed to create restaurant: {str(e)}")
        return Response({"error": f"Failed to create restaurant: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(
        {"message": "New Restaurant Data created successfully!"},
        status=status.HTTP_201_CREATED,
    )
    
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def start_preferences_editing(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if (my_restaurant.currently_logged_in > -1) or (
            my_restaurant.currently_logged_in == -10
        ):
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                # -10 is the id of a super user (Atonn)
                if my_restaurant.currently_logged_in != -10:
                    try:
                        my_restaurant_user = Restaurant_User.objects.get(
                            pk=my_restaurant.currently_logged_in
                        )
                    except Restaurant_User.DoesNotExist:
                        return Response(
                            {"error": f"{USER_DOES_NOT_EXIST}"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )

                try:
                    my_restaurant.private_name = F("public_name")
                    my_restaurant.private_description = F("public_description")
                    my_restaurant.private_address = F("public_address")
                    my_restaurant.private_country = my_restaurant.public_country
                    my_restaurant.private_phone = F("public_phone")
                    my_restaurant.private_instagram_url = F("public_instagram_url")
                    my_restaurant.private_facebook_url = F("public_facebook_url")
                    my_restaurant.private_twitter_url = F("public_twitter_url")
                    my_restaurant.private_website_url = F("public_website_url")
                    my_restaurant.private_facade_image_id = F("public_facade_image_id")
                    my_restaurant.private_logo_image_id = F("public_logo_image_id")
                    my_restaurant.private_show_images = F("public_show_images")
                    my_restaurant.private_show_restaurant_reviews = F(
                        "public_show_restaurant_reviews"
                    )
                    my_restaurant.private_show_dishes_reviews = F(
                        "public_show_dishes_reviews"
                    )
                    my_restaurant.private_show_prices = F("public_show_prices")
                    my_restaurant.private_show_ask_button = F("public_show_ask_button")
                    my_restaurant.private_monday_open_hour_in_minutes = F(
                        "public_monday_open_hour_in_minutes"
                    )
                    my_restaurant.private_tuesday_open_hour_in_minutes = F(
                        "public_tuesday_open_hour_in_minutes"
                    )
                    my_restaurant.private_wednesday_open_hour_in_minutes = F(
                        "public_wednesday_open_hour_in_minutes"
                    )
                    my_restaurant.private_thursday_open_hour_in_minutes = F(
                        "public_thursday_open_hour_in_minutes"
                    )
                    my_restaurant.private_friday_open_hour_in_minutes = F(
                        "public_friday_open_hour_in_minutes"
                    )
                    my_restaurant.private_saturday_open_hour_in_minutes = F(
                        "public_saturday_open_hour_in_minutes"
                    )
                    my_restaurant.private_sunday_open_hour_in_minutes = F(
                        "public_sunday_open_hour_in_minutes"
                    )

                    my_restaurant.private_monday_close_hour_in_minutes = F(
                        "public_monday_close_hour_in_minutes"
                    )
                    my_restaurant.private_tuesday_close_hour_in_minutes = F(
                        "public_tuesday_close_hour_in_minutes"
                    )
                    my_restaurant.private_wednesday_close_hour_in_minutes = F(
                        "public_wednesday_close_hour_in_minutes"
                    )
                    my_restaurant.private_thursday_close_hour_in_minutes = F(
                        "public_thursday_close_hour_in_minutes"
                    )
                    my_restaurant.private_friday_close_hour_in_minutes = F(
                        "public_friday_close_hour_in_minutes"
                    )
                    my_restaurant.private_saturday_close_hour_in_minutes = F(
                        "public_saturday_close_hour_in_minutes"
                    )
                    my_restaurant.private_sunday_close_hour_in_minutes = F(
                        "public_sunday_close_hour_in_minutes"
                    )

                    my_restaurant.preferences_edition_is_pending = True
                    my_restaurant.save()

                    return Response(
                        {
                            "message": f"{YOU_MAY_START_EDITING_PREFERENCES}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )
                except Exception as e:
                    return Response(
                        {"error": f"An error occurred: {str(e)}"},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_LOGIN_FIRST}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def discard_preferences_editing(request, restaurant_id):
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
    performer = Preferences_Editing_Publish_or_Discard()
    result = performer.discard_preferences_editing(my_restaurant)
    return Response(
        {
            "message": f"{result['message']}", # type: ignore
            "new_token": check_authorization_result["new_token"],
        },
        status=result["return_code"], # type: ignore
    )
    
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def publish_preferences_editing(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.preferences_edition_is_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                performer = Preferences_Editing_Publish_or_Discard()
                result = performer.publish_preferences_editing(my_restaurant)
                return Response(
                    {
                        "message": f"{result['message']}", # type: ignore
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=result["return_code"], # type: ignore
                )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_START_EDITING_PREFERENCES_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
@api_view(['PATCH'])
def save_device_description(request, device_description):   
    try:
        accessing_device = Accessing_Devices(
            device_description=device_description,
        )
        accessing_device.save()
    except Exception as e:
        # Log the error or print it for debugging
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    # Serialize the new record
    serializer = Accessing_Devices_Serializer(accessing_device)

    # Return a custom response
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Restaurant_User --------------------------------------
# Users -------------------------------------------------

@api_view(['GET'])
def retrieve_restaurant_user_for_edition(request, user_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_restaurant_user = Restaurant_User.objects.get(pk=user_id)
    except Restaurant_User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response(
        {
            "id": my_restaurant_user.id, # type: ignore
            "name":my_restaurant_user.private_name,
            # "phone":my_restaurant_user.private_phone,
            "image_id":my_restaurant_user.private_image_id,
            "password":decrypt_value(my_restaurant_user.private_password),
            "email":my_restaurant_user.private_email,
            "email_validated":my_restaurant_user.private_email_validated,
            # "phone_validated":my_restaurant_user.private_phone_validated,
            "new_token": check_authorization_result["new_token"],
        },
        status=status.HTTP_200_OK,
    )
    
@api_view(['GET'])
@transaction.atomic
def check_user_credentials(request, restaurant_rut):
    check_authorization_result = check_authorization(request) 
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Use request.GET instead of request.body
    user_name = request.GET.get("user_name")
    user_password = request.GET.get("user_password")

    if not user_name or not user_password:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        my_restaurant_user = Restaurant_User.objects.get(
            restaurant=my_restaurant, 
            public_name=user_name, 
            main_user=True
        )
    except Restaurant_User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    my_user_password = my_restaurant_user.get_decrypted_public_password() # type: ignore

    if user_password == my_user_password:
        return Response({"message": f"{CREDENTIALS_ARE_OK}"}, status=status.HTTP_200_OK)

    print(f"{CREDENTIALS_ARE_WRONG}")
    return Response({"error": f"{CREDENTIALS_ARE_WRONG}"}, status=status.HTTP_404_NOT_FOUND)

    
    
@api_view(['PATCH', 'POST'])#
@transaction.atomic
def restaurant_user(request, restaurant_user_id):
    # For creation restaurant_user_id must be -1
    check_authorization_result = check_authorization(request) 
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # I'll be using updating_user for knowing if it is creating (restaurant_user_id = -1) or updating,
    # restaurant_user_id is a str since it comes from a regular expression
    # re_path(r'^restaurant_user/(?P<restaurant_user_id>-?\d+)/$', restaurant_user)
    updating_user = int(restaurant_user_id) > -1
    
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data.get("user_id")  # don't rename it as request_user_id
    user_random = extracted_data.get("user_random")
    restaurant_id = extracted_data.get("restaurant_id")
    # restaurant_id has to always be sent in the request
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)
    
    # check_current_user_id_and_random checks for user_id or user_random not being None
    performer = check_current_user_id_and_random()
    if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
        return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)
    
    if my_restaurant.users_edition_is_pending and not my_restaurant.dont_allow_further_actions_from_this_user:
        # Get rid of the extra fields before passing request.data to the serializer
        request.data.pop("restaurant_id", None)
        request.data.pop("user_id", None)
        request.data.pop("user_random", None)
        
        if updating_user:
            # Update existing user
            try:
                my_restaurant_user = Restaurant_User.objects.get(pk=int(restaurant_user_id))
            except Restaurant_User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = Restaurant_User_Update_or_Create_Serializer(my_restaurant_user, data=request.data, partial=True)
        else:
            number_of_existing_users = Restaurant_User.objects.filter(
                    restaurant=restaurant_id
            ).count()

            if number_of_existing_users == MAX_NUMBER_OF_USERS:
                return Response(
                    {"error": f"{USERS_NUMBER_IS_AT_THE_MAXIMUM}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
                
            # Create new user
            new_user_data = request.data.copy()
            # Useful_procedures.FORMATTED_PRINT('request.data.copy:: ', request.data.copy)
            # This is needed when we're creating based on the serializer
            
            new_user_data['restaurant'] = my_restaurant.id # type: ignore
            
            # Useful_procedures.FORMATTED_PRINT('new_user_data:: ', new_user_data)
            try:
                serializer = Restaurant_User_Update_or_Create_Serializer(data=new_user_data)
            except Exception as e:
                print(f"error:: {e}")
                raise
        if serializer.is_valid():
            instance = serializer.save()
            if updating_user:
                return Response({'message': f"{USER_UPDATED}"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f"{RESTAURANT_USER_CREATED}", 'id': instance.id}, status=status.HTTP_201_CREATED) # type: ignore
        else:
            print('serializer is not valid')
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Please leave these questions there
        if not my_restaurant.users_edition_is_pending:
            print(f"{START_EDITING_USERS_FIRST}")
            return Response({"error": f"{START_EDITING_USERS_FIRST}"}, status=status.HTTP_403_FORBIDDEN)
        else:
            print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
            return Response({"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"}, status=status.HTTP_403_FORBIDDEN)

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def discard_restaurant_users_editing(request, restaurant_id):
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
    performer = Restaurant_Users_Editing_Publish_or_Discard()
    result = performer.discard_restaurant_users_editing(my_restaurant)
    return Response(
        {
            "message": f"{result['message']}", # type: ignore
            "new_token": check_authorization_result["new_token"],
        },
        status=result["return_code"], # type: ignore
    )
    
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def start_restaurant_users_editing(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if (my_restaurant.currently_logged_in > -1) or (
            my_restaurant.currently_logged_in == -10
        ):
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                if my_restaurant.currently_logged_in != -10:
                    try:
                        my_restaurant_user = Restaurant_User.objects.get(
                            pk=my_restaurant.currently_logged_in
                        )
                    except Restaurant_User.DoesNotExist:
                        print(f"{USER_DOES_NOT_EXIST}")
                        return Response(
                            {"error": f"{USER_DOES_NOT_EXIST}"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )

                try:
                    all_users = Restaurant_User.objects.filter(
                        restaurant=my_restaurant.id # type: ignore
                    )
                    all_users.update(
                        private_name=F("public_name"),
                        # private_phone=F("public_phone"),
                        private_image_id=F("public_image_id"),
                        private_password=F("public_password"),
                        private_email=F("public_email"),
                        private_email_validated=F("public_email_validated"),
                        # private_phone_validated=F("public_phone_validated"),
                        marked_for_deletion=False,
                        recently_created=False,
                        has_been_modified=False,
                    )
                    my_restaurant.users_edition_is_pending = True
                    my_restaurant.save()

                    return Response(
                        {
                            "message": f"{YOU_MAY_START_EDITING}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )

                except Exception as e:
                    print(f"{ERROR_OCURRED_WITH_UPDATES_OR_FILTER}")
                    return Response(
                        {"error": f"{ERROR_OCURRED_WITH_UPDATES_OR_FILTER}"},
                        status=status.HTTP_410_GONE,
                    )
            else:
                print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        else:
            print(f"{YOU_HAVE_TO_LOGIN_FIRST}")
            return Response(
                {"error": f"{YOU_HAVE_TO_LOGIN_FIRST}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
    else:
        print(f"{KEYS_DO_NOT_MATCH}")
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def publish_restaurant_users_editing(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.users_edition_is_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                performer = Restaurant_Users_Editing_Publish_or_Discard()
                result = performer.publish_restaurant_users_editing(my_restaurant)
                return Response(
                    {
                        "message": f"{result['message']}", # type: ignore
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=result["return_code"], # type: ignore
                )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_START_EDITING_USERS_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
@api_view(["GET"])
def load_restaurant_users(request, restaurant_id):
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
    restaurant_users = Restaurant_User.objects.filter(restaurant=my_restaurant)
    users_serializer = Restaurant_User_Retrieve_Serializer(restaurant_users, many=True)
    data = [{"restaurant_user": item} for item in users_serializer.data]

    return Response(data, status=status.HTTP_200_OK)

# Menu Editing --------------------------------------------------------

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def start_menu_editing(request, restaurant_id):
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
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if (my_restaurant.currently_logged_in > -1) or (
            my_restaurant.currently_logged_in == -10
        ):
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                if my_restaurant.currently_logged_in != -10:
                    try:
                        my_restaurant_user = Restaurant_User.objects.get(
                            pk=my_restaurant.currently_logged_in
                        )
                    except Restaurant_User.DoesNotExist:
                        return Response(
                            {"error": f"{USER_DOES_NOT_EXIST}"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )

                try:
                    my_restaurant.menu_edition_is_pending = True
                    my_restaurant.save()
                    my_categories = Category.objects.filter(restaurant=my_restaurant.id) # type: ignore
                    if not my_categories.exists():
                        return Response(
                            {"message": f"{NO_MENU_TO_EDIT}"},
                            status=status.HTTP_200_OK,
                        )
                    my_categories.update(
                        private_name=F("public_name"),
                        private_description=F("public_description"),
                        private_image_id=F("public_image_id"),
                        recently_created=False,
                        has_been_modified=False,
                        marked_for_deletion=False,
                    )
                    my_dishes = Dish.objects.filter(category__in=my_categories)
                    if my_dishes.exists():
                        my_dishes.update(
                            private_name=F("public_name"),
                            private_description=F("public_description"),
                            private_image_id=F("public_image_id"),
                            private_price=F("public_price"),
                            recently_created=False,
                            marked_for_deletion=False,
                            marked_for_deletion_by_parent=False,
                        )

                    return Response(
                        {
                            "message": f"{YOU_MAY_START_EDITING}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )

                except Exception as e:
                    return Response(
                        {"error": f"{ERROR_OCURRED_WITH_UPDATES_OR_FILTER}"},
                        status=status.HTTP_410_GONE,
                    )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_LOGIN_FIRST}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def discard_menu_editing(request, restaurant_id):
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
    performer = Menu_Editing_Publish_or_Discard()
    result = performer.discard_menu_editing(my_restaurant)
    return Response(
        {
            "message": f"{result['message']}", # type: ignore
            "new_token": check_authorization_result["new_token"],
        },
        status=result["return_code"], # type: ignore
    )

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def publish_menu_editing(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.menu_edition_is_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                performer = Menu_Editing_Publish_or_Discard()
                result = performer.publish_menu_editing(my_restaurant)

                return Response(
                    {
                        "message": f"{result['message']}", # type: ignore
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=result["return_code"], # type: ignore
                )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{START_EDITING_MENU_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
# Category ---------------------------------------------------

# @csrf_protect
@api_view(["PATCH", "POST"])
@transaction.atomic
def category(request, category_id, private_view_order=None):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    updating_category = int(category_id) > -1

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data.get("user_id")  # don't rename it as request_category_id
    user_random = extracted_data.get("user_random")
    restaurant_id = extracted_data.get("restaurant_id")

    # restaurant_id has to always be sent in the request
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)

    # check_current_user_id_and_random checks for user_id or user_random not being None
    performer = check_current_user_id_and_random()
    if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
        return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)

    edition_is_pending = my_restaurant.menu_edition_is_pending

    if private_view_order is not None:
        edition_is_pending = my_restaurant.menu_sorting_is_pending

    if edition_is_pending and not my_restaurant.dont_allow_further_actions_from_this_user:
        # Get rid of the extra fields before passing request.data to the serializer
        request.data.pop("restaurant_id", None)
        request.data.pop("user_id", None)
        request.data.pop("user_random", None)

        if private_view_order is not None:
            # Case 3: Setting the private_view_order
            if int(private_view_order) <= 0:
                return Response(
                    {"error": f"{VIEW_ORDER_CAN_NOT_BE_ZERO_NOR_LESS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            # Ensure the category exists
            try:
                my_category = Category.objects.get(pk=int(category_id))
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
            
            my_category.private_view_order = private_view_order
            my_category.has_been_modified = True
            my_category.save()

            return Response(
                {
                    "message": f"{CATEGORY_VIEW_ORDER_HAS_BEEN_SET}",
                    "new_token": check_authorization_result["new_token"],
                },
                status=status.HTTP_200_OK,
            )

        if updating_category:
            # Case 2: Updating an existing category
            try:
                my_category = Category.objects.get(pk=int(category_id))
            except Category.DoesNotExist:
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = Category_Serializer(my_category, data=request.data, partial=True)
        else:
            # Case 1: Creating a new category
            new_category_data = request.data.copy()
            # This is needed when we're creating based on the serializer
            new_category_data['restaurant'] = my_restaurant.id # type: ignore
            serializer = Category_Serializer(data=new_category_data)

        if serializer.is_valid():
            instance = serializer.save()
            if updating_category:
                return Response({'message': f"{CATEGORY_UPDATED}"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f"{CATEGORY_CREATED}", 'id': instance.id}, status=status.HTTP_201_CREATED) # type: ignore
        else:
            print('serializer is not valid')
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Check if menu editing is not pending or further actions are not allowed
        if not edition_is_pending:
            message = f"{START_EDITING_MENU_FIRST}"
            if private_view_order is not None:
                message = f"{START_SORTING_FIRST}"
            print(f"{message}")
            return Response({"error": f"{message}"}, status=status.HTTP_403_FORBIDDEN)
        else:
            print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
            return Response({"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"}, status=status.HTTP_403_FORBIDDEN)

# Dish ---------------------------------------------------

# @csrf_protect
@api_view(["PATCH", "POST"])
@transaction.atomic
def dish(request, category_id, dish_id, private_view_order=None):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    updating_dish = int(dish_id) > -1

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data.get("user_id")  # don't rename it as request_category_id
    user_random = extracted_data.get("user_random")
    restaurant_id = extracted_data.get("restaurant_id")

    # restaurant_id has to always be sent in the request
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)

    try:
        my_category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Category({"error": f"{CATEGORY_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)

    # check_current_user_id_and_random checks for user_id or user_random not being None
    performer = check_current_user_id_and_random()
    if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
        return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)

    edition_is_pending = my_restaurant.menu_edition_is_pending
    
    if private_view_order is not None:
        edition_is_pending = my_restaurant.menu_sorting_is_pending

    if edition_is_pending and not my_restaurant.dont_allow_further_actions_from_this_user:
        # Get rid of the extra fields before passing request.data to the serializer
        request.data.pop("restaurant_id", None)
        request.data.pop("user_id", None)
        request.data.pop("user_random", None)
        if updating_dish:
            try:
                my_dish = Dish.objects.get(pk=int(dish_id))
            except Dish.DoesNotExist:
                return Response({'error': 'Dish not found'}, status=status.HTTP_404_NOT_FOUND)
            # Case 3: Setting the private_view_order
            if private_view_order is not None:
                if int(private_view_order) <= 0:
                    return Response(
                        {"error": f"{VIEW_ORDER_CAN_NOT_BE_ZERO_NOR_LESS}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                my_dish.private_view_order = private_view_order
                my_dish.has_been_modified = True
                my_dish.save()

                return Response(
                    {
                        "message": f"{DISH_VIEW_ORDER_HAS_BEEN_SET}",
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=status.HTTP_200_OK,
                )

            # Case 2: Updating a dish
            serializer = Dish_Serializer(my_dish, data=request.data, partial=True)
        else:
            # Case 1: Creating a new dish
            new_dish_data = request.data.copy()
            # This is needed when we're creating based on the serializer
            new_dish_data['category'] = category_id
            serializer = Dish_Serializer(data=new_dish_data)

        if serializer.is_valid():
            instance = serializer.save()
            if updating_dish:
                return Response({'message': f"{DISH_UPDATED}"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f"{DISH_CREATED}", 'id': instance.id}, status=status.HTTP_201_CREATED) # type: ignore
        else:
            print('serializer is not valid')
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Please leave these questions there
        if not edition_is_pending:
            message = f"{START_EDITING_MENU_FIRST}"
            if private_view_order is not None:
                message=f"{START_SORTING_FIRST}"
            print(f"{message}")
            return Response({"error": f"{message}"}, status=status.HTTP_403_FORBIDDEN)
        else:
            print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
            return Response({"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"}, status=status.HTTP_403_FORBIDDEN)

# @csrf_protect
@api_view(["GET"])
def check_for_dish_revisions(request, dish_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_dish = Dish.objects.get(pk=dish_id)
    except Dish.DoesNotExist:
        return Response(
            {"error": f"{DISH_DOES_NOT_EXIST}"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
        
    reviews_exist = Review.objects.filter(dish=my_dish).exists()
    
    return Response(
        {
            "message": reviews_exist,
            "new_token": check_authorization_result["new_token"],
        },
        status=status.HTTP_200_OK,
    )
    
# @csrf_protect
@api_view(["GET"])
def check_for_category_dishes_revisions(request, category_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
           
    try:
        my_category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response(
            {"error": f"{CATEGORY_DOES_NOT_EXIST}"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
        
    reviews_exist = Review.objects.filter(dish__category_id=category_id).exists()
    
    return Response(
        {
            "message": reviews_exist,
            "new_token": check_authorization_result["new_token"],
        },
        status=status.HTTP_200_OK,
    )
       
# Reviews -----------------------------------------

# @csrf_protect
@api_view(["GET"])
def all_reviews_with_rejections_if_any(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    all_reviews = All_Reviews_Class()
    if all_reviews.restaurant_was_read:
        all_reviews.Load_Reviews_And_Rejections_if_any(restaurant_id)
        return JsonResponse(all_reviews.reviews, status=status.HTTP_200_OK, safe=False)
    else:
        return Response(
            {"message": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def start_reviews_editing(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
        
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if (my_restaurant.currently_logged_in > -1) or (
            my_restaurant.currently_logged_in == -10
        ):
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                if my_restaurant.currently_logged_in != -10:
                    try:
                        my_restaurant_user = Restaurant_User.objects.get(
                            pk=my_restaurant.currently_logged_in
                        )
                    except Restaurant_User.DoesNotExist:
                        return Response(
                            {"error": f"{USER_DOES_NOT_EXIST}"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )
                try:
                    my_reviews = Review.objects.filter(restaurant=my_restaurant.id) # type: ignore

                    my_reviews.update(
                        private_rejected=F("public_rejected"),
                    )

                    my_restaurant.reviews_updates_are_pending = True
                    my_restaurant.save()

                    return Response(
                        {
                            "message": f"{YOU_MAY_START_EDITING_REVIEWS}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )

                except Exception as e:
                    return Response(
                        {"error": f"An error occurred: {str(e)}"},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_LOGIN_FIRST}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def discard_reviews_editing(request, restaurant_id):
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
    my_performer = Reviews_Editing_Publish_or_Discard()
    result = my_performer.discard_reviews_editing(my_restaurant)

    return Response(
        {
            "message": f"{result['message']}", # type: ignore
            "new_token": check_authorization_result["new_token"],
        },
        status=result["return_code"], # type: ignore
    )

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def publish_reviews_editing(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.reviews_updates_are_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                performer = Reviews_Editing_Publish_or_Discard()
                result = performer.publish_reviews_editing(my_restaurant)
                return Response(
                    {
                        "message": f"{result['message']}", # type: ignore
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=result["return_code"], # type: ignore
                )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_START_EDITING_REVIEWS_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

@api_view(["PATCH"])
@transaction.atomic
def switch_review_rejection(request, restaurant_id, review_id, rejection_reason_id_arg):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        rejection_reason_id = int(rejection_reason_id_arg)
    except ValueError:
        return Response(
            {"error": f"{REJECTION_REASON_ID_MUST_BE_AN_INTEGER}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        my_review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return Response(
            {"message": "Review does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.reviews_updates_are_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                my_review.private_rejected = not my_review.private_rejected
                my_review.rejection_status_just_changed = True
                my_review.save()

                if my_review.private_rejected:  # it is being rejected
                    try:
                        my_rejection_reason = Rejection_Reason.objects.get(
                            pk=rejection_reason_id
                        )
                    except Rejection_Reason.DoesNotExist:
                        return Response(
                            {"message": "Rejection reason does not exist."},
                            status=status.HTTP_404_NOT_FOUND,
                        )

                    try:
                        my_review_rejection = Review_Rejection.objects.get(
                            review=my_review
                        )
                    except Review_Rejection.DoesNotExist:
                        new_review_rejection = Review_Rejection.objects.create(
                            review=my_review, rejection_reason=my_rejection_reason
                        )
                        return Response(
                            {
                                "id": new_review_rejection.pk,
                                "message": "Review rejected successfully.",
                                "new_token": check_authorization_result["new_token"],
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        my_review_rejection.rejection_reason = my_rejection_reason
                        my_review_rejection.save()
                        return Response(
                            {
                                "message": "Review rejected successfully.",
                            },
                            status=status.HTTP_200_OK,
                        )

                else:  # it is being approved
                    # don't do anything else, publishing will delete pending rejections if necessary
                    return Response(
                        {"message": "Review approved successfully."},
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_START_EDITING_REVIEWS_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# re_path(r'^review/(?P<element_id>\d+)/(?P<creating>(?:true|false))/(?P<review_type>(?:restaurant|dish))/$', review),
        
# review_type can only be 'restaurant' or 'dish'
# creating can only be 'true' or 'false'
# If creating == 'true', then element_id is the id of the corresponding item, 
#    if review_type is 'dish' then element_id is the id of the 'dish' that the review belongs 
#    to. If review_type is 'restaurant' then element_id is the id of the restaurant the review belongs to
# If creating == 'false', then element_id is the id of the review itself
@api_view(["POST", "PATCH"])
@transaction.atomic
def review(request, element_id, creating='true', review_type='restaurant'):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
      
    updating_review = creating != 'true'
    
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = -1
    user_random = -10
    if updating_review:  # for updating, must be logged in
        user_id = extracted_data.get("user_id")  
        user_random = extracted_data.get("user_random")
    restaurant_id = extracted_data.get("restaurant_id")
    
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": f"{RESTAURANT_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND)
    
    can_enter = creating == 'true'
    
    if updating_review:
        performer = check_current_user_id_and_random()
        
        if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
            return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)

    if can_enter:
        # Get rid of the extra fields before passing request.data to the serializer
        if updating_review:
            request.data.pop("user_id", None)
            request.data.pop("user_random", None)
        
        new_element_data = request.data.copy()
        new_element_data['review_type'] = review_type
        
        if review_type == 'dish':
            new_element_data['dish_id'] = int(element_id)  # Ensure dish_id is included for dish reviews
        
        if updating_review:
            try:
                my_element = Review.objects.get(pk=int(element_id))
            except Review.DoesNotExist:
                return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = Review_Serializer(my_element, data=new_element_data, partial=True)
        else:
            if review_type == 'restaurant':
                try:
                    my_element = Restaurant.objects.get(pk=int(element_id))
                    if restaurant_id != int(element_id):
                        print('wrong restaurant')
                        return Response({'error': 'wrong restaurant'}, status=status.HTTP_400_BAD_REQUEST)
                except Restaurant.DoesNotExist:
                    print('Restaurant not found')
                    return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                # It's 'dish'
                try:
                    my_element = Dish.objects.get(pk=int(element_id))
                except Dish.DoesNotExist:
                    print('Dish not found')
                    return Response({'error': 'Dish not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = Review_Serializer(data=new_element_data)
            
        if serializer.is_valid():
            instance = serializer.save()
            if updating_review:
                return Response({'message': f"{REVIEW_UPDATED}"}, status=status.HTTP_200_OK)
            else:
                return Response({'message': f"{REVIEW_CREATED}", 'id': instance.id}, status=status.HTTP_201_CREATED) # type: ignore
        else:
            print('serializer is not valid')
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        if my_restaurant.dont_allow_further_actions_from_this_user:
            print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
            return Response({"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"}, status=status.HTTP_403_FORBIDDEN)
        elif my_restaurant.reviews_updates_are_pending:
            print(f"{YOU_HAVE_TO_START_EDITING_REVIEWS_FIRST}")
            return Response({"error": f"{YOU_HAVE_TO_START_EDITING_REVIEWS_FIRST}"}, status=status.HTTP_403_FORBIDDEN)
        else:
            print("unknown error")
            return Response({"error": "unknown error"}, status=status.HTTP_400_BAD_REQUEST)

                
# Sorting ------------------------------------

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def start_menu_sort_editing(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if (my_restaurant.currently_logged_in > -1) or (
            my_restaurant.currently_logged_in == -10
        ):
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                if my_restaurant.currently_logged_in != -10:
                    try:
                        my_restaurant_user = Restaurant_User.objects.get(
                            pk=my_restaurant.currently_logged_in
                        )
                    except Restaurant_User.DoesNotExist:
                        return Response(
                            {"error": f"{USER_DOES_NOT_EXIST}"},
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )
                my_restaurant.menu_sorting_is_pending = True
                my_restaurant.save()
                my_categories = Category.objects.filter(restaurant=my_restaurant.id) # type: ignore

                if not my_categories.exists():
                    return Response(
                        {
                            "message": f"{NO_MENU_TO_EDIT}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )

                my_categories.update(
                    private_name=F("public_name"),
                    private_description=F("public_description"),
                    private_image_id=F("public_image_id"),
                    private_view_order=F("public_view_order"),
                    has_been_modified=False,
                )

                my_dishes = Dish.objects.filter(category__in=my_categories)

                my_dishes.update(
                    private_name=F("public_name"),
                    private_description=F("public_description"),
                    private_image_id=F("public_image_id"),
                    private_price=F("public_price"),
                    private_view_order=F("public_view_order"),
                    has_been_modified=False,
                )

                return Response(
                    {
                        "message": f"{YOU_MAY_START_SORTING}",
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_LOGIN_FIRST}"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
        
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def discard_menu_sort_editing(request, restaurant_id):
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
    performer = Menu_Sort_Editing_Publish_or_Discard()
    result = performer.discard_menu_sort_editing(my_restaurant)
    return Response(
        {
            "message": f"{result['message']}", # type: ignore
            "new_token": check_authorization_result["new_token"],
        },
        status=result["return_code"], # type: ignore
    )
    
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def publish_menu_sort_editing(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.menu_sorting_is_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                performer = Menu_Sort_Editing_Publish_or_Discard()
                result = performer.publish_menu_sort_editing(my_restaurant)
                return Response(
                    {
                        "message": f"{result['message']}", # type: ignore
                        "new_token": check_authorization_result["new_token"],
                    },
                    status=result["return_code"], # type: ignore
                )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_START_SORTING_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def clear_all_private_view_orders(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if my_restaurant.menu_sorting_is_pending:
            if not my_restaurant.dont_allow_further_actions_from_this_user:
                try:
                    with transaction.atomic():
                        # Retrieve all restaurant categories
                        my_categories = Category.objects.filter(
                            restaurant=my_restaurant
                        )
                        my_categories.update(private_view_order=None)

                        # Loop through each category
                        for category in my_categories:
                            # Update all dishes of the current category

                            Dish.objects.filter(category=category).update(
                                private_view_order=None
                            )

                    return Response(
                        {
                            "message": f"{ORDERS_CLEARED}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )

                except Exception as e:
                    # Handle any exceptions that may occur during the update process
                    return Response(
                        {"error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                return Response(
                    {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": f"{YOU_HAVE_TO_START_SORTING_FIRST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def clear_categories_private_view_orders(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        print("Unauthorized")
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        print(f"{RESTAURANT_DOES_NOT_EXIST}")
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data.get("user_id")
    user_random = extracted_data.get("user_random")

    if user_id is None or user_random is None:
        print("User ID and User Random are required")
        return Response(
            {"error": "User ID and User Random are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    performer = check_current_user_id_and_random()
    if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
        print(f"{KEYS_DO_NOT_MATCH}")
        return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)

    if not my_restaurant.menu_sorting_is_pending:
        print(f"{YOU_HAVE_TO_START_SORTING_FIRST}")
        return Response(
            {"error": f"{YOU_HAVE_TO_START_SORTING_FIRST}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if my_restaurant.dont_allow_further_actions_from_this_user:
        print(f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}")
        return Response(
            {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Update all categories' private_view_order to None
        Category.objects.filter(restaurant=my_restaurant).update(private_view_order=None)

        return Response(
            {
                "message": f"{CATEGORY_ORDERS_CLEARED}",
                "new_token": check_authorization_result["new_token"],
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print(str(e))
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

# @csrf_protect
@api_view(["PATCH"])
@transaction.atomic
def clear_category_dishes_private_view_orders(request, category_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_category = Category.objects.select_related('restaurant').get(pk=category_id)
        my_restaurant = my_category.restaurant
    except Category.DoesNotExist:
        return Response(
            {"error": f"{CATEGORY_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data.get("user_id")
    user_random = extracted_data.get("user_random")

    if not user_id or not user_random:
        return Response(
            {"error": "User ID and User Random are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    performer = check_current_user_id_and_random()
    if not performer.check_current_user_id_and_random(my_restaurant, user_id, user_random):
        return Response({"error": f"{KEYS_DO_NOT_MATCH}"}, status=status.HTTP_403_FORBIDDEN)

    if not my_restaurant.menu_sorting_is_pending:
        return Response(
            {"error": f"{YOU_HAVE_TO_START_SORTING_FIRST}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if my_restaurant.dont_allow_further_actions_from_this_user:
        return Response(
            {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Update all dishes for the given category
        Dish.objects.filter(category=my_category).update(private_view_order=None)

        return Response(
            {
                "message": f"{CATEGORY_DISHES_ORDERS_CLEARED}",
                "new_token": check_authorization_result["new_token"],
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
           
# Payment ------------------------------------------------------

@api_view(["GET"])
def load_payment_options(request, country_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_country = Country.objects.get(pk=country_id)
    except Country.DoesNotExist:
        return Response(
            {"error": f"{COUNTRY_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    payment_option = Payment_Option.objects.filter(
        country=my_country
    )

    serializer = Payment_Option_Serializer(payment_option, many=True)
    data = [{"payment_option": item} for item in serializer.data]
    return Response(data, status=status.HTTP_200_OK)

# Images ------------------------------------------------

@api_view(["GET"])
def get_all_images(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    restaurant_images = Image.objects.filter(restaurant=restaurant_id)
    serializer = Image_Serializer(restaurant_images, many=True)
    data = [{"image": item} for item in serializer.data]
    return Response(data, status=status.HTTP_200_OK)

@api_view(["PATCH"])
@transaction.atomic
def update_image_uses(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    # This method doesn't need to check for current user id nor logged random number
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if my_restaurant.update_image_uses:
        # Images are used in preferences facade, preferences logo, restaurant users, categories and dishes
        my_images = Image.objects.filter(restaurant=my_restaurant)
        for image in my_images:
            image.use_count = 0
            if image.id == my_restaurant.public_facade_image_id: # type: ignore
                image.use_count += 1
            if image.id == my_restaurant.public_logo_image_id: # type: ignore
                image.use_count += 1
            my_restaurant_users = Restaurant_User.objects.filter(
                restaurant=my_restaurant
            )
            for restaurant_user in my_restaurant_users:
                if image.id == restaurant_user.public_image_id: # type: ignore
                    image.use_count += 1
            my_categories = Category.objects.filter(restaurant=my_restaurant)
            for category in my_categories:
                if category.public_image_id == image.id: # type: ignore
                    image.use_count += 1
                my_dishes = Dish.objects.filter(category=category)
                for dish in my_dishes:
                    if dish.public_image_id == image.id: # type: ignore
                        image.use_count += 1
            image.save()
        my_restaurant.update_image_uses = False
        my_restaurant.save()
        return Response(
            {
                "message": f"{RETURN_OK}",
                "new_token": check_authorization_result["new_token"],
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"message": f"{IMAGE_USES_ARE_UP_TO_DATE_WITH_ALL_IMAGES_USED}"},
            status=status.HTTP_200_OK,
        )

@api_view(["PATCH"])
def handle_loaded_images(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if not my_restaurant.dont_allow_further_actions_from_this_user:
            return Response(
                {
                    "message": f"{RETURN_OK}",
                    "new_token": check_authorization_result["new_token"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# @csrf_protect
@api_view(["POST"])
@transaction.atomic
def add_image(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        my_new_image_entity = Image(
            image_name=request.data["image_name"],
            image_original_name=request.data["image_original_name"],
            image_public_id=request.data["image_public_id"],
            image_resource_type=request.data["image_resource_type"],
            image_url=request.data["image_url"],
            restaurant=my_restaurant,
        )
        my_new_image_entity.save()

        return Response(
            {
                "id": my_new_image_entity.id, # type: ignore
                "message": f"{IMAGE_UPLOADED}",
                "new_token": check_authorization_result["new_token"],
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# @csrf_protect
@api_view(["GET", "PATCH", "DELETE"])
@transaction.atomic
def image(request, pk):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        my_image = Image.objects.get(pk=pk)
    except Image.DoesNotExist:
        return Response(
            {"error": f"{IMAGE_DOES_NOT_EXIST}"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        serializer = Image_Serializer(my_image)
        return Response(serializer.data)

    try:
        my_restaurant = Restaurant.objects.get(pk=my_image.restaurant.id) # type: ignore
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    restaurant_id = extracted_data["restaurant_id"]
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]
    
    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if request.method in ["PATCH", "DELETE"]:
            if request.method == "PATCH":
                request.data.pop("restaurant_id", None)
                request.data.pop("user_id", None)
                request.data.pop("user_random", None)    
                          
                serializer = Image_Serializer(my_image, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    # this serializer save() is always setting finished_setting to True
                    return Response(
                        {
                            "message": f"{IMAGE_NAME_UPDATED}",
                            "new_token": check_authorization_result["new_token"],
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            if request.method == "DELETE":
                try:
                    my_restaurant = Restaurant.objects.get(pk=restaurant_id)
                except Restaurant.DoesNotExist:
                    return Response(
                        {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                Restaurant.objects.filter(
                    pk=restaurant_id, public_facade_image_id=my_image.id # type: ignore
                ).update(
                    public_facade_image_id=-1,
                )
                Restaurant.objects.filter(
                    pk=restaurant_id, public_logo_image_id=my_image.id # type: ignore
                ).update(
                    public_logo_image_id=-1,
                )

                Restaurant_User.objects.filter(
                    pk=restaurant_id, public_image_id=my_image.id # type: ignore
                ).update(
                    public_image_id=-1,
                )

                my_categories = Category.objects.filter(restaurant=my_restaurant.id) # type: ignore

                Dish.objects.filter(
                    category__in=my_categories, public_image_id=my_image.id # type: ignore
                ).update(
                    public_image_id=-1,
                )

                Category.objects.filter(
                    restaurant=my_restaurant.id, public_image_id=my_image.id # type: ignore
                ).update(
                    public_image_id=-1,
                )

                my_image.delete()

                return Response(
                    {"message": f"{IMAGE_DELETED}"},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"error": "Only PATCH and DELETE are allowed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# QR ---------------------------------------------------

@api_view(["PATCH"])
def handle_show_qr(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if not my_restaurant.dont_allow_further_actions_from_this_user:
            return Response(
                {"message": "Ok", "new_token": check_authorization_result["new_token"]},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# Random -----------------------------------------------

@api_view(["PATCH"])
def show_restaurant_number(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if not my_restaurant.dont_allow_further_actions_from_this_user:
            return Response(
                {"message": "Ok", "new_token": check_authorization_result["new_token"]},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# Pay ---------------------------------------------

@api_view(["PATCH"])
def pay(request, restaurant_id):
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

    extracted_data = extract_request_data_func_with_user_id_and_user_random(request)
    user_id = extracted_data["user_id"]
    user_random = extracted_data["user_random"]

    performer = check_current_user_id_and_random()
    user_can_go_on = performer.check_current_user_id_and_random(my_restaurant, user_id, user_random)
    if user_can_go_on:
        if not my_restaurant.dont_allow_further_actions_from_this_user:
            return Response(
                {
                    "message": f"{RETURN_OK}",
                    "new_token": check_authorization_result["new_token"],
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": f"{USER_CAN_NOT_PERFORM_FURTHER_ACTIONS}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    else:
        return Response(
            {"error": f"{KEYS_DO_NOT_MATCH}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

# Transbank

def payment_failed(request):
    return render(request, 'webpay-plus/payment_failed.html')

def webpay_plus_commit(request: HttpRequest) -> HttpResponse:

    token = request.GET.get("token_ws")
    
    tbk_token=request.GET.get("TBK_TOKEN")
    tbk_id_session=request.GET.get("TBK_ID_SESION")
    tbk_orden_compra=request.GET.get("TBK_ORDEN_COMRA")
    
    restaurant_rut = request.GET.get("restaurant_rut")
    
    price_type = request.GET.get("priceType")
    user_email = request.GET.get("userEMail")
    action = request.GET.get("action")
    
    if not token:
        return render(request, 'webpay_plus/payment_failed.html', {
            'error_message': 'Lo sentimos, pero la transacción no se pudo completar. Intente nuevamente.'
        }) 
        
    if action == CREATING:
        try:
            my_restaurant_data = New_Restaurant_Data.objects.get(rut=restaurant_rut)
        except New_Restaurant_Data.DoesNotExist:
            print("La data del restaurant no existe")
            return Response(
                {"error": "La data del restaurant no existe"},
                status=status.HTTP_404_NOT_FOUND,
            )

    try:
        response = WebpayTransaction(WebpayOptions(settings.WEBPAY_COMMERCE_CODE, settings.WEBPAY_API_KEY, IntegrationType.LIVE)).commit(token=token)
        response_code = response.get("response_code")  # Accessing response_code
        
        # comment
        if response_code == 0:
            success_message = "Transacción Exitosa!"

            if action == CREATING:
                new_restaurant = create_restaurant(restaurant_rut)
                
                send_qr_code_via_email_and_link_to_atonna(
                    new_restaurant["id"], user_email, restaurant_rut, REACT_BASE_URL, CATEGORIES_PATH # type: ignore
                )
                send_webpayplus_payment_confirmation_via_email(response, user_email, restaurant_rut, action, None)

            elif action == INITIALMENULOAD:
                try:
                    my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
                except Restaurant.DoesNotExist:
                    print(f"{RESTAURANT_DOES_NOT_EXIST}")
                    return Response(
                        {"error": RESTAURANT_DOES_NOT_EXIST},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                send_webpayplus_payment_confirmation_via_email(response, user_email, restaurant_rut, action, None)
                send_webpay_plus_payment_done(response, user_email, restaurant_rut)

            elif action in [REACTIVATING, PAYINGNORMALFEE]:
                try:
                    my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
                except Restaurant.DoesNotExist:
                    print(f"{RESTAURANT_DOES_NOT_EXIST}")
                    return Response(
                        {"error": RESTAURANT_DOES_NOT_EXIST},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                if (action == REACTIVATING):
                    # objects.create creates and saves automatically
                    reactivated_date = ReactivatedDate.objects.create(restaurant=my_restaurant)
                    my_restaurant.active_month_number = 1
                my_restaurant.last_payment_date = date.today()
                my_restaurant.payment_state = RESTAURANT_NOT_BLOCKED_DUE_TO_PAYMENT
                my_restaurant.save()
                send_link_to_atonna(
                    my_restaurant.id, user_email, restaurant_rut, REACT_BASE_URL, CATEGORIES_PATH # type: ignore
                )
                send_webpayplus_payment_confirmation_via_email(response, user_email, restaurant_rut, action, None)

            return render(request, 'webpay_plus/commit.html', {
                "token": token,
                "response": response,
                "response_code": response_code,
                "success_message": success_message,
                "restaurant_rut": restaurant_rut,
                "user_email": user_email if action != CREATING else my_restaurant_data.user_email, # type: ignore
                "price_type": price_type if action != CREATING else my_restaurant_data.price_type, # type: ignore
                "action": action,
            })
        
        else:
            print('Transaction failed, rendering payment_failed page...')
            return render(request, 'webpay_plus/payment_failed.html', {
                'error_message': 'Lo sentimos, pero la transacción no se pudo completar. Intenta nuevamente.'
            }) 

    except TransbankError as e:
        print(f"TransbankError: {str(e)}")
        return HttpResponse(f"Error: {e.message}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def webpay_plus_create(request: HttpRequest, country_id: int, restaurant_rut: str, price_type: str, user_email: str, action: str) -> HttpResponse:
    price_type=urllib.parse.unquote(price_type)
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        if action not in {CREATING, REACTIVATING, PAYINGNORMALFEE, INITIALMENULOAD}:
            return Response(
                {"error": f"{ACTION_IS_NOT_CREATING_NOR_REACTIVATING_NOR_PAYINGNORMALFEE}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        my_buy_order_session_id = None
        
        try:
            my_buy_order_session_id = BuyOrderSessionID.objects.get(pk=1)
        except BuyOrderSessionID.DoesNotExist:
            return Response(
                {"error": f"{BUY_ORDER_SESSION_ID_DOES_NOT_EXIST}"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        my_buy_order_session_id.increment_values()
        buy_order = str(my_buy_order_session_id.buy_order)
        session_id = str(my_buy_order_session_id.session_id)
        
        payment_value = Decimal('0.00')
        if action in {REACTIVATING, PAYINGNORMALFEE}:
            try:
                my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
            except Restaurant.DoesNotExist:
                return Response(
                    {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
                    status=status.HTTP_400_BAD_REQUEST,  # Changed from 406
                )
                
        try:
            my_country = Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            return Response(
                {"error": f"{COUNTRY_DOES_NOT_EXIST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if action in {CREATING, REACTIVATING}:
            payment_value = Converted_First_Month_Amount_To_Pay(price_type, my_country.name)
            
            if payment_value == -1:
                return Response(
                    {"error": f"{THERE_WAS_AN_ERROR}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if action == REACTIVATING:
                discount_value = payment_value * (my_restaurant.discount_percentage).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) # type: ignore
                payment_value -= discount_value

        elif (action == INITIALMENULOAD):  
            try:
                my_global_price = Global_Price.objects.get(pk=1)
            except Global_Price.DoesNotExist:
                return Response(
                    {"error": f"{GLOBAL_PRICE_DOES_NOT_EXIST}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            payment_value = my_global_price.initial_menu_load    
            if (payment_value != None):
                payment_value = payment_value * (
                    my_country.exchange_rate 
                    if my_country and my_country.exchange_rate is not None 
                    else Decimal('1.0')
                )
        else:
            # action == PAYINGNORMALFEE
            try:
                my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
            except Restaurant.DoesNotExist:
                return Response(
                    {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            payment_value = converted_app_total_cost_existing_restaurant(my_restaurant)
            discount_value = (payment_value * my_restaurant.discount_percentage).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) # type: ignore
            payment_value -= discount_value

        payment_value_to_integer = int(payment_value or Decimal(0))

        return_url = f"https://atonna-backend-a6bdca67b05e.herokuapp.com/api/v1/webpay-plus/commit/?restaurant_rut={restaurant_rut}&priceType={price_type}&userEMail={user_email}&action={action}"
        if action == PAYINGNORMALFEE:
            create_request = {
                "buy_order": buy_order,
                "session_id": session_id,
                "amount": payment_value_to_integer,
                "action": action,
                "restaurant_id": my_restaurant.id, # type: ignore
                "return_url": return_url
            }
        else:
            create_request = {
                "buy_order": buy_order,
                "session_id": session_id,
                "amount": payment_value_to_integer,
                "action": action,
                "return_url": return_url
            }
            
        response = WebpayTransaction(WebpayOptions(settings.WEBPAY_COMMERCE_CODE, settings.WEBPAY_API_KEY, IntegrationType.LIVE)).create(buy_order, session_id, payment_value_to_integer, return_url)
        return JsonResponse({
            "request": create_request,
            "response": response
        })

    except Exception as e:
        print(f"Error in webpay_plus_create: {str(e)}")
        return Response(
            {"error": "An error occurred during the payment process."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@csrf_exempt
def webpay_plus_refund(request: HttpRequest) -> HttpResponse:
    # request: token_ws, amount
    if request.method == "POST":
        token = request.POST.get("token_ws")
        amount = request.POST.get("amount")

        if not token:
            return HttpResponse("Token is required", status=status.HTTP_400_BAD_REQUEST)  # Handle missing token
        if not amount:
            return HttpResponse("Amount is required", status=status.HTTP_400_BAD_REQUEST)  # Handle missing amount

        try:
            amount_float = float(amount)  # Convert amount to float
        except ValueError:
            return HttpResponse("Amount must be a valid number", status=status.HTTP_400_BAD_REQUEST)  # Handle invalid amount


        try:
            response = WebpayTransaction(WebpayOptions(settings.WEBPAY_COMMERCE_CODE, settings.WEBPAY_API_KEY, IntegrationType.LIVE)).refund(token, amount_float)

            return render(request, "webpay/plus/refund.html", {"token": token, "amount": amount_float, "response": response})
        except TransbankError as e:
            print(e.message)
            return HttpResponse(e.message, status=status.HTTP_400_BAD_REQUEST)

    # Handle non-POST requests
    return HttpResponse("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

def webpay_plus_refund_form(request: HttpRequest) -> HttpResponse:
    return render(request, "webpay/plus/refund-form.html")

def webpay_show_create(request: HttpRequest) -> HttpResponse:
    return render(request, 'webpay/plus/status-form.html')

def webpay_status(request: HttpRequest) -> HttpResponse:
    # request: token_ws
    if request.method == "POST":
        token_ws = request.POST.get("token_ws")

        if not token_ws:
            return HttpResponse("Token is required", status=status.HTTP_400_BAD_REQUEST)  # Handle missing token

        tx = WebpayTransaction(WebpayOptions(settings.WEBPAY_COMMERCE_CODE, settings.WEBPAY_API_KEY, IntegrationType.LIVE))
        
        try:
            resp = tx.status(token_ws)  # Now token_ws is guaranteed to be a str
        except TransbankError as e:
            return HttpResponse(f"Error processing status: {e.message}", status=status.HTTP_400_BAD_REQUEST)  # Handle errors from the API

        return render(request, "webpay/plus/status.html", {"response": resp, "token": token_ws, "req": request.POST})

    # Handle non-POST requests
    return HttpResponse("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET"])
def get_user_object(request, user_id):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        my_user = Restaurant_User.objects.get(pk=user_id)
    except Restaurant_User.DoesNotExist:
        return Response(
            {"error": f"{USER_DOES_NOT_EXIST}"},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(
        {
            "name": my_user.public_name,
            "email": my_user.public_email, 
        },
        status=status.HTTP_200_OK,
    )