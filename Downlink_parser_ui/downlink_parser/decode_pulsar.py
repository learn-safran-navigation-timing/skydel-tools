#!/usr/bin/python
"""
    Messages supported :
        PULSAR NAV
"""

from downlink_parser import utility

PulsarDict = [
    {'name':"preamble",     'range':[0,  31]},
    
    {'name':"tors",         'range':[32, 63]},
    {'name':"iodrs",        'range':[64, 67]},
    {'name':"ssi",          'range':[68, 69]},
    {'name':"reserved1",    'range':[70, 71]},
    {'name':"svID",         'range':[72, 87]},
    {'name':"healthStatus", 'range':[88, 95]},

    {'name':"af0",          'range':[96, 131], 'signed':True, 'factor':2**-35, 'unit':utility.SECOND},
    {'name':"af1",          'range':[132,159], 'signed':True, 'factor':2**-43, 'unit':utility.SECOND_PER_SECOND},
    {'name':"dpr",          'range':[160,175], 'signed':True, 'factor':2**-10, 'unit':utility.METER},
    {'name':"dpa",          'range':[176,191], 'signed':True, 'factor':2**-10, 'unit':utility.METER},
    {'name':"dpc",          'range':[192,207], 'signed':True, 'factor':2**-10, 'unit':utility.METER},
    {'name':"dvr",          'range':[208,223], 'signed':True, 'factor':2**-15, 'unit':utility.METER_PER_SECOND},
    {'name':"dva",          'range':[224,239], 'signed':True, 'factor':2**-15, 'unit':utility.METER_PER_SECOND},
    {'name':"dvc",          'range':[240,255], 'signed':True, 'factor':2**-15, 'unit':utility.METER_PER_SECOND},
    {'name':"toc",          'range':[256,271], 'signed':True,                  'unit':utility.SECOND},
    {'name':"iode",         'range':[272,275]},
    {'name':"reserved2",    'range':[276,279]},
    {'name':"CRC",          'range':[280,303]},
    
    {'name':"MT#1",           'range':[304,311]},
    {'name':"iode MT#1",      'range':[312,315]},
    {'name':"reserved1 MT#1", 'range':[316,319]},
    {'name':"toe",            'range':[320,351],                                  'unit':utility.SECOND},
    {'name':"cfi",            'range':[352,367],                                  'unit':utility.SECOND},
    {'name':"sqrtA",          'range':[368,399],                'factor':2**-19,  'unit':utility.METER},
    {'name':"e",              'range':[400,431],                'factor':2**-33},
    {'name':"i0",             'range':[432,463], 'signed':True, 'factor':2**-31,  'unit':utility.SEMICIRCLE},
    {'name':"omega",          'range':[464,495], 'signed':True, 'factor':2**-31,  'unit':utility.SEMICIRCLE},
    {'name':"omega0",         'range':[496,527], 'signed':True, 'factor':2**-31,  'unit':utility.SEMICIRCLE},
    {'name':"m0",             'range':[528,559], 'signed':True, 'factor':2**-31,  'unit':utility.SEMICIRCLE},
    {'name':"reserbed2 MT#1", 'range':[560,591]},

    {'name':"MT#2",               'range':[592,599]},
    {'name':"iode MT#2",          'range':[600,603]},
    {'name':"reserved1 MT#2",     'range':[604,607]},
    {'name':"crs",                'range':[608,623], 'signed':True, 'factor':2**-3,  'unit':utility.METER},
    {'name':"crc",                'range':[624,639], 'signed':True, 'factor':2**-3,  'unit':utility.METER},
    {'name':"cis",                'range':[640,655], 'signed':True, 'factor':2**-27, 'unit':utility.RADIAN},
    {'name':"cic",                'range':[656,671], 'signed':True, 'factor':2**-27, 'unit':utility.RADIAN},
    {'name':"cus",                'range':[672,687], 'signed':True, 'factor':2**-27, 'unit':utility.RADIAN},
    {'name':"cuc",                'range':[688,703], 'signed':True, 'factor':2**-27, 'unit':utility.RADIAN},
    {'name':"idot",               'range':[704,719], 'signed':True, 'factor':2**-36, 'unit':utility.SEMICIRCLE_PER_SECOND},
    {'name':"omegaDot",           'range':[720,751], 'signed':True, 'factor':2**-43, 'unit':utility.SEMICIRCLE_PER_SECOND},
    {'name':"deltan",             'range':[752,767], 'signed':True, 'factor':2**-37, 'unit':utility.SEMICIRCLE_PER_SECOND},
    {'name':"scaleExponent MT#2", 'range':[768,775]},
    {'name':"e1_1 MT#2",          'range':[776,783]},
    {'name':"e2_2 MT#2",          'range':[784,791]},
    {'name':"e3_3 MT#2",          'range':[792,799]},
    {'name':"e4_4 MT#2",          'range':[800,807]},
    {'name':"e1_2 MT#2",          'range':[808,815], 'signed':True},
    {'name':"e1_3 MT#2",          'range':[816,823], 'signed':True},
    {'name':"e1_4 MT#2",          'range':[824,831], 'signed':True},
    {'name':"e2_3 MT#2",          'range':[832,839], 'signed':True},
    {'name':"e2_4 MT#2",          'range':[840,847], 'signed':True},
    {'name':"e3_4 MT#2",          'range':[848,855], 'signed':True},
    {'name':"reserved2 MT#2",     'range':[856,879]},

    {'name':"MT#3",               'range':[880,887]},
    {'name':"iode MT#3",          'range':[888,891]},
    {'name':"reserved1 MT#3",     'range':[892,895]},
    {'name':"toPV",               'range':[896,927],                                  'unit':utility.SECOND},
    {'name':"px",                 'range':[928,959],   'signed':True, 'factor':2**-8, 'unit':utility.METER},
    {'name':"py",                 'range':[960,991],   'signed':True, 'factor':2**-8, 'unit':utility.METER},
    {'name':"pz",                 'range':[992,1023],  'signed':True, 'factor':2**-8, 'unit':utility.METER},
    {'name':"vx",                 'range':[1024,1039], 'signed':True, 'factor':2**-8, 'unit':utility.METER_PER_SECOND},
    {'name':"vy",                 'range':[1040,1055], 'signed':True, 'factor':2**-8, 'unit':utility.METER_PER_SECOND},
    {'name':"vz",                 'range':[1056,1071], 'signed':True, 'factor':2**-8, 'unit':utility.METER_PER_SECOND},
    {'name':"scaleExponent MT#3", 'range':[1072,1079]},
    {'name':"e1_1 MT#3",          'range':[1080,1087]},
    {'name':"e2_2 MT#3",          'range':[1088,1095]},
    {'name':"e3_3 MT#3",          'range':[1096,1103]},
    {'name':"e4_4 MT#3",          'range':[1104,1111]},
    {'name':"e1_2 MT#3",          'range':[1112,1119], 'signed':True},
    {'name':"e1_3 MT#3",          'range':[1120,1127], 'signed':True},
    {'name':"e1_4 MT#3",          'range':[1128,1135], 'signed':True},
    {'name':"e2_3 MT#3",          'range':[1136,1143], 'signed':True},
    {'name':"e2_4 MT#3",          'range':[1144,1151], 'signed':True},
    {'name':"e3_4 MT#3",          'range':[1152,1159], 'signed':True},
    {'name':"reserved2 MT#3",     'range':[1160,1167]},

    {'name':"MT#4",         'range':[1168,1175]},
    {'name':"Payload MT#4", 'range':[1176,1455]},

    {'name':"MT#5",         'range':[1456,1463]},
    {'name':"Payload MT#5", 'range':[1464,1743]},

    {'name':"Parity",       'range':[1744,1999]}
    ]

"""
    Main functions for decoding a PULSAR downlink navigation message.
"""

def getDictPulsarNavigationMessage(message):
    dictToUse = PulsarDict
    binaryMessage = utility.convertToBinaryNavigationMessage(message, 2016)

    return utility.fillDict(binaryMessage, dictToUse)
