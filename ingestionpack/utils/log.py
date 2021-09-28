import logging
import os
import sys
from logging import Formatter
from logging.handlers import RotatingFileHandler

import jaeger_client
from jaeger_client import Config



class Log():
    def __init__(self, log_name, app_name, class_name, spanContext: jaeger_client.SpanContext, stdout=False):
        #TODO: comprobar si existe la varieble de entorno, url default
        logging_path = os.environ.get('LOGGING_DIR')

        self.directory = os.path.join(logging_path, log_name + '.log')
        self.logger= logging.getLogger(log_name)
        self.logger.propagate = False
        self.max_log_size = 10 * 1000 * 1000
        os.makedirs(os.path.dirname(self.directory), exist_ok=True)
        self.handler = RotatingFileHandler(
            self.directory, maxBytes=self.max_log_size, backupCount=5)
        self.formatter = Formatter(
            f'%(asctime)s  %(levelname)s [{app_name},{spanContext.trace_id},{spanContext.span_id}, true]: [%(threadName)s]{class_name}- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.handler.setFormatter(self.formatter)

        if len(self.logger.handlers) == 0:
            self.logger.addHandler(self.handler)

            if stdout:
                handler = logging.StreamHandler(sys.stdout)
                handler.setFormatter(self.formatter)
                self.logger.addHandler(handler)


    def debug(self, text):
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(text)

    def warning(self, text):
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(text)

    def error(self, text):
        self.logger.setLevel(logging.ERROR)
        self.logger.error(text)

    def info(self, text):
        self.logger.setLevel(logging.INFO)
        self.logger.info(text)

def init_tracer(service):
    config = Config(
        config={
            'sampler':
                {'type': 'const',
                 'param': 1},
            'logging': True,
            'reporter_batch_size': 1, },
        service_name=service)
    # this call also sets opentracing.tracer
    return config.initialize_tracer()
