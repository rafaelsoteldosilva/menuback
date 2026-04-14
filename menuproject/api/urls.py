from django.urls import path
from django.urls import re_path
from django.views.generic import RedirectView

from .utils.First_Month_Amount_To_Pay import (
    get_converted_first_month_amount_to_pay
)

from .views import (
    public_or_private,
    send_key_via_email,
    whole_menu,
    all_reviews_with_rejections_if_any,
    check_restaurant_existence,
    check_restaurant_rut_existence,
    get_help_video_url,
    restaurant_delivery_company,
    start_promotions_editing,
    promotion,
    retrieve_restaurant_user_for_edition,
    load_restaurant_users,
    restaurant,
    category,
    dish,
    restaurant_user,
    load_delivery_companies,
    load_payment_options,
    update_image_uses,
    get_all_images,
    review,
    switch_review_rejection,
    start_menu_editing,
    start_reviews_editing,
    start_menu_sort_editing,
    start_restaurant_deliveries_editing,
    start_preferences_editing,
    discard_preferences_editing,
    publish_preferences_editing,
    publish_restaurant_deliveries_editing,
    discard_restaurant_deliveries_editing,
    discard_menu_editing,
    publish_menu_editing,
    discard_reviews_editing,
    publish_reviews_editing,
    discard_menu_sort_editing,
    publish_promotions_editing,
    discard_promotions_editing,
    publish_menu_sort_editing,
    clear_all_private_view_orders,
    clear_categories_private_view_orders,
    clear_category_dishes_private_view_orders,
    add_image,
    image,
    delete_cloudinary_resource,
    delete_cloudinary_resource_and_image,
    start_restaurant_users_editing,
    discard_restaurant_users_editing,
    publish_restaurant_users_editing,
    handle_loaded_images,
    show_restaurant_number,
    pay,
    handle_show_qr,
    send_qr_code_via_email,
    check_for_connection,
    save_device_description,
    payment_period,
    service_period,
    is_restaurant_blocked,
    check_for_category_dishes_revisions,
    check_for_dish_revisions,
    get_amount_to_be_paid,
    does_the_restaurant_have_to_pay,
    save_new_restaurant_data,
    # create_restaurant,
    load_countries,
    get_country_by_id,
    get_country_by_name,
    get_restaurant_main_user_email,
    get_restaurant_main_user_data,
    get_restaurant_from_rut,
    webpay_plus_create,
    webpay_plus_commit,
    payment_failed,
    webpay_plus_refund,
    webpay_plus_refund_form,
    webpay_show_create,
    webpay_status,
    # webpay_plus_pay
    get_user_object,
    restaurant_basic_data,
    check_user_credentials,
    get_app_total_cost,
    send_pdf_via_email,
    get_menu_load_cost,
    send_support_request_via_email,
    update_restaurant_user_name_and_password,
    get_datetime_from_backend
)

from .authorization_views import get_first_token
from .payment_views import create_paypal_order_atonna, create_paypal_order_little_atonna, capture_paypal_order_atonna, capture_paypal_order_little_atonna

from .logging_views import (
    try_to_login_into_the_admin_area,
    login_normally,
    login_no_further_actions,
    logout_from_admin_area,
)
from menuproject.api import views

urlpatterns = [
    path('access_backend/', views.access_backend_view, name='access_backend'),
    path("get_datetime_from_backend/", get_datetime_from_backend, name="get_datetime_from_backend"),
    re_path(r'^favicon.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    
    # Webpay Plus ---------------------------------------------------------------
    path("webpay-plus/create/<int:country_id>/<str:restaurant_rut>/<str:price_type>/<str:user_email>/<str:action>/", webpay_plus_create),
    path('webpay-plus/payment_failed/', payment_failed, name='payment_failed'),
    path('webpay-plus/commit/', webpay_plus_commit, name='webpay_plus_commit'),
    # path('webpay_plus/commit/', include('webpay_plus.urls')),
    path("webpay-plus/refund/", webpay_plus_refund),
    path("webpay-plus/refund-form/", webpay_plus_refund_form),
    path("webpay-plus/show-create/", webpay_show_create),
    path("webpay-plus/status/", webpay_status),
    # path("webpay_plus_pay/", webpay_plus_pay),
    
    path("get_user_object/<int:user_id>/", get_user_object),
    
    path("get_converted_first_month_amount_to_pay/<str:price_type>/<str:country_name>/", get_converted_first_month_amount_to_pay),
    path("get_app_total_cost/<str:price_type>/<str:country_name>/", get_app_total_cost),
    path("get_menu_load_cost/<str:country_name>/", get_menu_load_cost),
    path("get_restaurant_from_rut/<str:restaurant_rut>/", get_restaurant_from_rut),
    path("save_new_restaurant_data/", save_new_restaurant_data),
    path("load_countries/", load_countries),
    path("get_country_by_id/<int:country_id>/", get_country_by_id),
    path("get_country_by_name/<str:country_name>/", get_country_by_name),
    
    path("check_for_category_dishes_revisions/<int:category_id>/", check_for_category_dishes_revisions),
    path("check_for_dish_revisions/<int:dish_id>/", check_for_dish_revisions),
    
    path("does_the_restaurant_have_to_pay/<int:restaurant_id>/", does_the_restaurant_have_to_pay),
    path("get_amount_to_be_paid/<int:restaurant_id>/", get_amount_to_be_paid),
    
    path("public_or_private/<int:restaurant_id>/", public_or_private),
    path("is_restaurant_blocked/<int:restaurant_id>/", is_restaurant_blocked),
    
    path(
        "send_key_via_email/<str:email_address>/<str:four_digits_key>/<str:restaurant_id>/",
        send_key_via_email,
    ),
    path("send_qr_code_via_email/", send_qr_code_via_email),

    path("send_pdf_via_email/", send_pdf_via_email),
    path("send_support_request_via_email/", send_support_request_via_email),

    path("get_first_token/", get_first_token),
    path("check_for_connection/<int:restaurant_id>/", check_for_connection),
    
    path("whole_menu/<int:restaurant_id>/", whole_menu),
    
    path("get_help_video_url/<str:video_name>/", get_help_video_url),
    
    # Cloudinary
    
    path(
        "delete_cloudinary_resource/<str:public_id>/",
        delete_cloudinary_resource,
    ),
    re_path(
        r"^delete_cloudinary_resource_and_image/(?P<restaurant_id>\d+)/(?P<image_id>\d+)/(?P<public_id>.+)/$",
        delete_cloudinary_resource_and_image,
        name="delete_cloudinary_resource_and_image",
    ),
    
    # Payment Option ---------------------------------------------------------------
    
    path("create_paypal_order_atonna/<int:restaurant_id>/<str:action>/", create_paypal_order_atonna),
    path("create_paypal_order_little_atonna/<str:price_type>/<str:action>/", create_paypal_order_little_atonna),
    
    path("capture_paypal_order_atonna/<int:restaurant_id>/", capture_paypal_order_atonna),
    path("capture_paypal_order_little_atonna/<str:restaurant_rut>/<str:user_email>/<str:action>/", capture_paypal_order_little_atonna),
    
    path(
        "load_payment_options/<int:country_id>/",
        load_payment_options,
    ),
    path(
        "pay/<int:restaurant_id>/",
        pay,
    ),
    path(
        "payment_period/<int:restaurant_id>/", payment_period,
    ),
    path(
        "service_period/<int:restaurant_id>/", service_period,
    ),
    # Delivery -------------------------------------------------------------------------
    
    path(
        "load_delivery_companies/<int:restaurant_id>/",
        load_delivery_companies,
    ),
    re_path(
        r'^restaurant_delivery_company/(?P<restaurant_delivery_company_id>-?\d+)/(?:(?P<delivery_selected_id>\d+)/)?$', 
        restaurant_delivery_company
    ),
    
    # Restaurant -------------------------------------------------------
    
    path("check_user_credentials/<str:restaurant_rut>/", check_user_credentials),
    # path("did_data_change/<int:restaurant_id>/", did_data_change),
    # path("set_data_changed/<int:restaurant_id>/", set_data_changed),
    path("update_restaurant_user_name_and_password/<int:user_id>/", update_restaurant_user_name_and_password),
    re_path(r"^get_restaurant_main_user_email/(?P<restaurant_id>-?\d+)/$", get_restaurant_main_user_email),
    re_path(r"^get_restaurant_main_user_data/(?P<restaurant_id>-?\d+)/$", get_restaurant_main_user_data),
    # path("get_restaurant_main_user_data/<int:restaurant_id>/", get_restaurant_main_user_data),
    path("restaurant_basic_data/", restaurant_basic_data),
    path("check_restaurant_existence/<int:pk>/", check_restaurant_existence),
    path("check_restaurant_rut_existence/<str:rut>/", check_restaurant_rut_existence),
    # def save_device_description(request, device_description):
    path("save_device_description/<str:device_description>/", save_device_description),
    # path("restaurant/<int:create>/", restaurant),
    re_path(r'^restaurant(?:/(?P<create>-?\d+))?/$', restaurant),
    
    # Category ----------------------------------------------------------------
    
    re_path(r'^category/(?P<category_id>-?\d+)(?:/(?P<private_view_order>\d+))?/$', category),
    
    # Dish -----------------------------------------------------------------------
    
    re_path(r'^dish/(?P<category_id>\d+)/(?P<dish_id>-?\d+)(?:/(?P<private_view_order>\d+))?/$', dish),
    
    # Promotion -------------------------------------------------------------------------
    
    re_path(r'^promotion/(?P<promotion_id>-?\d+)/$', promotion),
    
    # Login --------------------------------------------------------------------------------------
    
    # Logout ------------------------------------------------------------------------------------------

    path(
        "try_to_login_into_the_admin_area/<int:restaurant_id>/",
        try_to_login_into_the_admin_area,
    ),
    path(
        "login_normally/<int:restaurant_id>/", login_normally),
    path("login_no_further_actions/<int:restaurant_id>/", login_no_further_actions),

    path(
        "logout_from_admin_area/<int:restaurant_id>/",
        logout_from_admin_area,
    ),
    
    # start methods ----------------------------------------------------------------------------
    
    path(
        "start_menu_editing/<int:restaurant_id>/",  # it checks the restaurant's currently logged user id
        start_menu_editing,
    ),
    path(
        "start_restaurant_deliveries_editing/<int:restaurant_id>/",  # it checks the restaurant's currently logged user id
        start_restaurant_deliveries_editing,
    ),
    path(
        "start_preferences_editing/<int:restaurant_id>/",  # it checks the restaurant's currently logged user id
        start_preferences_editing,
    ),
    path(
        "start_reviews_editing/<int:restaurant_id>/",  # it checks the restaurant's currently logged user id
        start_reviews_editing,
    ),
    path(
        "start_menu_sort_editing/<int:restaurant_id>/",  # it checks the restaurant's currently logged user id
        start_menu_sort_editing,
    ),
    path(
        "start_promotions_editing/<int:restaurant_id>/",  # it checks the restaurant's currently logged user id
        start_promotions_editing,
    ),
    path("start_restaurant_users_editing/<int:restaurant_id>/", start_restaurant_users_editing),
    
    # order -----------------------------------------------------------------------------------
    
    path(
        "clear_all_private_view_orders/<int:restaurant_id>/",  # it checks the restaurant's currently logged user id
        clear_all_private_view_orders,
    ),
    path(
        "clear_categories_private_view_orders/<int:restaurant_id>/",  # it checks the restaurant's currently logged user id
        clear_categories_private_view_orders,
    ),
    path(
        "clear_category_dishes_private_view_orders/<int:category_id>/",  # it checks the restaurant's currently logged user id
        clear_category_dishes_private_view_orders,
    ),
    
    # Cancel editing -----------------------------------------------------------------------------
    
    path(
        "discard_menu_editing/<int:restaurant_id>/",
        discard_menu_editing,
    ),
    path(
        "discard_restaurant_deliveries_editing/<int:restaurant_id>/",
        discard_restaurant_deliveries_editing,
    ),
    path(
        "discard_preferences_editing/<int:restaurant_id>/",
        discard_preferences_editing,
    ),
    path(
        "discard_promotions_editing/<int:restaurant_id>/",
        discard_promotions_editing,
    ),
    path(
        "discard_menu_sort_editing/<int:restaurant_id>/",
        discard_menu_sort_editing,
    ),
    path(
        "discard_reviews_editing/<int:restaurant_id>/",
        discard_reviews_editing,
    ),
    path("discard_restaurant_users_editing/<int:restaurant_id>/", discard_restaurant_users_editing),
    
    # Publish editing ----------------------------------------------------------------------------
    
    path(
        "publish_restaurant_deliveries_editing/<int:restaurant_id>/",
        publish_restaurant_deliveries_editing,
    ),
    path(
        "publish_promotions_editing/<int:restaurant_id>/",
        publish_promotions_editing,
    ),
    path(
        "publish_menu_editing/<int:restaurant_id>/",
        publish_menu_editing,
    ),
    path(
        "publish_menu_sort_editing/<int:restaurant_id>/",
        publish_menu_sort_editing,
    ),
    path(
        "publish_preferences_editing/<int:restaurant_id>/",
        publish_preferences_editing,
    ),
    path(
        "publish_reviews_editing/<int:restaurant_id>/",
        publish_reviews_editing,
    ),
    path("publish_restaurant_users_editing/<int:restaurant_id>/", publish_restaurant_users_editing),
    
    # User ---------------------------------------------------------------------
    
    path(
        "load_restaurant_users/<int:restaurant_id>/",
        load_restaurant_users,
    ),
    path(
        "retrieve_restaurant_user_for_edition/<int:user_id>/",
        retrieve_restaurant_user_for_edition,
    ),
    re_path(r'^restaurant_user/(?P<restaurant_user_id>-?\d+)/$', restaurant_user),
  
    # Images -------------------------------------------------------------------
    
    path(
        "get_all_images/<int:restaurant_id>/",
        get_all_images,
    ),
    path(
        "update_image_uses/<int:restaurant_id>/",
        update_image_uses,
    ),
    path(
        "handle_loaded_images/<int:restaurant_id>/",
        handle_loaded_images,
    ),
    path(
        "add_image/<int:restaurant_id>/",
        add_image,
    ),
    path("image/<int:pk>/", image),
    
    # Random --------------------------------------------------------------------------
    
    path(
        "show_restaurant_number/<int:restaurant_id>/",
        show_restaurant_number,
    ),
       
    # qr ----------------------------------------------------------------------------------
    
    path(
        "handle_show_qr/<int:restaurant_id>/",
        handle_show_qr,
    ),
    
    # Reviews -------------------------------------------------------
    
    re_path(r'^review/(?P<element_id>\d+)/(?P<creating>(?:true|false))/(?P<review_type>(?:restaurant|dish))/$', review),
    path(
        "switch_review_rejection/<int:restaurant_id>/<int:review_id>/<str:rejection_reason_id_arg>/",
        switch_review_rejection,
    ),
    path(
        "all_reviews_with_rejections_if_any/<int:restaurant_id>/",
        all_reviews_with_rejections_if_any,
    ),
]