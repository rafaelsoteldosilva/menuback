from dataclasses import fields
from rest_framework import serializers
from django.db.models import ForeignKey

from .utils.Encryption import decrypt_value, encrypt_value

from .utils.Constants_and_strings import *

from .models import (
    Past_Token,
    Global_Price,
    Country,
    Restaurant,
    Super_User,
    Delivery_Company,
    Payment_Option,
    Review_Rejection,
    Rejection_Reason,
    Restaurant_Delivery_Company,
    Promotion,
    Category,
    Dish,
    Restaurant_User,
    Review,
    Image,
    Accessing_Devices,
    Monthly_Accesses
)


class Past_Token_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Past_Token
        fields = [
            f.name for f in Past_Token._meta.fields if not isinstance(f, ForeignKey)
        ]


# ------------------------- Begin Prefilled Models Serializers --------------------------------

class Global_Price_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Global_Price
        fields = "__all__"


class Country_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class Delivery_Company_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery_Company
        fields = "__all__"


class Payment_Option_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Payment_Option
        fields = "__all__"


class Rejection_Reason_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Rejection_Reason
        fields = ["id"] + ["reason"] + ["explanation"]


class Rejection_Reason_Serializer_For_All_Reviews(serializers.ModelSerializer):
    class Meta:
        model = Rejection_Reason
        fields = ["id"] + ["reason"]


# ------------------------- End Prefilled Models Serializers --------------------------------

class Restaurant_Serializer(serializers.ModelSerializer):
    public_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=False)
    private_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=False)

    class Meta:
        model = Restaurant
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['public_country'] = Country_Serializer(instance.public_country).data if instance.public_country else None
        representation['private_country'] = Country_Serializer(instance.private_country).data if instance.private_country else None
        return representation

    def update(self, instance, validated_data):
        public_country_data = validated_data.pop('public_country', None)
        private_country_data = validated_data.pop('private_country', None)
        
        # Update each field in the instance with validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If private_country_data is provided, update it
        if private_country_data is not None:
            try:
                private_country_instance = Country.objects.get(pk=private_country_data.pk)
                instance.private_country = private_country_instance
            except Country.DoesNotExist:
                raise serializers.ValidationError(f"Country with pk {private_country_data.pk} does not exist")

        instance.save()
        return instance

class Super_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Super_User
        fields = [
            f.name for f in Super_User._meta.fields if not isinstance(f, ForeignKey)
        ]

class Restaurant_User_Retrieve_Image_And_Name_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_User
        fields = ['id', 'public_name', 'main_user', 'public_email', 'public_image_id', 'public_email_validated']  # Only include the 'public_image_id' and 'id' fields

class Restaurant_User_Retrieve_Serializer(serializers.ModelSerializer):
    decrypted_public_password = serializers.SerializerMethodField(read_only=True)
    decrypted_private_password = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Restaurant_User
        fields = [
            f.name for f in Restaurant_User._meta.fields if not isinstance(f, ForeignKey)
        ] + ['decrypted_public_password', 'decrypted_private_password']

    def get_decrypted_public_password(self, obj):
        return decrypt_value(obj.public_password)

    def get_decrypted_private_password(self, obj):
        return decrypt_value(obj.private_password) if obj.private_password else ''
 
        
class Restaurant_User_Update_or_Create_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_User
        fields = [
            f.name for f in Restaurant_User._meta.fields if not isinstance(f, ForeignKey)
        ] + ['restaurant']
        
    def update(self, current_instance, updated_data): # type: ignore
        for attr, value in updated_data.items():
            if attr in ['public_password', 'private_password'] and (value not in (None, '')):
                value = encrypt_value(value)
            setattr(current_instance, attr, value)
        current_instance.save()
        return current_instance
    
    def create(self, validated_data):  # type: ignore
    # Make a copy of validated_data to avoid modifying the original data
        user_data = validated_data.copy()
        
        for attr, value in user_data.items():
            print(f'Restaurant_User_Update_or_Create_Serializer:: value:: {value}')
            print(f'Restaurant_User_Update_or_Create_Serializer:: attr:: {attr}')
            if attr in ['public_password', 'private_password'] and value not in (None, ''):
                user_data[attr] = encrypt_value(value)
                
        # Create the Restaurant_User instance with modified data
        return Restaurant_User.objects.create(**user_data)

class Restaurant_Delivery_Company_Serializer(serializers.ModelSerializer):
    delivery_company_details = Delivery_Company_Serializer(
        source="delivery_company", read_only=True
    )

    class Meta:
        model = Restaurant_Delivery_Company
        fields = '__all__'  # Include all fields initially

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Check the context for 'include_details' and add/remove field as needed
        if not self.context.get('include_details', False):
            # Remove the 'delivery_company_details' field if not needed
            representation.pop('delivery_company_details', None)
        
        return representation

    def update(self, instance, validated_data):
        delivery_company = validated_data.pop('delivery_company', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # If a new delivery_company is provided, update it
        if delivery_company is not None:
            instance.delivery_company = delivery_company
        
        instance.save()
        return instance

    def create(self, validated_data):
        # Extract nested objects if needed
        delivery_company = validated_data.pop('delivery_company', None)
        
        # Create and return a new Restaurant_Delivery_Company instance
        instance = Restaurant_Delivery_Company.objects.create(
            **validated_data,
            delivery_company=delivery_company
        )
        return instance
       
class Promotion_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = [
            f.name for f in Promotion._meta.fields if not isinstance(f, ForeignKey)
        ] + ['restaurant']
        
    def update(self, current_instance, updated_data): # type: ignore
        for attr, value in updated_data.items():
            setattr(current_instance, attr, value)
        current_instance.save()
        return current_instance
    
    def create(self, new_user_data): # type: ignore
        return Promotion.objects.create(**new_user_data)
      
class Category_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            f.name for f in Category._meta.fields if not isinstance(f, ForeignKey)
        ] + ['restaurant']
        
    def update(self, current_instance, updated_data): # type: ignore
        for attr, value in updated_data.items():
            setattr(current_instance, attr, value)
        current_instance.save()
        return current_instance
    
    def create(self, new_user_data): # type: ignore
        return Category.objects.create(**new_user_data)


class Dish_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            f.name for f in Dish._meta.fields if not isinstance(f, ForeignKey)
        ] + ['category']
        
    def update(self, current_instance, updated_data): # type: ignore
        for attr, value in updated_data.items():
            setattr(current_instance, attr, value)
        current_instance.save()
        return current_instance
    
    def create(self, new_user_data): # type: ignore
        return Dish.objects.create(**new_user_data)
    
class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        
    def create(self, validated_data):
        # Expecting 'review_type', 'restaurant_id', and 'dish_id' fields in the request data
        review_type = self.initial_data.get('review_type') # type: ignore
        restaurant_id = self.initial_data.get('restaurant_id') # type: ignore
        dish_id = self.initial_data.get('dish_id') # type: ignore
        if not review_type or not restaurant_id or (review_type == 'dish' and not dish_id):
            print("Review type or restaurant_id or dish_id (the last one for dish reviews only) are required")
            raise serializers.ValidationError("Review type or restaurant_id or dish_id (the last one for dish reviews only) are required")

        if review_type == 'restaurant':
            my_restaurant = Restaurant.objects.get(id=restaurant_id)
            validated_data.update({
                'parent_type': 'restaurant',
                'parent_name': my_restaurant.public_name,
                'dish': None,
                'restaurant': my_restaurant,
            })
        elif review_type == 'dish':
            my_restaurant = Restaurant.objects.get(id=restaurant_id)
            my_dish = Dish.objects.get(id=dish_id)
            validated_data.update({
                'parent_type': 'dish',
                'parent_name': my_dish.public_name,
                'dish': my_dish,
                'restaurant': my_restaurant,
            })
        else:
            print('Invalid review type provided.')
            raise serializers.ValidationError("Invalid review type provided.")
        
        return Review.objects.create(**validated_data)

class Review_Rejection_Serializer(serializers.ModelSerializer):
    rejection_reason = Rejection_Reason_Serializer()

    class Meta:
        model = Review_Rejection
        fields = ["rejection_reason"]


class Review_Rejection_Serializer_For_All_Reviews(serializers.ModelSerializer):
    rejection_reason = Rejection_Reason_Serializer_For_All_Reviews()

    class Meta:
        model = Review_Rejection
        fields = ["rejection_reason"]


class Image_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [f.name for f in Image._meta.fields if not isinstance(f, ForeignKey)]

    def update(self, instance, validated_data):
        validated_data["finished_setting"] = True
        return super().update(instance, validated_data)


class Accessing_Devices_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Accessing_Devices
        fields = [
            f.name for f in Accessing_Devices._meta.fields if not isinstance(f, ForeignKey)
        ]