import os

import secrets
import string
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone

from .utils.Constants_and_strings import *

from dotenv import load_dotenv

load_dotenv()

from .models import (
    Past_Token,
)


def generate_new_token(length=164):
    # Define the characters to be used for the token, excluding the single quote character
    alphabet = (
        string.ascii_letters + string.digits + string.punctuation.replace("'", "")
    )
    # Generate the token
    token = "".join(secrets.choice(alphabet) for i in range(length))
    return token


def generate_token(now):
    generated_token = generate_new_token()
    Past_Token.objects.create(  # I should insert the first token at first launch of the app
        token=generated_token,  # it should be equal to the first token the front end sends when starting
    )
    return {"new_token": generated_token}


def check_token_time(now, last_token):
    if now < last_token.created_at + TOKEN_EXPIRATION_DAYS:
        return {"valid": True, "new_token": None}
    else:
        new_token = generate_token(now)
        return {"valid": True, "new_token": new_token["new_token"]}


@api_view(["PATCH", "GET"])
def get_first_token(request):
    try:
        # Attempt to extract 'appName' and 'secretKey' from request data
        app_name = request.data.get('appName')
        secret_key = request.data.get('secretKey')
        print(f"'appName', 'secretKey':: {app_name}, {secret_key}")
        if not app_name or not secret_key:
            print(f"Missing 'appName' or 'secretKey':: {app_name}, {secret_key}")
            return Response(
                {"error": "Missing 'appName' or 'secretKey'", "token": None},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the provided keys match the expected settings
        if secret_key == settings.SECRET_KEY and app_name == settings.APP_NAME:

            # Attempt to retrieve the most recent token
            try:
                last_token = Past_Token.objects.last()
                if last_token:
                    return Response(
                        {"token": last_token.token},
                        status=status.HTTP_200_OK,
                    )
                else:
                    print("No tokens found")
                    return Response(
                        {"error": "No tokens found", "token": None},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            except Exception as e:
                # Handle errors during token retrieval
                return Response(
                    {"error": f"Error retrieving token: {str(e)}", "token": None},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            # Return unauthorized response if keys don't match
            return Response(
                {"error": "Unauthorized", "token": None},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    except Exception as e:
        # Handle unexpected errors
        return Response(
            {"error": f"An unexpected error occurred: {str(e)}", "token": None},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def check_token(now, token):
    last_token = Past_Token.objects.last()
    if last_token is not None and token == last_token.token:
        # this question makes most of the requests faster, since it requires only one database
        # round trip
        return check_token_time(now, last_token)
    else:
        # If it is here, then we have to make another round trip to the database
        if Past_Token.objects.filter(token=token).exists():
            return check_token_time(now, last_token)
        else:
            return {"valid": False, "new_token": None}


def check_authorization(request):
    # Extract token from request headers and validate it
    token = request.headers.get(settings.ATONNA_APP_TOKEN)
    return check_token(timezone.now(), token)
