import logging
import sys


LOG_LEVEL = 'DEBUG'

class EventsAppLogger(logging.Logger):

    def __init__(self, logger_name=__name__):

        self.logger = logging.getLogger(logger_name)
        self.ch = logging.StreamHandler(sys.stdout)
        self.ch.setLevel(LOG_LEVEL)
        self.logger.setLevel(LOG_LEVEL)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.ch.setFormatter(self.formatter )
        self.logger.addHandler(self.ch)