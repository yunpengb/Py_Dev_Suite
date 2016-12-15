################################################################################
# @version               v1
# @date                  2015-08-10
# @author                Yunpeng
#
# Original author        Yunpeng
#
# Copyright 2015 Nokia Networks. All rights reserved.
################################################################################

import os
import sys
import telnetlib
from RS_calss import RS_Meter
import xlwt
import xlrd

def getAllfreq(row): # row and col is integer,begin from 0
    'this is just use for my own excel - Yunpeng'
    allFreq = [[],[]]
    book = xlrd.open_workbook('plan.xlsx')
    sheet = book.sheet_by_name('Freqtestplan')

    for j in range(10): # tx freq data
        for i in range(2,7):
            try:
                out = sheet.cell_value(row+i,3+j*4)
                if(out != ""):
                    allFreq[0].append(out)
            except:
                break

    for j in range(1,10): # rx freq data
        for i in range(2,7):
            try:
                out = sheet.cell_value(row+i,5+j*4)
                if(out != ""):
                    allFreq[1].append(out)
            except:
                break
    return allFreq

if __name__ == '__main__':
    fsv = "192.168.1.2"
    smu = "192.168.1.3"

    if(len(sys.argv) != 7):
        print()
        sys.exit(1)

    biao = RS_Meter(fsv,smu)

    biao.calcCableloss(pinlv,"0")

