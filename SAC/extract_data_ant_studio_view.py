import numpy as np
from PyQt5.QtWidgets import QMessageBox


class ReadAnt:

    def __init__(self):
        pass

    def readFile(self, fileName, lineSkip):
        with open(fileName) as f:
            for i, l in enumerate(f):
                pass
        length = i + 1
        length_skipline = i + 1 - lineSkip

        with open(fileName, 'r') as f:
            lines = f.readlines()
            new_lines = lines[lineSkip:length]
            theta_sample = lines[2]
            theta_sample = theta_sample.split(': ')
            theta_sample = theta_sample[1]

            phi_sample = lines[3]
            phi_sample = phi_sample.split(': ')
            phi_sample = phi_sample[1]

        return new_lines, theta_sample, phi_sample, length_skipline

    def readline(self, new_lines, length_skipline):
        i = 0
        theta_elev = np.empty(length_skipline)
        phi_azim = np.empty(length_skipline)
        gain_total = np.empty(length_skipline)
        for line in new_lines:
            words = line.split()
            try:
                theta_elev[i] = np.float(words[0])
                phi_azim[i] = np.float(words[1])
                gain_total[i] = np.float(words[8])
            except:
                print(" ")
            i += 1
        return theta_elev, phi_azim, gain_total
