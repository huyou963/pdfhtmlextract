#coding=gbk
__author__ = 'CQC'
# -*- coding:utf-8 -*-
 

class Cell(object):
    rowIndex = ''
    columnIndex = ''
    cellText = ''    
    def __init__(self):        
         
        return True 
        
    def getCellText(self):
        return self.cellText
        
if __name__ == '__main__':
    cell = Cell()

