from datetime import datetime
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
import random
from datetime import date
from datetime import time
from django.utils.timezone import now
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.utils import timezone 
import inspect
from decimal import Decimal

import logging

logger = logging.getLogger(__name__)

from .utils.Encryption import encrypt_value, decrypt_value

from dateutil.relativedelta import relativedelta

from .utils.Useful_procedures import Useful_procedures

from .utils.Constants_and_strings import *

import re

def get_next_revision_date():
    return timezone.now().date() + relativedelta(months=3)

def get_day_before_first_of_month():
    today = date.today()
    # Get the first day of the current month
    first_of_current_month = today.replace(day=1)
    # Return the day before the first day of the current month
    return first_of_current_month - timedelta(days=1)

def get_current_day():
    return datetime.now().day  

def get_current_month():
    return datetime.now().month  

def get_yesterday():
    return date.today() - timedelta(days=1)

class Help_Atonn(models.Model):
    video_name = models.CharField(max_length=HELP_VIEW_NAME_MAX_LENGTH, default="")
    video_url = models.URLField(max_length=URLS_MAX_LENGTH, default="")


# ---------------------- Prefilled models ---------------------------
class Global_Price(models.Model):
    minimum_price=models.DecimalField(
        # aquí
        max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00')
    ) # type: ignore
    full_price=models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00')
    ) 
    initial_menu_load=models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00')
    ) 

class Country(models.Model):
    name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    alpha2_code = models.CharField(max_length=ALPHA2_CODE_MAX_LENGTH, default="")
    locale = models.CharField(max_length=LOCALE_IDENTIFIER_MAX_LENGTH, default="")
    timezone = models.CharField(max_length=64, default="UTC")  
    flag_image_url = models.URLField(max_length=URLS_MAX_LENGTH, default="")
    currency_symbol = models.CharField(max_length=CURRENCY_SYMBOL_MAX_LENGTH, default="")
    minimum_fraction_digits = models.IntegerField(default=0, null=False)
    maximum_fraction_digits = models.IntegerField(default=0, null=False)
    exchange_rate=models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=Decimal('0.00')
    ) 
    document_type = models.CharField(
        max_length=DOCUMENT_TYPE_CHOICES_MAX_LENGTH, 
        choices=DOCUMENT_TYPES, 
        default=None, 
        null=True, 
        blank=True
    )
    
class BuyOrderSessionID(models.Model):
    buy_order = models.PositiveBigIntegerField(default=1)
    session_id = models.PositiveBigIntegerField(default=1)
    transaction_time = models.DateTimeField(default=now)

    def increment_values(self):
        """ Increments buy_order and session_id, updates transaction_time """
        self.buy_order += 1
        self.session_id += 1
        self.transaction_time = now()
        self.save(update_fields=['buy_order', 'session_id', 'transaction_time'])

    def __str__(self):
        formatted_time = self.transaction_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"Order #{self.buy_order:05d} | Session #{self.session_id:05d} | Time: {formatted_time}"

    
class Buy_order_session_id(models.Model):
    pass

class Delivery_Company(models.Model):
    name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    company_image_url = models.URLField(max_length=URLS_MAX_LENGTH, default="")
    url_template = models.CharField(max_length=URLS_MAX_LENGTH, default="")
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)


class Payment_Option(models.Model):
    name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    payment_option_image_url = models.URLField(max_length=URLS_MAX_LENGTH, default="")
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)


class Rejection_Reason(models.Model):
    reason = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    explanation = models.CharField(max_length=DESCRIPTIONS_MAX_LENGTH, default="")


class Past_Token(models.Model):
    token = models.CharField(max_length=TOKEN_MAX_LENGTH, default="")
    created_at = models.DateTimeField(auto_now_add=True)


# ---------------------- End Prefilled models ---------------------------
class Super_User(models.Model):
    name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    password = models.CharField(
        max_length=ENCRYPTED_PASSWORDS_MAX_LENGTH,
        default="gAAAAABmkTV4y8NR-Pmy_FsBOzEecCpJOvG9akb7xQOeo04pC_MVe9TGevZ7OIs43kI4prB1CtylFtrZHp0Gplya2I9KCHQtPA=="
    )
    
    def save(self, *args, **kwargs):
        if self.password:
            self.password = encrypt_value(self.password)
        super(Super_User, self).save(*args, **kwargs)  # Corrected line
        
    def get_decrypted_password(self):
        return decrypt_value(self.password)
    
class New_Restaurant_Data(models.Model):
    rut = models.CharField(max_length=RUT_MAX_LENGTH, unique=True, default="")
    country_id = models.BigIntegerField(default=-1)
    price_type = models.CharField(max_length=PRICE_CHOICES_MAX_LENGTH, default=None)
    user_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    user_password = models.CharField(max_length=ENCRYPTED_PASSWORDS_MAX_LENGTH, default="")
    user_email = models.EmailField(max_length=EMAILS_MAX_LENGTH, default="")
    created_at = models.DateTimeField(auto_now_add=True) 
    
class Restaurant(models.Model):
    rut = models.CharField(max_length=RUT_MAX_LENGTH, unique=True, default="")
    public_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    private_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    public_description = models.CharField(
        max_length=DESCRIPTIONS_MAX_LENGTH, default="", null=False, blank=True
    )
    private_description = models.CharField(
        max_length=DESCRIPTIONS_MAX_LENGTH, default="", null=False, blank=True
    )
    public_address = models.CharField(max_length=ADDRESSES_MAX_LENGTH, default="")
    private_address = models.CharField(max_length=ADDRESSES_MAX_LENGTH, default="")
    public_phone = models.CharField(max_length=PHONES_MAX_LENGTH, default="")
    private_phone = models.CharField(max_length=PHONES_MAX_LENGTH, default="")
    public_country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, related_name="public_country", null=True
    )
    private_country = models.ForeignKey(
        Country, on_delete=models.DO_NOTHING, related_name="private_country", null=True
    )
    public_facade_image_id = models.BigIntegerField(default=-1)
    private_facade_image_id = models.BigIntegerField(default=-1)
    public_logo_image_id = models.BigIntegerField(default=-1)
    private_logo_image_id = models.BigIntegerField(default=-1)
    public_show_images = models.BooleanField(default=True)
    private_show_images = models.BooleanField(default=False)
    public_show_restaurant_reviews = models.BooleanField(default=True)
    private_show_restaurant_reviews = models.BooleanField(default=True)
    public_show_dishes_reviews = models.BooleanField(default=True)
    private_show_dishes_reviews = models.BooleanField(default=True)
    public_show_prices = models.BooleanField(default=True)
    private_show_prices = models.BooleanField(default=True)
    public_show_ask_button = models.BooleanField(default=True)
    private_show_ask_button = models.BooleanField(default=True)

    public_instagram_url = models.URLField(
        max_length=INSTAGRAM_URL_MAX_LENGTH, default="", blank=True
    )
    private_instagram_url = models.URLField(
        max_length=INSTAGRAM_URL_MAX_LENGTH, default="", blank=True
    )
    public_facebook_url = models.URLField(
        max_length=FACEBOOK_URL_MAX_LENGTH, default="", blank=True
    )
    private_facebook_url = models.URLField(
        max_length=FACEBOOK_URL_MAX_LENGTH, default="", blank=True
    )
    public_twitter_url = models.URLField(max_length=TWITTER_URL_MAX_LENGTH, default="", blank=True)
    private_twitter_url = models.URLField(max_length=TWITTER_URL_MAX_LENGTH, default="", blank=True)
    public_website_url = models.URLField(
        max_length=URLS_MAX_LENGTH, default="", null=False, blank=True
    )
    private_website_url = models.URLField(
        max_length=URLS_MAX_LENGTH, default="", null=False, blank=True
    )
    # ---------------- PUBLIC OPEN HOURS ---------------------
    
    # 660 = 11 * 60 => 11 am
    
    public_monday_open_hour_in_minutes = models.IntegerField(default=660, null=False)
    public_tuesday_open_hour_in_minutes = models.IntegerField(default=660, null=False)
    public_wednesday_open_hour_in_minutes = models.IntegerField(default=660, null=False)
    public_thursday_open_hour_in_minutes = models.IntegerField(default=660, null=False)
    public_friday_open_hour_in_minutes = models.IntegerField(default=660, null=False)
    public_saturday_open_hour_in_minutes = models.IntegerField(
        default=660, null=False, blank=True
    )
    public_sunday_open_hour_in_minutes = models.IntegerField(
        default=660, null=False, blank=True
    )
    # ----------------- PRIVATE OPEN HOURS ---------------------
    private_monday_open_hour_in_minutes = models.IntegerField(default=0, null=False)
    private_tuesday_open_hour_in_minutes = models.IntegerField(default=0, null=False)
    private_wednesday_open_hour_in_minutes = models.IntegerField(default=0, null=False)
    private_thursday_open_hour_in_minutes = models.IntegerField(default=0, null=False)
    private_friday_open_hour_in_minutes = models.IntegerField(default=0, null=False)
    private_saturday_open_hour_in_minutes = models.IntegerField(default=0, null=False)
    private_sunday_open_hour_in_minutes = models.IntegerField(default=0, null=False)
    # ----------------------- PUBLIC CLOSE HOURS -----------------------
    
    # 210 = 3.5 * 60 => 3 hours 30 minutes back from 24 hours => 20:30 (8 pm)
    
    public_monday_close_hour_in_minutes = models.IntegerField(default=-210, null=False)
    public_tuesday_close_hour_in_minutes = models.IntegerField(default=-210, null=False)
    public_wednesday_close_hour_in_minutes = models.IntegerField(
        default=-210, null=False
    )
    public_thursday_close_hour_in_minutes = models.IntegerField(default=-210, null=False)
    public_friday_close_hour_in_minutes = models.IntegerField(default=-210, null=False)
    public_saturday_close_hour_in_minutes = models.IntegerField(default=-210, null=False)
    public_sunday_close_hour_in_minutes = models.IntegerField(default=-210, null=False)
    # --------------------- PRIVATE CLOSE HOURS ------------------------
    private_monday_close_hour_in_minutes = models.IntegerField(default=-120, null=False)
    private_tuesday_close_hour_in_minutes = models.IntegerField(default=-120, null=False)
    private_wednesday_close_hour_in_minutes = models.IntegerField(default=-120, null=False)
    private_thursday_close_hour_in_minutes = models.IntegerField(default=-120, null=False)
    private_friday_close_hour_in_minutes = models.IntegerField(default=-120, null=False)
    private_saturday_close_hour_in_minutes = models.IntegerField(default=-120, null=False)
    private_sunday_close_hour_in_minutes = models.IntegerField(default=-120, null=False)
    # -----------------------------------------------------------------
    restaurant_creation_date = models.DateField(auto_now_add=True)
    restaurant_recently_created = models.BooleanField(default=True)
    restaurant_current_date = models.DateField(default=get_yesterday)
    # These next two fields are useful for identifying changes. See Load_Restaurant
    restaurant_current_day = models.IntegerField(default=get_current_day)
    restaurant_current_month = models.IntegerField(default=get_current_month)
    main_user_id = models.IntegerField(default=-1)
    previous_restaurant_number_of_reviews = models.IntegerField(default=0)
    previous_restaurant_reviews_average = models.IntegerField(default=0)
    update_image_uses = models.BooleanField(default=False)
    todays_random_number = models.IntegerField(default=-1)
    currently_logged_in = models.IntegerField(default=-1)
    logged_in_time = models.CharField(max_length=DATESTR_MAX_LENGTH, default="")
    logged_out_time = models.CharField(max_length=DATESTR_MAX_LENGTH, default="")
    logged_in_user_random_number = models.IntegerField(default=-1)
    menu_edition_is_pending = models.BooleanField(default=False)
    reviews_updates_are_pending = models.BooleanField(default=False)
    menu_sorting_is_pending = models.BooleanField(default=False)
    restaurant_deliveries_edition_is_pending = models.BooleanField(default=False)
    promotions_edition_is_pending = models.BooleanField(default=False)
    preferences_edition_is_pending = models.BooleanField(default=False)
    users_edition_is_pending = models.BooleanField(default=False)
    dont_allow_further_actions_from_this_user = models.BooleanField(default=False)
    price_type = models.CharField(
        max_length=PRICE_CHOICES_MAX_LENGTH, choices=PRICE_CHOICES, default=FULL_PRICE  
    )
    next_price_type = models.CharField(
        max_length=PRICE_CHOICES_MAX_LENGTH, choices=PRICE_CHOICES, null=True, default=FULL_PRICE
    )
    total_number_of_accesses = models.IntegerField(default=0)
    number_of_pending_free_months = models.IntegerField(default=0) 
    last_payment_date = models.DateField(default=get_day_before_first_of_month)
    payment_state = models.CharField(
        max_length=PAYMENT_STATE_MAX_LENGTH, choices=PAYMENT_STATES, default=RESTAURANT_NOT_BLOCKED_DUE_TO_PAYMENT  
    )
    number_of_days_served_in_current_month = models.IntegerField(default=0) 
    number_of_sent_payment_reminders = models.IntegerField(default=0) 
    active_month_number = models.IntegerField(default=1) 
    discount_percentage = models.DecimalField(
        max_digits=5,  # Adjust based on your needs (e.g., 100.00 max)
        decimal_places=2,  # Allows values like 99.99%
        default=Decimal("0.00")
    )
    
    def self_update_restaurant_current_date(self):
        """If the current time is greater that 24:00, but the restaurant closes later, then do not change the date"""
        current_datetime = Useful_procedures.get_current_datetime()
        self.restaurant_current_date = current_datetime.date()  # just in case, it's not necessary

        current_datetime_weekday = current_datetime.weekday()
        close_hour_in_minutes = 0
        if current_datetime_weekday == 0:
            if self.public_monday_close_hour_in_minutes != None:
                close_hour_in_minutes = self.public_monday_close_hour_in_minutes
        elif current_datetime_weekday == 1:
            if self.public_tuesday_close_hour_in_minutes != None:
                close_hour_in_minutes = self.public_tuesday_close_hour_in_minutes
        elif current_datetime_weekday == 2:
            if self.public_wednesday_close_hour_in_minutes != None:
                close_hour_in_minutes = self.public_wednesday_close_hour_in_minutes
        elif current_datetime_weekday == 3:
            if self.public_thursday_close_hour_in_minutes != None:
                close_hour_in_minutes = self.public_thursday_close_hour_in_minutes
        elif current_datetime_weekday == 4:
            if self.public_friday_close_hour_in_minutes != None:
                close_hour_in_minutes = self.public_friday_close_hour_in_minutes
        elif current_datetime_weekday == 5:
            if self.public_saturday_close_hour_in_minutes != None:
                close_hour_in_minutes = self.public_saturday_close_hour_in_minutes
        elif current_datetime_weekday == 6:
            if self.public_sunday_close_hour_in_minutes != None:
                close_hour_in_minutes = self.public_sunday_close_hour_in_minutes

        if close_hour_in_minutes == 0:  # closes at midnight
            self.restaurant_current_date = current_datetime.date()
        else:
            if close_hour_in_minutes > 0:  # closes after midnight
                if (
                    current_datetime.time().hour * 60 + current_datetime.time().minute
                ) > close_hour_in_minutes:
                    self.restaurant_current_date = current_datetime.date()
                else:
                    self.restaurant_current_date = current_datetime.date() - timedelta(
                        days=1
                    )  # for practical reasons the day hasn't changed
            else:  # closes before midnight
                if (
                    current_datetime.time().hour * 60 + current_datetime.time().minute
                ) > 24 * 60 + close_hour_in_minutes:  # remember, close_hour... is negative
                    if current_datetime.date() == self.restaurant_current_date:
                        self.restaurant_current_date = current_datetime.date() + timedelta(days=1)
                    else:  # it's greater, it can't be less, but if it was, it shouldn't matter
                        self.restaurant_current_date = current_datetime.date()
                else:  # it isn't closed yet or it is closing right now
                    self.restaurant_current_date = current_datetime.date()
                    
class ReactivatedDate(models.Model):
    reactivation_date = models.DateField(default=date.today)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
                    
class CuttingServiceDate(models.Model):
    cutting_service_date = models.DateField(default=date.today)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
                            
class Image(models.Model):
    image_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    image_original_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    image_public_id = models.CharField(
        max_length=CLOUDINARY_PUBLIC_ID_MAX_LENGTH, default=""
    )
    image_resource_type = models.CharField(
        max_length=CLOUDINARY_RESOURCE_TYPE_MAX_LENGTH, default=""
    )
    image_url = models.URLField(max_length=URLS_MAX_LENGTH, default="")
    use_count = models.IntegerField(default=0)
    finished_setting = models.BooleanField(default=False)
    # if finished_setting === True, it means that the user hasn't set the name, if the creation process
    # was interrupted, it will remain unused in the database and Cloudinary
    image_creation_date = models.DateField(auto_now_add=True)
    image_next_revision_date = models.DateField(default=get_next_revision_date)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
class Monthly_Accesses(models.Model):
    month = models.CharField(default="")
    accesses = models.IntegerField(default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Restaurant_User(models.Model):
    public_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    private_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    # public_phone = models.CharField(max_length=PHONES_MAX_LENGTH, default="")
    # private_phone = models.CharField(max_length=PHONES_MAX_LENGTH, default="")
    public_image_id = models.BigIntegerField(default=-1)
    private_image_id = models.BigIntegerField(default=-1)
    public_password = models.CharField(max_length=ENCRYPTED_PASSWORDS_MAX_LENGTH, default="")
    private_password = models.CharField(max_length=ENCRYPTED_PASSWORDS_MAX_LENGTH, default="")
    public_email = models.EmailField(max_length=EMAILS_MAX_LENGTH, default="")
    private_email = models.EmailField(max_length=EMAILS_MAX_LENGTH, default="")
    public_email_validated = models.BooleanField(default=False)
    private_email_validated = models.BooleanField(default=False)
    # public_phone_validated = models.BooleanField(default=False)
    # private_phone_validated = models.BooleanField(default=False)
    logged_in = models.BooleanField(default=False)
    last_logged_in = models.CharField(max_length=DATESTR_MAX_LENGTH, default="")
    last_logged_out = models.CharField(max_length=DATESTR_MAX_LENGTH, default="")
    recently_created = models.BooleanField(default=True)
    marked_for_deletion = models.BooleanField(default=False)
    main_user = models.BooleanField(default=False)
    has_been_modified = models.BooleanField(default=False)
    random_number_to_validate = models.CharField(
        max_length=VERIFICATION_KEY_LENGTH, default=""
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
        
    def get_decrypted_public_password(self):
        return decrypt_value(self.public_password)
        
    def get_decrypted_private_password(self):
        return decrypt_value(self.private_password)
    
# The foreign key to Delivery Company is there to ease getting the delivery company data
# Have to make sure that both Restaurant and Delivery Company point to the same flag
class Restaurant_Delivery_Company(models.Model):
    public_token = models.CharField(max_length=DELIVERY_TOKEN_MAX_LENGTH, default="")
    private_token = models.CharField(max_length=DELIVERY_TOKEN_MAX_LENGTH, default="")
    recently_created = models.BooleanField(default=True)
    marked_for_deletion = models.BooleanField(default=False)
    has_been_modified = models.BooleanField(default=False)
    delivery_company = models.ForeignKey(Delivery_Company, on_delete=models.DO_NOTHING)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Promotion(models.Model):
    public_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    private_name = models.CharField(
        max_length=NAMES_MAX_LENGTH, default=f"{PROMOTION_PROVISIONAL_NAME}"
    )
    public_attractor_text = models.CharField(max_length=NAMES_MAX_LENGTH, default="", blank=True)
    private_attractor_text = models.CharField(max_length=NAMES_MAX_LENGTH, default="", blank=True)
    public_promotion_text = models.TextField(default="")
    private_promotion_text = models.TextField(default="")
    recently_created = models.BooleanField(default=False)
    has_been_modified = models.BooleanField(default=False)
    marked_for_deletion = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Category(models.Model):
    public_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    private_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    public_description = models.CharField(
        max_length=DESCRIPTIONS_MAX_LENGTH, default=""
    )
    private_description = models.CharField(
        max_length=DESCRIPTIONS_MAX_LENGTH, default=""
    )
    public_view_order = models.IntegerField(null=True)
    private_view_order = models.IntegerField(null=True)
    public_image_id = models.BigIntegerField(default=-1)
    private_image_id = models.BigIntegerField(default=-1)
    recently_created = models.BooleanField(default=True)
    has_been_modified = models.BooleanField(default=False)
    marked_for_deletion = models.BooleanField(default=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Dish(models.Model):
    public_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    private_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    public_description = models.CharField(
        max_length=DESCRIPTIONS_MAX_LENGTH, default=""
    )
    private_description = models.CharField(
        max_length=DESCRIPTIONS_MAX_LENGTH, default=""
    )
    public_price = models.CharField(max_length=PRICES_MAX_LENGTH, default="0.0")
    private_price = models.CharField(max_length=PRICES_MAX_LENGTH, default="0.0")
    public_view_order = models.IntegerField(null=True)
    private_view_order = models.IntegerField(null=True)
    public_image_id = models.BigIntegerField(default=-1)
    private_image_id = models.BigIntegerField(default=-1)
    previous_dish_number_of_reviews = models.IntegerField(default=0)
    previous_dish_reviews_average = models.IntegerField(default=0)
    recently_created = models.BooleanField(default=True)
    marked_for_deletion = models.BooleanField(default=False)
    marked_for_deletion_by_parent = models.BooleanField(default=False)
    has_been_modified = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Review(models.Model):
    diner_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    creation_date = models.DateTimeField(auto_now_add=True)
    number_of_stars = models.IntegerField(default=5)
    review_comment = models.CharField(max_length=COMMENT_MAX_LENGTH, default="")
    public_rejected = models.BooleanField(default=False)
    private_rejected = models.BooleanField(default=False)
    rejection_status_just_changed = models.BooleanField(default=False)
    parent_type = models.CharField(max_length=100, default="restaurant")
    parent_name = models.CharField(max_length=NAMES_MAX_LENGTH, default="")
    has_been_modified = models.BooleanField(default=False)
    # The review acts upon a restaurant or a dish
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True)


class Review_Rejection(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="rejections"
    )
    rejection_reason = models.ForeignKey(Rejection_Reason, on_delete=models.CASCADE)

class Accessing_Devices(models.Model):
    device_description = models.CharField(max_length=DEVICE_DESCRIPTION_LENGTH, default="")
