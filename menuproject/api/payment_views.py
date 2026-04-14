import os
import re

import base64
import requests
from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from django.utils import timezone
from dateutil.parser import parse
from babel.dates import format_datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db import transaction
from django.db.models import F
from decimal import ROUND_HALF_UP
import uuid

from .utils.First_Month_Amount_To_Pay import Converted_First_Month_Amount_To_Pay, First_Month_Amount_To_Pay
from .utils.Amount_To_Pay import converted_app_total_cost_existing_restaurant, app_total_cost_existing_restaurant
from .utils.Encryption import encrypt_value

from .views import replace_placeholder_for_sending_emails, send_qr_code_via_email_and_link_to_atonna, send_link_to_atonna, create_restaurant

from .utils.Constants_and_strings import *
from django.template import Template, Context
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from datetime import date
import urllib.parse

from .models import Global_Price, Country, Restaurant, New_Restaurant_Data, Restaurant_User

from .authorization_views import check_authorization

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL")

REACT_BASE_URL = os.getenv("DJANGO_REACT_BASE_URL")
HTTPS_BASE_URL = os.getenv("DJANGO_HTTPS")
CATEGORIES_PATH = os.getenv("DJANGO_CATEGORIES_PATH")

def send_paypal_payment_confirmation_via_email(data, main_user_email, other_user_email):  
    subject = PAYMENT_CONFIRMATION
    from_email = FROM_EMAIL
    recipient_list = [main_user_email]
    if (other_user_email != None):
        recipient_list.append(other_user_email)
        
    payer_name = (
        data["payer"]["name"]["given_name"] + " " + data["payer"]["name"]["surname"]
    )
    payer_email = data["payer"]["email_address"]
    transaction_id = data["purchase_units"][0]["payments"]["captures"][0]["id"]
    update_time = data["purchase_units"][0]["payments"]["captures"][0]["update_time"]
    update_time_parsed = parse(update_time)
    local_timezone = timezone.get_current_timezone()
    update_time_local = update_time_parsed.astimezone(local_timezone)
    transaction_date = format_datetime(
        update_time_local, "MMMM d 'de' yyyy, h:mm:ss a", locale="es"
    )
    transaction_amount = data["purchase_units"][0]["payments"]["captures"][0]["amount"][
        "value"
    ]
    transaction_currency = data["purchase_units"][0]["payments"]["captures"][0][
        "amount"
    ]["currency_code"]
    # credit_card = data['payment_source']['paypal']['account_status'] == 'UNVERIFIED'
    constants = {
        "RECEIPT": RECEIPT,
        "PAYER_INFORMATION": PAYER_INFORMATION,
        "NAME": NAME,
        "EMAIL": EMAIL,
        "TRANSACTION_DETAILS": TRANSACTION_DETAILS,
        "TRANSACTION_ID": TRANSACTION_ID,
        "DATE": DATE,
        "AMOUNT": AMOUNT,
        "CURRENCY": CURRENCY,
        "THANK_YOU_FOR_YOUR_PAYMENT": THANK_YOU_FOR_YOUR_PAYMENT
    }
    text_content = f"""
    {RECEIPT}
    
    {PAYER_INFORMATION}:
    {NAME}: {payer_name}
    {EMAIL}: {payer_email}
    
    {TRANSACTION_DETAILS}:
    {TRANSACTION_ID}: {transaction_id}
    {DATE}: {transaction_date}
    {AMOUNT}: {transaction_amount}
    {CURRENCY}: {transaction_currency}
    
    {THANK_YOU_FOR_YOUR_PAYMENT}
    """
    
    text_content = text_content.format(**constants)
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>RECIBO DE PAGO</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .receipt-container {
                width: 100%;
                padding: 20px;
                box-sizing: border-box;
            }
            .receipt {
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
            .details {
                margin-bottom: 20px;
            }
            .details h2 {
                margin: 0 0 10px;
            }
            .details p {
                margin: 5px 0;
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
        <div class="receipt-container">
            <div class="receipt">
                <div class="header">
                    <img src="cid:logo" alt="Application Logo">
                    <h1>RECIBO DE PAGO POR PEYPAL</h1>
                    <h3>Por favor no responda este mensaje</h3>
                </div>
                <div class="details">
                    <h2>INFORMACIÓN DEL PAGADOR</h2>
                    <p><strong>NOMBRE:</strong> {{ payer_name }}</p>
                    <p><strong>EMAIL:</strong> {{ payer_email }}</p>
                </div>
                <div class="details">
                    <h2>DETALLE DE LA TRANSACCIÓN</h2>
                    <p><strong>ID DE LA TRANSACCIÓN:</strong> {{ transaction_id }}</p>
                    <p><strong>FECHA:</strong> {{ transaction_date }}</p>
                    <p><strong>MONTO:</strong> {{ transaction_amount }}</p>
                    <p><strong>MONEDA:</strong> {{ transaction_currency }}</p>

                </div>
                <div class="footer">
                    <p>GRACIAS POR SU PAGO</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    html_template = re.sub(r'\*\*\*(.*?)\*\*\*', replace_placeholder_for_sending_emails, html_template)
    # {% if credit_card %}
    # <p style="margin-top: 10px;">This transaction will appear on your credit card statement in the currency you selected during the PayPal payment process, so no conversion fees will be charged.</p>
    # {% endif %}

    # Render the HTML content with the provided context
    template = Template(html_template)
    context = Context(
        {
            "payer_name": payer_name,
            "payer_email": payer_email,
            "transaction_id": transaction_id,
            "transaction_date": transaction_date,
            "transaction_amount": transaction_amount,
            "transaction_currency": transaction_currency,
            # 'credit_card': credit_card
        }
    )
    html_content = template.render(context)

    # Build the path to the image
    image_path = os.path.join(
        settings.BASE_DIR, "api", "specific_files", "DigitalMenuLogo.jpg"
    )

    # Create the email
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Plain text content
        from_email=from_email,
        to=recipient_list,
    )
    msg.attach_alternative(
        html_content, "text/html"
    )  # Attach HTML content as an alternative
    # Attach the image
    with open(image_path, "rb") as img_file:
        logo = MIMEImage(img_file.read())
        logo.add_header("Content-ID", "<logo>")
        msg.attach(logo) # type: ignore
    # Send the email
    msg.send()


def generate_paypal_access_token():
    if not PAYPAL_CLIENT_ID or not PAYPAL_SECRET:
        raise ValueError("Missing PayPal credentials")

    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}"
    auth = base64.b64encode(auth.encode()).decode("utf-8")

    response = requests.post(
        f"{PAYPAL_BASE_URL}/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {auth}"},
    )

    try:
        response.raise_for_status()
        data = response.json()
        return data["access_token"]
    except requests.exceptions.HTTPError as http_err:
        print(f"generate_paypal_access_token:: HTTP error: {http_err}")
        raise
    except Exception as error:
        print(f"generate_paypal_access_token:: error: {error}")
        raise


@api_view(["POST"])
@transaction.atomic
def create_paypal_order_atonna(request, restaurant_id, action):
    response = None 

    try:
        check_authorization_result = check_authorization(request)
        if not check_authorization_result["valid"]:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            my_restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        # ATONNA always collects the whole app value
        payment_value = Decimal("0")  # Ensure it's always a Decimal

        payment_value = app_total_cost_existing_restaurant(my_restaurant) or Decimal("0")

        # Ensure payment_value is Decimal before multiplication
        payment_value = Decimal(payment_value)

        # Calculate discount value
        discount_value = payment_value * (my_restaurant.discount_percentage / Decimal("100"))
        discount_value = discount_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Subtract discount from payment value
        payment_value = payment_value - discount_value

        # Ensure payment_value has exactly two decimal places
        payment_value = payment_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        payment_value = str(payment_value)  # Convert to string after rounding


        access_token = generate_paypal_access_token()
        url = f"{PAYPAL_BASE_URL}/v2/checkout/orders"

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{"amount": {"currency_code": "USD", "value": payment_value}}],
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        response = requests.post(url, headers=headers, json=payload)  # ✅ Now response is always assigned

        response.raise_for_status()

        data = response.json()
        return Response(data, status=status.HTTP_200_OK)

    except requests.exceptions.HTTPError as http_err:
        error_response = response.json() if response is not None else {"error": "No response received"}
        print(f"PayPal Error: {error_response}")
        return Response(
            {"error": "PayPal API error", "details": error_response},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        print(f"create_paypal_order:: error:: {error}")
        return Response(
            {"error": "An error occurred while creating PayPal order"},
            status=status.HTTP_400_BAD_REQUEST,
        )

        
@api_view(["POST"])
@transaction.atomic
def create_paypal_order_little_atonna(request, price_type, action):
    price_type = urllib.parse.unquote(price_type)
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        payment_value = Decimal("0")  # Ensure it's always defined

        # the action is either CREATING or REACTIVATING, because it comes from little atonna
        # if it was REACTIVATING, it's like a first_month
        # in little atonna action will never be PAYINGNORMALFEE
        if action in [CREATING, REACTIVATING]:
            payment_value = First_Month_Amount_To_Pay(price_type)
        elif action == INITIALMENULOAD:
            try:
                my_global_price = Global_Price.objects.get(pk=1)
                payment_value = my_global_price.initial_menu_load
            except Global_Price.DoesNotExist:
                return Response(
                    {"error": f"{GLOBAL_PRICE_DOES_NOT_EXIST}"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

        payment_value = Decimal(payment_value or 0)  
        payment_value = payment_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        payment_value = str(payment_value)

        access_token = generate_paypal_access_token()
        url = f"{PAYPAL_BASE_URL}/v2/checkout/orders"

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": payment_value,
                    }
                }
            ],
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.post(url, headers=headers, json=payload)

        # Ensure the response is successful
        response.raise_for_status()

        # Extract JSON data from the response
        data = response.json()

        return Response(data, status=status.HTTP_200_OK)

    except requests.exceptions.HTTPError as http_err:
        print(f"create_paypal_order_little_atonna:: HTTP error occurred: {http_err}")
        return Response(
            {"error": "HTTP error occurred while creating PayPal order"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        print(f"create_paypal_order_little_atonna:: error:: {error}")
        return Response(
            {"error": "An error occurred while creating PayPal order"},
            status=status.HTTP_400_BAD_REQUEST,
        )

@api_view(["POST"])
@transaction.atomic
def capture_paypal_order_atonna(request, restaurant_id):
    check_authorization_result = check_authorization(request)
    advanced_to_level = 1
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        my_restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    order_id = request.data.get("orderID")
    if not order_id:
        return Response(
            {"error": "orderID is required", "done": False},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        my_restaurant_main_user = Restaurant_User.objects.get(
            pk=my_restaurant.main_user_id # type: ignore
        )
    except Restaurant_User.DoesNotExist:
        return Response(
            {"error": f"{USER_DOES_NOT_EXIST}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    my_restaurant_user = None
    
    currently_logged_in = request.data.get("currently_logged_in")
    if currently_logged_in != my_restaurant.main_user_id: # type: ignore
        try:
            my_restaurant_user = Restaurant_User.objects.get(pk=currently_logged_in)
        except Restaurant_User.DoesNotExist:
            return Response(
                {"error": f"{USER_DOES_NOT_EXIST}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    advanced_to_level = 2

    access_token = generate_paypal_access_token()
    url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.post(url, headers=headers)
    # Ensure the response is successful
    response.raise_for_status()
    # Extract JSON data from the response
    data = response.json()
    advanced_to_level = 3
    if (data["status"]) == "COMPLETED":
        advanced_to_level = 4
        update_time_str = data["purchase_units"][0]["payments"]["captures"][0][
            "update_time"
        ]
        update_time_parsed = parse(update_time_str)
        local_timezone = timezone.get_current_timezone()
        update_time_local = update_time_parsed.astimezone(local_timezone)
        # This has to be done in every succesful payment
        my_restaurant.last_payment_date = update_time_local.date()
        my_restaurant.number_of_sent_payment_reminders = 0
        my_restaurant.restaurant_recently_created = False
        my_restaurant.payment_state = RESTAURANT_NOT_BLOCKED_DUE_TO_PAYMENT
        my_restaurant.save()
        advanced_to_level = 5
        # payment confirmation
        if my_restaurant_main_user and my_restaurant_main_user.public_email and my_restaurant_user and my_restaurant_user.public_email:
            send_paypal_payment_confirmation_via_email(
                data, my_restaurant_main_user.public_email, my_restaurant_user.public_email
            )
        else:
            print("Error: One or both restaurant users are None or missing public_email.")
        data["done"] = True
    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def capture_paypal_order_little_atonna(request, restaurant_rut, user_email, action):
    check_authorization_result = check_authorization(request)
    if not check_authorization_result["valid"]:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try: 
        order_id = request.data.get("orderID")
        if not order_id:
            return Response(
                {"error": "orderID is required", "done": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = generate_paypal_access_token()
        url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.post(url, headers=headers)

        # Ensure the response is successful
        response.raise_for_status()
        # Extract JSON data from the response
        data = response.json()
        
        if (data["status"]) == "COMPLETED":
            update_time_str = data["purchase_units"][0]["payments"]["captures"][0][
                "update_time"
            ]
            update_time_parsed = parse(update_time_str)
            local_timezone = timezone.get_current_timezone()
            update_time_local = update_time_parsed.astimezone(local_timezone)

            # This has to be done in every succesful payment
            # Successful_Payment(my_restaurant, update_time_local.date()) # type: ignore
            # payment confirmation
            send_paypal_payment_confirmation_via_email(
                data, user_email, None
            )
            if action == CREATING:
                new_restaurant = create_restaurant(restaurant_rut)

                if not isinstance(new_restaurant, dict) or "id" not in new_restaurant:
                    return Response({"error": "Failed to create restaurant."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                send_qr_code_via_email_and_link_to_atonna(
                    new_restaurant["id"], user_email, restaurant_rut, REACT_BASE_URL, CATEGORIES_PATH
                ) # type: ignore

                try:
                    my_restaurant = Restaurant.objects.get(pk=new_restaurant["id"])
                except Restaurant.DoesNotExist:
                    return Response(
                        {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )

            else:
                # it's REACTIVATING or PAYINGNORMALFEE
                try:
                    my_restaurant = Restaurant.objects.get(rut=restaurant_rut)
                except Restaurant.DoesNotExist:
                    return Response(
                        {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
                my_restaurant.last_payment_date = date.today()
                my_restaurant.payment_state = RESTAURANT_NOT_BLOCKED_DUE_TO_PAYMENT
                my_restaurant.save()
                send_link_to_atonna(my_restaurant.id, user_email, restaurant_rut, REACT_BASE_URL, CATEGORIES_PATH) # type: ignore
                
            data["restaurant_taxid"] = my_restaurant.rut
            data["done"] = True
        return Response(data, status=status.HTTP_200_OK)

    except requests.exceptions.HTTPError as http_err:
        print(f"capture_paypal_order:: HTTP error occurred: {http_err}")
        return Response(
            {
                "error": "HTTP error occurred while capturing PayPal order",
                "done": True,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as error:
        print(f"capture_paypal_order:: error:: {error}")
        return Response(
            {
                "error": "An error occurred while capturing PayPal order",
                "done": True,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# Not finished...
# @api_view(["POST"])
# @transaction.atomic
# def create_paypal_subscription(request, restaurant_id):
#     check_authorization_result = check_authorization(request)
#     if not check_authorization_result["valid"]:
#         return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
#     try:
        # try:
        #     my_restaurant = Restaurant.objects.get(pk=restaurant_id)
        # except Restaurant.DoesNotExist:
        #     return Response(
        #         {"error": f"{RESTAURANT_DOES_NOT_EXIST}"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

#         url = f"{PAYPAL_BASE_URL}/v1/billing/plans"

#         payload = {
#             "intent": "CAPTURE",
#             "purchase_units": [
#                 {
#                     "amount": {
#                         "currency_code": "USD",
#                         "value": payment_value,
#                     }
#                 }
#             ],
#             # "payment_source": {
#             #     "paypal": {
#             #         "experience_context": {
#             #             "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
#             #             "brand_name": "EXAMPLE INC",
#             #             "locale": "en-US",
#             #             "user_action": "PAY_NOW",
#             #             "landing_page": "LOGIN",
#             #             # "shipping_preference": "SET_PROVIDED_ADDRESS",
#             #             # "return_url": "https://example.com/returnUrl",
#             #             # "discard_url": "https://example.com/cancelUrl",
#             #         }
#             #     }
#             # },
#         }
#         headers = {
#             "X-PAYPAL-SECURITY-CONTEXT": '{"consumer":{"accountNumber":1181198218909172527,"merchantId":"5KW8F2FXKX5HA"},"merchant":{"accountNumber":1659371090107732880,"merchantId":"2J6QB8YJQSJRJ"},"apiCaller":{"clientId":"AdtlNBDhgmQWi2xk6edqJVKklPFyDWxtyKuXuyVT-OgdnnKpAVsbKHgvqHHP","appId":"APP-6DV794347V142302B","payerId":"2J6QB8YJQSJRJ","accountNumber":"1659371090107732880"},"scopes":["https://api-m.paypal.com/v1/subscription/.*","https://uri.paypal.com/services/subscription","openid"]}',
#             "Content-Type": "application/json",
#             "Accept": "application/json",
#             "PayPal-Request-Id": "PLAN-18062019-001",
#             "Prefer": "return=representation",
#         }
#         #   X-PAYPAL-SECURITY-CONTEXT::

#         #   "consumer":{
#         # 	"accountNumber":1181198218909172527,
#         # 	"merchantId":"5KW8F2FXKX5HA"},
#         # 	"merchant":{
#         # 		"accountNumber":1659371090107732880,
#         # 		"merchantId":"2J6QB8YJQSJRJ"},
#         # 		"apiCaller":{
#         # 			"clientId":"AdtlNBDhgmQWi2xk6edqJVKklPFyDWxtyKuXuyVT-OgdnnKpAVsbKHgvqHHP",
#         # 			"appId":"APP6DV794347V142302B",
#         # 			"payerId":"2J6QB8YJQSJRJ",
#         # 			"accountNumber":"1659371090107732880"},
#         # 		"scopes":[
#         # 			"https://api-.paypal.com/v1/subscription/.*",
#         # 			"https://uri.paypal.com/services/subscription",
#         # 			"openid"]

#         response = requests.post(url, headers=headers, json=payload)

#         # Ensure the response is successful
#         response.raise_for_status()

#         # Extract JSON data from the response

#         data = response.json()

#         return Response(data, status=status.HTTP_200_OK)

#     except requests.exceptions.HTTPError as http_err:
#         print(f"create_paypal_order:: HTTP error occurred: {http_err}")
#         return Response(
#             {"error": "HTTP error occurred while creating PayPal order"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     except Exception as error:
#         print(f"create_paypal_order:: error:: {error}")
#         return Response(
#             {"error": "An error occurred while creating PayPal order"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )
