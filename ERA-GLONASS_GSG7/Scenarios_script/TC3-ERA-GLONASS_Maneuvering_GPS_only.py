#!/usr/bin/python

# This Python script has been generated by the SKYDEL GNSS simulator
import sys

sys.path.append("../../")

FILE_PATH = r"../Trajectories/RsgERAGLONASSManeuvering.csv"

from datetime import datetime
from datetime import date
from skydelsdx import *
from skydelsdx.commands import *
from datetime import timedelta
import skydelsdx

# from skydelsdx.commands import New
# from skydelsdx.commands import SetModulationTarget
# from skydelsdx.commands import ChangeModulationTargetSignals
# from skydelsdx.commands import SetGpsStartTime
# from skydelsdx.commands import SetVehicleTrajectory
from skydelsdx.units import Ecef
from skydelsdx.units import Lla
from skydelsdx.units import Attitude
from skydelsdx.units import toRadian
import csv
import sys
import codecs
import numpy as np

# Read the trajectory file
def readRow(row):
    # Each row has [Time, X (km), Y (km), Z (km), Yaw (deg), Pitch (deg), Roll (deg)] as string
    time = int(row[0])
    L = toRadian(float(row[1]))
    l = toRadian(float(row[2]))
    h = toRadian(float(row[3]))
    yaw = toRadian(float(row[4]))
    pitch = toRadian(float(row[5]))
    roll = toRadian(float(row[6]))
    ypr = Attitude(yaw, pitch, roll)
    Llh = Lla(L, l, h)
    yield time
    yield Llh
    yield ypr


# timedelta.total_seconds() (line 63) need Python 2.7 and above
assert sys.version_info >= (2, 7)

# create a new simulation
sim = RemoteSimulator(True)
sim.connect()

# Fix the simulation parameters
sim.call(New(True))
sim.call(SetModulationTarget("DTA-2116", "", "", True, "uniqueId"))
sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA", 50, False, "uniqueId"))
sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
sim.call(SetVehicleTrajectory("Track"))

# Read the trajectory file
sim.beginTrackDefinition()

print("Reading " + FILE_PATH)
with codecs.open(FILE_PATH, "rb", encoding="UTF-8") as f:
    reader = csv.reader(f)
    field_names = next(reader)  # Skip first line: CSV Header
    for row in reader:
        elapsedTime, xyz, ypr = readRow(row)
        sim.pushTrackLlaNed(elapsedTime, xyz, ypr)

sim.endTrackDefinition()

SetVehicleType("Airborne / Spaceborne")

sim.call(SetSignalPowerOffset("L1CA", 1.5))
sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
sim.call(EnableSignalStrengthModel(False))
sim.call(EnableElevationMaskBelow(False))
sim.call(SetTropoModel("Saastamoinen"))
sim.call(SetIonoModel("Klobuchar"))
sim.call(SetLeapSecond(16))

# Save the NMEA data
sim.call(EnableLogNmea(True))
sim.call(SetLogNmeaRate(1))

# Start the simulation
sim.start()

sim.stop(3600.0)

sim.disconnect()
