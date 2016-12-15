#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# @version               v1
# @date                  2014-08-10
# @author                Yunpeng
#
# @Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import xlrd
import xlwt
import datetime

def testXlrd(filename):
    book=xlrd.open_workbook(filename)
    sh=book.sheet_by_index(0)
    print "Worksheet name(s): ",book.sheet_names()[0]
    print 'book.nsheets',book.nsheets
    print 'sh.name:',sh.name,'sh.nrows:',sh.nrows,'sh.ncols:',sh.ncols
    print 'A1:',sh.cell_value(rowx=0,colx=1)
    print 'A2:',sh.cell_value(0,2).encode('gb2312')

def testXlwt(filename):
    book=xlwt.Workbook()
    sheet1=book.add_sheet('RF_pTest')
    book.add_sheet('backinfo')
    # create title
    sheet1.write(0,0,'Results')
    sheet1.write(0,1,'TX_ACLR_B')
    sheet1.write(0,2,'TX_ACLR_M')
    sheet1.write(0,3,'TX_ACLR_T')
    sheet1.write(0,4,'TX_EVM_B')
    sheet1.write(0,5,'TX_EVM_M')
    sheet1.write(0,6,'TX_EVM_T')
    sheet1.write(0,7,'RX_EVM_B')
    sheet1.write(0,8,'RX_EVM_M')
    sheet1.write(0,9,'RX_EVM_T')

    sheet1.write(1,0,'Pipe1')
    sheet1.write(2,0,'Pipe2')
    sheet1.write(3,0,'Pipe3')

    row1 = sheet1.row(1)
    row1.write(1,'value1')
    row1.write(2,'value2')

    sheet1.col(0).width = 6000
    for i in range(1,10):
        sheet1.col(i).width = 3300

    sheet2 = book.get_sheet(1)
    sheet2.row(0).write(0,'Sheet 2 A1')
    sheet2.row(0).write(1,'Sheet 2 B1')
    sheet2.flush_row_data()

    sheet2.write(1,0,'Sheet 2 A3')
    sheet2.col(0).width = 5000
    sheet2.col(0).hidden = True

    book.save(filename)

if __name__=='__main__':
    #testXlrd(u'1.xls')
    testXlwt('RFtest_result.xls')
    base=datetime.date(1899,12,31).toordinal()
    tmp=datetime.date(2013,07,16).toordinal()
    print datetime.date.fromordinal(tmp+base-1).weekday()