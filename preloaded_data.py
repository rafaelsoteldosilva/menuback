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

    help_atonn_data = {
        "video_name": "public_categories",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1728163667/HelpVideos/public_categories_jbaibp.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
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
    
    help_atonn_data = {
        "video_name": "dialog_edit_basic_data",
        "video_url": "https://res.cloudinary.com/dtrd4b7uc/video/upload/v1739450897/HelpVideos/little_atonna_dialog_edit_basic_data_kjjsd8.mp4",
    }

    try:
        new_help_atonn = help_atonn.objects.create(**help_atonn_data)
    except Exception as e:
        print(f"error creating help {e}")
        raise e
    
    global_price = apps.get_model("api", "Global_Price")

    global_price_data = {
        "minimum_price": 70.00,
        "full_price": 100.00
    }

    try:
        my_global_price = global_price.objects.create(**global_price_data)
    except Exception as e:
        print(f"error creating Global price {e}")
        raise e
    
    country = apps.get_model("api", "Country")

    usa_data = {
        "name": "USA",
        "alpha2_code": "US",
        "flag_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1718743711/Shared_Images/usa_gdabim.jpg",
        "locale": "es-CL",
        "currency_symbol": "USD ",
        "minimum_fraction_digits": 2,
        "maximum_fraction_digits": 2,
        "exchange_rate": 1,
        "document_type": "EIN"
    }

    try:
        usa = country.objects.create(**usa_data)
    except Exception as e:
        print(f"error creating the country {e}")
        raise e

    chile_data = {
        "name": "Chile",
        "alpha2_code": "CL",
        "flag_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1700851282/Shared_Images/Chile_Flag_hahf0s.jpg",
        "locale": "es-CL",
        "currency_symbol": "CLP ",
        "minimum_fraction_digits": 0,
        "maximum_fraction_digits": 0,
        "exchange_rate": 900.0000,
        "document_type": "RUT"
    }

    try:
        chile = country.objects.create(**chile_data)
    except Exception as e:
        print(f"error creating the country {e}")
        raise e

    argentina_data = {
        "name": "Argentina",
        "alpha2_code": "AR",
        "flag_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703877212/Shared_Images/Argentina_mdii3e.jpg",
        "locale": "es-AR",
        "currency_symbol": "ARS ",
        "minimum_fraction_digits": 2,
        "maximum_fraction_digits": 2,
        "exchange_rate": 980.0000,
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
        "payment_option_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1718399015/Shared_Images/Paypal_omsat2.jpg",
        "country": chile,
    }

    try:
        paypal = payment_option.objects.create(**paypal_data)
    except Exception as e:
        print(f"error creating the payment option {e}")
        raise e

    webPay_data = {
        "name": "WebPay",
        "payment_option_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1718465159/Shared_Images/WebPay_uavfzs.jpg",
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
        "company_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703854967/Shared_Images/Uber_eats_msaqsi.jpg",
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
        "company_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703854967/Shared_Images/Rappi_vefh3f.jpg",
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
        "company_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703854967/Shared_Images/Pedidos_Ya_xsewwq.jpg",
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
        "company_image_url": "https://res.cloudinary.com/dtrd4b7uc/image/upload/v1703854967/Shared_Images/Propio_jxt8ea.jpg",
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

    restaurant = apps.get_model("api", "Restaurant")

    restaurant_data = {
        "rut": "53.322.839-9",
        "public_name": "El Restaurant",
        "public_description": "En este restaurant servimos las mejores comidas que puedas encontrar",
        "public_address": "Fray Camilo Henríquez 686. Apto 1401. Santiago de Chile",
        "public_country": chile,
        "public_phone": "+56975703826",
        "public_website_url": "www.elrestaurant.cl/",
        "public_instagram_url": "www.instagram.com/elrestaurant/",
        "public_facebook_url": "www.facebook.com/elrestaurant",
        "public_twitter_url": "twitter.com/elrestaurant",
        
        # positive values: Number of minutes from midnight
        # negative values: Number of minutes before midnight
        
        "public_monday_open_hour_in_minutes": 570,
        "public_tuesday_open_hour_in_minutes": 570,
        "public_wednesday_open_hour_in_minutes": 570,
        "public_thursday_open_hour_in_minutes": 570,
        "public_friday_open_hour_in_minutes": 660,
        "public_saturday_open_hour_in_minutes": 660,
        "public_sunday_open_hour_in_minutes": 660,
        #
        "public_monday_close_hour_in_minutes": -120,
        "public_tuesday_close_hour_in_minutes": -120,
        "public_wednesday_close_hour_in_minutes": -120,
        "public_thursday_close_hour_in_minutes": -120,
        "public_friday_close_hour_in_minutes": -120,
        "public_saturday_close_hour_in_minutes": -120,
        "public_sunday_close_hour_in_minutes": -120,
        "price_type": "Full Price",
    }
    try:
        restaurant_il_romano_pizza = restaurant.objects.create(**restaurant_data)
    except Exception as e:
        print(f"error creating the first restaurant {e}")
        raise e

    restaurant_delivery_company = apps.get_model("api", "Restaurant_Delivery_Company")

    restaurant_delivery_company_data = {
        "public_token": "il-romano-pizza/XKySqjlbTmij6oTWSFWQ3w",
        "delivery_company": uber_eats_company,
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        uber_eats_restaurant_delivery_company = (
            restaurant_delivery_company.objects.create(
                **restaurant_delivery_company_data
            )
        )
    except Exception as e:
        print(f"error creating the restaurant delivery company {e}")
        raise e

    restaurant_delivery_company_data = {
        "public_token": "www.google.com",
        "delivery_company": propio_company,
        "restaurant": restaurant_il_romano_pizza,
    }
    try:
        restaurant_delivery_company.objects.create(**restaurant_delivery_company_data)
    except Exception as e:
        print(f"error creating the restaurant delivery company {e}")
        raise e

    restaurant_user = apps.get_model("api", "Restaurant_User")

    user_data = {
        "public_name": "Rafael",
        # "gAAAAABmkTV4y8NR-Pmy_FsBOzEecCpJOvG9akb7xQOeo04pC_MVe9TGevZ7OIs43kI4prB1CtylFtrZHp0Gplya2I9KCHQtPA=="
        # is Chile.17 encrypted with the key FIXED_KEY = os.getenv("PASSWORDS_ENCRYPTION_KEY")
        "public_password": "gAAAAABmkTV4y8NR-Pmy_FsBOzEecCpJOvG9akb7xQOeo04pC_MVe9TGevZ7OIs43kI4prB1CtylFtrZHp0Gplya2I9KCHQtPA==",
        "public_email": "rafael.soteldo@gmail.com",
        "public_email_validated": True,
        # "public_phone_validated": True,
        "recently_created": False,
        "main_user": True,
        "restaurant": restaurant_il_romano_pizza,
    }
    try:
        rafael_user = restaurant_user.objects.create(**user_data)
        # rafael_user.save()
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    user_data = {
        "public_name": "Other",
        # "gAAAAABmkTV4y8NR-Pmy_FsBOzEecCpJOvG9akb7xQOeo04pC_MVe9TGevZ7OIs43kI4prB1CtylFtrZHp0Gplya2I9KCHQtPA=="
        # is Chile.17 encrypted with the key FIXED_KEY = os.getenv("PASSWORDS_ENCRYPTION_KEY")
        "public_password": "gAAAAABmkTV4y8NR-Pmy_FsBOzEecCpJOvG9akb7xQOeo04pC_MVe9TGevZ7OIs43kI4prB1CtylFtrZHp0Gplya2I9KCHQtPA==",
        "public_email": "other@gmail.com",
        "public_email_validated": False,
        "main_user": False,
        "recently_created": False,
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        other_user = restaurant_user.objects.create(**user_data)
        # other_user.save()
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    restaurant_il_romano_pizza.main_user_id = rafael_user.id
    restaurant_il_romano_pizza.save()

    review = apps.get_model("api", "Review")

    restaurant_review_data = {
        "diner_name": "Daniel",
        "creation_date": "2022-12-14T13:45:10.612602Z",
        "number_of_stars": 5,
        "review_comment": "Me gustó mucho este restaurant Pizzería Da Bruno",
        "public_rejected": False,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": restaurant_il_romano_pizza.public_name,
        "dish": None,
    }

    try:
        restaurant_review = review.objects.create(**restaurant_review_data)
    except Exception as e:
        print(f"Error creating Restaurant review {e}")
        raise e

    restaurant_data = {
        "rut": "26.445.363-1",
        "public_name": "Otro Restaurant",
        "public_address": "en otra parte",
        "public_country": chile,
        "public_phone": "+56975736349",
        "public_website_url": "https://otrorestaurant.com",
        "public_monday_open_hour_in_minutes": 570,
        "public_tuesday_open_hour_in_minutes": 570,
        "public_wednesday_open_hour_in_minutes": 570,
        "public_thursday_open_hour_in_minutes": 570,
        "public_friday_open_hour_in_minutes": 660,
        "public_saturday_open_hour_in_minutes": 660,
        "public_sunday_open_hour_in_minutes": 660,
        #
        "public_monday_close_hour_in_minutes": -120,
        "public_tuesday_close_hour_in_minutes": -120,
        "public_wednesday_close_hour_in_minutes": -120,
        "public_thursday_close_hour_in_minutes": -120,
        "public_friday_close_hour_in_minutes": 150,
        "public_saturday_close_hour_in_minutes": 150,
        "public_sunday_close_hour_in_minutes": -360,
        "price_type": "Full Price",
        "next_price_type": "Full Price"
    }
    try:
        otro_restaurant = restaurant.objects.create(**restaurant_data)
    except Exception as e:
        print(f"Error creating Restaurant the other restaurant {e}")
        raise e

    restaurant_user_data = {
        "public_name": "Elsy",
        # "public_password": "Chile.17",
        # "public_phone": "+56975736349",
        "public_email": "elsy@gmail.com",
        "public_email_validated": True,
        "recently_created": False,
        "main_user": True,
        "restaurant": otro_restaurant,
    }

    try:
        elsy_user = restaurant_user.objects.create(**restaurant_user_data)
        # elsy_user.save()
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    otro_restaurant.main_user_id = elsy_user.id
    otro_restaurant.save()

    promotion = apps.get_model("api", "Promotion")

    promotion_data = {
        "public_name": "Viernes de Damas",
        "public_attractor_text": "Cervezas Gratis",
        "public_promotion_text": '<p>👩&nbsp;<span style="color: orange;">Viernes Femenino</span>&nbsp;👩:</p><p>Sólo por estos días tenemos el&nbsp;<strong>viernes femenino</strong>, a partir de las 18 horas de ese viernes, con&nbsp;la compra de&nbsp;uno de&nbsp;<em>nuestros&nbsp;</em><span style="background-color: black;">platos</span></p><p>Tendrás:</p><ol><li><span style="color: blue;">Dos&nbsp;Cervezas&nbsp;</span>gratis 🍻</li><li>Mucho amor ❤️❤️❤️</li></ol><p><br></p>',
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        promotion_viernes = promotion.objects.create(**promotion_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    promotion_data = {
        "public_name": "Sábado de Caballeros",
        "public_attractor_text": "Cervezas Gratis",
        "public_promotion_text": '<p>🧑&nbsp;<span style="color: orange;">Sábado Masculino</span>🧑:</p><p><br></p><p>Sólo por estos días tenemos el <span style="color: blue;">Sábado Masculino</span>, a partir de las 18 horas de ese sábado, con la compra uno de nuestros platos</p><p>Tendrás:</p><ul><li><u>2 Cervezas</u> gratis 🍻</li></ul><p><br></p>',
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        promotion_sabados = promotion.objects.create(**promotion_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    category = apps.get_model("api", "Category")

    category_data = {
        "public_name": "Pizzas",
        "public_description": "Estas son las ricas Pizzas",
        "recently_created": False,
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        pizzas_category = category.objects.create(**category_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    category_data = {
        "public_name": "Licores",
        "public_description": "Estos son los ricos Licores",
        "recently_created": False,
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        licores_category = category.objects.create(**category_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    category_data = {
        "public_name": "Carnes",
        "public_description": "Estas son las ricas carnes",
        "recently_created": False,
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        carnes_category = category.objects.create(**category_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    # category_data = {
    #     "public_name": "Pizzas",
    #     "public_description": "Estas son las Pizzas del otro restaurant",
    #     "recently_created": False,
    #     "restaurant": otro_restaurant,
    # }

    # try:
    #     pizzas_del_otro_restaurant_category = category.objects.create(**category_data)
    # except Exception as e:
    #     raise Exception(f"Error creating object: {e}")

    dish = apps.get_model("api", "Dish")

    dish_data = {
        "public_name": "Pizza Picante",
        "public_description": "Esta es la deliciosa Pizza Picante",
        "recently_created": False,
        "public_price": "8500",
        "category": pizzas_category,
    }

    try:
        pizza_picante_created_dish = dish.objects.create(**dish_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    dish_data = {
        "public_name": "Pizza Vegetariana",
        "public_description": "Esta es la deliciosa Pizza Vegetariana",
        "recently_created": False,
        "public_price": "5500",
        "category": pizzas_category,
    }

    try:
        pizza_vegetariana_created_dish = dish.objects.create(**dish_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    dish_data = {
        "public_name": "Pizza Margarita",
        "public_description": "Esta es la deliciosa Pizza Margarita",
        "recently_created": False,
        "public_price": "4500",
        "category": pizzas_category,
    }

    try:
        pizza_margarita_created_dish = dish.objects.create(**dish_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    # dish_data = {
    #     "public_name": "Black & White",
    #     "public_description": "Este es el delicioso Black & White",
    #     "recently_created": False,
    #     "public_price": "12500",
    #     "category": licores_category,
    # }

    # try:
    #     black_and_white_created_dish = dish.objects.create(**dish_data)
    # except Exception as e:
    #     raise Exception(f"Error creating object: {e}")

    dish_data = {
        "public_name": "Lomito Encebollado",
        "public_description": "Este es el delicioso Lomito Encebollado",
        "recently_created": False,
        "public_price": "19000",
        "category": carnes_category,
    }

    try:
        lomito_encebollado_created_dish = dish.objects.create(**dish_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    review = apps.get_model("api", "Review")

    dish_review_data = {
        "diner_name": "Esteban",
        "number_of_stars": 5,
        "review_comment": "Esta pizza margarita es muy buena",
        "parent_type": "dish",
        "dish": pizza_margarita_created_dish,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": pizza_margarita_created_dish.public_name,
    }
    try:
        dish_review = review.objects.create(**dish_review_data)
    except Exception as e:
        print(f"Error creating Dish review {e}")
        raise e

    # dish_review_data = {
    #     "diner_name": "juán",
    #     "number_of_stars": 5,
    #     "review_comment": "Este blacw&white es muy bueno",
    #     "parent_type": "dish",
    #     "dish": black_and_white_created_dish,
    #     "restaurant": restaurant_il_romano_pizza,
    #     "parent_name": black_and_white_created_dish.public_name,
    # }
    # try:
    #     dish_review = review.objects.create(**dish_review_data)
    # except Exception as e:
    #     print(f"Error creating Dish review {e}")
    #     raise e

    dish_review_data = {
        "diner_name": "Gloria",
        "number_of_stars": 3,
        "review_comment": "Me gustó esta Pizza Picante, es demasiado buena, me encantó, además de que una de las más sabrosas que he probado",
        "parent_type": "dish",
        "dish": pizza_picante_created_dish,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": pizza_picante_created_dish.public_name,
    }
    try:
        dish_review = review.objects.create(**dish_review_data)
    except Exception as e:
        print(f"Error creating Dish review {e}")
        raise e

    dish_review_data = {
        "diner_name": "Pierre",
        "number_of_stars": 2,
        "review_comment": "Me gustó esta Pizza Picante",
        "parent_type": "dish",
        "dish": pizza_picante_created_dish,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": pizza_picante_created_dish.public_name,
    }
    try:
        dish_review = review.objects.create(**dish_review_data)
    except Exception as e:
        print(f"Error creating Dish review {e}")
        raise e

    dish_review_data = {
        "diner_name": "Carlos",
        "number_of_stars": 5,
        "review_comment": "Me gustó mucho la pizza picante. La recomiendo",
        "parent_type": "dish",
        "dish": pizza_picante_created_dish,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": pizza_picante_created_dish.public_name,
    }
    try:
        dish_review = review.objects.create(**dish_review_data)
    except Exception as e:
        print(f"Error creating Dish review {e}")
        raise e

    dish_review_data = {
        "diner_name": "José",
        "number_of_stars": 2,
        "review_comment": "Me voy a llevar otra pizza margarita, Me gustó mucho",
        "parent_type": "dish",
        "dish": pizza_margarita_created_dish,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": pizza_margarita_created_dish.public_name,
    }
    try:
        dish_review = review.objects.create(**dish_review_data)
    except Exception as e:
        print(f"Error creating Dish review {e}")
        raise e

    dish_review_data = {
        "diner_name": "Petra",
        "number_of_stars": 2,
        "review_comment": "Pídanla esta pízza vegetariana. Es muy buena",
        "parent_type": "dish",
        "dish": pizza_vegetariana_created_dish,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": pizza_vegetariana_created_dish.public_name,
    }
    try:
        dish_review = review.objects.create(**dish_review_data)
    except Exception as e:
        print(f"Error creating Dish review {e}")
        raise e

    dish_review_data = {
        "diner_name": "William",
        "number_of_stars": 2,
        "review_comment": "La mejor pizza picante que me he comido hasta ahora",
        "parent_type": "dish",
        "dish": pizza_picante_created_dish,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": pizza_picante_created_dish.public_name,
    }
    try:
        dish_review = review.objects.create(**dish_review_data)
    except Exception as e:
        print(f"Error creating Dish review {e}")
        raise e

    # dish_data = {
    #     "public_name": "Pizza Picante del otro restaurant",
    #     "public_description": "Esta es la deliciosa Pizza Picante del otro restaurant, que cuesta 8.500",
    #     "recently_created": False,
    #     "public_price": "8500",
    #     "category": pizzas_del_otro_restaurant_category,
    # }

    # try:
    #     dish.objects.create(**dish_data)
    # except Exception as e:
    #     raise Exception(f"Error creating object: {e}")

    dish_data = {
        "public_name": "Pizza con Chorizo",
        "public_description": "Esta es la deliciosa Pizza con Chorizo",
        "recently_created": False,
        "public_price": "7500",
        "category": pizzas_category,
    }

    try:
        created_dish = dish.objects.create(**dish_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    dish_data = {
        "public_name": "Pizza con Jamón",
        "public_description": "Esta es la deliciosa Pizza con jamón",
        "recently_created": False,
        "public_price": "8000",
        "category": pizzas_category,
    }

    try:
        pizza_con_jamón_created_dish = dish.objects.create(**dish_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    dish_review_data = {
        "diner_name": "el secuestrador",
        "number_of_stars": 4,
        "review_comment": "Demasiado rica la pizza con jamón",
        "parent_type": "dish",
        "dish": pizza_con_jamón_created_dish,
        "restaurant": restaurant_il_romano_pizza,
        "parent_name": pizza_con_jamón_created_dish.public_name,
    }
    try:
        dish_review = review.objects.create(**dish_review_data)
    except Exception as e:
        print(f"Error creating Dish review {e}")
        raise e

    category_data = {
        "public_name": "Bebidas",
        "public_description": "Estas son las ricas Bebidas",
        "recently_created": False,
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        bebidas_category = category.objects.create(**category_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    dish_data = {
        "public_name": "Limonada",
        "public_description": "Esta es la fabulosa Limonada",
        "recently_created": False,
        "public_price": "2000",
        "category": bebidas_category,
    }

    try:
        limonada_created_dish = dish.objects.create(**dish_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    category_data = {
        "public_name": "Postres",
        "public_description": "Estos son los ricos Postres",
        "recently_created": False,
        "restaurant": restaurant_il_romano_pizza,
    }

    try:
        postres_category = category.objects.create(**category_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")

    dish_data = {
        "public_name": "Pie de Maracuyá",
        "public_description": "Fabuloso Pie de Maracuyá",
        "recently_created": False,
        "public_price": "2500",
        "category": postres_category,
    }

    try:
        pie_de_maracuyá_created_dish = dish.objects.create(**dish_data)
    except Exception as e:
        raise Exception(f"Error creating object: {e}")


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
