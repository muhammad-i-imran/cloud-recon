import requests
import time
import envvars
import os

from logging_config import Logger

logger = Logger(log_file_path=envvars.LOGS_FILE_PATH, log_level=envvars.LOG_LEVEL, logger_name=os.path.basename(__file__)).logger


# def call_service(url, method, **args):
#     pass

def call_service_get_method(url, parameters = None, **args):
    logger.debug("Sending GET request on %s." % url)
    response = requests.get(url, parameters, **args)
    handle_response(response)
    return response.json()

def call_service_post_method(url, json, **args):
    logger.debug("Sending POST request on %s." % url)
    response = requests.post(url, json=json, **args)
    handle_response(response)
    return response.json()

def call_service_put_method(url, json, **args):
    logger.debug("Sending PUT request on %s." % url)
    response = requests.put(url, json=json, **args)
    handle_response(response)
    return response.json()

def call_service_delete_method(url, json, **args):
    logger.debug("Sending DELETE request on %s." % url)
    response = requests.post(url, json=json, **args)
    handle_response(response)
    return response.json()

def handle_response(response):
    logger.debug("Received response with status code %s." % str(response.status_code))

# def status_handler(status_code):
#     status_code_message_mappings = {
#         200: "Request was successful."
#     }