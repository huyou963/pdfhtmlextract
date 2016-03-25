#coding=gbk

__author__ = 'CQC'
# -*- coding:utf-8 -*-
 
import os
from bs4 import BeautifulSoup
import urllib2
import re
import table
import logger

class PdfHtmlExtractor(object):
    htmlfile = ''
    soup = ''
    def __init__(self, htmlfile):
        
        htmlfilelog = htmlfile + '.log'
        if os.path.exists(htmlfilelog):
            os.remove(htmlfilelog)
        self.logger = logger.Logger(logname=htmlfilelog, loglevel="DEBUG", logger=__name__).getlogger()
        self.logger.info("Begin extract: %s" % htmlfile)
        
        self.htmlfile = htmlfile
        self.soup = BeautifulSoup(open(self.htmlfile), "html.parser")
        
    def getSectionStartEndPage(self,sectionName):
        
        pageRange = []
        startPage = ''
        endPage = ''
        
        if sectionName == None:
            self.logger.error("sectionName is None")
            return None
        
        self.logger.info("Begin find Page range of section: %s" % sectionName)
        
        outline=self.soup.find_all('div',{'id':'outline'})
        print 'outline:',outline
        for li in outline:
            li_list = li.find_all('li')
            for li in li_list:
                if re.search(sectionName, li.a.get_text()):
                    startPage = li.a['href'][1:]
                    endPage = li.next_sibling.a['href'][1:]
        
        pageRange.append(startPage)
        pageRange.append(endPage)
        
        self.logger.debug("Page range is (%s, %s, %s)" % (sectionName, startPage, endPage))
        return pageRange
    
    def getPageContent(self,pageNum):
        pageContentList = self.soup.find_all('div',{'id':pageNum})
        pageLen = len(pageContentList)
        
        if  1 == pageLen:
            return pageContentList[0]
        elif 1 < pageLen:
            self.logger.error("Find two same pageNum: %s" % pageNum)
        else:
            self.logger.error("pageLen=", pageLen)            
        return None

    
    def getTableinPage(self, pageNum):
        
        pageContent = self.getPageContent(pageNum)
        if pageContent == None:
            self.logger.error("Get page content None")
            return None
        
        pageElement = pageContent.div.div
        elementIndex = 0
        totalElemet = 0
        rowNum = 1            #保存有多少行
        columnNum = 1         #保存有多少列
        columnIndex = 1       #记录列的序号
        tableStartIndex = 0   #保存table开始时的元素位置
        tableEndIndex = 0     #保存table结束时的元素位置
        
        while True:
            if None != pageElement:
                if 'c' == pageElement['class'][0] and 'c' == pageElement.previous_sibling['class'][0]:
                    
                    #得到前列个元素
                    if columnNum == 1:
                        compareColumnElemnt = pageElement.previous_sibling
                    if columnNum == 2:
                        compareColumnElemnt = pageElement.previous_sibling.previous_sibling
                    if columnNum == 3:
                        compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling
                    if columnNum == 4:
                        compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling
                    if columnNum == 5:
                        compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
                    if columnNum == 6:
                        compareColumnElemnt = pageElement.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
                    
                    self.logger.debug("pageElement= %s, pre-pageElement= %s, compareColumnElemnt= %s" % (pageElement.get_text(), pageElement.previous_sibling.get_text(), compareColumnElemnt.get_text()))                    
                    self.logger.debug("pageElement Y= %s, pre-pageElement Y= %s" % (pageElement['class'][2], pageElement.previous_sibling['class'][2]))
                    self.logger.debug("pageElement X= %s, compareColumnElemnt X= %s" % (pageElement['class'][1], compareColumnElemnt['class'][1]))
                    self.logger.debug("pageElement = %s, pre-pageElement= %s, compareColumnElemnt= %s" % (pageElement.get_text(), pageElement.previous_sibling.get_text(), compareColumnElemnt.get_text()))
                    #print 'pageElement:', pageElement.get_text(),' pre-pageElement:',pageElement.previous_sibling.get_text(),'  compareColumnElemnt:', compareColumnElemnt.get_text()
                    #print 'pageElement Y:',pageElement['class'][2], 'pageElement.previous_sibling Y:',pageElement.previous_sibling['class'][2]
                    #print 'pageElement X:',pageElement['class'][1],'compareColumnElemnt X:',compareColumnElemnt['class'][1]
                    print 'columnNum =',columnNum
                    # 与前一个元素的Y坐标比较
                    if pageElement.previous_sibling['class'][2] == pageElement['class'][2]:    
                        columnIndex += 1
                        # 与前列个元素的X坐标比较
                        if pageElement['class'][1] != compareColumnElemnt['class'][1]:
                            columnNum = columnIndex
                            # 如果table没开始
                            if tableStartIndex == 0:
                                tableStartIndex = elementIndex
                                self.logger.info("Find a table in page:%s, table start index:%s" % (pageNum, tableStartIndex))
                                self.logger.debug("Find a cur-cell(rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex,pageElement.get_text()))
                                self.logger.debug("Find a pre-cell(rowIndex,columnIndex,value) (%s,%s,%s)" % (rowNum, columnIndex-1,pageElement.previous_sibling.get_text()))
                                
                                # Save cur-cell, pre-cell, tableStartIndex 
                                
                            else:
                                print 'save2 X element(row=',rowNum,',column=',columnIndex,',value=',pageElement.get_text(),',)'  
                        else:
                            print 'save3 X element(row=',rowNum,',column=',columnIndex,',value=',pageElement.get_text(),',)'
                    else:
                        if pageElement['class'][1] == compareColumnElemnt['class'][1]:
                            if tableStartIndex != 0:
                                rowNum += 1
                                columnNum = columnIndex
                                columnIndex = 1
                            print 'save4 X element(row=',rowNum,',column=',columnIndex,',value=',pageElement.get_text(),',)'
                        else:
                            # 与前一个Y坐标不等 与前列个X坐标不等 table结束
                            if tableStartIndex != 0:
                                tableEndIndex = elementIndex
                                print 'Table is end due to (X,Y)!=pre(X,Y): tableStartIndex=', tableStartIndex, 'tabEndIndex=', tableEndIndex
                            
                elif 't' == pageElement['class'][0]:
                    if tableStartIndex != 0:
                        tableEndIndex = elementIndex
                        print 'Table is end due to find t after table: tableStartIndex=', tableStartIndex, 'tabEndIndex=', tableEndIndex
                
            elif None == pageElement:
                if tableStartIndex != 0:
                    tableEndIndex = elementIndex
                    print 'Table is end due to page end: tableStartIndex=', tableStartIndex, 'tabEndIndex=', tableEndIndex
                break
            else:
                print 'findTableinPage():ERROR' 
            pageElement =pageElement.next_sibling
            elementIndex += 1
        totalElemet = elementIndex
        print 'findTableinPage(): elementIndex=', elementIndex
        #for classC in classClist:
        #    index = +1
        #    if classClist[index] == None:
        #        break
                
        #    if classClist[index-1]['class'][3] == classClist[index]['class'][3]:
        #        continue
                    
        #    elif classClist[index-1]['class'][3] != classClist[index]['class'][3]:
        #        continue
                
                #print classC['class']
                #print classC.div.get_text()
         
        
if __name__ == '__main__':
    pdfhtmlextact = PdfHtmlExtractor('../2014.html')
    pageRange = pdfhtmlextact.getSectionStartEndPage(u" 财务报告")
    print pageRange
    #pageRange = pdfhtmlextact.soup.find_all('div',{'id':pageRange[0]})
    #if 1 < len(pagelist):
       #print "WRN there has more than one same page", pageRange[0] 
    #for page in pagelist:
        #page.next_sibling
    tableinpage = pdfhtmlextact.getTableinPage('pf3a')
