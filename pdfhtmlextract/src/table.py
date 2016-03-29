#coding=gbk
__author__ = 'CQC'
# -*- coding:utf-8 -*-

from logger import Logger

class Table(object):
    pageNum = 0
    tableStartIndex = 0
    tableEndIndex = 0
    rowNum = 0
    columnNum = 0
    preExtend = 2
    aftExtend = 2
    cellArray = []
     
    def __init__(self, rowNum, columnNum):
        self.logger = Logger(logname=htmlfilelog, loglevel="DEBUG", logger=__name__).getlogger()
        self.logger.info("Init a table size(rowNum,columnNum) (%s,%s)" % (rowNum,columnNum)
        self.cellArray = [['' for self.rowNum in range(rowNum)] for self.columnNum in range(columnNum)]
        self.rowNum = rowNum
        self.columnNum = columnNum
        
        return
    
    def setCellValue(self, rowIndex, columnIndex, value):
        self.cellArray[rowIndex][columnIndex] = value
        
    def getCellValue(self, rowIndex, columnIndex):
        if self.cellArray[rowIndex][columnIndex] != None:
            return self.cellArray[rowIndex][columnIndex]
        else:
            return None
        
    def isValidTable(self):
        return True
     
if __name__ == '__main__':
    my = Table(3,3)
    my.setCellValue(1, 2, u'财')
    print my.getCellValue(1, 2)
    
