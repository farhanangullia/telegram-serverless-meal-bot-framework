from typing import Any, Dict, Tuple
import json
import logging
import requests
import os
from keyboards import markups
from boto3 import client

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

API_BOT_TOKEN = os.environ["API_BOT_TOKEN"]
LOGIN_FUNCTION_ARN = os.environ["LOGIN_FUNCTION_ARN"]
GET_MENU_FUNCTION_ARN = os.environ["GET_MENU_FUNCTION_ARN"]
UPLOAD_MENU_FUNCTION_ARN = os.environ["UPLOAD_MENU_FUNCTION_ARN"]
BASE_URL = "https://api.telegram.org/bot{}".format(API_BOT_TOKEN)

lambda_client = client("lambda")


def lambda_handler(event, context):
    logger.info(event)
    try:
        body = json.loads(event["Records"][0]["body"])
        if is_callback_query(body):
            handle_callback(body)
        else:
            if "message" in body:
                handle_message(body["message"])

    except Exception as e:
        logger.error("Error occurred in handler: %s", str(e), exc_info=1)


def is_callback_query(body: Any) -> bool:
    if "callback_query" in body:
        return True
    else:
        return False


def handle_callback(body: Any) -> None:
    callback_query_id = body["callback_query"]["id"]
    chat_id = str(body["callback_query"]["message"]["chat"]["id"])
    callback_data = body["callback_query"]["data"]
    message_id = int(body["callback_query"]["message"]["message_id"])

    callbacks = {
        "login": login,
        "menu_today": get_menu,
        "menu_tomorrow": get_menu,
        "feedback": feedback,
        "sys_admin": sys_admin,
        "upload_menu": upload_menu,
        "log_out": log_out,
    }
    callbacks.get(callback_data, default_func)(
        chat_id, message_id, callback_query_id, body
    )


def handle_message(message: Any) -> None:
    if "text" not in message:
        return None

    chat_id = str(message["chat"]["id"])  # user/chat id
    text = message["text"]
    message_id = int(message["message_id"])
    id = int(message["from"]["id"])  # user id
    entities = None

    if "entities" in message:
        entities = message["entities"]

    if is_bot_command(entities):
        process_command(chat_id, text)


def is_bot_command(entities: Dict[str, Any]) -> bool:
    if entities is None:
        return False
    elif any(entity["type"] == "bot_command" for entity in entities):
        return True
    else:
        return False


def process_command(chat_id: str, text: str) -> None:
    logger.info("process_command ({})".format(text))

    commands = {"/start": display_main_menu, "/menu": display_main_menu}
    commands.get(text, default_func)(chat_id)


def get_encoded_keyboard(key: str) -> str:
    return json.JSONEncoder().encode(markups.get(key))


def display_main_menu(
    chat_id: str, text: str = "Main Menu. Please select a menu option."
) -> str:
    params = "&reply_markup={}".format(get_encoded_keyboard("MainMenuKeyboardMarkup"))
    send_message(chat_id, text, params)


def display_login_menu(
    chat_id: str,
    message_id: int,
    callback_query_id: str,
    text: str = "Login Menu. Please login to access System Admin features.",
) -> str:
    params = "&reply_markup={}".format(get_encoded_keyboard("LoginMenuKeyboardMarkup"))
    respond_callback_query(
        chat_id, text, message_id, callback_query_id, edit_message_text_params=params
    )


def display_sys_admin_menu(
    chat_id: str,
    message_id: int,
    callback_query_id: str,
    text: str = "System Admin. Please select a menu option.",
) -> str:
    params = "&reply_markup={}".format(
        get_encoded_keyboard("SystemAdminMenuKeyboardMarkup")
    )
    respond_callback_query(
        chat_id, text, message_id, callback_query_id, edit_message_text_params=params
    )


def send_message(chat_id: str, text: str, params: str = None) -> None:
    response =         requests.get(
            "{}/sendMessage?chat_id={}&text={}{}".format(
                BASE_URL, chat_id, text, params
            )
        )

    logger.info(response.text
    )
    logger.info(response.status_code
    )

    logger.info(response.reason)

def respond_callback_query(
    chat_id: str,
    text: str,
    message_id: int,
    callback_query_id: str,
    answer_callback_params: str = None,
    edit_message_text_params: str = None,
) -> None:
    answer_callback_query(callback_query_id, answer_callback_params)
    edit_message_text(chat_id, text, message_id, edit_message_text_params)


def answer_callback_query(
    callback_query_id: str, answer_callback_params: str = None
) -> None:
    response = requests.get(
            "{}/answerCallbackQuery?callback_query_id={}{}".format(
                BASE_URL, callback_query_id, answer_callback_params
            )
        )

    logger.info(response.text
    )
    logger.info(response.status_code
    )

    logger.info(response.reason)


def edit_message_text(
    chat_id: str, text: str, message_id: int, edit_message_text_params: str = None
) -> None:
    response = requests.get(
            "{}/editMessageText?chat_id={}&message_id={}&text={}{}".format(
                BASE_URL, chat_id, message_id, text, edit_message_text_params
            )
        )


    logger.info(response.text
    )
    logger.info(response.status_code
    )

    logger.info(response.reason)


def get_menu(chat_id: str, message_id: int, callback_query_id: str, body: Any):
    response = lambda_client.invoke(
        FunctionName=GET_MENU_FUNCTION_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(body),
    )

    payload = json.load(response["Payload"])
    logger.info(payload)
    respond_callback_query(
        chat_id, payload["date"] + payload["menu"], message_id, callback_query_id
    )


def feedback():
    pass


def sys_admin(chat_id: str, message_id: int, callback_query_id: str, body: Any) -> None:
    response = lambda_client.invoke(
        FunctionName=LOGIN_FUNCTION_ARN,
        InvocationType="RequestResponse",
        Payload=json.dumps(body),
    )
    payload = json.load(response["Payload"])
    logger.info(payload)
    if payload["is_logged_in"]:
        display_sys_admin_menu(chat_id, message_id, callback_query_id)
    else:
        display_login_menu(chat_id, message_id, callback_query_id)


def login():
    pass


def upload_menu():
    pass


def log_out():
    pass


def default_func(chat_id=None, message_id=None, callback_query_id=None, body=None):
    return
