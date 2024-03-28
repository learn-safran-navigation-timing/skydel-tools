import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import butter, lfilter

import random
from statistics import mean

"""Version 2 --- Outputs both samples spaced by Ts seconds (zScint) and
%               averages over Ts seconds that are also spaced by Ts seconds
%               (zScintA).  Only the underlying high-sample-rate zScintC
%               (effectively continuous time) is normalized so that
%               E[|zScintC(k)|^2] = 1.  Hence, zScint and zScintA are only
%               approximately normalized.

 Version 3 --- Like Version 2 but assumes a 2nd-order Butterworth power
%               spectrum given by Sxx(f) = 1/[1 + 16 (f^4/Bd^4)], where Bd =
%               sqrt(2)*beta0/(pi*tau0) is the fading bandwidth, with beta0
%               = 1.23964643681047.  Hence, the scintillaiton model only
%               depends on tau0 and K, nothing else.  Also, the number of
%               samples per average is made an input.

 Version 4 --- Like Version 3 but uses an actual 2nd-order Butterworth
%               filter instead of a spectral weighting function to
%               produce the time histories of scintillation.

 INPUTS
% Ts           Sampling interval of the output time histories zScint and
%              zScintA, in seconds

Nt           Number of samples in the output time histories zScint
%              and zScintA.

tau0         The decorrelation time (in seconds) of the 2nd-order
%              Butterworth model used to generate the scintillation.

K            The Ricean K (noncentrality) parameter

Nspa         Number of sub-samples that are used in calculating the
              averages in zScintA.  Using more sub-samples increases the
             accuracy of the averages at the expense of a greater
             computational burden.

OUTPUTS
 zScint       Nt-by-1 vector containing the normalized complex
              scintillation time history in the form of samples with
              sampling interval Ts.  zScint(k) is the sample taken at
              time tScint(k).

% zScintA      Nt-by-1 vector containing the normalized complex scintillation
%              time history in the form of averages over Ts with sampling
%              interval Ts.  zScintA(kp1) is the average over tk to tkp1.
% 
% tScint       Nt-by-1 vector of time points corresponding to zScint

+------------------------------------------------------------------+
References: Humphreys et al., Simulating Ionosphere-Induced Scintillation
 for Testing GPS Receiver Phase Tracking Loops, In preparation for submission to an IEEE journal.
% 
% Notes:  K is related to S4 under the Ricean model by 
%         K = sqrt(m^2 - m)/(m - sqrt(m^2 - m)) where 
%         m = max(1,1/(S4^2)).
%
% Author:  Todd Humphreys
+==================================================================+
"""

class Model04():

    def __int__(self):
        self.Ts = int()
        self.Nt = int()
        #self.tau0 = int()
        self.K = int()
        self.Nspa = int()

    # Simulates a realistic complex scintillation time history.

    # def model_scint(self, Ts, Nt, tau0, K, Nspa):
    #
    #     TsSub = Ts / Nspa
    #     tScint = []
    #
    #     Nt = int(Nt)
    #     # For convenience, make Ns even
    #     Ns = Nt * Nspa
    #     Ns = int(Ns)
    #
    #     for i in range(0, Ns - 1, 1):
    #         tScint.append(i * TsSub)
    #
    #     # tScint = [0:Ns-1]*TsSub
    #     print(TsSub, Ns, tScint)
    #
    #     # df = 1/tScint(end)
    #
    #     beta0 = 1.23964643681047
    #
    #     # ----- Set up the Butterworth filter
    #     # See Eq. 3.8 in the scintillation modeling paper
    #     print(tau0)
    #     Bd = beta0 / (math.sqrt(2) * math.pi * int(tau0))
    #     fn = 0.5 * (1 / TsSub)
    #     Wn = Bd / fn
    #     #Wn_array = np.array(Bd) / fn
    #     #print(Wn)
    #     # [B,A] = butter(2,Wn)
    #     # B, A = signal.butter(2, Wn, analog=False, 'low')
    #     B, A = signal.butter(2, Wn)
    #     # output = signal.filtfilt(B, A, signalc)
    #     # ----- Filter white noise to produce a time history with the correct
    #     #      power spectrum.
    #     # nVec = random.randint(Ns,1) + j*random.randint(Ns,1)
    #     print(Ns)
    #     nVec = np.random.randn(Ns) + 1j*np.random.randn(Ns)
    #
    #     #nVec = np.random.normal(loc=0, scale=1, size=Ns) + np.random.normal(loc=0, scale=1, size=Ns) * 1j
    #     # xiScint = filter(B,A,nVec);
    #
    #     xiScint = signal.lfilter(B, A, nVec)
    #     # xiScint = signal.lfilter(B, A, xiScint)
    #
    #     # ----- Add the line of sight component to get zScint
    #     # Calculate the mean squared value sigmaxi2
    #
    #     temp_xs = np.conj(xiScint)
    #     sigmaxi = xiScint * temp_xs
    #     sigmaxi2 = 0.5 * mean(sigmaxi.real)
    #     # Calculate the required value for the line-of sight component zBar.
    #     # This comes from the definition of the Ricean K parameter: K = (zBar^2/2)/sigmaxi2
    #     zBar = math.sqrt(2 * sigmaxi2 * K)
    #     # zScintC represents the high sampling rate (quasi continuous time) time
    #     # history of the complex scintillation
    #     zScintC = zBar + xiScint
    #     # Normalize zScintC so that E[|zScintC(k)|^2] = 1.
    #
    #     step_1 = abs(zScintC) * abs(zScintC)
    #     step_2 = mean(step_1)
    #     step3 = math.sqrt(step_2)
    #     zScintC = zScintC / step3
    #
    #     # ----- Sample zScintC to get zScint
    #
    #     # disp(Nspa)
    #     iidum = []
    #     zScint = []
    #
    #     for x in range(1, Ns, Nspa):
    #         print(x)
    #         iidum.append(x)
    #         zScint.append(zScintC[x])
    #
    #     # zScint = zScintC(iidum)
    #
    #     tScint = []
    #     for t in range(0, Nt, 1):
    #         print(t)
    #         tScint.append(t * Ts)
    #
    #     # ----- Average zScintC to get zScintA
    #     s = (Nspa, Nt)
    #     M_0 = np.zeros(s)
    #     M = np.array(zScintC).reshape((Nspa, Nt))
    #     zScintA = np.conj(np.mean(M, axis=0))
    #
    #     return zScint, zScintA, tScint


    def model_scint(self, Ts, Nt, tau0, K, Nspa):
        Nt = int(Nt)
        TsSub = Ts / Nspa
        # For convenience, make Ns even
        Ns = Nt * Nspa
        Ns = int(Ns)

        tScint = np.arange(Ns) * TsSub
        df = 1 / tScint[-1]
        beta0 = 1.23964643681047
        # ----- Set up the Butterworth filter
        #Bd = beta0 / (np.sqrt(2) * np.pi * tau0)
        Bd = beta0 / (math.sqrt(2) * math.pi * float(tau0))

        fn = 0.5 * (1 / TsSub)
        Wn = Bd / fn
        B, A = butter(2, Wn)
        # ----- Filter white noise to produce a time history with the correct power spectrum.
        nVec = np.random.randn(Ns) + 1j * np.random.randn(Ns)
        xiScint = lfilter(B, A, nVec)
        # ----- Add the line of sight component to get zScint
        sigmaxi2 = 0.5 * np.mean(xiScint * np.conj(xiScint))
        zBar = np.sqrt(2 * sigmaxi2 * K)
        zScintC = zBar + xiScint
        zScintC = zScintC / np.sqrt(np.mean(np.abs(zScintC) ** 2))
        # ----- Sample zScintC to get zScint
        iidum = np.arange(0, Ns, Nspa)
        zScint = zScintC[iidum]
        tScint = np.arange(Nt) * Ts
        # ----- Average zScintC to get zScintA
        M = np.zeros((Nspa, Nt), dtype=np.complex_)
        M.flat = zScintC
        zScintA = np.conj(np.mean(M, axis=0))
        print("A")

        return zScint, zScintA, tScint



