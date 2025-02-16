#!/usr/bin/python

# This Python script has been generated by the SKYDEL GNSS simulator
import sys

sys.path.append("../../")

import time
from datetime import datetime
from datetime import date
from skydelsdx import *
from skydelsdx.commands import *
from datetime import timedelta
import skydelsdx

from skydelsdx.units import Ecef
from skydelsdx.units import Lla
from skydelsdx.units import Attitude
from skydelsdx.units import toRadian
import csv
import sys
import codecs
import numpy as np

# timedelta.total_seconds() (line 63) need Python 2.7 and above
assert sys.version_info >= (2, 7)

# create a new simulation
sim = RemoteSimulator(True)
sim.connect()

# Fix the simulation parameters
sim.call(New(True))
sim.call(SetModulationTarget("DTA-2116", "", "", True, "uniqueId"))
sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA,G1", 50, False, "uniqueId"))
sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
sim.call(SetVehicleTrajectoryFixEcef("Fix", 3069028.047, 2509456.599, 4979704.738, 0, 0, 0))

SetVehicleType("Airborne / Spaceborne")

sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
sim.call(EnableSignalStrengthModel(False))
sim.call(EnableElevationMaskBelow(False))
sim.call(SetTropoModel("Saastamoinen"))
sim.call(SetIonoModel("Klobuchar"))
sim.call(SetLeapSecond(16))

sim.call(SetSignalPowerOffset("L1CA", 0))
sim.call(SetSignalPowerOffset("G1", 0))
sim.call(AddVehicleGainPatternOffset(GNSSBand.L1, -10, "Basic Antenna"))
sim.call(SetGlobalPowerOffset(-40))

# Start the simulation
sim.start()

print("First test Record mode ")
Psign = -200

idb = 0

# Decrease the power offset of 1dBm each 120s
while Psign <= -133:
    if idb != 0:
        Psign += 1
        sim.call(SetGlobalPowerOffset(-40 + idb))
    time.sleep(120)
    idb += 1

print("Second test Tracking mode ")

sim.call(SetGlobalPowerOffset(30))
Prec = -130

idb = 0

# Increase the power offset of 1dBm each 120s
while Prec > -200:
    if idb != 0:
        Prec -= 1
        sim.call(SetGlobalPowerOffset(30 - idb))
    time.sleep(120)
    idb += 1


sim.stop(1800.0)


sim.disconnect()
