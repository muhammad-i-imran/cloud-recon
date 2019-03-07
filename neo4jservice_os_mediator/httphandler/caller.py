import requests
import time

def call_service(url, method, **args):
    pass

def call_service_get_method(url, parameters = None, **args):
    response = requests.get(url, parameters, **args)
    handle_response(response)
    return response.json()

def call_service_post_method(url, json, **args):
    response = requests.post(url, json=json, **args)
    handle_response(response)
    return response.json()

def call_service_put_method(url, json, **args):
    response = requests.put(url, json=json, **args)
    handle_response(response)
    return response.json()

def call_service_delete_method(url, json, **args):
    response = requests.post(url, json=json, **args)
    handle_response(response)
    return response.json()

def handle_response(response):
    print(response.status_code, response.reason)

# def status_handler(status_code):
#     status_code_message_mappings = {
#         200: "Request was successful."
#     }