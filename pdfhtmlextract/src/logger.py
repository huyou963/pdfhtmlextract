#coding=gbk

__author__ = 'CQC'
# -*- coding:utf-8 -*-

import logging

class Logger():
    def __init__(self, logname, loglevel, logger):

        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(logname)
        ch = logging.StreamHandler()
        if loglevel == 'ERROR':
            fh.setLevel(logging.ERROR)
            ch.setLevel(logging.ERROR)
        elif loglevel == 'WARNING':
            fh.setLevel(logging.WARNING)
            ch.setLevel(logging.WARNING)    
        elif loglevel == 'INFO':
            fh.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)
        elif loglevel == 'DEBUG':
            fh.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            print 'Set a wrong log level:', loglevel
            return 
        
        formatter = logging.Formatter('%(asctime)s - %(module)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s')
        #formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        return
    
    def getlogger(self):
        return self.logger
    
if __name__ == '__main__':
    logger = Logger(logname='log.txt', loglevel=1, logger=__name__).getlogger()
    logger.info("Process pid is not valid,skip it.")