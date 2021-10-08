import json


def lambda_handler(event, context):
    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    is_logged_in = False

    return {"is_logged_in": is_logged_in, "event": event}
