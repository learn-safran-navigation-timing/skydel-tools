import os
import csv
import datetime
from datetime import date
from datetime import datetime as dt
from skydelsdx import *
from skydelsdx.commands import *

class SkydelSim():

    def __init__(self):
        pass

    def apply2skydel(self, scint_file):
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

        with open(scint_file, 'r') as fid_sat:
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
                day.append(int(float(row[0])))
                hour.append(int(float(row[1])))
                minute.append(int(float(row[2])))
                sec.append(int(float(row[3])))
                m_sec.append(float(row[4]))
                prn.append(int(float(row[5])))
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

        sim = RemoteSimulator()
        sim.connect()
        N = len(scint_dict["SIGNAL"])
        N_list = len(scint_dict["SIGNAL"][0])

        sim.start()

        simStartTime = sim.call(GetGpsStartTime())
        result = simStartTime.startTime()
        result = dt.strptime(str(result), "%Y-%m-%d %H:%M:%S")
        result = result.time()

        hour = result.hour
        min = result.minute
        sec = result.second

        start_sec = hour*3600 + min*60 + sec

        for i in range(0, N, 1):
            for k in range(0, N_list, 2):
                # L1 band
                power_loss = scint_dict["SIGNAL"][i][k]
                print(scint_dict["HOUR"][i][k] * 3600,  scint_dict["MINUTE"][i][k] * 60, scint_dict["SEC"][i][
                    k])
                elapsed_time = scint_dict["HOUR"][i][k] * 3600 + scint_dict["MINUTE"][i][k] * 60 + scint_dict["SEC"][i][
                    k]
                post_time = elapsed_time - start_sec
                cmd_apply_scint = SetMultipathForSV("L1CA", scint_dict["PRN"][i][k], power_loss, 0, 0, 0, 1,
                                                    "{8b643e39-9d47-4576-a390-89369eb414c2}")
                sim.post(cmd_apply_scint, post_time)
                print("Time:", start_sec, elapsed_time, post_time)
        sim.stop(1000000)

        sim.disconnect()
