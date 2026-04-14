from datetime import timedelta

# Contsnts and strings

# -------------- Numbers --------------------

RIGHT_VALUE = 1
WRONG_VALUE = -1

PRICE_CHOICES_MAX_LENGTH=20
DOCUMENT_TYPE_CHOICES_MAX_LENGTH=20
PAYMENT_STATE_MAX_LENGTH=50
DEVICE_DESCRIPTION_LENGTH = 300
NAMES_MAX_LENGTH = 80
DOCUMENT_TYPE_MAX_LENGTH = 10
RUT_MAX_LENGTH = 30
TOKEN_MAX_LENGTH = 200
ALPHA2_CODE_MAX_LENGTH = 2
LOCALE_IDENTIFIER_MAX_LENGTH = 5
DESCRIPTIONS_MAX_LENGTH = 500
URLS_MAX_LENGTH = 254
DELIVERY_TOKEN_MAX_LENGTH = 100
PROMOTIONS_TEXT_MAX_LENGTH = 700
EMAILS_MAX_LENGTH = 254
PHONES_MAX_LENGTH = 25
INSTAGRAM_URL_MAX_LENGTH = 80
FACEBOOK_URL_MAX_LENGTH = 80
TWITTER_URL_MAX_LENGTH = 80
ADDRESSES_MAX_LENGTH = 250
DATESTR_MAX_LENGTH = 20
PASSWORDS_MAX_LENGTH = 30
ENCRYPTED_PASSWORDS_MAX_LENGTH = 512
PRICES_MAX_LENGTH = 30
COMMENT_MAX_LENGTH = 500
HELP_VIEW_NAME_MAX_LENGTH = 80
HTML_CODES_MAX_LENGTH = 500
CLOUDINARY_PUBLIC_ID_MAX_LENGTH = 100
CLOUDINARY_RESOURCE_TYPE_MAX_LENGTH = 100
DELIVERY_STRING_MAX_LENGTH = 100
MAX_NUMBER_OF_USERS = 2
MAX_NUMBER_OF_DELIVERY_COMPANIES = 10
CURRENCY_SYMBOL_MAX_LENGTH = 6
VERIFICATION_KEY_LENGTH = 4
TOKEN_EXPIRATION_DAYS = timedelta(days=1)  # Token expires after 1 days
SERVICE_PERIOD_LENGTH_IN_DAYS=30
GRACE_PERIOD_LENGTH_IN_DAYS=28
LOCAL_DJANGO_HOURS_FIX=4

NUMBER_OF_DAYS_OK_TO_PAY=15

# ---------------------- Do not translate -----------------------

PROVISIONAL_VALUE = "**!***!Provisional!**!***"

RESTAURANT_BLOCKED_DUE_TO_PAYMENT = "blocked_due_to_payment"
RESTAURANT_NOT_BLOCKED_DUE_TO_PAYMENT = "not_blocked_due_to_payment"

# ---------------------- End Do not translate -----------------------

# -------------- Strings --------------------
SPECIAL_NOTE = "Nota Especial"

RESTAURANT_ALREADY_EXISTS= "Ya existe un restaurant con ese mismo documento"
RESTAURANT_ID_DOES_NOT_MATCH = "los identificadores del restaurant no coindiden"
PAYMENT_RECEIVED_OK = "El pago fue recibido correctamente"
RESTAURANT_DOES_NOT_EXIST = "El restaurante no existe"
BUY_ORDER_SESSION_ID_DOES_NOT_EXIST = "La tabla de orden de compra no existe"
GLOBAL_PRICE_DOES_NOT_EXIST = "Global Price no existe"
COUNTRY_DOES_NOT_EXIST = "Country no existe"
PRICE_TYPE_IS_NOT_FULL_PRICE_NOR_MINIMUM_PRICE='Price type is not full nor minimum'
FULL_PRICE_TYPE = 'Full Price'
MINIMUM_PRICE_TYPE = 'Minimum Price'
PAYMENT_REQUIRED = "Se requiere el pago"
COUNTRY_DOES_NOT_EXIST = "El país no existe"
IMAGE_DELETED = "La imagen fué eliminada"
IMAGE_NOT_FOUND = "Imagen no encontrada"
USER_CAN_NOT_PERFORM_FURTHER_ACTIONS = "Se le recomienda hacer logout y luego login"
KEYS_DO_NOT_MATCH = "La claves dadas no coinciden"
INVALID_BOOL_VALUE = "Valor inválido para user_forced_in. Debe ser 'true' o 'false'."
USER_CAN_NOT_GO_ON = "El usuario no puede continuar"
IMAGE_USES_ARE_UP_TO_DATE_WITH_ALL_IMAGES_USED = (
    "Los usos de imágenes fueron actualizados"
)
PRIVATE_NAME_IS_NECESSARY = "Se necesita el private_name"
PRIVATE_PHONE_IS_NECESSARY = "Se necesita el private_phone"
PRIVATE_DESCRIPTION_IS_NECESSARY = "Se necesita el private_description"
PRIVATE_ATTRACTOR_TEXT_IS_NECESSARY = "Se necesita el private_attractor_text"
PRIVATE_PROMOTION_TEXT_IS_NECESSARY = "Se necesita el private_promotion_text"
PRIVATE_PASSWORD_IS_NECESSARY = "Se necesita el private_password"
PRIVATE_EMAIL_IS_NECESSARY = "Se necesita el private_password"
PRIVATE_PRICE_IS_NECESSARY = "Se necesita el private_price"
PRIVATE_IMAGE_ID_IS_NECESSARY = "Se necesita el private_image_id"
RESTAURANT_CREATED = "El restaurant fué creado"
RESTAURANT_UPDATED = "El restaurant fué actualizado"
RESTAURANT_DELETED = "El restaurant fué eliminado"
USERS_NUMBER_IS_AT_THE_MAXIMUM = "Máximo número de usuarios ya fué alcanzado"
DELIVERY_COMPANIES_NUMBER_IS_AT_THE_MAXIMUM = (
    "Número máximo de compañías de delivery ya fué alcanzado"
)
START_EDITING_FIRST = "Debe comenzar a editar primero"
START_EDITING_MENU_FIRST = "Debe comenzar a editar el menú primero"
START_EDITING_PREFERENCES_FIRST = "Debe comenzar a editar las preferencias primero"
START_EDITING_USERS_FIRST = "Debe comenzar a editar usuarios primero"
START_EDITING_PROMOTIONS_FIRST = "You have to start editing promotions first"
USER_DOES_NOT_EXIST = "El usuario no existe"
MAIN_USER_DOES_NOT_EXIST = "El usuario principal no existe"
USER_DOES_EXIST = "El usuario si existe"
CREDENTIALS_ARE_OK = "Las credenciales son correctas"
CREDENTIALS_ARE_WRONG = "Las credenciales son incorrectas"
USER_CREATED = "El usuario fué creado"
USER_UPDATED = "El usuario fué actualizado"
USER_DELETED = "El usuario fué eliminado"
USER_MARKED_UNMARKED_FOR_DELETION = (
    "El usario fué marcado/desmarcado para su eliminación"
)
CATEGORY_DOES_NOT_EXIST = "La categoría no existe"
CATEGORY_CREATED = "La categroría fué creada"
CATEGORY_UPDATED = "La categoría fué actualizada"
CATEGORY_DELETED = "La categoría fué eliminada"
CATEGORY_MARKED_UNMARKED_FOR_DELETION = (
    "La categoría fué marcada/desmarcada para su eliminación"
)
VIEW_ORDER_CAN_NOT_BE_ZERO_NOR_LESS = "orden de vista no puede ser cero o menor"
CATEGORY_VIEW_ORDER_HAS_BEEN_SET = "El orden de vista de las categorías fué establecido"
START_SORTING_FIRST = "Debe comenzar a ordenar primero"
DISH_DOES_NOT_EXIST = "The dish does not exist"
DISH_CREATED = "La item/plato fué creado"
DISH_UPDATED = "La item/plato fué actualizado"
DISH_DELETED = "La item/plato fué eliminado"
DISH_VIEW_ORDER_HAS_BEEN_SET = "El orden de vista de los items/platos fué establecido"
BAD_CREDENTIALS = "Las credenciales dadas no coinciden con las correctas"
YOU_ARE_LOGGED_INTO_ADMIN_AREA = "Usted entró al área de administación"
LOGOUT_AND_LOGIN_AGAIN = "Usted había entrado desde otro dispositivo, por favor haga 'logout' y 'login' otra vez"
EDITION_IS_ALREADY_BEING_MADE_BY = "El menú se encuentra en edición por: "
YOU_MAY_START_EDITING_PREFERENCES = "Puede comenzar a editar las preferencias"
YOU_HAVE_TO_LOGIN_FIRST = "Debe hacer login primero"
YOU_MAY_START_EDITING_REVIEWS = "Puede comenzar a editar las revisiones"
NO_MENU_TO_EDIT = "No hay menu todavía"
YOU_MAY_START_SORTING = "Puede comenzar a establecer el orden"
YOU_MAY_START_EDITING = "Puede comenzar a editar"
ERROR_OCURRED_WITH_UPDATES_OR_FILTER = "ocurrió un error con los updates o filter"
CURRENT_LOGGED_IN_USER_WAS_LOGGED_OUT = (
    "El usuario actual a salido del área administrativa"
)
NO_USER_TO_LOGOUT = "No hay usuario dentro"
YOU_HAVE_TO_START_EDITING_PREFERENCES_FIRST = (
    "Debe comenzar a editar las preferencias primero"
)
YOU_HAVE_TO_START_SORTING_FIRST = "Debe comenzar a dar orden primero"
YOU_HAVE_TO_START_EDITING_RESTAURANT_DELIVERIES_FIRST = (
    "Debe comenzar a editar los deliveries del restaurant primero"
)
YOU_HAVE_TO_START_EDITING_PROMOTIONS_FIRST = (
    "Debe comenzar a editar promociones primero"
)
YOU_HAVE_TO_START_EDITING_REVIEWS_FIRST = (
    "debe comenzar a editar las revisiones primero"
)
YOU_HAVE_TO_START_EDITING_USERS_FIRST = "Debe comenzar a editar usuarios primero"
RETURN_OK = "OK"
RESTAURANT_REVIEW_CREATED = "La revisión del restaurant fué creada"
DISH_REVIEW_CREATED = "La revisón del Item/Plato ha sido creada"
REVIEW_DOES_NOT_EXIST = "La revisión no existe"
REVIEW_UPDATED='La revisión fué modificada'
REVIEW_CREATED='La revisión fué creada'
REVIEW_DELETED = "La revisión fué eliminada"
REVIEW_MARKED_FOR_REJECTION_OR_ACCEPTANCE = (
    "La revisión fué marcada para rechazo/aceptación"
)
ORDERS_CLEARED = "Todos los ordenamientos fueron limpiados"
CATEGORY_ORDERS_CLEARED = "Ordenes de categprías fueron limpiados"
CATEGORY_DISHES_ORDERS_CLEARED = "Ordenes de items/platos fueron limpiados"
IMAGE_UPLOADED = "La imagen fué cargada"
IMAGE_DELETED = "La imagen fué eliminada"
KEY_SENT = "Clave Enviada"
PAYMENT_NOTIFICATION_SENT = "Notificación de pago enviada"
NO_PAYMENT_NOTIFICATION_SENT = "Notificación de pago no enviada"
RESOURCE_AND_IMAGE_DELETED = "El recurso y registro de la imagen fueron eliminados"
IMAGE_DOES_NOT_EXIST = "La imagen no existe"
IMAGE_IS_BEING_USED = "La imagen está siendo usada"
IMAGE_NAME_UPDATED = "La imagen fué actualizada"
HELP_ATONN_DOES_NOT_EXIST = "Ayuda para ese componente no existe"
DELIVERY_COMPANY_DOES_NOT_EXIST = "La compañía de delivery no existe"
RESTAURANT_DELIVERY_COMPANY_CREATED = "El delivery del restaurant fué creado"
RESTAURANT_USER_CREATED = "The restaurant user was created succesfully"
PROMOTION_CREATED = "The promotion was created succesfully"
PROMOTION_PROVISIONAL_NAME = "Nueva Promoción"
RESTAURANT_DELIVERY_COMPANY_DOES_NOT_EXIST = "El restaurant delivery no existe"
PROMOTION_DOES_NOT_EXIST = "La promoción no existe"
RESTAURANT_DELIVERY_COMPANY_UPDATED = "El restaurant delivery fué actualizado"
PROMOTION_UPDATED = "La promoción fué actualizada"
RESTAURANT_DELIVERY_COMPANY_MARKED_UNMARKED_FOR_DELETION = (
    "El restaurant delivery fué marcado/desmarcado para su eliminación"
)
OWN_DELIVERY = "Propio"
OTHER_DELIVERY = "Otro"
NO_RESTAURANT_DELIVERY_COMPANIES_TO_DELETE = "No hay compañías de delivery"
RESTAURANT_DELIVERY_COMPANY_ALREADY_EXISTS = (
    "La compañía de delivery del estaurant ya existe"
)
RESTAURANT_DELIVERY_COMPANY_DELETED = "Compañía de delivery del restaurant eliminada"
RESTAURANT_DELIVERY_COMPANIES_DELETED = (
    "Compañias de delivery del restaurant eliminadas"
)
RESTAURANT_DELIVERY_COMPANY_MARKED_FOR_DELETION_WAS_SWITCHED = (
    "La marca de eliminación del delivery del restaurant fué cambiada"
)
PROMOTION_MARKED_FOR_DELETION_WAS_SWITCHED = (
    "La marca de eliminación de la promoción fué cambiada"
)
YOU_MAY_START_EDITING_RESTAURANT_DELIVERIES = (
    "Puede comenzar a editar los deliveries del restaurant"
)
YOU_MAY_START_EDITING_PROMOTIONS = "Puede comenzar a editar promociones"
CANNOT_ADD_AN_ALREADY_REJECTED_REVIEW = "No puede añadir una revisión ya rechazada"
CANNOT_ADD_A_REJECTION_TO_A_NON_REJECTED_REVIEW = (
    "No puede añadir una razón de rechazo a una revisión no rechazada"
)
CANNOT_ADD_A_REJECTION_REASON_TO_A_NON_EXISTENT_REVIEW = (
    "No puede añadir una razón de rechazo a una revisión no existente"
)
REVIEW_REJECTIONS_SWITCHED_DELETION_STATUS = (
    "El estatus de eliminación de las revisiones a cambiado"
)
REJECTION_REASON_ID_MUST_BE_AN_INTEGER = (
    "El ID de la razón de rechazo debe ser un entero positivo"
)
FROM_EMAIL = ("rafael.soteldo@gmail.com")
FIRST_PAYMENT_NOTIFICATION = "Primera de dos notificaciones. El período de gracia para el pago de su cuenta ha sido activado. Por favor, asegúrese de que sus pagos estén al día para evitar interrupciones en el servicio"
SECOND_PAYMENT_NOTIFICATION = "Segunda y última notificacion. El período de gracia para el pago de su cuenta ha sido activado. Por favor, asegúrese de que sus pagos estén al día para evitar interrupciones en el servicio"
GRACE_PERIOD_ACTIVATED = ("Período de Gracia de quince días para el pago activado")
PAYMENT_CONFIRMATION = "Confirmación de pago. SN Software ©Atonna"
INITIAL_MENU_LOAD_PAYMENT_CONFIRMATION = "Pago Solicitud de Carga Inicial del Menú Hecho "
DO_NOT_RESPOND_THIS_MESSAGE = "Por favor, no responda este mensaje"
THANK_YOU_IN_ADVANCE = "Gracias de antemano"
YOUR_ATONNA_VERIFICATION_KEY = "Su clave de verificación de SN Software @Atonna"
YOUR_FOUR_DIGITS_EMAIL_VERIFICATION_KEY = "Su clave de cuatro dígitos para verificar el email es"
VERIFICATION_KEY = "Clave de Verificación"
EMAIL_VERIFICATION_KEY = "Clave de Verificación de EMail"
YOUR_FOUR_DIGITS_KEY_IS = "Su clave de cuatro dígitos es"
USE_THIS_KEY_TO_COMPLETE_EMAIL_VERIFICATION_PROCESS = "Por favor, use esta clave para completar el proceso de verificación del email"
YOUR_QR_CODE_FOR_ENTERING_ATONNA = "Su código QR, SN Software ©Atonna"
QR_CODE = "Código QR"
YOUR_QR_CODE_IS_IN_THE_ATTACHMENT = "El código QR requerido por usted se encuentra en el attachement"
THANK_YOU_FOR_USING_OUR_SERVICE = "Gracias por usar nuestro servicio"
RECEIPT="Recibo de Pago"
PAYPAL_PAYMENT_RECEIPT = "Recibo de pago, pago hecho con Paypal"
PAYER_INFORMATION="Información de quien paga"
NAME = "Nombre"
EMAIL = "EMail"
TRANSACTION_DETAILS = "Detalles de la transacción"
TRANSACTION_ID = "Identificación de la transacción"
DATE = "Fecha"
AMOUNT = "Cantidad"
CURRENCY = "Moneda"
THANK_YOU_FOR_YOUR_PAYMENT = "Gracias por su pago"
CREATING = "CREATING"
REACTIVATING = "REACTIVATING"
PAYINGNORMALFEE = "PAYINGNORMALFEE"
INITIALMENULOAD = "INITIALMENULOAD"
ACTION_IS_NOT_CREATING_NOR_REACTIVATING_NOR_PAYINGNORMALFEE = "Action is not creating nor reactivating nor paying normal fee"
THERE_WAS_AN_ERROR = "There was an error"

RUT = "RUT"
CUIT = "CUIT"
EIN = "EIN"

DOCUMENT_TYPES = [
    (None, "No Selection"),  # Explicit null option
    (RUT, "Registro Único Tributario"),
    (CUIT, "Código Único de Identificación Tributaria"),
    (EIN, "Employer Identification Number"),
]

FULL_PRICE = "Full Price"
MINIMUM_PRICE = "Minimum Price"

PRICE_CHOICES = [
    (None, "No Selection"),  # Explicit null option
    (FULL_PRICE, "Full Price"),
    (MINIMUM_PRICE, "Minimum Price"),
]

PAYMENT_STATES = [
    (RESTAURANT_NOT_BLOCKED_DUE_TO_PAYMENT, "Restaurant not blocked due to payment"),
    (RESTAURANT_BLOCKED_DUE_TO_PAYMENT, "Restaurant blocked due to payment"),
]