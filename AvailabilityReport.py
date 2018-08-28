# -*- coding: latin5 -*-
import pyodbc
import logging


def connecttodb():
    availability_logger = logging.getLogger('AvailabilityGraphSender.ConnecttoDB')
    availability_logger.info('Connecting to DB')
    cnxn = pyodbc.connect('DSN=xxx;UID=xxx;PWD=xxx')
    availability_logger.info('Connected DB')
    cursor = cnxn.cursor()
    return cursor



