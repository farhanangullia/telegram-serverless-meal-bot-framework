import json


def lambda_handler(event, context):
    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    return {
        "menu": "Go Serverless v1.0! Your function executed successfully!",
        "date": "date",
        "event": event,
    }
