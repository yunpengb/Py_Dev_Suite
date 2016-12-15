#!/usr/bin/python
# coding: utf-8

import xlwt
import sys
import time
import xlrd
from xlutils.copy import copy

def setstyle(fontsize,backcolor,bold=False,):
    style = xlwt.XFStyle()

    font = xlwt.Font()   #set font
    font.name = 'Times New Roman'
    font.size = fontsize
    font.bold = bold
    font.color_index = 4
    #font.height = height

    borders= xlwt.Borders()   #set border
    borders.left= 6
    borders.right= 6
    borders.top= 6
    borders.bottom= 6

    pattern = xlwt.Pattern() # set Pattern
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
    pattern.pattern_fore_colour = backcolor # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...


    style.font = font
    style.borders = borders
    style.pattern = pattern
    return style


def createEmptyXls(xlsName,sheetName):
    bookname = xlsName+'.xls'
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetName)
    wb.save(bookname)

def addData2Xls(Data,emptyXlsName,coords,datatype):
    carrierband = N[0][0]
    yvalue = int(coords)
    print yvalue
    doubleband = str(2*int(carrierband))
    typedict = {
               'txaclr':["TxAclr","carrierBand","freq","TxPower","Aclr_"+carrierband+"M_lower","Aclr_"+carrierband+"M_upper","Aclr_"+doubleband+"M_lower","Aclr_"+doubleband+"M_lower"],
               'txevm':["TxEvm","carrierBand","freq","TxEvm_average","TxEvm_max","TxEvm_min"],
               'rxevm':["RxEvm","carrierBand","freq","RxEvm_max","RxEvm_average","RxEvm_alignment"]
               }

    oldWorkbook = xlrd.open_workbook(emptyXlsName, formatting_info=True)
    newWorkbook = copy(oldWorkbook)
    newWS = newWorkbook.get_sheet(0)

    newWS.write(0, 0, "value1");

    #print header
    newWS.row(yvalue).height = 15
    newWS.col(0).width = 9
    newWS.col(1).width = 10
    newWS.col(2).width = 10
    for i in range(3,7):
        newWS.col(i).width= 17
    newWS.write(0,i,typedict[datatype][0])#setstyle(20,3,True))
    for i in range(1,len(typedict[datatype])):     #write header line
        newWS.write(0,i,typedict[datatype][i])#setstyle(20,22,True))

    for i in range(len(Data)):
        for j in range(len(Data[0])):
            newWS.write(yvalue+i,j+1,Data[i][j])#setstyle(10,1,False))
    newWorkbook.save(emptyXlsName)

timestamp = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
sheetname = "testResult_"+timestamp

createEmptyXls("goodone",sheetname)
N=[['10','5','3.1','1.2','-3100'],['10','5','2.9','1.1','-3300']]
print N
addData2Xls(N,"goodone.xls",'1','rxevm')