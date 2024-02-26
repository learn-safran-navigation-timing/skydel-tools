#!/usr/bin/python
# This Python script illustrates basic commands to automate Skydel.
# Before running this script, make sure Skydel is runnin and the splash screen is closed.
import math

import numpy as np
import pyproj
import datetime
import skydelsdx
from skydelsdx.commands import *
import time
import os
import csv
import codecs
import sys


class ScenFunction():
    def __init(self, file_path):
        self.scen_file_path = file_path

    def scen_main(self, file_path, RADIO_TYPE):
        # # Connect
        # sim = skydelsdx.RemoteSimulator()
        # sim.setVerbose(True)
        # sim.connect() #same as sim.connect("localhost")
        # # Create new config
        # sim.call(New(True))

        # signals
        is_GPS = False
        is_GLONASS = False
        is_GALILEO = False
        is_BEIDOU = False
        is_QZSS = False
        is_IRNSS = False
        is_SBAS = False

        signal_upper_band = ""
        signal_lower_band = ""
        signal_lower_band2 = ""
        signal_lower_band_E6 = ""

        SkydelDictSdx = {'startDay': None,
                         'startTime': None,
                         'duration': None,
                         'startPos': None,
                         "GpsTotal": int,
                         "GlonassTotal": int,
                         "BeidouTotal": int,
                         "GalileoTotal": int,
                         "QzssTotal": int,
                         "IrnssTotal": int,
                         'BaseStationPos': None,
                         'RtcmConfig': None,
                         'ElevationMask': None,
                         'RandomMpCP': None,
                         'UserTrajectory': None,
                         'DefaultGpsSv': None,
                         'AntennaModel': None,
                         'LeverArm': list,
                         'GnssPowerOffsetMode': None,
                         'Signals_UpperLBand': None,
                         'Signals_LowerLBand': None,
                         'Signals_LowerLBand2': None,
                         'Signals_LowerLBandE6': None,
                         }

        SkydelDictPy = {'startTime': list,
                        'duration': str,
                        'startPos': list,
                        'BaseStationPos': str,
                        'RtcmConfig': str,
                        'ElevationMask': str,
                        'RandomMpCP': str,
                        'DefaultGpsSv': str,
                        'GnssPowerOffsetMode': str,
                        'AntennaModel': str,
                        'IonoModel': str,
                        'TropoModel': str,
                        "GpsTotal": int,
                        "GlonassTotal": int,
                        "BeidouTotal": int,
                        "GalileoTotal": int,
                        "QzssTotal": int,
                        "IrnssTotal": int,
                        'UserTrajectory': str,
                        'TrajectoryParameters': str,
                        'DurationMode': str,
                        'CircleParam': list,
                        'NmeaParam': str,
                        'TrajParam': str,
                        'LeverArm': None,
                        'Signals_UpperLBand_none': str,
                        'Signals_LowerLBand_none': str,
                        'Signals_LowerLBand2_none': str,
                        'Signals_LowerLBandE6_none': str,
                        'Signals_UpperLBand_dta_2115': str,
                        'Signals_LowerLBand_dta_2115': str,
                        'Signals_LowerLBand2_dta_2115': str,
                        'Signals_LowerLBandE6_dta_2115': str,
                        'Signals_UpperLBand_dta_2116': str,
                        'Signals_LowerLBand_dta_2116': str,
                        'Signals_LowerLBand2_dta_2116': str,
                        'Signals_LowerLBandE6_dta_2116': str,
                        }

        #f = open(file_path, 'r', encoding="utf-8")
        with open(file_path, 'r', encoding="utf-8") as f:
            # Save the file in a table
            # lines = f.readlines()
            #
            # lines_iter = iter(lines)

            self.GPS_list = list()
            self.Glonass_list = list()
            self.Galileo_list = list()
            self.Qzss_list = list()
            self.Irnss_list = list()
            self.Sbas_list = list()

            # Read the lines of the file
            for line in f:

                # Get all words of a line
                words = line.split()
                first_word = words[0]

                # if the first word is the time configuration
                if first_word == "StartTime":
                    date = words[1].split("/")
                    hour = words[2].split(":")
                    # sim.call(SetGpsStartTime(datetime.datetime(int(date[2]), int(date[0]), int(date[1]), int(hour[0]), int(hour[1]), int(hour[2]))))
                    SkydelDictPy["startTime"] = [int(date[2]), int(date[0]), int(date[1]), int(hour[0]), int(hour[1]),
                                                 int(hour[2])]
                    SkydelDictSdx["startDay"] = date
                    SkydelDictSdx["startTime"] = hour

                if first_word == "Duration":
                    days = words[1]
                    hours = words[2]
                    minutes = words[3]
                    duration_mode = words[4]
                    SkydelDictPy["DurationMode"] = int(duration_mode)
                    SkydelDictSdx["DurationMode"] = int(duration_mode)
                    # sim.call(SetDuration(int(days)*86400 + int(hours)*3600 + int(minutes)*60))
                    SkydelDictPy["Duration"] = int(days) * 86400 + int(hours) * 3600 + int(minutes) * 60
                    SkydelDictSdx["Duration"] = int(days) * 86400 + int(hours) * 3600 + int(minutes) * 60

                if first_word == "Startpos":
                    positionN = float(words[1]) * np.pi / 180
                    if float(words[3]) < 180:
                        positionE = float(words[3]) * np.pi / 180
                    else:
                        positionE = (180 - float(words[3]) % 180) * np.pi / 180
                    positionAlt = float(words[5])

                    SkydelDictPy["Startpos"] = ["Fix", positionN, positionE, positionAlt, 0, 0, 0]
                    SkydelDictSdx["Startpos"] = [positionN, positionE, positionAlt]
                    # sim.call(SetVehicleTrajectoryFix("Fix", positionN, positionE, positionAlt, 0, 0, 0))

                if first_word == "BaseStationPos":
                    pass

                if first_word == "RtcmConfig":
                    pass

                if first_word == "ElevationMask":
                    elevation_mask = words[1]
                    SkydelDictPy['ElevationMask'] = math.radians(float(elevation_mask))
                    SkydelDictSdx['ElevationMask'] = math.radians(float(elevation_mask))

                if first_word == "RandomMpCP":
                    pass

                if first_word == "DefaultGpsSv":
                    pass

                if first_word == "SvBlockIIA":
                    pass

                if first_word == "SvBlockIIR":
                    pass

                if first_word == "SvBlockIIF":
                    pass

                if first_word == "DefaultGlonass":
                    pass

                if first_word == "UserTrajectory":
                    trajectory_name = words[1]

                    if trajectory_name == "Static" or trajectory_name == "3GPP":

                        SkydelDictPy["UserTrajectory"] = trajectory_name
                        SkydelDictSdx["UserTrajectory"] = trajectory_name

                    elif trajectory_name == "Circle":

                        SkydelDictPy["UserTrajectory"] = trajectory_name
                        SkydelDictSdx["UserTrajectory"] = trajectory_name

                        # param_line = next(lines_iter)
                        #
                        # print(param_line)
                        # words = param_line.split()
                        # first_word = words[0]

                    elif "nmea" in trajectory_name.split("."):

                        SkydelDictPy["UserTrajectory"] = "NmeaFile"
                        SkydelDictSdx["UserTrajectory"] = "NmeaFile"

                        SkydelDictPy["NmeaParam"] = trajectory_name
                        SkydelDictSdx["NmeaParam"] = trajectory_name

                    elif "traj" in trajectory_name.split("."):

                        SkydelDictPy["UserTrajectory"] = "TrajFile"
                        SkydelDictSdx["UserTrajectory"] = "TrajFile"

                        SkydelDictPy["TrajParam"] = trajectory_name
                        SkydelDictSdx["TrajParam"] = trajectory_name

                    else:
                        pass

                if first_word == "TrajectoryParameters":
                    circle_diameter = words[1]
                    circle_speed = words[2]
                    if words[3] == 1:
                        clockwise = "true"
                    else:
                        clockwise = "false"

                    SkydelDictPy["CircleParam"] = [circle_diameter, circle_speed, clockwise]
                    SkydelDictSdx["CircleParam"] = [circle_diameter, circle_speed, clockwise]

                if first_word == "LeverArm":
                    dX_m = words[1]
                    dY_m = words[2]
                    dZ_m = words[3]

                    SkydelDictPy["LeverArm"] = [dX_m, dY_m, dZ_m]
                    print(dX_m, dY_m, dZ_m)

                    SkydelDictSdx["LeverArm"] = [dX_m, dY_m, dZ_m]
                    print(dX_m, dY_m, dZ_m)

                if first_word == "Ephemeris":
                    pass

                if first_word == "AntennaModel":
                    antenna_model = words[1]
                    SkydelDictPy['AntennaModel'] = antenna_model
                    SkydelDictSdx['AntennaModel'] = antenna_model
                    # SetVehicleAntennaGainCSV("C:/Users/Jean-Grace Oulai/Documents/Skydel-SDX/Templates/Antennas/Zero Antenna pattern.csv", AntennaPatternType.Custom, GNSSBand.L2, "Basic Antenna")

                    pass

                if first_word == "DeltaLSF":
                    pass

                if first_word == "GpsToUtcOffset":
                    pass

                if first_word == "IonoModel":
                    iono_model = words[1]
                    SkydelDictPy['IonoModel'] = iono_model
                    SkydelDictSdx['IonoModel'] = iono_model

                if first_word == "TropoModel":
                    tropo_model = words[1]
                    SkydelDictPy['TropoModel'] = tropo_model
                    SkydelDictSdx['TropoModel'] = tropo_model

                if first_word == "Temperature":
                    pass

                if first_word == "Pressure":
                    pass

                if first_word == "Humidity":
                    pass

                if first_word == "GnssPowerOffsetMode":
                    power_offset = words[1]
                    SkydelDictPy['GnssPowerOffsetMode'] = str(SetGlobalPowerOffset(int(power_offset)))
                    SkydelDictSdx['GnssPowerOffsetMode'] = power_offset

                if first_word == "UserTrajectory":
                    pass

                if first_word == "MultipathSignals":
                    pass

                ############################################ NoneRT ###################################################
                if RADIO_TYPE == "NoneRT" or RADIO_TYPE == "None":

                    if first_word == "GpsSatellites" and words[1] != str(0):
                        is_GPS = True
                        GPS_number = words[1]
                        SkydelDictPy["GpsTotal"] = GPS_number
                        SkydelDictSdx["GpsTotal"] = GPS_number

                    if first_word == "GlonassSatellites" and words[1] != str(0):
                        is_GLONASS = True
                        Glonass_number = words[1]
                        SkydelDictPy["GlonassTotal"] = Glonass_number
                        SkydelDictSdx["GlonassTotal"] = Glonass_number

                    if first_word == "GalileoSatellites" and words[1] != str(0):
                        is_GALILEO = True
                        print(is_GALILEO, words[1])
                        Galileo_number = words[1]
                        SkydelDictPy["GalileoTotal"] = Galileo_number
                        SkydelDictSdx["GalileoTotal"] = Galileo_number

                    if first_word == "BeiDouSatellites" and words[1] != str(0):
                        is_BEIDOU = True
                        Beidou_number = words[1]
                        SkydelDictPy["BeidouTotal"] = Beidou_number
                        SkydelDictSdx["BeidouTotal"] = Beidou_number

                    if first_word == "QZSSSatellites" and words[1] != str(0):
                        is_QZSS = True
                        QZSS_number = words[1]
                        SkydelDictPy["QzssTotal"] = QZSS_number
                        SkydelDictSdx["QzssTotal"] = QZSS_number

                    if first_word == "IRNSSSatellites" and words[1] != str(0):
                        is_IRNSS = True
                        IRNSS_number = words[1]
                        SkydelDictPy["IrnssTotal"] = IRNSS_number
                        SkydelDictSdx["IrnssTotal"] = IRNSS_number

                    if first_word == "SBASSatellites":
                        is_SBAS = True
                        SBAS_number = words[1]
                        SkydelDictPy["SbasTotal"] = SBAS_number
                        SkydelDictSdx["SbasTotal"] = SBAS_number

                    if first_word == "GPSL1CA" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1CA"
                        else:
                            signal_upper_band += ",L1CA"

                    if first_word == "GPSL1P" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1P"
                        else:
                            signal_upper_band += ",L1P"

                    if first_word == "GPSL1C" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1C"
                        else:
                            signal_upper_band += ",L1C"

                    if first_word == "GPSL2P" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L2P"
                        else:
                            signal_lower_band += ",L2P"

                    if first_word == "GPSL2C" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L2C"
                        else:
                            signal_lower_band += ",L2C"

                    if first_word == "GPSL5" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L5"
                        else:
                            signal_lower_band += ",L5"

                    if first_word == "GPSPY" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L5"
                        else:
                            signal_lower_band += ",L5"


                    if first_word == "GLOL1" and words[1] != str(0) and is_GLONASS:
                        if signal_upper_band == "":
                            signal_upper_band += "G1"
                        else:
                            signal_upper_band += ",G1"

                    if first_word == "GLOL2" and words[1] != str(0) and is_GLONASS:
                        if signal_lower_band == "":
                            signal_lower_band += "G2"
                        else:
                            signal_lower_band += ",G2"

                    if first_word == "GALE1" and words[1] != str(0) and is_GALILEO:
                        if signal_upper_band == "":
                            signal_upper_band += "E1"
                        else:
                            signal_upper_band += ",E1"

                    if first_word == "GALE5a" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band == "":
                            signal_lower_band += "E5a"
                        else:
                            signal_lower_band += ",E5a"

                    if first_word == "GALE5b" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band == "":
                            signal_lower_band += "E5b"
                        else:
                            signal_lower_band += ",E5b"

                    if first_word == "GALE6" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band_E6 == "":
                            signal_lower_band_E6 += "E6BC"
                        else:
                            signal_lower_band_E6 += ",E6BC"

                    if first_word == "BDSB1" and words[1] != str(0) and is_BEIDOU:
                        if signal_upper_band == "":
                            signal_upper_band += "B1"
                        else:
                            signal_upper_band += ",B1"

                    if first_word == "BDSB2" and words[1] != str(0) and is_BEIDOU:
                        if signal_lower_band == "":
                            signal_lower_band += "B2"
                        else:
                            signal_lower_band += ",B2"

                    if first_word == "BDSB1C" and words[1] != str(0) and is_BEIDOU:
                        if signal_upper_band == "":
                            signal_upper_band += "B1C"
                        else:
                            signal_upper_band += ",B1C"

                    if first_word == "BDSB2a" and words[1] != str(0) and is_BEIDOU:
                        if signal_lower_band == "":
                            signal_lower_band += "B2a"
                        else:
                            signal_lower_band += ",B2a"

                    if first_word == "BDSB3" and words[1] != str(0) and is_BEIDOU:
                        pass

                        # if signal_lower_band == "":
                        #     signal_lower_band += "B3I"
                        # else:
                        #     signal_lower_band += ",B3I"

                    if first_word == "QZSSL1CA" and words[1] != str(0) and is_QZSS:
                        if signal_upper_band == "":
                            signal_upper_band += "QZSSL1CA"
                        else:
                            signal_upper_band += ",QZSSL1CA"

                    if first_word == "QZSSL1SAIF" and words[1] != str(0) and is_QZSS:
                        if signal_upper_band == "":
                            signal_upper_band += "QZSSL1S"
                        else:
                            signal_upper_band += ",QZSSL1S"

                    if first_word == "QZSSL2C" and words[1] != str(0) and is_QZSS:
                        if signal_lower_band == "":
                            signal_lower_band += "QZSSL2C"
                        else:
                            signal_lower_band += ",QZSSL2C"

                    if first_word == "QZSSL5" and words[1] != str(0) and is_QZSS:
                        if signal_lower_band == "":
                            signal_lower_band += "QZSSL5"
                        else:
                            signal_lower_band += ",QZSSL5"

                    if first_word == "IRNSSL5" and words[1] != str(0) and is_IRNSS:
                        if signal_lower_band == "":
                            signal_lower_band += "NAVICL5"
                        else:
                            signal_lower_band += ",NAVICL5"

                    if first_word == "SBASL1" and words[1] != str(0) and is_SBAS:
                        if signal_upper_band == "":
                            signal_upper_band += "SBASL1"
                        else:
                            signal_upper_band += ",SBASL1"

                    if first_word == "SBASL5" and words[1] != str(0) and is_SBAS:
                        if signal_lower_band == "":
                            signal_lower_band += "SBASL5"
                        else:
                            signal_lower_band += ",SBASL5"

                    SkydelDictPy['Signals_UpperLBand_none'] = signal_upper_band
                    SkydelDictPy['Signals_LowerLBand_none'] = signal_lower_band
                    SkydelDictPy['Signals_LowerLBand2_none'] = signal_lower_band2
                    SkydelDictPy['Signals_LowerLBandE6_none'] = signal_lower_band_E6

                ############################################ DTA-2115B ###################################################
                if RADIO_TYPE == "DTA-2115B":

                    if first_word == "GpsSatellites" and words[1] != str(0):
                        is_GPS = True
                        GPS_number = words[1]
                        SkydelDictPy["GpsTotal"] = GPS_number
                        SkydelDictSdx["GpsTotal"] = GPS_number

                    if first_word == "GlonassSatellites" and words[1] != str(0):
                        is_GLONASS = True
                        Glonass_number = words[1]
                        SkydelDictPy["GlonassTotal"] = Glonass_number
                        SkydelDictSdx["GlonassTotal"] = Glonass_number

                    if first_word == "GalileoSatellites" and words[1] != str(0):
                        is_GALILEO = True
                        Galileo_number = words[1]
                        SkydelDictPy["GalileoTotal"] = Galileo_number
                        SkydelDictSdx["GalileoTotal"] = Galileo_number

                    if first_word == "BeiDouSatellites" and words[1] != str(0):
                        is_BEIDOU = True
                        Beidou_number = words[1]
                        SkydelDictPy["BeidouTotal"] = Beidou_number
                        SkydelDictSdx["BeidouTotal"] = Beidou_number

                    if first_word == "QZSSSatellites" and words[1] != str(0):
                        is_QZSS = True
                        QZSS_number = words[1]
                        SkydelDictPy["QzssTotal"] = QZSS_number
                        SkydelDictSdx["QzssTotal"] = QZSS_number

                    if first_word == "IRNSSSatellites" and words[1] != str(0):
                        is_IRNSS = True
                        IRNSS_number = words[1]
                        SkydelDictPy["IrnssTotal"] = IRNSS_number
                        SkydelDictSdx["IrnssTotal"] = IRNSS_number

                    if first_word == "SBASSatellites":
                        is_SBAS = True
                        SBAS_number = words[1]
                        SkydelDictPy["SbasTotal"] = SBAS_number
                        SkydelDictSdx["SbasTotal"] = SBAS_number

                    if first_word == "GPSL1CA" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1CA"
                        else:
                            signal_upper_band += ",L1CA"

                    if first_word == "GPSL1P" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1P"
                        else:
                            signal_upper_band += ",L1P"

                    if first_word == "GPSL1C" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1C"
                        else:
                            signal_upper_band += ",L1C"

                    if first_word == "GPSL2P" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L2P"
                        else:
                            signal_lower_band += ",L2P"

                    if first_word == "GPSL2C" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L2C"
                        else:
                            signal_lower_band += ",L2C"

                    if first_word == "GPSL5" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L5"
                        else:
                            signal_lower_band += ",L5"

                    if first_word == "GPSPY" and words[1] != str(0) and is_GPS:
                        is_SBAS = True

                    if first_word == "GLOL1" and words[1] != str(0) and is_GLONASS:
                        if signal_upper_band == "":
                            signal_upper_band += "G1"
                        else:
                            signal_upper_band += ",G1"

                    if first_word == "GLOL2" and words[1] != str(0) and is_GLONASS:
                        if signal_lower_band2 == "":
                            signal_lower_band2 += "G2"
                        else:
                            signal_lower_band2 += ",G2"

                    if first_word == "GALE1" and words[1] != str(0) and is_GALILEO:
                        if signal_upper_band == "":
                            signal_upper_band += "E1"
                        else:
                            signal_upper_band += ",E1"

                    if first_word == "GALE5a" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band == "":
                            signal_lower_band += "E5a"
                        else:
                            signal_lower_band += ",E5a"

                    if first_word == "GALE5b" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band == "":
                            signal_lower_band += "E5b"
                        else:
                            signal_lower_band += ",E5b"

                    if first_word == "GALE6" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band_E6 == "":
                            signal_lower_band_E6 += "E6BC"
                        else:
                            signal_lower_band_E6 += ",E6BC"

                    if first_word == "BDSB1" and words[1] != str(0) and is_BEIDOU:
                        if signal_upper_band == "":
                            signal_upper_band += "B1"
                        else:
                            signal_upper_band += ",B1"

                    if first_word == "BDSB2" and words[1] != str(0) and is_BEIDOU:
                        if signal_lower_band == "":
                            signal_lower_band += "B2"
                        else:
                            signal_lower_band += ",B2"

                    if first_word == "BDSB1C" and words[1] != str(0) and is_BEIDOU:
                        if signal_upper_band == "":
                            signal_upper_band += "B1C"
                        else:
                            signal_upper_band += ",B1C"

                    if first_word == "BDSB2a" and words[1] != str(0) and is_BEIDOU:
                        if signal_lower_band == "":
                            signal_lower_band += "B2a"
                        else:
                            signal_lower_band += ",B2a"

                    if first_word == "BDSB3" and words[1] != str(0) and is_BEIDOU:
                        pass
                        # if signal_lower_band == "":
                        #     signal_lower_band += "B3I"
                        # else:
                        #     signal_lower_band += ",B3I"

                    if first_word == "QZSSL1CA" and words[1] != str(0) and is_QZSS:
                        if signal_upper_band == "":
                            signal_upper_band += "QZSSL1CA"
                        else:
                            signal_upper_band += ",QZSSL1CA"

                    if first_word == "QZSSL1SAIF" and words[1] != str(0) and is_QZSS:
                        if signal_upper_band == "":
                            signal_upper_band += "QZSSL1S"
                        else:
                            signal_upper_band += ",QZSSL1S"

                    if first_word == "QZSSL2C" and words[1] != str(0) and is_QZSS:
                        if signal_lower_band == "":
                            signal_lower_band += "QZSSL2C"
                        else:
                            signal_lower_band += ",QZSSL2C"

                    if first_word == "QZSSL5" and words[1] != str(0) and is_QZSS:
                        if signal_lower_band == "":
                            signal_lower_band += "QZSSL5"
                        else:
                            signal_lower_band += ",QZSSL5"

                    if first_word == "IRNSSL5" and words[1] != str(0) and is_IRNSS:
                        if signal_lower_band == "":
                            signal_lower_band += "NAVICL5"
                        else:
                            signal_lower_band += ",NAVICL5"

                    if first_word == "SBASL1" and words[1] != str(0) and is_SBAS:
                        if signal_upper_band == "":
                            signal_upper_band += "SBASL1"
                        else:
                            signal_upper_band += ",SBASL1"

                    if first_word == "SBASL5" and words[1] != str(0) and is_SBAS:
                        if signal_lower_band == "":
                            signal_lower_band += "SBASL5"
                        else:
                            signal_lower_band += ",SBASL5"
                    SkydelDictPy['Signals_UpperLBand_dta_2115'] = signal_upper_band
                    SkydelDictPy['Signals_LowerLBand_dta_2115'] = signal_lower_band
                    SkydelDictPy['Signals_LowerLBand2_dta_2115'] = signal_lower_band2
                    SkydelDictPy['Signals_LowerLBandE6_dta_2115'] = signal_lower_band_E6

                ############################################ DTA-2116 ###################################################
                if RADIO_TYPE == "DTA-2116":

                    if first_word == "GpsSatellites" and words[1] != str(0):
                        is_GPS = True
                        GPS_number = words[1]
                        SkydelDictPy["GpsTotal"] = GPS_number
                        SkydelDictSdx["GpsTotal"] = GPS_number

                    if first_word == "GlonassSatellites" and words[1] != str(0):
                        is_GLONASS = True
                        Glonass_number = words[1]
                        SkydelDictPy["GlonassTotal"] = Glonass_number
                        SkydelDictSdx["GlonassTotal"] = Glonass_number

                    if first_word == "GalileoSatellites" and words[1] != str(0):
                        is_GALILEO = True
                        Galileo_number = words[1]
                        SkydelDictPy["GalileoTotal"] = Galileo_number
                        SkydelDictSdx["GalileoTotal"] = Galileo_number

                    if first_word == "BeiDouSatellites" and words[1] != str(0):
                        is_BEIDOU = True
                        Beidou_number = words[1]
                        SkydelDictPy["BeidouTotal"] = Beidou_number
                        SkydelDictSdx["BeidouTotal"] = Beidou_number

                    if first_word == "QZSSSatellites" and words[1] != str(0):
                        is_QZSS = True
                        QZSS_number = words[1]
                        SkydelDictPy["QzssTotal"] = QZSS_number
                        SkydelDictSdx["QzssTotal"] = QZSS_number

                    if first_word == "IRNSSSatellites" and words[1] != str(0):
                        is_IRNSS = True
                        IRNSS_number = words[1]
                        SkydelDictPy["IrnssTotal"] = IRNSS_number
                        SkydelDictSdx["IrnssTotal"] = IRNSS_number

                    if first_word == "SBASSatellites":
                        is_SBAS = True
                        SBAS_number = words[1]
                        SkydelDictPy["SbasTotal"] = SBAS_number
                        SkydelDictSdx["SbasTotal"] = SBAS_number

                    if first_word == "GPSL1CA" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1CA"
                        else:
                            signal_upper_band += ",L1CA"

                    if first_word == "GPSL1P" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1P"
                        else:
                            signal_upper_band += ",L1P"

                    if first_word == "GPSL1C" and words[1] != str(0) and is_GPS:
                        if signal_upper_band == "":
                            signal_upper_band += "L1C"
                        else:
                            signal_upper_band += ",L1C"

                    if first_word == "GPSL2P" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L2P"
                        else:
                            signal_lower_band += ",L2P"

                    if first_word == "GPSL2C" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L2C"
                        else:
                            signal_lower_band += ",L2C"

                    if first_word == "GPSL5" and words[1] != str(0) and is_GPS:
                        if signal_lower_band == "":
                            signal_lower_band += "L5"
                        else:
                            signal_lower_band += ",L5"

                    if first_word == "GPSPY" and words[1] != str(0) and is_GPS:
                        is_SBAS = True

                    if first_word == "GLOL1" and words[1] != str(0) and is_GLONASS:
                        if signal_upper_band == "":
                            signal_upper_band += "G1"
                        else:
                            signal_upper_band += ",G1"

                    if first_word == "GLOL2" and words[1] != str(0) and is_GLONASS:
                        if signal_lower_band == "":
                            signal_lower_band += "G2"
                        else:
                            signal_lower_band += ",G2"

                    if first_word == "GALE1" and words[1] != str(0) and is_GALILEO:
                        if signal_upper_band == "":
                            signal_upper_band += "E1"
                        else:
                            signal_upper_band += ",E1"

                    if first_word == "GALE5a" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band == "":
                            signal_lower_band += "E5a"
                        else:
                            signal_lower_band += ",E5a"

                    if first_word == "GALE5b" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band == "":
                            signal_lower_band += "E5b"
                        else:
                            signal_lower_band += ",E5b"

                    if first_word == "GALE6" and words[1] != str(0) and is_GALILEO:
                        if signal_lower_band_E6 == "":
                            signal_lower_band_E6 += "E6BC"
                        else:
                            signal_lower_band_E6 += ",E6BC"

                    if first_word == "BDSB1" and words[1] != str(0) and is_BEIDOU:
                        if signal_upper_band == "":
                            signal_upper_band += "B1"
                        else:
                            signal_upper_band += ",B1"

                    if first_word == "BDSB2" and words[1] != str(0) and is_BEIDOU:
                        if signal_lower_band == "":
                            signal_lower_band += "B2"
                        else:
                            signal_lower_band += ",B2"

                    if first_word == "BDSB1C" and words[1] != str(0) and is_BEIDOU:
                        if signal_upper_band == "":
                            signal_upper_band += "B1C"
                        else:
                            signal_upper_band += ",B1C"

                    if first_word == "BDSB2a" and words[1] != str(0) and is_BEIDOU:
                        if signal_lower_band == "":
                            signal_lower_band += "B2a"
                        else:
                            signal_lower_band += ",B2a"

                    if first_word == "BDSB3" and words[1] != str(0) and is_BEIDOU:
                        pass
                        # if signal_lower_band == "":
                        #     signal_lower_band += "B3I"
                        # else:
                        #     signal_lower_band += ",B3I"

                    if first_word == "QZSSL1CA" and words[1] != str(0) and is_QZSS:
                        if signal_upper_band == "":
                            signal_upper_band += "QZSSL1CA"
                        else:
                            signal_upper_band += ",QZSSL1CA"

                    if first_word == "QZSSL1SAIF" and words[1] != str(0) and is_QZSS:
                        if signal_upper_band == "":
                            signal_upper_band += "QZSSL1S"
                        else:
                            signal_upper_band += ",QZSSL1S"

                    if first_word == "QZSSL2C" and words[1] != str(0) and is_QZSS:
                        if signal_lower_band == "":
                            signal_lower_band += "QZSSL2C"
                        else:
                            signal_lower_band += ",QZSSL2C"

                    if first_word == "QZSSL5" and words[1] != str(0) and is_QZSS:
                        if signal_lower_band == "":
                            signal_lower_band += "QZSSL5"
                        else:
                            signal_lower_band += ",QZSSL5"

                    if first_word == "IRNSSL5" and words[1] != str(0) and is_IRNSS:
                        if signal_lower_band == "":
                            signal_lower_band += "NAVICL5"
                        else:
                            signal_lower_band += ",NAVICL5"

                    if first_word == "SBASL1" and words[1] != str(0) and is_SBAS:
                        if signal_upper_band == "":
                            signal_upper_band += "SBASL1"
                        else:
                            signal_upper_band += ",SBASL1"

                    if first_word == "SBASL5" and words[1] != str(0) and is_SBAS:
                        if signal_lower_band == "":
                            signal_lower_band += "SBASL5"
                        else:
                            signal_lower_band += ",SBASL5"

                    SkydelDictPy['Signals_UpperLBand_dta_2116'] = signal_upper_band
                    SkydelDictPy['Signals_LowerLBand_dta_2116'] = signal_lower_band
                    SkydelDictPy['Signals_LowerLBand2_dta_2116'] = signal_lower_band2
                    SkydelDictPy['Signals_LowerLBandE6_dta_2116'] = signal_lower_band_E6

                if first_word == "InterferenceSignals":
                    break


            print(SkydelDictPy['Signals_UpperLBand_none'], 0)
            print(SkydelDictPy['Signals_LowerLBand_none'], 1)
            print(SkydelDictPy['Signals_LowerLBand2_none'], 2)
            print(SkydelDictPy['Signals_LowerLBandE6_none'], 3)

            print(SkydelDictPy['Signals_UpperLBand_dta_2115'], 0)
            print(SkydelDictPy['Signals_LowerLBand_dta_2115'], 1)
            print(SkydelDictPy['Signals_LowerLBand2_dta_2115'], 2)
            print(SkydelDictPy['Signals_LowerLBandE6_dta_2115'], 3)

            print(SkydelDictPy['Signals_UpperLBand_dta_2116'], 0)
            print(SkydelDictPy['Signals_LowerLBand_dta_2116'], 1)
            print(SkydelDictPy['Signals_LowerLBand2_dta_2116'], 2)
            print(SkydelDictPy['Signals_LowerLBandE6_dta_2116'], 3)

            return SkydelDictPy, SkydelDictSdx
#
# sim.call(SetVehicleTrajectoryCircular("Circular", 0.7853995339022749, -1.2740964277717111, 0, 50, 3, True))
#
# sim.call(SetVehicleAntennaGain([], AntennaPatternType.AntennaNone, GNSSBand.L1))

# Arm the simulation
# sim.arm()

# # Asynchronous command examples

# # Set +5 dB of manual power offset to all signals of satellite 13
# sim.post(SetManualPowerOffsetForSV("GPS", 13, {"All": 5}, False))

# # When simulation elapsed time is 9.567 sec, set -25 dB of manual power offset to signal L1CA of satellite 18
# cmd1 = sim.post(SetManualPowerOffsetForSV("GPS", 18, {"L1CA": -25}, False), 9.567)

# # When simulation elapsed time is 12.05 sec, add 10 dB of manual power offset to all signals of satellite 29
# cmd2 = sim.post(SetManualPowerOffsetForSV("GPS", 29, {"All": 10}, True), 12.05)

# # Start the simulation
# sim.start()

# time.sleep(10)

# # Right after start, set -15 dB of manual power offset to all signals of satellite 15
# sim.call(SetManualPowerOffsetForSV("GPS", 15, {"All": -15}, False))

# # Wait for commands to complete
# sim.wait(cmd1)
# sim.wait(cmd2)

# # When simulation elapsed time is 15, reset all satellites manual power offsets
# sim.call(ResetManualPowerOffsets("GPS"), 15)

# # Pause vehicle motion and resume at 18 sec
# sim.call(Pause())
# sim.call(Resume(), 18)

# # Stop simulation when elapsed time is 20 sec
# sim.stop(20)

# #sim.call(Quit(True)) #will quit Skydel

# sim.disconnect()
#
# if __name__=="__main__":
#     file_path = "C:\\Users\\Jean-Grace Oulai\\Desktop\\test_GSG6\\A3GPP130.scen"
#
#     RADIO_TYPE = "DTA-2116"
#
#     a = ScenFunction()
#     a.scen_main(file_path, RADIO_TYPE)
