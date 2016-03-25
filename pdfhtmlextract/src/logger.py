#coding=gbk

__author__ = 'CQC'
# -*- coding:utf-8 -*-

import logging

class Logger():
    def __init__(self, logname, loglevel, logger):

        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(filename)s- %(module)s - %(funcName)s - %(levelname)s - %(message)s')
        #formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    
    def getlogger(self):
        return self.logger
    
if __name__ == '__main__':
    logger = Logger(logname='log.txt', loglevel=1, logger=__name__).getlogger()
    logger.info("Process pid is not valid,skip it.")