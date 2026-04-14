from ..models import Restaurant, Category, Dish
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from django.db.models import F, Value
from typing import Dict, Any
from django.db.models import Q
from .Useful_procedures import Useful_procedures

# methods should receive the restaurant object, not just the id


class Menu_Editing_Publish_or_Discard:
    def discard_menu_editing(self, my_restaurant):
        try:
            # cancel editing has to check that the editing was started, the same with cancel reviews updates
            # categories will have all Restaurant categories
            all_categories = Category.objects.filter(restaurant=my_restaurant.id)
            # it's cancel, so delete the recent new ones
            all_categories.filter(recently_created=True).delete()
            # get all categories again since some of them may have been deleted

            all_categories = Category.objects.filter(restaurant=my_restaurant.id)
            if all_categories.exists():
                all_categories.update(
                    private_name="",
                    private_description="",
                    private_image_id=-1,
                    recently_created=False,
                    has_been_modified=False,
                    marked_for_deletion=False,
                )
                all_dishes = Dish.objects.filter(category__in=all_categories)
                all_dishes.filter(recently_created=True).delete()

                all_dishes = Dish.objects.filter(category__in=all_categories)
                if all_dishes.exists():
                    all_dishes.update(
                        private_name="",
                        private_description="",
                        private_image_id=-1,
                        private_price=0.0,
                        recently_created=False,
                        has_been_modified=False,
                        marked_for_deletion=False,
                        marked_for_deletion_by_parent=False,
                    )

            my_restaurant.menu_edition_is_pending = False

            my_restaurant.save()
            return {
                "return_code": status.HTTP_200_OK,
                "message": f"You have discarded changes",
            }

        except Exception as e:
            return {
                "return_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }

    def publish_menu_editing(self, my_restaurant):
        if my_restaurant.currently_logged_in == -1:
            # No one is logged in
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You are not logged in",
            }

        if my_restaurant.dont_allow_further_actions_from_this_user:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You can't perform any actions, please logout",
            }
        if not my_restaurant.menu_edition_is_pending:
            return {
                "return_code": status.HTTP_400_BAD_REQUEST,
                "message": "You haven't started the edition",
            }

        try:
            # categories will have all the Restaurant's categories
            all_categories = Category.objects.filter(restaurant=my_restaurant.id)
            # delete all categories marked for deletion
            all_categories.filter(marked_for_deletion=True).delete()
            # Now refetch all categories since some of them may have been deleted
            all_categories = Category.objects.filter(restaurant=my_restaurant.id)

            # Proceed with the rest
            if all_categories.exists():
                for category in all_categories:
                    # Check if public_image_id is being updated
                    if category.public_image_id != category.private_image_id:
                        # Update image use count for old and new public_image_id
                        Useful_procedures.procedure_update_image_use_count(
                            category.public_image_id, category.private_image_id
                        )
                all_categories.filter().update(
                    public_name=F("private_name"),
                    public_description=F("private_description"),
                    public_image_id=F("private_image_id"),
                    private_name="",
                    private_description="",
                    private_image_id=-1,
                    marked_for_deletion=False,
                    recently_created=False,
                    has_been_modified=False,
                )

                # all_dishes will have all_categories dishes
                all_dishes = Dish.objects.filter(category__in=all_categories)
                # delete all dishes of all_categories marked for deletion
                all_dishes.filter(marked_for_deletion=True).delete()
                # Now refetch all dishes of all_categories since some of them may have been deleted
                all_dishes = Dish.objects.filter(category__in=all_categories)

                # Proceed with the rest
                if all_dishes.exists():
                    for dish in all_dishes:
                        # Check if public_image_id is being updated
                        if dish.public_image_id != dish.private_image_id:
                            # Update image use count for old and new public_image_id
                            Useful_procedures.procedure_update_image_use_count(
                                dish.public_image_id, dish.private_image_id
                            )
                    all_dishes.filter().update(
                        public_name=F("private_name"),
                        public_description=F("private_description"),
                        public_image_id=F("private_image_id"),
                        public_price=F("private_price"),
                        private_name="",
                        private_description="",
                        private_image_id=-1,
                        private_price=0.0,
                        marked_for_deletion=False,
                        marked_for_deletion_by_parent=False,
                        recently_created=False,
                        has_been_modified=False,
                    )
            my_restaurant.data_changed = True
            my_restaurant.menu_edition_is_pending = False
            my_restaurant.update_image_uses = True
            my_restaurant.save()
            return {
                "return_code": status.HTTP_200_OK,
                "message": f"Your updates were performed succesfully",
            }

        except Exception as e:
            # If any exception occurs, the transaction is rolled back automatically
            return {
                "return_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }
