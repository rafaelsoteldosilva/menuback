from django.db import IntegrityError, migrations

from ..utils.Constants_and_strings import *

def load_data(apps, schema_editor):

    past_token = apps.get_model("api", "Past_Token")

    # generated with the help of WebDev/react-apps/react-generate-token
    past_token_data = {
        "token": '!asdV;3En:9EI|aDQQH;*7SxUf4ETcQ%?>Q|l#HF};a#[lHu>OGIW,P%$fHj>>Y&H3bdSZGdy%h|Y{Y?)Y=[71L}?}L`Uq9"#f"a/U%lGo~grG*Fv6<rB5QOwAuvZ)#ue)EYnvFDdWGf`.Z@j|4&r?a(%oecMDB?!U`L',
    }

    try:
        new_past_token = past_token.objects.create(**past_token_data)
    except Exception as e:
        print(f"error creating the past token {e}")
        raise e

    help_atonn = apps.get_model("api", "Help_Atonn")
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_support_request",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830609/HelpVideos/little_atonna_dialog_support_request_pxhjlo.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_select_payment_option",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830609/HelpVideos/little_atonna_select_payment_option_l0j5s3.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_initial_menu_load",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740835435/HelpVideos/little_atonna_dialog_initial_menu_load_sewbzf.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_new_restaurant",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830610/HelpVideos/little_atonna_dialog_new_restaurant_zfmhps.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_login",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830609/HelpVideos/little_atonna_dialog_login_ksri6n.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_forgot_my_credentials",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830609/HelpVideos/little_atonna_dialog_forgot_my_credentials_q9enfn.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_edit_restaurant_basic_data",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830608/HelpVideos/little_atonna_dialog_edit_restaurant_basic_data_iwledh.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_email_validation",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830608/HelpVideos/little_atonna_dialog_email_validation_ipviys.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_ask_for_a_country",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830608/HelpVideos/little_atonna_dialog_ask_for_a_country_ialyon.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "little_atonna_dialog_ask_for_restaurant_rut",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1740830608/HelpVideos/little_atonna_dialog_ask_for_restaurant_rut_rtmabs.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ---
    
    help_atonn_data = {
        "video_name": "public_categories",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163667/HelpVideos/public_categories_jbaibp.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    # ----
    
    help_atonn_data = {
        "video_name": "public_dialog_add_new_review_dish",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163667/HelpVideos/public_dialog_add_new_review_dish_g9sgua.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_dialog_add_new_review_home",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163667/HelpVideos/public_dialog_add_new_review_home_nardw9.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    

    help_atonn_data = {
        "video_name": "public_dialog_select_public_restaurant_delivery",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163667/HelpVideos/public_dialog_select_public_restaurant_delivery_t1kvel.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_dialog_whatsapp_share_dish",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163668/HelpVideos/public_dialog_whatsapp_share_dish_jfkhwo.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_dialog_whatsapp_share_home",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163667/HelpVideos/public_dialog_whatsapp_share_home_wu5j6v.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_home",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163668/HelpVideos/public_home_xwytog.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_item",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163668/HelpVideos/public_item_nlb5xt.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_items",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163669/HelpVideos/public_items_wq0uoz.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_showreview_dish",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163669/HelpVideos/public_showreview_dish_mxva4p.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_showreview_home",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163668/HelpVideos/public_showreview_home_ey69fy.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_showreviews_dish",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728166841/HelpVideos/public_showreviews_dish_moazpn.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_showreviews_home",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163669/HelpVideos/public_showreviews_home_j4rnc0.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_showpublicpromotions",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728505203/HelpVideos/public_showpublicpromotions_smfgve.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_showpublicpromotion",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728505203/HelpVideos/public_showpublicpromotion_xfcexj.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "public_dialog_management_login",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1737479501/HelpVideos/public_dialog_management_login_gmmr6r.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_showimagecollection",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335059/HelpVideos/private_image_collection_gkqbqu.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_helponhelp",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335059/HelpVideos/private_helponhelp_jbetsy.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
        
    help_atonn_data = {
        "video_name": "private_management",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335059/HelpVideos/private_management_wy3tdd.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_paymentstate",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335060/HelpVideos/private_paymentstate_qboytq.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_paypalonepayment",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335060/HelpVideos/private_paypalonepayment_wqbf9a.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_restaurant_number",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335060/HelpVideos/private_restaurant_number_tbkux3.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_showprivatepromotions",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335061/HelpVideos/private_showprivatepromotions_f4oi2k.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_showpreferences",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335061/HelpVideos/private_showpreferences_fqhi3q.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_showqr",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335061/HelpVideos/private_showqr_lhaavp.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_ShowRestaurantDeliveries",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335061/HelpVideos/private_ShowRestaurantDeliveries_san8au.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_categories",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733348339/HelpVideos/private_categories_hb8omb.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_dish",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335104/HelpVideos/private_dialog_dish_wfrbmn.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_category",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335104/HelpVideos/private_dialog_category_ycsxrw.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_restaurant_delivery",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335104/HelpVideos/private_dialog_restaurant_delivery_pxpuna.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_select_delivery_for_adding_a_new_restaurant_delivery",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335105/HelpVideos/private_dialog_select_delivery_for_adding_a_new_restaurant_delivery_ietjcl.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_promotion",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335105/HelpVideos/private_dialog_promotion_od9exl.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_select_file_source",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335105/HelpVideos/private_dialog_select_file_source_fktrko.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_restaurant_user",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335105/HelpVideos/private_dialog_restaurant_user_hirmph.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_preferences",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335105/HelpVideos/private_dialog_preferences_tagwxr.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_select_local_image_file",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335105/HelpVideos/private_dialog_select_local_image_file_vg7pqu.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_select_payment_option",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733335106/HelpVideos/private_dialog_select_payment_option_mjabfs.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_rejection_reason",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733926947/HelpVideos/private_dialog_rejection_reason_riiq34.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_dialog_image_name",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733927319/HelpVideos/private_dialog_image_name_oc3z0y.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_showusers",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733406181/HelpVideos/private_showusers_sjyfss.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_sorting",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733406182/HelpVideos/private_sorting_t2fjkr.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_showreviews",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733411630/HelpVideos/private_showreviews_wfaiik.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    help_atonn_data = {
        "video_name": "private_showreview",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1733411630/HelpVideos/private_showreview_mndzdp.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    global_price = apps.get_model("api", "Global_Price")

    global_price_data = {
        "minimum_price": 100000.00,
        "full_price": 125000.00,
        "initial_menu_load": 40000.00
    }

    try:
        my_global_price = global_price.objects.create(**global_price_data)
    except Exception as e:
        print(f"error creating Global price {e}")
        raise e
    
    country = apps.get_model("api", "Country")

    chile_data = {
        "name": "Chile",
        "alpha2_code": "CL",
        "flag_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1700851282/Chile_Flag_hahf0s.jpg",
        "locale": "es-CL",
        "timezone": "America/Santiago",
        "currency_symbol": "CLP",
        "minimum_fraction_digits": 0,
        "maximum_fraction_digits": 0,
        "exchange_rate": 1.0000,
        "document_type": "RUT"
    }

    try:
        chile = country.objects.create(**chile_data)
    except Exception as e:
        print(f"error creating the country {e}")
        raise e
    
    usa_data = {
        "name": "USA",
        "alpha2_code": "US",
        "flag_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1718743711/usa_gdabim.jpg",
        "locale": "en-US",
        "timezone": "America/Santiago",
        "currency_symbol": "USD",
        "minimum_fraction_digits": 2,
        "maximum_fraction_digits": 2,
        "exchange_rate": 1.0000,
        "document_type": "TIN"
    }

    try:
        usa = country.objects.create(**usa_data)
    except Exception as e:
        print(f"error creating the country {e}")
        raise e

    argentina_data = {
        "name": "Argentina",
        "alpha2_code": "AR",
        "flag_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703877212/Argentina_mdii3e.jpg",
        "locale": "es-AR",
        "timezone": "America/Santiago",
        "currency_symbol": "ARS",
        "minimum_fraction_digits": 2,
        "maximum_fraction_digits": 2,
        "exchange_rate": 1.0000,
        "document_type": "CUIT"
    }

    try:
        argentina = country.objects.create(**argentina_data)
    except Exception as e:
        print(f"error creating the country {e}")
        raise e

    Rejection_Reason = apps.get_model("api", "Rejection_Reason")

    rejection_reason_data = {
        "reason": "Contenido Inapropiado",
        "explanation": "Los comentarios que contengan lenguaje ofensivo, discursos de odio o contenido explícito, tales como contenido sexualmente explícito, contenido de violencia, etc., deben ser rechazados para mantener un ambiente respetuoso y acogedor para todos los usuarios",
    }

    try:
        inappropriate_content = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating inapropriate content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Contenido Irrelevante",
        "explanation": "Los comentarios que no estén relacionados con el plato o la experiencia gastronómica, como el spam o anuncios no relacionados, deben ser rechazados",
    }

    try:
        irrelevant_content = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Información Engañosa",
        "explanation": "Los comentarios que contengan información engañosa sobre el plato o el restaurante deben ser rechazados para mantener la integridad de la plataforma",
    }

    try:
        false_information = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Ataque Personal",
        "explanation": "Los comentarios que ataquen personalmente o acosen a otros usuarios, al personal del restaurante o a individuos asociados con el restaurante deben ser rechazados para prevenir conflictos y mantener un ambiente positivo",
    }

    try:
        personal_attacks = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Contenido Promocional",
        "explanation": "Los comentarios que sean excesivamente promocionales o sesgados, como los publicados por el personal del restaurante o afiliados sin revelación, deben ser rechazados para garantizar la imparcialidad y autenticidad",
    }

    try:
        promotional_content = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Incoherente o Incomprensible",
        "explanation": "Los comentarios que sean difíciles de entender o carezcan de coherencia pueden ser rechazados ya que no contribuyen significativamente a la discusión",
    }

    try:
        incoherent_or_incomprehensible = Rejection_Reason.objects.create(
            **rejection_reason_data
        )
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Violación de la Privacidad",
        "explanation": "Los comentarios que divulguen información personal sobre individuos sin su consentimiento, como el personal del restaurante u otros clientes, deben ser rechazados para proteger la privacidad",
    }

    try:
        vialoates_privacy = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Spam o Generado por Bots",
        "explanation": "Los comentarios generados por bots o sistemas automatizados con el propósito de hacer spam o manipular calificaciones deben ser rechazados para mantener la calidad del contenido generado por los usuarios",
    }

    try:
        spam_or_bot_data = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Reseña Deshonesta",
        "explanation": "Los comentarios que parezcan deshonestos o fabricados con el propósito de promocionar o desprestigiar al restaurante deben ser rechazados para garantizar la autenticidad de las reseñas de los usuarios",
    }

    try:
        dishonest_reviews = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    rejection_reason_data = {
        "reason": "Solicitud del Usuario",
        "explanation": "Por solicitud del mismo usuario",
    }

    try:
        diner_request = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e
    
    rejection_reason_data = {
        "reason": SPECIAL_NOTE,
        "explanation": "Se pueden crear revisiones positivas y negativas, con la condición de que no caigan entre las razones dadas. También se pueden escribir quejas sobre alguna característica del restaurant o sobre el mal trato del personal del restaurante",
    }

    try:
        special_note = Rejection_Reason.objects.create(**rejection_reason_data)
    except Exception as e:
        print(f"error creating irrelevant content reason {e}")
        raise e

    payment_option = apps.get_model("api", "Payment_Option")

    paypal_data = {
        "name": "PayPal",
        "payment_option_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1718399015/Paypal_omsat2.jpg",
        "country": chile,
    }

    try:
        paypal = payment_option.objects.create(**paypal_data)
    except Exception as e:
        print(f"error creating the payment option {e}")
        raise e

    webPay_data = {
        "name": "WebPay",
        "payment_option_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1718465159/WebPay_uavfzs.jpg",
        "country": chile,
    }

    try:
        webPay = payment_option.objects.create(**webPay_data)
    except Exception as e:
        print(f"error creating the payment option {e}")
        raise e

    delivery_company = apps.get_model("api", "Delivery_Company")

    uber_eats_data = {
        "name": "Uber Eats",
        "company_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703854967/Uber_eats_msaqsi.jpg",
        "url_template": "https://www.ubereats.com/cl/store/<**TokeN**>?diningMode=DELIVERY",
        "country": chile,
    }

    try:
        uber_eats_company = delivery_company.objects.create(**uber_eats_data)
    except Exception as e:
        print(f"error creating the delivery company {e}")
        raise e

    rappi_data = {
        "name": "Rappi",
        "company_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703854967/Rappi_vefh3f.jpg",
        "url_template": "https://www.rappi.cl/restaurantes/<**TokeN**>",
        "country": chile,
    }

    try:
        rappi_company = delivery_company.objects.create(**rappi_data)
    except Exception as e:
        print(f"error creating the delivery company {e}")
        raise e

    pedidosya_data = {
        "name": "Pedidos Ya",
        "company_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703854967/Pedidos_Ya_xsewwq.jpg",
        "url_template": "https://www.pedidosya.cl/restaurantes/santiago/<**TokeN**>?origin=shop_list",
        "country": chile,
    }

    try:
        pedidosya_company = delivery_company.objects.create(**pedidosya_data)
    except Exception as e:
        print(f"error creating the delivery company {e}")
        raise e

    propio_data = {
        "name": f"{OWN_DELIVERY}",
        "company_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703854967/Propio_jxt8ea.jpg",
        "url_template": "https://<**TokeN**>",
        "country": chile,
    }

    try:
        propio_company = delivery_company.objects.create(**propio_data)
    except Exception as e:
        print(f"error creating the delivery company {e}")
        raise e

    super_user = apps.get_model("api", "Super_User")

    super_user_data = {
        "name": "_____ Rafael Y Elsy _____",
        "password": "Chile.17",
    }

    try:
        atonn_user = super_user.objects.create(**super_user_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
