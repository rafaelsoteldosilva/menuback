from datetime import date
from dateutil.relativedelta import relativedelta
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
import json
from ..utils.Constants_and_strings import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class Useful_procedures:
    @staticmethod
    def get_current_datetime():
        return timezone.localtime(timezone.now())
        # return timezone.now() - timedelta(hours=LOCAL_DJANGO_HOURS_FIX)

    @staticmethod
    def phone_number(value):
        reg = re.compile("^\\+(?:[0-9]●?){6,14}[0-9]$") 
        if not reg.match(value):
            raise ValidationError(f"{value} is not a valid number")

    @staticmethod
    def get_period_start_date():
        current_date = Useful_procedures.get_current_datetime().date().replace(day=1)
        return current_date

    @staticmethod
    def procedure_update_image_use_count(old_image_id, new_image_id):
        from ..models import Image  # Import Image model here to avoid circular importing references

        # Decrease use_count for the old image
        if old_image_id != new_image_id:
            if old_image_id != -1:
                try:
                    my_image = Image.objects.get(pk=old_image_id)
                    my_image.use_count -= 1
                    if my_image.use_count < 0:  # it should never happen
                        my_image.use_count = 0
                        print("update_image_uses:: my_image.use_count < 0 ???")
                    my_image.save()
                except Image.DoesNotExist:
                    print(f"update_image_uses:: Image with id {old_image_id} DoesNotExist")
                except Exception as e:
                    print(f"An error occurred while updating old image {old_image_id}: {e}")

            # Increase use_count for the new image
            if new_image_id != -1:
                try:
                    my_image = Image.objects.get(pk=new_image_id)
                    my_image.use_count += 1
                    my_image.save()
                except Image.DoesNotExist:
                    print(f"update_image_uses:: Image with id {new_image_id} DoesNotExist")
                except Exception as e:
                    print(f"An error occurred while updating new image {new_image_id}: {e}")

    @staticmethod
    def FORMATTED_PRINT(str, data):
        formatted_data = json.dumps(data, indent=4)
        print(f"{str}:: {formatted_data}")

    @staticmethod
    def date_month(my_date):
        # Parse the input date string into a datetime object
        date_obj = datetime.strptime(my_date, '%Y-%m-%d')
        # Format the date as 'YYYY-month'
        return date_obj.strftime('%Y-%B').lower()
    
    @staticmethod
    def months_appart(date_1, date_2):
        earlier_date, later_date = sorted([date_1, date_2])
        
        # Calculate the difference in years and months
        year_diff = later_date.year - earlier_date.year
        month_diff = later_date.month - earlier_date.month
        
        # Total calendar months between the two dates
        total_months = year_diff * 12 + month_diff
        
        return total_months
        

    @staticmethod
    def days_appart(date_1, date_2):
        return abs((date_2 - date_1).days)
