from typing import Any, Dict, List
import os
import json
from urllib.parse import quote_plus

__all__ = ["markups"]


COGNITO_AUTHORIZATION_URL = quote_plus(os.environ["COGNITO_AUTHORIZATION_URL"]) # safe escape query string URL parameter

markups = {
    "MainMenuKeyboardMarkup": {
        "inline_keyboard": [
            [{"text": "Menu Today", "callback_data": "menu_today"}],
            [{"text": "Menu Tomorrow", "callback_data": "menu_tomorrow"}],
            [{"text": "Feedback", "callback_data": "feedback"}],
            [{"text": "System Admin", "callback_data": "sys_admin"}],
        ]
    },
    "LoginMenuKeyboardMarkup": {"inline_keyboard": [[{"text":"Login","url":COGNITO_AUTHORIZATION_URL,}]]},
    "SystemAdminMenuKeyboardMarkup": {
        "inline_keyboard": [
            [{"text": "Upload Menu", "callback_data": "upload_menu"}],
            [{"text": "Log Out", "callback_data": "log_out"}],
        ]
    },
}
