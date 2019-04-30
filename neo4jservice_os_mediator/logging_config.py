import logging


# def singleton(cls):
#     instances = {}
#
#     def get_instance(log_file_path:str, log_level:str, logger_name:str):
#         if cls not in instances:
#             instances[cls] = cls(log_file_path, log_level, logger_name)
#         return instances[cls]
#
#     return get_instance
#
#
# @singleton
class Logger(object):
    def __init__(self, log_file_path, log_level, logger_name):
        if log_level == 'DEBUG':
            log_level = logging.DEBUG
        elif log_level == 'ERROR':
            log_level = logging.ERROR
        elif log_level == 'INFO':
            log_level = logging.INFO
        elif log_level == 'FATAL':
            log_level = logging.FATAL
        elif log_level == 'CRITICAL':
            log_level = logging.CRITICAL
        elif log_level == 'WARN':
            log_level = logging.WARN
        else:#default
            log_level = logging.DEBUG

        logging.basicConfig(filename=log_file_path, level=log_level,
                            format='%(asctime)s %(levelname)s %(name)s %(lineno)s %(message)s')
        self.logger = logging.getLogger(logger_name)
