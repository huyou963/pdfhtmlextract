#coding=gbk
import new
from win32print import EndPage
from BeautifulSoup import PageElement
__author__ = 'CQC'
# -*- coding:utf-8 -*-
 
import os
from bs4 import BeautifulSoup
import urllib2
import re
import table

class PdfHtmlExtractor(object):
    pdfhtmlfile = ''
    soup = ''
    
    def __init__(self, pdfhtmlfile):
        self.pdfhtmlfile = pdfhtmlfile
        self.soup = BeautifulSoup(open(self.pdfhtmlfile), "html.parser")
        
    def findSectionStartEndPage(self,sectionName):
        pageRange = []
        startPage = ''
        endPage = ''
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
        
        return pageRange
    
    def findPage(self,pageNum):
        print pageNum
        pageContentList = self.soup.find_all('div',{'id':pageNum})
        pageLen = len(pageContentList)
        
        if  1 == pageLen:
            return pageContentList[0]
        elif 1 < pageLen:
            print "findPage(): find two same page" 
        else:
            print "findPage(): pageLen =",pageLen
        
    #def findPageElemetNum(self, pageContent): 
        #return pageElementNum
    
    def findTableinPage(self, pageNum):
        
        pageContent = self.findPage(pageNum)
        #pageElementNum = self.findPageElemetNum(pageContent)
        
        #print pageContent.div.div['class']
        
        pageElement = pageContent.div.div
        elementIndex = 0
        totalElemet = 0
        rowNum = 1      #保存有多上行
        columnNum = 1      #保存有多少列
        columnIndex = 1
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
                    
                    print 'pageElement:', pageElement.get_text(),' pre-pageElement:',pageElement.previous_sibling.get_text(),'  compareColumnElemnt:', compareColumnElemnt.get_text()
                    print 'pageElement Y:',pageElement['class'][2], 'pageElement.previous_sibling Y:',pageElement.previous_sibling['class'][2]
                    print 'pageElement X:',pageElement['class'][1],'compareColumnElemnt X:',compareColumnElemnt['class'][1]
                    print 'columnNum =',columnNum
                    # 与前一个元素的Y坐标比较
                    if pageElement.previous_sibling['class'][2] == pageElement['class'][2]:    
                        # 与前列个元素的X坐标比较
                        columnIndex += 1
                        if pageElement['class'][1] != compareColumnElemnt['class'][1]:
                            columnNum = columnIndex
                            # 如果table没开始
                            if tableStartIndex == 0:
                                tableStartIndex = elementIndex
                                print 'table start, save X-1 element(row=',rowNum,',column=',columnIndex-1,',value=',pageElement.previous_sibling.get_text(),',)'
                                print 'save1 X element(row=',rowNum,',column=',columnIndex,',value=',pageElement.get_text(),',)' 
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
    pdfhtmlextact = PdfHtmlExtractor('2014.html')
    pageRange = pdfhtmlextact.findSectionStartEndPage(u" 财务报告")
    print pageRange
    #pageRange = pdfhtmlextact.soup.find_all('div',{'id':pageRange[0]})
    #if 1 < len(pagelist):
       #print "WRN there has more than one same page", pageRange[0] 
    #for page in pagelist:
        #page.next_sibling
    tableinpage = pdfhtmlextact.findTableinPage('pf3a')
