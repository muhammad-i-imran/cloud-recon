import requests
import time

def call_service(url, method, **args):
    pass

def call_service_get_method(url, parameters = None, **args):
    response = requests.get(url, parameters, **args)
    handle_response(response)
    return response

def call_service_post_method(url, data, **args):
    response = requests.post(url, data=data, **args)
    handle_response(response)
    return response

def call_service_put_method(url, data, **args):
    response = requests.put(url, data=data, **args)
    handle_response(response)
    return response

def call_service_delete_method(url, data, **args):
    response = requests.post(url, data=data, **args)
    handle_response(response)
    return response

def handle_response(response):
    print(response.status_code, response.reason)

# def status_handler(status_code):
#     status_code_message_mappings = {
#         200: "Request was successful."
#     }