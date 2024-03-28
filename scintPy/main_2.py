from scipy.io import loadmat
import pandas as pd
import numpy as np
from genUAF2 import genUAF2


# S = loadmat("scintDat.mat")
# S_L2 = loadmat("scintDat_L2.mat")
#
# tkhist_gen = np.transpose(S['tkhist'])
# zkhist_gen = np.transpose(S['zkhist'])
#
# tkhist_gen_L2 = np.transpose(S_L2['tkhist_L2'])
# zkhist_gen_L2 = np.transpose(S_L2['zkhist_L2'])

S = loadmat("scintPyDat.mat")
S_L2 = loadmat("scintPyDat_L2.mat")
tkhist_gen = S['time']
zkhist_gen = S['data']
tkhist_gen_L2 = S_L2['time']
zkhist_gen_L2 = S_L2['data']

Tquiet = 2
prn = [2]

zkhist_2D = [zkhist_gen, zkhist_gen_L2]

appli_scint = genUAF2()
gen_param = appli_scint.gen_param(zkhist_2D, tkhist_gen, prn, Tquiet)
