import datetime
from datetime import timedelta
from django.utils.timezone import now
from django.utils import timezone
import random
from django.db import models
from django.db.models import Avg

from ..utils.Constants_and_strings import *
from ..models import (
    Country,
    Restaurant,
    Monthly_Accesses,
    Promotion,
    Delivery_Company,
    Rejection_Reason,
    Restaurant_Delivery_Company,
    Category,
    Dish,
    Super_User,
    Restaurant_User,
    Review,
    Image,
)
from ..serializer import (
    Country_Serializer,
    Restaurant_Serializer,
    Promotion_Serializer,
    Restaurant_User_Retrieve_Image_And_Name_Serializer,
    Rejection_Reason_Serializer,
    Restaurant_Delivery_Company_Serializer,
    Category_Serializer,
    Dish_Serializer,
    Review_Serializer,
    Image_Serializer,
)
from rest_framework import status

from ..utils.Useful_procedures import Useful_procedures

class Menu_Class:
    def __init__(self):
        self.menu = {}
        self.restaurant_was_read = True

    def Load_Restaurant(self, my_restaurant):
        my_restaurant.total_number_of_accesses += 1
        current_datetime = Useful_procedures.get_current_datetime()
        if current_datetime.date() != my_restaurant.restaurant_current_date:
            my_restaurant.todays_random_number = random.randint(10, 99)
        
        my_restaurant.self_update_restaurant_current_date()

        # Check change in the restaurant month
        updated_month = my_restaurant.restaurant_current_date.month
        if (updated_month != my_restaurant.restaurant_current_month):
            my_restaurant.number_of_days_served_in_current_month = 0
            my_restaurant.active_month_number += 1
            my_restaurant.restaurant_current_month = updated_month
            if (my_restaurant.number_of_pending_free_months > 0):
                my_restaurant.number_of_pending_free_months -= 1
                
        # Check change in the restaurant day
        updated_day = my_restaurant.restaurant_current_date.day
        if (updated_day != my_restaurant.restaurant_current_day):
            my_restaurant.number_of_days_served_in_current_month += 1
            my_restaurant.restaurant_current_day = updated_day

        my_restaurant.save()
        restaurant_serialized = Restaurant_Serializer(my_restaurant)

        self.menu["restaurant"] = {}
        self.menu["restaurant"] = restaurant_serialized.data

    def Load_Restaurant_Reviews(self, my_restaurant):
        # Get filtered reviews and aggregate the average number of stars
        restaurant_reviews_filtered = Review.objects.filter(
            restaurant_id=my_restaurant.id, public_rejected=False, parent_type="restaurant"
        ).order_by("-creation_date")
        restaurant_reviews_aggregate = restaurant_reviews_filtered.aggregate(
            Avg("number_of_stars")
        )

        # Get the current number of reviews
        restaurant_current_number_of_reviews = restaurant_reviews_filtered.count()

        # Calculate the average number of stars
        restaurant_reviews_average = (
            restaurant_reviews_aggregate.get("number_of_stars__avg", 0) or 0
        )

        # Calculate the combined average with previous average if available
        if my_restaurant.previous_restaurant_reviews_average != 0:
            restaurant_reviews_average = (
                restaurant_reviews_average
                + my_restaurant.previous_restaurant_reviews_average
            ) / 2

        # Calculate the combined number of reviews with previous count
        restaurant_number_of_reviews = (
            restaurant_current_number_of_reviews
            + my_restaurant.previous_restaurant_number_of_reviews
        )

        # Serialize reviews and store in menu dictionary
        reviews_data = []
        for review in restaurant_reviews_filtered:
            review_serialized = Review_Serializer(review).data
            reviews_data.append(
                {
                    "review": review_serialized,
                    "review_rejection": {},  # Include an empty review_rejection field
                }
            )

        # Store review data in menu dictionary
        self.menu["restaurant_reviews"] = {
            "number_of_reviews": restaurant_number_of_reviews,
            "reviews_average": restaurant_reviews_average,
            "reviews": reviews_data,
        }

    def Load_Restaurant_Delivery_Companies(self, my_restaurant):
        try:
            # Filter restaurant delivery companies
            restaurant_delivery_companies_filtered = Restaurant_Delivery_Company.objects.filter(restaurant=my_restaurant)

            # Check if any delivery companies are found
            if not restaurant_delivery_companies_filtered.exists():
                self.menu["restaurant_delivery_companies"] = []
                return

            # Serialize the delivery companies
            restaurant_delivery_companies_data = []
            for restaurant_delivery in restaurant_delivery_companies_filtered:
                try:
                    serialized_data = Restaurant_Delivery_Company_Serializer(
                        restaurant_delivery,
                        context={'include_details': True}
                    ).data
                    restaurant_delivery_companies_data.append({
                        "restaurant_delivery_company": serialized_data
                    })
                except Exception as e:
                    print(f'Error serializing delivery company {restaurant_delivery.id}: {e}') # type: ignore

            self.menu["restaurant_delivery_companies"] = restaurant_delivery_companies_data

        except Exception as e:
            print(f'Error in Load_Restaurant_Delivery_Companies: {e}')
            # Optionally handle the error or return a response indicating the error

    def Load_Promotions(self, my_restaurant):
        promotions_filtered = Promotion.objects.filter(restaurant=my_restaurant)

        promotions_data = [
            {"promotion": Promotion_Serializer(promotion).data}
            for promotion in promotions_filtered
        ]

        self.menu["promotions"] = promotions_data
        
    def Load_Restaurant_User_Images_And_Names(self, my_restaurant):
        # Filter the Restaurant_Users by the given restaurant ID
        users_filtered = Restaurant_User.objects.filter(restaurant=my_restaurant)

        # Serialize the public_image_id for each Restaurant_User
        users_images_and_names_data = [
            {"user": Restaurant_User_Retrieve_Image_And_Name_Serializer(user).data}
            for user in users_filtered
        ]

        # Add the serialized data to a desired key in your menu or context
        self.menu["restaurant_user_images_and_names"] = users_images_and_names_data

    def Load_Rejection_Reasons(self):
        all_reasons = Rejection_Reason.objects.all().order_by("pk")
        rejection_reasons_data = [
            {"rejection_reason": Rejection_Reason_Serializer(reason).data}
            for reason in all_reasons
        ]
        self.menu["rejection_reasons"] = rejection_reasons_data

    def Load_Countries(self):
        all_countries = Country.objects.all().order_by("pk")
        countries_data = [
            {"country": Country_Serializer(country).data} for country in all_countries
        ]
        self.menu["countries"] = countries_data

    def Load_Whole_Rest_Of_Menu(self, my_restaurant):
        images_filtered = Image.objects.filter(restaurant=my_restaurant).order_by(
            "image_name"
        )
        images_data = [
            {"image": Image_Serializer(image).data} for image in images_filtered
        ]
        categories_filtered = Category.objects.filter(
            restaurant=my_restaurant
        ).order_by("public_view_order")
        categories_data = []
        for category in categories_filtered:
            category_serializer = Category_Serializer(category)
            category_data = {"category": category_serializer.data, "dishes": []}

            dishes_filtered = Dish.objects.filter(category=category.id).order_by( # type: ignore
                "public_view_order"
            )
            for dish in dishes_filtered:
                dish_serializer = Dish_Serializer(dish)
                dish_data = {"dish": dish_serializer.data}

                dish_reviews_filtered = Review.objects.filter(
                    dish=dish.id, public_rejected=False, parent_type="dish" # type: ignore
                ).order_by("-creation_date")
                dish_data["dish_reviews_average"] = (
                    dish_reviews_filtered.aggregate(Avg("number_of_stars")).get(
                        "number_of_stars__avg", 0
                    )
                    or 0
                )
                dish_data["dish_number_of_reviews"] = dish_reviews_filtered.count()
                dish_data["reviews"] = [
                    {
                        "review": Review_Serializer(review).data,
                        "review_rejection": {},  # Include an empty review_rejection field
                    }
                    for review in dish_reviews_filtered
                ]
                category_data["dishes"].append(dish_data)
            categories_data.append(category_data)
        self.menu.update(
            {
                "images": images_data,
                "categories": categories_data,
            }
        )

    def Update_Accesses(self, my_restaurant):
        current_month = now().strftime("%Y-%B").lower()
        
        try:
            # Attempt to get or create the Monthly_Accesses record
            monthly_access, created = Monthly_Accesses.objects.get_or_create(
                month=current_month,
                restaurant=my_restaurant,
                defaults={"accesses": 1}
            )
            if not created:
                # Increment accesses if the record already exists
                monthly_access.accesses += 1
                monthly_access.save()

        except Exception as e:
            print(f"Error creating/updating Monthly_Accesses: {e}")
            raise e  # Raise the exception after logging it for debugging

