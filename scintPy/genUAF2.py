# function [] = genUAF2(zkhist,tkhist,prn,Tquiet)

# genUAF2        Generate a User Actions File from a scintillation time history
#
# Created by Joanna Hinks and Todd Humphreys, 29 May 2008.
#
# INPUTS
# zkhist         Nt-by-2-by-Ns matrix containing the normalized complex scintillation
#                time histories that will be used to drive variations in the
#                L1 and/or L2 output signal of the RF signal simulator.
#                Column 1 contains the L1 scintillation history column 2
#                contains the L2 scintillation history. A column of zeros
#                means no scintillation will be commanded for that
#                frequency. The dimension Ns corresponds to the satellite 
#                prn number. The time history is expressed in the form of 
#                averages over Ts with sampling interval Ts.  zkhist(kp1,L,s) 
#                is the average over tk to tkp1 for the frequency L and prn s.
#
# tkhist         Nt-by-1 vector of time points corresponding to zkhist.
#                The sampling interval Ts = tkhist(ii+1)  - tkhist(ii). 
#
# prn            Ns-by-1 vector of PRN identifiers of the GPS satellites 
#                whose signals will be commanded to scintillate (in the same 
#                order in which the 3-dimensional zkhist matrix is
#                stacked).
#
# Tquiet         Length of the quiet interval (no scintillation) that
#                precedes the onset of the scintillation interval, in
#                seconds.  The quiet interval allows the tracking loops of 
#                the receiver under test to lock and settle.
#

# Check dimensions of zkhist (must be Nt x 2 x Ns)
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
from PyQt5.QtWidgets import QMessageBox


class genUAF2:

    def __int__(self):

        self.zkhist = []
        self.tkhist = []
        self.prn = []
        self.Tquiet = int()


    def gen_param(self, zkhist, tkhist, prn, Tquiet, gen_file, custom_time):

        gen_filednames = ['day', 'hour', 'minute', 'sec', 'round(csec)', 'prn', 'Lvec', 'signal level', 'phase hist']

        gen_file_open = open(gen_file, 'w', newline='')
        gen_file_writer = csv.DictWriter(gen_file_open, fieldnames=gen_filednames)
        gen_file_writer.writeheader()

        tkhist = np.transpose(tkhist)
        zkhist = np.transpose(zkhist)

        temp_val_1 = zkhist[0, :, :]
        temp_val_1 = temp_val_1[0]
        lz = len(temp_val_1)

        temp_val_2 = zkhist[0, :, :]
        lprn = len(temp_val_2)

        if lz != 2:
            print('Input zkhist is not correctly formatted.')
        #
        Ns = len(prn)
        Ts = 100 * (tkhist[1][0] - tkhist[0][0])

        Tonset = Tquiet + Ts / 100
        Tonset = round(Tonset * 100) / 100
        Tonset_temp = Tonset

        noL1 = 0
        noL2 = 0
        sum_z_1 = []

        size_zkhist = zkhist.shape

        sum_z1 = 0
        sum_z2 = 0

        z_1 = zkhist[:, :, 0]
        for el1 in z_1:
            if el1[0] != 0:
                sum_z1 += 1
        if sum_z1 == 0:
            noL1 = 1

        z_2 = zkhist[:, :, 1]
        for el2 in z_2:
            if el2[0] != 0:
                sum_z2 += 1
        if sum_z2 == 0:
            noL2 = 1

        if noL1 and noL2:
            print('No scintillation commanded on any frequency')
        elif noL1:
            zkhist = zkhist[:, :, 0]
        elif noL2:
            zkhist = zkhist[:, :, 1]

        NL = size_zkhist[2]
        if NL == 2:
            Lvec = [0, 1]
        else:
            Lvec = noL1

        # Determine constant sampling rate (in units of csec)
        Ts = 100 * (tkhist[1] - tkhist[0])
        Nt = len(tkhist)
        day = Tonset // (60 * 60 * 24)
        Tresidual = Tonset - day * 60 * 60 * 24
        hour = Tresidual // (60 * 60)
        Tresidual = Tresidual - hour * 60 * 60
        minute = Tresidual // 60
        Tresidual = Tresidual - minute * 60
        sec = Tresidual // 1
        csec = round((Tresidual - sec) * 100)

        hour = float(str(custom_time[0]))
        minute = float(str(custom_time[1]))
        sec = float(str(custom_time[2]))

        # Separate out amplitude and phase information.
        amphist = np.abs(zkhist)
        phasehist = np.unwrap(np.angle(zkhist))

        # Compute change in signal level from amphist
        sig_level = 10 * np.log10(amphist ** 2)

        # Convert change in phase from radians to meters
        lambdavec = [0.190293672798365, 0.244210213424568]

        for ii in range(0, NL, 1):
            lam = lambdavec[Lvec[ii]]
            pha = phasehist[:, :, ii]
            phasehist[:, :, ii] = (pha / (2 * math.pi)) * lam

        time_list = []
        sig_level_list = []
        phase_level_list = []

        # Create file and write command lines
        for k in range(0, Nt, 1):
            for f in range(0, NL, 1):
                for s in range(0, Ns, 1):
                    print(day, hour, minute, sec, csec, prn[s], Lvec[f], "signal level:", sig_level[k, :, f][s],
                          "phase:", phasehist[k, :, f][s])

                    gen_file_writer.writerow(
                        {'day': day, 'hour': hour, 'minute': minute, 'sec': sec, 'round(csec)': csec,
                         'prn': prn[s], 'Lvec': Lvec[f], 'signal level': sig_level[k, :, f][s],
                         'phase hist': phasehist[k, :, f][s]})

                    time_list.append(day * 24 * 60 * 60 + hour * 60 * 60 + minute * 60 + sec)
                    sig_level_list.append(sig_level[k, :, f][s])
                    phase_level_list.append(phasehist[k, :, f][s])


            csec = csec + Ts[0]
            if csec >= 100:
                sec = sec + 1
                csec = csec - 100

            if sec >= 60:
                minute = minute + 1
                sec = 0

            if minute >= 60:
                hour = hour + 1
                minute = 0

            if hour >= 24:
                day = day + 1
                hour = 0

        plt.figure()
        plt.subplot(211)
        plt.plot(time_list, sig_level_list)
        plt.ylabel("Signal level(dB)")
        plt.xlabel("Time (s)")

        plt.subplot(212)
        plt.plot(time_list, phase_level_list)
        plt.ylabel("Phase (rad)")
        plt.xlabel("Time (s)")

        plt.show()

        # #Zero the output once scintillation has ended
        for f in range(0, NL, 1):
            for s in range(0, Ns, 1):
                print(day, hour, minute, sec, csec, prn[s], Lvec[f])
                gen_file_writer.writerow(
                    {'day': day, 'hour': hour, 'minute': minute, 'sec': sec, 'round(csec)': csec,
                     'prn': prn[s], 'Lvec': Lvec[f], 'signal level': 0,
                     'phase hist': 0})
        # #Close file
        # #fclose(fid);

