################################################################################
# @name             Channel Number\Frequency convert to each other
# @
# @date                  2016-03-24
# @author                Yunpeng
# @version               v1
#################################################################################



EARFCN = {            #every row stand for: band:Fdl_low[Mhz],Noffs-DL,Range of Ndl,Ful_low[Mhz],Noffs-UL,Range of Nul.(this information is get from 3GPP 36141v1114)
        1:[2110,0,range(600),1920,18000,range(18000,186000)],
        2:[1930,600,range(600,1200),1850,18600,range(18600,19200)],
        3:[1805,1200,range(1200,1950),1710,19200,range(19200,19950)],
        4:[2110,1950,range(1950,2400),1710,19950,range(19950,20400)],
        5:[869,2400,range(2400,2650),824,20400,range(20400,20650)],
        6:[875,2650,range(2650,2750),830,20650,range(20650,20750)],
        7:[2620,2750,range(2750,3450),2500,20750,range(20750,21450)],
        8:[925,3450,range(3450,3800),880,21450,range(21450,21800)],
        9:[1844.9,3800,range(3800,4149),1749.9,21800,range(21800,22149)],
        10:[2110,4150,range(4150,4750),1710,22150,range(22150,22745)],
        11:[1475.9,4750,range(4750,4950),1427.9,22750,range(22750,22950)],
        12:[729,5010,range(5010,5180),699,23010,range(23010,23180)],
        13:[746,5180,range(5180,5280),777,23180,range(23180,23280)],
        14:[758,5280,range(5280,5380),788,23280,range(23280,23379)],
        17:[734,5730,range(5730,5850),704,23730,range(23730,23850)],
        18:[860,5850,range(5850,6000),815,23850,range(23850,24000)],
        19:[875,6000,range(6000,6150),830,24000,range(24000,24150)],
        20:[791,6150,range(6150,6450),832,24150,range(24150,24450)],
        21:[1495.9,6450,range(6450,6600),1447.9,24450,range(24450,24600)],
        22:[3510,6600,range(6600,7400),3410,24600,range(24600,25399)],
        23:[2180,7500,range(7500,7700),2000,25500,range(25500,25699)],
        24:[1525,7700,range(7700,8040),1626.5,25700,range(25700,26040)],
        25:[1930,8040,range(8040,8690),1850,26040,range(26040,26690)],
        26:[859,8690,range(8690,9040),814,26690,range(26690,27040)],
        27:[852,9040,range(9040,9209),807,27040,range(27040,27210)],
        28:[758,9210,range(9210,9660),703,27210,range(27210,27660)],
        33:[1900,36000,range(36000,36200),1900,36000,range(36000,36200)],
        34:[2010,36200,range(36200,36350),2010,36200,range(36200,36350)],
        35:[1850,36350,range(36350,36950),1850,36350,range(36350,36950)],
        36:[1930,36950,range(36950,37550),1930,36950,range(36950,37550)],
        37:[1910,37550,range(37550,37750),1910,37550,range(37550,37750)],
        38:[2570,37750,range(37750,38250),2570,37750,range(37750,38250)],
        39:[1880,38250,range(38250,38650),1880,38250,range(38250,38650)],
        40:[2300,38650,range(38650,39650),2300,38650,range(38650,39650)],
        41:[2496,39650,range(39650,41590),2496,39650,range(39650,41590)],
        42:[3400,41590,range(41590,43590),3400,41590,range(41590,43590)],
        43:[3600,43590,range(43590,45590),3600,43590,range(43590,45590)],
        44:[703,45590,range(45590,46590),703,45590,range(45590,46590)]
        }
FDDbandPool = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,17,18,19,20,21,22,23,24,25,26,27,28]
TDDbandPool = [33,34,35,36,37,38,39,40,41,42,43,44]
        
def N2F(n):
    # transfer channel number to frequency
    f = 0.0
    N = int(n) # channel number should be a integer
    for i in FDDbandPool:
        if N in EARFCN[i][2]:
            Fdl = EARFCN[i][0] + 0.1*(N - EARFCN[i][1])
            print '@@ hi, this is a FDD-DL channel number ~'
            f = Fdl 
            return f
        if N in EARFCN[i][5]:
            Ful = EARFCN[i][3] + 0.1*(N - EARFCN[i][4])
            print '@@ hi, this is a FDD-UL channel number ~'
            f = Ful 
            return f
    if (f == 0.0):
        for i in TDDbandPool:
            if N in EARFCN[i][2]:
                Fdl = EARFCN[i][0] + 0.1*(N - EARFCN[i][1])
                print '@@ hi, this is a TDD channel number ~' # DL\UL frequency and channel number are same in TDD
                f = Fdl 
                return f
def F2N(F,band,DU):
    # tranfer frequency to channel number
    if 'DL' in DU or 'dl' in DU:
        Ndl = 10*(F - EARFCN[band][0]) + EARFCN[band][1]
        return Ndl
    if 'UL' in DU or 'ul' in DU:
        Nul = 10*(F - EARFCN[band][3]) + EARFCN[band][4]
        return Nul
        
print"\
#===================================\n\
#   Which transform you want to do ?\n\
#        1.Channel Number to Frequency\n\
#        2.Frequency to Channel Number\n\
#   Please input the choice[1 or 2]:"

NFchoice = raw_input('Your choice:>')  
if '1' in NFchoice:
    cnum = int(raw_input('#   Please tell me the Channel Number ~\nChannel_Number:>'))
    f = N2F(cnum)
    print ("matching frequency is [%s][Mhz]" % str(f))
if '2' in NFchoice:
    freq = float(raw_input('#   Please tell me the Frequency ~\nFrequency[Mhz]:>'))
    bandNum = int(raw_input('#   Please tell me the Band number[integer]\nBand number:>'))
    DU = raw_input('#   Please tell me this is a UL or DL frequency?\ntype "UL" or "DL":>')
    nn = int(F2N(freq,bandNum,DU))
    print 'matching Channel number is [%s]' % str(nn)