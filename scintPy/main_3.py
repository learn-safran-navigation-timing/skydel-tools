import os
import csv
from datetime import datetime
from datetime import date
from skydelsdx import *
from skydelsdx.commands import *
import time

scint_data = "C://Users//Jean-Grace Oulai//Documents//GitHub//app-eng-scripts//scintPy//gen.csv"
scint_dict = {
              "DAY": [],
              "HOUR": [],
              "MINUTE": [],
              "SEC": [],
              "M_SEC": [],
              "PRN": [],
              "LVEC": [],
              "SIGNAL": [],
              "PHASE": []
              }

with open(scint_data, 'r') as fid_sat:
    lines = []
    day = []
    hour = []
    minute = []
    sec = []
    m_sec = []
    prn = []
    Lvec = []
    signal_level = []
    phase = []
    hist = []

    reader = csv.reader(fid_sat)
    next(reader)

    for row in reader:
        lines.append(row)
        day.append(int(row[0]))
        hour.append(int(row[1]))
        minute.append(int(row[2]))
        sec.append(int(row[3]))
        m_sec.append(float(row[4]))
        prn.append(int(row[5]))
        Lvec.append(float(row[6]))
        signal_level.append(float(row[7]))
        phase.append(float(row[8]))

scint_dict["DAY"].append(day)
scint_dict["HOUR"].append(hour)
scint_dict["MINUTE"].append(minute)
scint_dict["SEC"].append(sec)
scint_dict["M_SEC"].append(m_sec)
scint_dict["PRN"].append(prn)
scint_dict["LVEC"].append(Lvec)
scint_dict["SIGNAL"].append(signal_level)
scint_dict["PHASE"].append(day)

sim = RemoteSimulator(True)
sim.connect()

sim.call(New(True, True))
sim.call(New(True, True))
sim.call(SetModulationTarget("NoneRT", "", "", True, "{c2214639-6358-4589-9cbd-84b9e6bd3f6d}"))
sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000, "UpperL", "L1CA", 0, False, "{c2214639-6358-4589-9cbd-84b9e6bd3f6d}", None))

N = len(scint_dict["SIGNAL"])
N_list = len(scint_dict["SIGNAL"][0])

sim.start()
time.sleep(5)
for i in range(0, N, 1):
    for k in range(0, N_list, 2):
        # L1 band
        power_loss = scint_dict["SIGNAL"][i][k]
        print(scint_dict["HOUR"][i][k]*3600)
        elapsed_time = scint_dict["HOUR"][i][k]*3600 + scint_dict["MINUTE"][i][k]*60 + scint_dict["SEC"][i][k]
        print(elapsed_time)
        #id = "echo_prn_"
        cmd_apply_scint = SetMultipathForSV("L1CA", scint_dict["PRN"][i][k], power_loss, 0, 0, 0, 1, "{8b643e39-9d47-4576-a390-89369eb414c2}")
        sim.post(cmd_apply_scint, elapsed_time)

        # for k in range(1, N_list, 2):
        #     # L2 band
        #     power_loss = scint_dict["SIGNAL"][i][k]
        #     print(scint_dict["HOUR"][i][k] * 3600)
        #     elapsed_time = scint_dict["HOUR"][i][k] * 3600 + scint_dict["MINUTE"][i][k] * 60 + scint_dict["SEC"][i][k]
        #     print(elapsed_time)
        #     # id = "echo_prn_"
        #     cmd_apply_scint = SetMultipathForSV("L1CA", scint_dict["PRN"][i][k], power_loss, 0, 0, 0, 1,
        #                                         "{8b643e39-9d47-4576-a390-89369eb414c2}")
        #     sim.post(cmd_apply_scint, elapsed_time)
        #
sim.stop(1000000)

sim.disconnect()