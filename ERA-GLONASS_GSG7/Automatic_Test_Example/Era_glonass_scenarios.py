# -*- coding: utf-8 -*-

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

# launch test Case 1
def Case1(constellation):
    if constellation == "GPS":
        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetLeapSecond(16))
        sim.call(SetVehicleTrajectoryFixEcef("Fix", 3069028.047, 2509456.599, 4979704.738, 0, 0, 0))

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("L1CA", 1.5))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

    elif constellation == "GLONASS":
        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "G1", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetLeapSecond(16))
        sim.call(SetVehicleTrajectoryFixEcef("Fix", 3069028.047, 2509456.599, 4979704.738, 0, 0, 0))

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("G1", -1))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

    else:
        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA,G1", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetLeapSecond(16))
        sim.call(SetVehicleTrajectoryFixEcef("Fix", 3069028.047, 2509456.599, 4979704.738, 0, 0, 0))

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("L1CA", 1.5))
        sim.call(SetSignalPowerOffset("G1", -1))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

# launch test Case 2
def Case2(constellation):
    if constellation == "GPS":
        FILE_PATH = r"../Trajectories/RsgERAGLONASSAcceleration.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetLeapSecond(16))
        sim.call(SetVehicleTrajectory("Track"))

        # Read the trajectory file
        sim.beginTrackDefinition()

        # print("Reading " + FILE_PATH)
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
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

    elif constellation == "GLONASS":
        FILE_PATH = r"../Trajectories/RsgERAGLONASSAcceleration.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "G1", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetLeapSecond(16))
        sim.call(SetVehicleTrajectory("Track"))

        # Read the trajectory file
        sim.beginTrackDefinition()

        # print("Reading " + FILE_PATH)
        with codecs.open(FILE_PATH, "rb", encoding="UTF-8") as f:
            reader = csv.reader(f)
            field_names = next(reader)  # Skip first line: CSV Header
            for row in reader:
                elapsedTime, xyz, ypr = readRow(row)
                sim.pushTrackLlaNed(elapsedTime, xyz, ypr)

        sim.endTrackDefinition()

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("G1", -1))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

    else:
        FILE_PATH = r"../Trajectories/RsgERAGLONASSAcceleration.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA,G1", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetLeapSecond(16))
        sim.call(SetVehicleTrajectory("Track"))

        # Read the trajectory file
        sim.beginTrackDefinition()

        # print("Reading " + FILE_PATH)
        with codecs.open(FILE_PATH, "rb", encoding="UTF-8") as f:
            reader = csv.reader(f)
            field_names = next(reader)  # Skip first line: CSV Header
            for row in reader:
                elapsedTime, xyz, ypr = readRow(row)
                sim.pushTrackLlaNed(elapsedTime, xyz, ypr)

        sim.endTrackDefinition()

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("L1CA", 1.5))
        sim.call(SetSignalPowerOffset("G1", -1))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

# launch test Case 3
def Case3(constellation):
    if constellation == "GPS":
        FILE_PATH = r"../Trajectories/RsgERAGLONASSManeuvering.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetVehicleTrajectory("Track"))

        sim.beginTrackDefinition()

        # Read the trajectory file
        # print("Reading " + FILE_PATH)
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
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

    elif constellation == "GLONASS":
        FILE_PATH = r"../Trajectories/RsgERAGLONASSManeuvering.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "G1", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetVehicleTrajectory("Track"))

        # Read the trajectory file
        sim.beginTrackDefinition()

        # print("Reading " + FILE_PATH)
        with codecs.open(FILE_PATH, "rb", encoding="UTF-8") as f:
            reader = csv.reader(f)
            field_names = next(reader)  # Skip first line: CSV Header
            for row in reader:
                elapsedTime, xyz, ypr = readRow(row)
                sim.pushTrackLlaNed(elapsedTime, xyz, ypr)

        sim.endTrackDefinition()

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("G1", -1))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

    else:
        FILE_PATH = r"../Trajectories/RsgERAGLONASSManeuvering.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA,G1", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetVehicleTrajectory("Track"))

        # Read the trajectory file
        sim.beginTrackDefinition()

        # print("Reading " + FILE_PATH)
        with codecs.open(FILE_PATH, "rb", encoding="UTF-8") as f:
            reader = csv.reader(f)
            field_names = next(reader)  # Skip first line: CSV Header
            for row in reader:
                elapsedTime, xyz, ypr = readRow(row)
                sim.pushTrackLlaNed(elapsedTime, xyz, ypr)

        sim.endTrackDefinition()

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("L1CA", 1.5))
        sim.call(SetSignalPowerOffset("G1", -1))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

# launch test Case 4
def Case4(constellation):
    if constellation == "GPS":
        FILE_PATH = r"../Trajectories/RsgERAGLONASSManeuveringInBlockage.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetVehicleTrajectory("Track"))

        # Read the trajectory file
        sim.beginTrackDefinition()

        # print("Reading " + FILE_PATH)
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
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

    elif constellation == "GLONASS":
        FILE_PATH = r"../Trajectories/RsgERAGLONASSManeuveringInBlockage.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "G1", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetVehicleTrajectory("Track"))

        # Read the trajectory file
        sim.beginTrackDefinition()

        # print("Reading " + FILE_PATH)
        with codecs.open(FILE_PATH, "rb", encoding="UTF-8") as f:
            reader = csv.reader(f)
            field_names = next(reader)  # Skip first line: CSV Header
            for row in reader:
                elapsedTime, xyz, ypr = readRow(row)
                sim.pushTrackLlaNed(elapsedTime, xyz, ypr)

        sim.endTrackDefinition()

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("G1", -1))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim

    else:
        FILE_PATH = r"../Trajectories/RsgERAGLONASSManeuveringInBlockage.csv"

        # create a new simulation
        sim = RemoteSimulator(True)
        sim.connect()

        # Fix the simulation parameters
        sim.call(New(True))
        sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA, G1", 50, False, "uniqueId"))
        sim.call(SetGpsStartTime(datetime(2015, 3, 5, 10, 0, 0)))
        sim.call(SetVehicleTrajectory("Track"))

        # Read the trajectory file
        sim.beginTrackDefinition()

        # print("Reading " + FILE_PATH)
        with codecs.open(FILE_PATH, "rb", encoding="UTF-8") as f:
            reader = csv.reader(f)
            field_names = next(reader)  # Skip first line: CSV Header
            for row in reader:
                elapsedTime, xyz, ypr = readRow(row)
                sim.pushTrackLlaNed(elapsedTime, xyz, ypr)

        sim.endTrackDefinition()

        SetVehicleType("Airborne / Spaceborne")

        sim.call(SetSignalPowerOffset("L1CA", 1.5))
        sim.call(SetSignalPowerOffset("G1", -1))
        sim.call(SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
        sim.call(EnableSignalStrengthModel(False))
        sim.call(EnableElevationMaskBelow(False))
        sim.call(SetIonoModel("Klobuchar"))
        sim.call(SetTropoModel("Saastamoinen"))
        sim.call(SetLeapSecond(16))

        return sim
