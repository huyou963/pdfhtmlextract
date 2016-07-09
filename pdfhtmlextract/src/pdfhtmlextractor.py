#coding=gbk

__author__ = 'CQC'
# -*- coding:utf-8 -*-
 
import os
from bs4 import BeautifulSoup
#import urllib2
import re
from table import Table
from logger import Logger
import string
from dataBaseManager import dataBaseManager

class PdfHtmlExtractor(object):
    htmlfile = ''
    soup = ''
    tableList = []              #����һ���½���ÿҳ���ҵ���table ֮����Ҫ�ж��Ƿ���Ҫ�ϲ�table
    pageRange1=[0,0]            #save table page range
    pageRange2=[0,0]
    pageRange3=[0,0]
    paragraphPageList1 = []
    paragraphPageList2 = []
    paragraphPageList3 = []
     
    def __init__(self, htmlfile):
        
        htmlfilelog = htmlfile + '.log'
        if os.path.exists(htmlfilelog):
            os.remove(htmlfilelog)
        self.logger = Logger(logname=htmlfilelog, loglevel="DEBUG", logger=__name__).getlogger()
        self.logger.info("Begin extract: %s" % htmlfile)
        
        self.htmlfile = htmlfile
        self.soup = BeautifulSoup(open(self.htmlfile), "html.parser")
    
    def getPageContent(self,pageNum):
        
        pageContentList = self.soup.find_all('div',{'id':pageNum}) 
        if  1 == len(pageContentList):
            return pageContentList[0]
        elif 1 < len(pageContentList):
            self.logger.error("Find two same pageNum: %s" % pageNum)
        else:
            self.logger.error("pageLen=", len(pageContentList))            
        return None
    
    #cmpStr==None return total num of page element, cmpStr!=None return cmpStr position in page    
    def getPageElementIndexOrTotalNum(self,pageNum,cmpStr=None):
        pageElementIndex = 0
        
        pageContent = self.getPageContent(pageNum)
        if pageContent == None:
            self.logger.error("Get page content None")
            return None
        pageElement = pageContent.div.div
        
        while True:
            if None != pageElement:
                if cmpStr!= None:
                    if re.search(cmpStr, pageElement.get_text()):
                        self.logger.info("Find (cmpStr,Page,ElementIndex) (%s, %s, %s)" % (cmpStr, pageNum, pageElementIndex))
                        return pageElementIndex
                pageElement =pageElement.next_sibling
                pageElementIndex += 1
            else:
                break
        if cmpStr == None:
            self.logger.info("Page:%s. Total element Num:%s" % (pageNum, pageElementIndex))
            return pageElementIndex
        else:
            self.logger.error("Cann't find str:%s in page:%s" % (cmpStr,pageNum))    
            return None
    
    def getCompareColumnElemnt2(self, pageElement, columnNum):
        if columnNum !=0:
            columnNum -= 1
            compareColumnElement = self.getCompareColumnElemnt2(pageElement.previous_sibling, columnNum)
            return compareColumnElement
        else:
            return compareColumnElement
    
        
    def getCompareColumnElemnt(self, pageElement, columnNum):
        if columnNum == 1:
            compareColumnElement = pageElement.previous_sibling
        if columnNum == 2:
            compareColumnElement = pageElement.previous_sibling.previous_sibling
        if columnNum == 3:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 4:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 5:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 6:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 7:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 8:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 9:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 10:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 11:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        if columnNum == 12:
            compareColumnElement = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
        return compareColumnElement
    
    #��startElementIndex��startElementIndexֵ��Ч������ÿһҳ��������֮���Ԫ��
    def getTablesinPage(self, pageNum, startElementIndex=0, endElementIndex=65535):
        
        self.logger.info("Page %s fetch start" % pageNum)
        pageContent = self.getPageContent(pageNum)
        if pageContent == None:
            self.logger.error("Get page content None")
            return None
        
        pageElement = pageContent.div.div
        pageElementNum =  self.getPageElementIndexOrTotalNum(pageNum)
        elementIndex = 0
        
        #table��Ϣ�����ʱ����
        rowNum = 1            #�����ж����� �� rowIndex
        columnNum = 1         #�����ж�����
        columnIndex = 1       #��¼�е����
        tableStartIndex = 0   #����table��ʼʱ��Ԫ��λ��
        tableEndIndex = 0     #����table����ʱ��Ԫ��λ��
        tmpTable = None
        while True:
            if elementIndex >= startElementIndex:
                if (None != pageElement and elementIndex <= endElementIndex):
                    #�ҵ�����class C���ж��ǲ���table��ʼ
                    if 'c' == pageElement['class'][0] and 'c' == pageElement.previous_sibling['class'][0]:
                        if tmpTable == None:
                            tmpTable = Table(50,20)
                        #�õ�ǰ�и�Ԫ��
                        compareColumnElemnt = self.getCompareColumnElemnt(pageElement, columnNum)
                        
                        self.logger.debug("pageElement= %s, pre-pageElement= %s, compareColumnElemnt= %s" % (pageElement.get_text(), pageElement.previous_sibling.get_text(), compareColumnElemnt.get_text()))                    
                        self.logger.debug("pageElement Y= %s, pre-pageElement Y= %s" % (pageElement['class'][2], pageElement.previous_sibling['class'][2]))
                        self.logger.debug("pageElement X= %s, compareColumnElemnt X= %s" % (pageElement['class'][1], compareColumnElemnt['class'][1]))
    
                        # ��ǰһ��Ԫ�ص�Y����Ƚ�
                        if pageElement.previous_sibling['class'][2] == pageElement['class'][2]:    
                            columnIndex += 1
                            #��ǰһ��Ԫ�ص�Y�ȣ���ǰ�и�Ԫ�ص� X���� ----��һ��Ԫ��
                            if pageElement['class'][1] != compareColumnElemnt['class'][1]:
                                columnNum = columnIndex
                                # ���tableû��ʼ�����ҵ���һ��1/2cell
                                if tableStartIndex == 0:
                                    tableStartIndex = elementIndex
                                    self.logger.info("Find a table in page:%s, table start index:%s" % (pageNum, tableStartIndex))
                                    
                                    # Save cur-cell, pre-cell, tableStartIndex
                                    tableSavedFlag = False
                                     
                                    tmpTable.tableStartIndex = tableStartIndex
                                    tmpTable.setCellValue(rowNum-1, columnIndex-2, pageElement.previous_sibling.get_text())
                                    tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                                   
                                    self.logger.debug("Find 1st/2nd cell (rowIndex,columnIndex,value) (%s,%s,%s), (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex-1,pageElement.previous_sibling.get_text(),rowNum, columnIndex,pageElement.get_text()))
                                #�ҵ���һ������cell
                                else:
                                    tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                                    self.logger.debug("Find other 1st row cell (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                                    # Save cur-cell
                            #��ǰһ��Ԫ�ص�Y�ȣ���ǰ�и�Ԫ�ص� X���----����һ�е�һ�������Ԫ��        
                            else:
                                tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())
                                self.logger.debug("Find Cell row>1,column>1 (rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                                
                        else:
                            #��ǰһ��Ԫ�ص�Y���ȣ���ǰ�и�Ԫ�ص�X���----��(1,1)����ĵ�һ��Ԫ��
                            if pageElement['class'][1] == compareColumnElemnt['class'][1]:
                                if tableStartIndex != 0:
                                    rowNum += 1
                                    columnNum = columnIndex
                                    columnIndex = 1
                                self.logger.debug("Find first column cell(rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex, pageElement.get_text()))
                                tmpTable.setCellValue(rowNum-1, columnIndex-1, pageElement.get_text())                            
                               
                            else:
                                # ��ǰһ��Y���겻�ȣ���ǰ�и�X���겻��----table����
                                if tableStartIndex != 0:
                                    tableEndIndex = elementIndex
                                    self.logger.info("Table is ended due to Y!=,X!= with info(rowNum,columnNum,tableEndIndex,content,pageNum) (%s,%s,%s,%s,%s)" % (rowNum, columnIndex, tableEndIndex, pageElement.get_text(),pageNum))
                                    #Save tableEndIndex, rowNum, columnNum append tableList
                                    if tableSavedFlag == False and rowNum >= 1 and columnNum > 1:
                                        tmpTable.tableEndIndex = tableEndIndex
                                        tmpTable.rowNum = rowNum
                                        tmpTable.columnNum = columnNum
                                        self.saveTable(tmpTable,rowNum,columnNum,pageElementNum)
                                        tableSavedFlag = True
                                    # ���������tmptable��ر���
                                    tableStartIndex = 0
                                    rowNum = 1
                                    columnNum = 1
                                    columnIndex = 1
                                    tableEndIndex = 0
                                    tmpTable.reset()
                                    
                    elif 't' == pageElement['class'][0]:
                        if tableStartIndex != 0:
                            tableEndIndex = elementIndex
                            self.logger.info("Table is ended due to find a class t info(rowNum,columnNum,tableEndIndex,pageNum) (%s,%s,%s,%s)" % (rowNum, columnIndex, tableEndIndex,pageNum))
                            #Save tableEndIndex, rowNum, columnNum
                            if tableSavedFlag == False and rowNum >= 1 and columnNum > 1:
                                tmpTable.tableEndIndex = tableEndIndex
                                tmpTable.rowNum = rowNum
                                tmpTable.columnNum = columnNum
                                self.saveTable(tmpTable,rowNum,columnNum,pageElementNum)
                                tableSavedFlag = True
                            # ���������tmptable��ر���
                            tableStartIndex = 0
                            rowNum = 1
                            columnNum = 1
                            columnIndex = 1
                            tableEndIndex = 0
                            tmpTable.reset()      
                #���������һ��Ԫ�أ�������ѭ��
                else:
                    if tableStartIndex != 0:
                        tableEndIndex = elementIndex
                        self.logger.info("Table is ended due to last element info(rowNum,columnNum,tableEndIndex,pageNum) (%s,%s,%s,%s)" % (rowNum, columnIndex, tableEndIndex,pageNum))
                        #Save tableEndIndex, rowNum, columnNum
                        if tableSavedFlag == False and rowNum >= 1 and columnNum > 1:
                            tmpTable.tableEndIndex = tableEndIndex
                            tmpTable.rowNum = rowNum
                            tmpTable.columnNum = columnNum
                            self.saveTable(tmpTable,rowNum,columnNum,pageElementNum)
                            tableSavedFlag = True
                        
                        # ���������tmptable��ر���
                        tableStartIndex = 0
                        rowNum = 1
                        columnNum = 1
                        columnIndex = 1
                        tableEndIndex = 0
                        tmpTable.reset()   
                    break
            
            # ��ȡ��һ��Ԫ��
            pageElement =pageElement.next_sibling
            elementIndex += 1
            
        self.logger.info("Page %s fetch end" % pageNum)        
        return True
    
    def saveTable(self, tmpTable, rowNum, columnNum, pageElementNum):
        myTable = Table(rowNum,columnNum)
        myTable.tableStartIndex = tmpTable.tableStartIndex
        myTable.tableEndIndex = tmpTable.tableEndIndex
        myTable.rowNum = rowNum
        myTable.columnNum = columnNum
        myTable.pageNum = tmpTable.pageNum
        
        #�ж��Ƿ���ǰ������
        if tmpTable.tableStartIndex < 5:
            myTable.preExtend = 1
        else:
            myTable.preExtend = 0
        if (pageElementNum - tmpTable.tableEndIndex) < 5:
            myTable.aftExtend = 1
        else:
            myTable.aftExtend = 0
            
        #����������
        for row in range(0,rowNum):
            for column in range(0,columnNum):
                myTable.setCellValue(row, column, tmpTable.getCellValue(row,column))
                self.logger.debug("Save cell (row, column, tmpTablevalue, myTablevalue) (%s, %s, %s ,%s)" % (row, column, tmpTable.getCellValue(row,column), myTable.getCellValue(row, column)))
                 
        self.tableList.append(myTable)

        return
    
    def processNode(self, node, level): 
        if node.name == "a":
            self.logger.debug("Find a title (TitleName, Level, href) (%s,%s,%s)" % (node.string, level, string.atoi(node['href'][3:],base=16)))
        if node.name == "li":
            for child in node.children:
                if child.name == "a":
                    strTable1 = u"�ϲ��ʲ���ծ��"
                    strTable2 = u"�ϲ������"
                    strTable3 = u"�ϲ��ֽ�������"
                    pageNum=string.atoi(child['href'][3:],base=16)
                    if re.search(strTable1, child.string):
                        self.pageRange1[0]=pageNum
                    elif 0!=self.pageRange1[0] and 0==self.pageRange1[1]:
                        self.pageRange1[1]=pageNum
                    
                    if re.search(strTable2, child.string):
                        self.pageRange2[0]=pageNum
                    elif 0!=self.pageRange2[0] and 0==self.pageRange2[1]:
                        self.pageRange2[1]=pageNum
                        
                    if re.search(strTable3, child.string):
                        self.pageRange3[0]=pageNum
                    elif 0!=self.pageRange3[0] and 0==self.pageRange3[1]:
                        self.pageRange3[1]=pageNum
                    self.logger.debug("Find a title under li (TitleName, Level, href) (%s,%s,%s)" % (child.string, level, string.atoi(child['href'][3:],base=16)))
                if child.name == "ul":
                    self.processNode(child,level)
        if node.name == "ul":
            level += 1
            for child in node.children:
                self.processNode(child,level)
    
    
    #������Ҫ����������ʼλ�ã� paragraphPageList[0....n-3,n-2,n-1,n] 0:��ʼҳ  n-2:��ʼҳ��ʼλ��  n-3:����ҳ  n-1:����ҳλ��  n:�������� 
    def getFetchTablePageLists(self):
        outlines=self.soup.find_all('div',{'id':'outline'})
        outlineIndex = 0
        times = 0
        for outline in outlines:
            if outlineIndex > 1:
                self.logger.error("Find more than one outline")
                return False
            for child in outline.children:
                self.processNode(child, times)

            outlineIndex += 1
            
        self.logger.info("Page range: �ϲ��ʲ���ծ�� (%s,%s), �ϲ������ (%s,%s), �ϲ��ֽ������� (%s,%s)" % (self.pageRange1[0], self.pageRange1[1], self.pageRange2[0], self.pageRange2[1], self.pageRange3[0], self.pageRange3[1]))

        self.paragraphPageList1 = self.createPageList(self.pageRange1)
        startIndexInPage1 = self.getPageElementIndexOrTotalNum(self.paragraphPageList1[0],u'�ϲ��ʲ���ծ��')
        endIndexInPage1 = self.getPageElementIndexOrTotalNum(self.paragraphPageList1[len(self.paragraphPageList1)-1],u'ĸ��˾�ʲ���ծ��')
        self.paragraphPageList1.append(startIndexInPage1)
        self.paragraphPageList1.append(endIndexInPage1)
        self.paragraphPageList1.append(u'�ϲ��ʲ���ծ��')
        
        self.paragraphPageList2 = self.createPageList(self.pageRange2)
        startIndexInPage2 = self.getPageElementIndexOrTotalNum(self.paragraphPageList2[0],u'�ϲ������')
        endIndexInPage2 = self.getPageElementIndexOrTotalNum(self.paragraphPageList2[len(self.paragraphPageList2)-1],u'ĸ��˾�����')
        self.paragraphPageList2.append(startIndexInPage2)
        self.paragraphPageList2.append(endIndexInPage2)
        self.paragraphPageList2.append(u'�ϲ������')
        
        self.paragraphPageList3 = self.createPageList(self.pageRange3)
        startIndexInPage3 = self.getPageElementIndexOrTotalNum(self.paragraphPageList3[0],u'�ϲ��ֽ�������')
        endIndexInPage3 = self.getPageElementIndexOrTotalNum(self.paragraphPageList3[len(self.paragraphPageList3)-1],u'ĸ��˾�ֽ�������')
        self.paragraphPageList3.append(startIndexInPage3)
        self.paragraphPageList3.append(endIndexInPage3)
        self.paragraphPageList3.append(u'�ϲ��ֽ�������')
        
        print "paragraphPageList1:", self.paragraphPageList1
        print "paragraphPageList2:", self.paragraphPageList2
        print "paragraphPageList3:", self.paragraphPageList3
        return True
    
    def createPageList(self, pageRange):
        pageList = []
        pageNum = pageRange[0]
        while pageNum <= pageRange[1]:
            tempPage = pageNum
            tempPage = "pf" + hex(tempPage)[2:]
            pageList.append(tempPage)
            pageNum += 1
        
        return pageList
        #self.logger.debug("pageList: (%l)")% (pageList)
        
    def fetchTableInParagraph(self,paragraphPageList):
        pageNums = len(paragraphPageList)-3
        if(2==pageNums and paragraphPageList[0] == paragraphPageList[1]):
            self.getTablesinPage(paragraphPageList[0],paragraphPageList[pageNums],paragraphPageList[pageNums+1])
        else:
            for i in range(0,pageNums):
                startIndex=0
                endIndex=65535
                if 0==i:
                    startIndex=paragraphPageList[pageNums]
                if pageNums-1==i:
                    endIndex=paragraphPageList[pageNums+1]
                #    
                self.getTablesinPage(paragraphPageList[i],startIndex,endIndex)
        
        print "tableList:",len(self.tableList)
    
    def stringTof(self,src):
        print "stringTof:src=",src
        if(src.strip()==''):
            return 
        src = src.replace(',', '')
        if(-1 != src.find('%')):
            src = src.replace('%', '')
            return (string.atof(src)/100)
        return string.atof(src)
    
    def mergeTableList(self,sheetName):
        
        dm=dataBaseManager()
        dm.openDataBase()
        dm.displayDataBase()
        
        fieldsName=[]
        fieldsValue=[]
        #datas=["600004","","111","222","333"]
        
        numFields = 0;
        
        for tableIndex in range(0, len(self.tableList)):
            for row in range(1,self.tableList[tableIndex].rowNum):
                    fieldsName.append(self.tableList[tableIndex].getCellValue(row,0) + u"_%d" % numFields)  
                    fieldsValue.append( self.stringTof(self.tableList[tableIndex].getCellValue(row,1)) )                    
                    print "tableIndex,row,col0 value:",tableIndex,row,self.tableList[tableIndex].getCellValue(row,0),"col1 value:",self.tableList[tableIndex].getCellValue(row,1)
                    numFields+=1
        print "fieldsName:",fieldsName
        print "fieldsValue:",fieldsValue
        fieldPrimaryKeyIndex = dm.insertStockFieldsTable("300412",sheetName, numFields, fieldsName)
        dm.insertStockSheetTable("300412", fieldPrimaryKeyIndex,sheetName, numFields, fieldsValue)

        #dm.createDataTable(recordsNames)
        #dm.insertDataInTable(fieldsName, datas)  
    
    def clearTableList(self):
        #һ������ı��д�����ݿ������tableList
        self.tableList = []
        return
 
    
    def writeTableinDB(self):
        #��һ����ı�д�����ݿ���
        return    
        
                   
    
    
if __name__ == '__main__':
    pdfhtmlextact = PdfHtmlExtractor('../2014.html')
    pdfhtmlextact.getFetchTablePageLists()
    pdfhtmlextact.fetchTableInParagraph(pdfhtmlextact.paragraphPageList1)
    pdfhtmlextact.mergeTableList('balanceSheet')
    #pdfhtmlextact.writeTableinDB()
    pdfhtmlextact.clearTableList()
    
    #pdfhtmlextact.fetchTableInParagraph(pdfhtmlextact.paragraphPageList2)
    #pdfhtmlextact.mergeTableList()
    #pdfhtmlextact.writeTableinDB()
    #pdfhtmlextact.clearTableList()
    
    #pdfhtmlextact.fetchTableInParagraph(pdfhtmlextact.paragraphPageList3)
    #pdfhtmlextact.mergeTableList()
    #pdfhtmlextact.writeTableinDB()
    #pdfhtmlextact.clearTableList()
    
    
