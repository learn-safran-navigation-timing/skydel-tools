from scipy.io import loadmat
import pandas as pd
import numpy as np
from genUAF2 import genUAF2

class genCSV:

    def __init__(self):
        pass

    def get_csv(self, gen_csv, prn, custom_time):
        # Load the generated data matrix for L1 & L2
        dt_L1 = loadmat("scintPyDat.mat")
        dt_L2 = loadmat("scintPyDat_L2.mat")
        tkhist_gen_L1 = dt_L1['time']
        zkhist_gen_L1 = dt_L1['data']
        tkhist_gen_L2 = dt_L2['time']
        zkhist_gen_L2 = dt_L2['data']

        Tquiet = 2

        prn = [int(prn)]

        zkhist_2D = [zkhist_gen_L1, zkhist_gen_L2]

        appli_scint = genUAF2()
        appli_scint.gen_param(zkhist_2D, tkhist_gen_L1, prn, Tquiet, gen_csv, custom_time)
