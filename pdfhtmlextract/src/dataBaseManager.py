#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb

class dataBaseManager():
    conn=''
    cursor=''
    def openDataBase(self):
        # 打开数据连接
        self.conn = MySQLdb.connect("localhost","admin","huyou123",charset='utf8')
        # 使用cursor()方法获取操作游标 
        self.cursor = self.conn.cursor()
        dbName="stockData"
        #cursor.execute("create database %s" % dbName)
        self.cursor.execute("use %s" % dbName)
        
    def displayDataBase(self):
        self.cursor.execute("show databases")
        for db in self.cursor.fetchall():
            print db
            
    def createDataTable(self, datas):
        print "createDataTable:",datas[0]
        #sqlStr="create table stock"+datas[0]+ " if not exists " + "id int" 
        sqlStr="create table if not exists stock"+datas[0]
        sqlStr=sqlStr+"(id int(6) not null primary key auto_increment,"+"stockId int,company varchar(100)"
        for i in range(2, len(datas)):
            sqlStr = sqlStr+","+datas[i]+" double"
        sqlStr=sqlStr+")"
        print sqlStr
        self.cursor.execute(sqlStr)
        
    def insertDataInTable(self, recordsNames, datas):
        print "insertDataInTable:",datas[0]
        sqlStr="insert into stock"+recordsNames[0]+"(stockId"
        for i in range(1, len(recordsNames)):
            sqlStr = sqlStr+","+recordsNames[i]
        sqlStr=sqlStr+")" +" values("+datas[0]
        sqlStr=sqlStr+","+"'"+datas[1]+"'"
        for i in range(2, len(datas)):
            sqlStr = sqlStr+","+datas[i]
        sqlStr=sqlStr+")"
               
        print sqlStr
        self.cursor.execute(sqlStr)

    def displayDataTableRecords(self, stockNum):
        print "displayDataTableRecords:"
        sqlStr="SELECT column_name FROM information_schema.columns WHERE table_name='stock'"
        for field_desc in self.cursor.execute(sqlStr):
            print field_desc
    def closeDataBase(self, conn):
        cursor = conn.cursor()
        cursor.close()
        conn.commit()
        conn.close()

#recordsNames=["600004","company","aaa","bbb","ccc"]
#datas=["600004","ƽ��","111","222","333"]
#dm=dataBaseManager()
#dm.openDataBase()
#dm.displayDataBase()
#dm.createDataTable(recordsNames)
#dm.insertDataInTable(recordsNames, datas)
#dm.displayDataTableRecords(datas[0])
