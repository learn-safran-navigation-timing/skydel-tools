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
import matplotlib.pyplot as plt
import cv2

import Era_glonass_scenarios as scr


####################### Test 5.1 / 5.2 / 5.3 #######################


def testPrecision(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, constellation):
    """Check if the receiver position is displayed on a map.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)
        constellation :: string
            Constellation used for the test

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    sim = scr.Case2(constellation)
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )
    sim.start()
    sim.stop(1800)
    sim.disconnect()
    success = input("\n Did the receiver display on the map with position and speed ? (Y/N) ")
    while success != "Y" and success != "N":
        success = input("\n Did the receiver display on the map with position and speed ? (Y/N) ")
    if success == "Y":
        return "Success"


####################### Test 5.4 #######################


def testNmea(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl):
    """Check if the NMEA are send by the receiver.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    sim = scr.Case1("GPS&GLONASS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )
    input(
        "\n During the simulation, visualize the NMEA frames of your receiver on a receiver interface on your computer. Press Enter to start the simulation. \n"
    )
    sim.start()
    sim.stop(1800)
    sim.disconnect()
    success = input("\n Have the NMEA navigation data been received and displayed on the receiver interface ? (Y/N) ")
    while success != "Y" and success != "N":
        success = input("\n Have the NMEA navigation data been received and displayed on the receiver interface ? (Y/N) ")
    if success == "Y":
        return "Success"


####################### Test 5.5 #######################


def testEphError(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl):
    """Check if the receiver is sentitive to ephemeris errors.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    sim = scr.Case1("GPS&GLONASS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input("\n During the simulation, check when the receiver lost the signal NSC. Press Enter to start the simulation. ")

    sim.start()

    cmd1 = SetMessageModificationToGpsLNav(
        ["L1CA"],
        7,
        600,
        0,
        1,
        0,
        3,
        True,
        "----000000000000--------------",
        "{9ae7e2ac-7941-4a7a-a0f0-4fa4f5e0644e}",
    )

    sim.post(cmd1, 600)
    sim.wait(cmd1)

    cmd2 = SetMessageModificationToGpsLNav(
        ["L1CA"],
        31,
        600,
        0,
        2,
        0,
        3,
        True,
        "----000000000000--------------",
        "{488aeb39-a3f6-47d6-b755-b245ee2564ac}",
    )

    sim.post(cmd2, 600)
    sim.wait(cmd2)

    cmd3 = SetMessageModificationToGlonassNav(
        ["G1"],
        7,
        600,
        0,
        1,
        1,
        True,
        "------------------------------------------------------00000000000--------------------",
        "{49e8a9dd-59ae-4bba-a659-51afde0bf7d9}",
    )

    sim.post(cmd3, 600)
    sim.wait(cmd3)

    sim.stop(1800)
    sim.disconnect()
    success = input("\n Did the receiver lost the signal 10min after the start of the simulation? (Y/N) ")
    while success != "Y" and success != "N":
        success = input("\n Did the receiver lost the signal 10min after the start of the simulation? (Y/N) ")
    if success == "Y":
        return "Success"


####################### Test 5.6 #######################


def testNavParam(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl):
    """Check the NMEA position data precision between two different coordinate systems.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    sim = scr.Case1("GPS")

    sim.call(EnableLogNmea(True))
    sim.call(SetLogNmeaRate(1))
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )
    input(
        "\n Configure the stream of the NMEA data of the receiver (GGA, RMC, VTG, GSA, DTM and GSV) with a frequency of 1Hz."
        " Press Enter when it is done."
    )
    input("\n During the simulation check if the DTM data are given in WGS84 on the receiver interface. Press Enter to start the simulation. ")

    sim.start()
    sim.stop(1800)
    sim.disconnect()

    nmeaOKGPS = input(
        "\n Check in the folder Skydel-SDX/Output/Untitled if the nmea_receiver.txt file is filled with at least GGA and RMC frames. (Y/N) "
    )
    while nmeaOKGPS != "Y" and nmeaOKGPS != "N":
        nmeaOKGPS = input(
            "\n Check in the folder Skydel-SDX/Output/Untitled if the nmea_receiver.txt file is filled with at least GGA and RMC frames. (Y/N) "
        )

    dtm_refGPS = input("\n Are the DTM data given in WGS84 on the receiver interface. (Y/N) ")
    while dtm_refGPS != "Y" and dtm_refGPS != "N":
        dtm_refGPS = input("\n Are the DTM data given in WGS84 on the receiver interface. (Y/N) ")

    input("\n Change the location of the file nmea_receiver.txt in Skydel-SDX/Output/Untitled in another folder. Press Enter When it is done.")

    # AND

    sim = scr.Case1("GLONASS")

    sim.call(EnableLogNmea(True))
    sim.call(SetLogNmeaRate(1))
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )
    input(
        "\n Configure the stream of the NMEA data of the receiver (GGA, RMC, VTG, GSA, DTM and GSV) "
        "with a frequency of 1Hz. Press Enter when it is done. "
    )

    input("\n During the simulation check if the DTM data are given in PZ90 on the receiver interface. Press Enter to start the simulation. ")

    sim.start()
    sim.stop(1800)
    sim.disconnect()

    nmeaOKGLONASS = input(
        "\n Check in the folder Skydel-SDX/Output/Untitled if the nmea_receiver.txt file is filled with at least GGA and RMC frames. (Y/N) "
    )
    while nmeaOKGLONASS != "Y" and nmeaOKGLONASS != "N":
        nmeaOKGLONASS = input(
            "\n Check in the folder Skydel-SDX/Output/Untitled if the nmea_receiver.txt file is filled with at least GGA and RMC frames. (Y/N) "
        )

    dtm_refGLONASS = input("\n Are the DTM data given in PZ90 on the receiver interface. (Y/N) ")
    while dtm_refGLONASS != "Y" and dtm_refGLONASS != "N":
        dtm_refGLONASS = input("\n Are the DTM data given in PZ90 on the receiver interface. (Y/N) ")

    input("\n Change the location of the file nmea_receiver.txt in Skydel-SDX/Output/Untitled in another folder. Press Enter When it is done.")

    input(
        """\n Select 50 GGA (RMC) sentences corresponding to the same time moments in both files :
          - convert the coordinates from a system to the other one
          - compare both coordinates
          - With a tolerance of 0.95 : 
              o delta plane value coordinates <= 15m 
              o delta altitude value coordinates <= 20m.
              
          Press Enter when it is done.    
          """
    )

    tolerance = input("\n Is the tolerance respected? (Y/N) ")
    while tolerance != "Y" and tolerance != "N":
        tolerance = input("\n Is the tolerance respected? (Y/N) ")

    if nmeaOKGPS == "Y" and dtm_refGPS == "Y" and nmeaOKGLONASS == "Y" and dtm_refGLONASS == "Y" and tolerance == "Y":
        return "Success"


####################### Test 5.7 / 5.8 #######################


def testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, system, velocity, case):
    """Check the precision of the NMEA data comparing the simulator and the receiver.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)
        system :: string
            Constellation used for the test
        velocity :: bool
            If the receiver is moving, velocity is True
        case :: string
            Scenario used for the test

    Returns:
        string
            'Success' if the test is successful, nothing if it is not
        mat_rec_gga :: array 
            Array of all positions and velocity given by the GGA of the receiver

    """

    sim = case(system)

    sim.call(EnableLogNmea(True))
    sim.call(SetLogNmeaRate(1))

    sim.start()
    sim.stop(3600)
    sim.disconnect()

    with open("../../../Output/Untitled/nmea_simulator.txt") as f:
        nb_gga_sim = 0
        nb_rmc_sim = 0
        lines_sim = f.readlines()
        list_gga_sim = []
        list_rmc_sim = []
        for line_sim in lines_sim:
            first_char = line_sim.find("$")
            line_sim = line_sim[first_char:]
            if line_sim[3:6] == "GGA":
                (idS, utctime, lat, lat_ori, long, long_ori, _, _, _, alt, _) = line_sim.split(",", 10)
                list_gga_sim.append([utctime, lat, long, alt])
                nb_gga_sim += 1
            elif line_sim[3:6] == "RMC":
                idS, utctime, _, _, _, speed, _ = line_sim.split(",", 6)
                list_rmc_sim.append([utctime, speed])
                nb_rmc_sim += 1

    mat_sim_gga_temp = np.zeros((nb_gga_sim, 4))
    for p in range(nb_gga_sim):
        mat_sim_gga_temp[p][:] = list_gga_sim[p]

    mat_sim_rmc_temp = np.zeros((nb_rmc_sim, 2))
    for q in range(nb_rmc_sim):
        mat_sim_rmc_temp[q][:] = list_rmc_sim[q]

    with open("../../../Output/Untitled/nmea_receiver.txt") as f:
        nb_gga_rec = 0
        nb_rmc_rec = 0
        lines_rec = f.readlines()
        list_gga_rec = []
        list_rmc_rec = []
        for line_rec in lines_rec:
            first_char = line_rec.find("$")
            line_rec = line_rec[first_char:]
            if line_rec[3:6] == "GGA":
                (idS, utctime, lat, lat_ori, long, long_ori, _, _, _, alt, _) = line_rec.split(",", 10)
                list_gga_rec.append([utctime, lat, long, alt])
                nb_gga_rec += 1
            elif line_rec[3:6] == "RMC":
                idS, utctime, _, _, _, speed, _ = line_rec.split(",", 6)
                list_rmc_rec.append([utctime, speed])
                nb_rmc_rec += 1

    mat_rec_gga = np.zeros((nb_gga_rec, 4))
    for l in range(nb_gga_rec):
        mat_rec_gga[l][:] = list_gga_rec[l]

    mat_rec_rmc = np.zeros((nb_rmc_rec, 2))
    for k in range(nb_rmc_rec):
        mat_rec_rmc[k][:] = list_rmc_rec[k]

    # Find the same gga in receiver and simulator
    mat_sim_gga = np.zeros((mat_rec_gga.shape))
    for i in range(len(mat_rec_gga)):
        idfix = np.where(mat_sim_gga_temp[:, 0] == mat_rec_gga[i, 0])
        int_id = int(idfix[0])
        mat_sim_gga[i, :] = mat_sim_gga_temp[int_id, :]

    # Find the same rmc in receiver and simulator
    mat_sim_rmc = np.zeros((mat_rec_rmc.shape))
    for j in range(len(mat_rec_rmc)):
        idfix_rmc = np.where(mat_sim_rmc_temp[:, 0] == mat_rec_rmc[j, 0])
        int_id_rmc = int(idfix_rmc[0])
        mat_sim_rmc[j, :] = mat_sim_rmc_temp[int_id_rmc, :]

    diff_array = np.absolute(mat_rec_gga[:, 1:] - mat_sim_gga[:, 1:])
    sys_err = np.mean(diff_array, axis=0)

    N = len(diff_array)
    a = 6378137.0
    f = 1 / 298.257223563
    b = a * (1 - f)
    e = np.sqrt((a**2 - b**2) / a**2)
    phi = mat_sim_gga[0, 0]

    dB = 2 * ((a * (1 - e**2)) / (1 - (e**2) * np.sin(phi) ** 2) ** 3 / 2) * ((0.5 * np.pi) / (180 * 3600)) * sys_err[0]

    dL = 2 * ((a * np.cos(phi)) / (1 - (e**2) * np.sin(phi) ** 2) ** 1 / 2) * ((0.5 * np.pi) / (180 * 3600)) * sys_err[1]

    sigmaB = np.sqrt(np.sum((diff_array[:, 0] - dB) ** 2) / (N - 1))

    sigmaL = np.sqrt(np.sum((diff_array[:, 1] - dL) ** 2) / (N - 1))

    sigmaH = np.sqrt(np.sum((diff_array[:, 2] - sys_err[2]) ** 2) / (N - 1))

    err_plan = np.sqrt(dB**2 + dL**2) + 2 * np.sqrt(sigmaB**2 + sigmaL**2)

    err_alti = sys_err[2] + 2 * sigmaH

    mean_plani = (sys_err[0] + sys_err[1]) / 2

    borne_plani = 1.96 * err_plan / np.sqrt(N)

    borne_alti = 1.96 * err_alti / np.sqrt(N)

    if velocity:
        diff_speed = np.absolute(mat_rec_rmc[:, 1] - mat_sim_rmc[:, 1])
        N_speed = len(diff_speed)
        dV = np.mean(diff_speed)
        sigmaV = np.sqrt(np.sum((diff_speed - dV) ** 2) / (N_speed - 1))
        err_speed = dV + 2 * sigmaV
        borne_speed = 1.96 * err_speed / np.sqrt(N_speed)

        if mean_plani - borne_plani <= 15 and sys_err[2] - borne_alti <= 20 and dV - borne_speed <= 0.1:
            return "Success", mat_rec_gga
        else:
            return "Failed", mat_rec_gga
    else:
        if mean_plani - borne_plani <= 15 and sys_err[2] - borne_alti <= 20:
            input(
                "\n The simulated test succeded. To completely achieve this test, you must do the part 5.7 of "
                "the norm in real time so that the navigation signals are transmitted"
                " from the antenna located at a geodetic point (check point) in response "
                "to real signals of GLONASS/GPS. The result of the real time test will not be"
                "taken in account for the result of the test. Press Enter. "
            )
            return "Success", mat_rec_gga
        else:
            return "Failed", mat_rec_gga


####################### Test 5.9 #######################


def testTimeInter(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, listOfGga):
    """Check that the position change between two consecutive GGA.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)
        listOfGga :: array
            Array of all positions and velocity given by the GGA of the receiver

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    for gga_tab in listOfGga:
        for i in range(len(gga_tab) - 1):
            if gga_tab[i, 1] == gga_tab[i + 1, 1] and gga_tab[i, 2] == gga_tab[i + 1, 2]:
                return "Failed"
    return "Success"


####################### Test 5.10 #######################


def testRecovery(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl):
    """Check the time the receiver spends to recover its position after disconnecting the simulator.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    print("\n Test with GPS only \n")
    sim = scr.Case1("GPS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input(
        "\n During the simulation, measure the time interval between the moment when the antenna is disconnected and reconnected and the moment when an indication"
        " that the tracking from the working NSC constellation has resumed appears in the interface program dialog. Press Enter to start the simulation. "
    )

    sim.start()

    time1 = 0

    while time1 < 10:

        time.sleep(60)
        sim.call(DisconnectSerialPortReceiver())

        time.sleep(30)
        sim.call(
            ConnectSerialPortReceiver(
                PortName,
                int(BaudRate),
                int(DataBits),
                int(Parity),
                int(StopBits),
                int(FlowControl),
            )
        )

        time1 += 1

    sim.stop(1800)
    sim.disconnect()

    successGPS = input("\n Are positions recovered in less than 5s in average time? (Y/N) ")
    while successGPS != "Y" and successGPS != "N":
        successGPS = input("\n Are positions recovered in less than 5s in average time? (Y/N) ")

    # AND
    print("\n Test with GLONASS only \n")
    sim = scr.Case1("GLONASS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input(
        "\n During the simulation, measure the time interval between the moment when the antenna is disconnected and reconnected and the moment when an indication that "
        "the tracking from the working NSC constellation has resumed appears in the interface program dialog. Press Enter to start the simulation. "
    )

    sim.start()

    time1 = 0

    while time1 < 10:

        time.sleep(60)
        sim.call(DisconnectSerialPortReceiver())

        time.sleep(30)
        sim.call(
            ConnectSerialPortReceiver(
                PortName,
                int(BaudRate),
                int(DataBits),
                int(Parity),
                int(StopBits),
                int(FlowControl),
            )
        )

        time1 += 1

    sim.stop(1800)
    sim.disconnect()

    successGLONASS = input("\n Are positions recovered in less than 5s in average time? (Y/N) ")
    while successGLONASS != "Y" and successGLONASS != "N":
        successGLONASS = input("\n Are positions recovered in less than 5s in average time? (Y/N) ")

    # AND

    print("\n Test with GLONASS and GPS \n")
    sim = scr.Case1("GPS&GLONASS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input(
        "\n During the simulation, measure the time interval between the moment when the antenna is disconnected and reconnected and the moment when an indication that the tracking from the working NSC constellation has resumed appears in the interface program dialog. Press Enter to start the simulation. "
    )

    sim.start()

    time1 = 0

    while time1 < 10:

        time.sleep(60)
        sim.call(DisconnectSerialPortReceiver())

        time.sleep(30)
        sim.call(
            ConnectSerialPortReceiver(
                PortName,
                int(BaudRate),
                int(DataBits),
                int(Parity),
                int(StopBits),
                int(FlowControl),
            )
        )

        time1 += 1

    sim.stop(1800)
    sim.disconnect()

    successGG = input("\n Are positions recovered in less than 5s in average time? (Y/N) ")
    while successGG != "Y" and successGG != "N":
        successGG = input("\n Are positions recovered in less than 5s in average time? (Y/N) ")

    if successGPS == "Y" and successGLONASS == "Y" and successGG == "Y":
        return "Success"


####################### Test 5.11 #######################


def testTimeFix(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl):
    """Check the time the receiver spends to recover its position after disconnecting it from the simulator and cold start it.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    print("\n Test with GPS only \n")
    sim = scr.Case1("GPS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input(
        "\n During the simulation, measure the time interval between the moment when the antenna is disconnected and reconnected and the moment when an indication that the tracking from the working NSC constellation has resumed appears in the interface program dialog. Press Enter to start the simulation. "
    )

    sim.start()

    time1 = 0

    while time1 < 10:

        time.sleep(150 * time1)
        input("\n" + str(time1) + " Cold start your receiver and press Enter. ")

        time1 += 1

    sim.stop(1800)
    sim.disconnect()

    successGPS = input("\n Are positions recovered in less than 60s in average time? (Y/N) ")
    while successGPS != "Y" and successGPS != "N":
        successGPS = input("\n Are positions recovered in less than 60s in average time? (Y/N) ")

    # AND
    print("\n Test with GLONASS only \n")
    sim = scr.Case1("GLONASS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input(
        "\n During the simulation, measure the time interval between the moment when the antenna is disconnected and reconnected and the moment when an indication that the tracking from the working NSC constellation has resumed appears in the interface program dialog. Press Enter to start the simulation. "
    )

    sim.start()

    time1 = 0

    while time1 < 10:

        time.sleep(150 * time1)
        input("\n" + str(time1) + " Cold start your receiver and press Enter. ")

        time1 += 1

    sim.stop(1800)
    sim.disconnect()

    successGLONASS = input("\n Are positions recovered in less than 60s in average time? (Y/N) ")
    while successGLONASS != "Y" and successGLONASS != "N":
        successGLONASS = input("\n Are positions recovered in less than 60s in average time? (Y/N) ")

    # AND

    print("\n Test with GLONASS and GPS \n")
    sim = scr.Case1("GPS&GLONASS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input(
        "\n During the simulation, measure the time interval between the moment when the antenna is disconnected and reconnected and the moment when an indication that the tracking from the working NSC constellation has resumed appears in the interface program dialog. Press Enter to start the simulation. "
    )

    sim.start()

    time1 = 0

    while time1 < 10:

        time.sleep(150 * time1)
        input("\n" + str(time1) + " Cold start your receiver and press Enter. ")

        time1 += 1

    sim.stop(1800)
    sim.disconnect()

    successGG = input("\n Are positions recovered in less than 60s in average time? (Y/N) ")
    while successGG != "Y" and successGG != "N":
        successGG = input("\n Are positions recovered in less than 60s in average time? (Y/N) ")

    if successGPS == "Y" and successGLONASS == "Y" and successGG == "Y":
        return "Success"


####################### Test 5.12 #######################


def testSensitivity(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl):
    """Check the signal power limit before the lost of position and check the signal power limit until the recovery of position.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    input("\n Calibrate your Vector Network Analyser (VNA). Press Enter when it is done. ")
    im1 = cv2.imread(r"/images/VNA1.png")
    cv2.imshow("Assemble this circuit", im1)
    cv2.waitKey(0)
    Ktract = input(
        "\n Set zero signal path attenuation on attenuators. Measure the frequency response for a given signal path in the L1 band of GLONASS/GPS. What is the average path transmission factor (in dB) in this frequency band? "
    )
    Ktract = float(Ktract)
    im2 = cv2.imread(r"/images/VNA2.png")
    cv2.imshow("Assemble this circuit with 70dB of attenuation", im2)
    cv2.waitKey(0)
    input("\n Cold start your receiver. Press Enter when it is done. ")
    sim = scr.Case1("GPS&GLONASS")
    sim.call(SetSignalPowerOffset("L1CA", 0))
    sim.call(SetSignalPowerOffset("G1", 0))
    sim.call(AddVehicleGainPatternOffset(GNSSBand.L1, -10, "Basic Antenna"))
    sim.call(SetGlobalPowerOffset(-40))

    input("\n Press Enter to start the first test Record mode. ")

    sim.start()

    Psign = -200
    Pmin = Psign + Ktract

    fix1 = "N"
    idb = 0

    while fix1 == "N" and Pmin <= -133:
        if idb != 0:
            Psign += 1
            sim.call(SetGlobalPowerOffset(-40 + idb))

        time.sleep(120)
        fix1 = input("\n Did the receiver make a fix? (Y/N) ")
        while fix1 != "Y" and fix1 != "N":
            fix1 = input("\n Did the receiver make a fix? (Y/N) ")

        Pmin = Psign + Ktract
        idb += 1

    SuccRecord = False

    if Pmin <= -133:
        SuccRecord = True

    input("\n Press Enter to start the second test Tracking mode. ")

    sim.call(SetGlobalPowerOffset(30))
    Prec = -130

    fix2 = "N"
    SuccTracking = False
    idb = 0

    while fix2 == "N":
        if idb != 0:
            Prec -= 1
            sim.call(SetGlobalPowerOffset(30 - idb))

        time.sleep(120)
        fix2 = input("\n Did the receiver lost the signal? (Y/N) ")
        while fix2 != "Y" and fix2 != "N":
            fix2 = input("\n Did the receiver lost the signal? (Y/N) ")
        idb += 1

    if Prec <= -150:
        SuccTracking = True

    sim.stop()
    sim.disconnect()

    if SuccTracking and SuccRecord:
        return "Success"


####################### Test 5.13 #######################


def testRate(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl):
    """Check output rate of the receiver NMEA.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    im1 = cv2.imread(r"/images/Osc.png")
    cv2.imshow("Assemble this circuit", im1)
    cv2.waitKey(0)

    sim = scr.Case2("GPS&GLONASS")
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )
    input(
        "\n Configure the stream of the NMEA data of the receiver (GGA, RMC, VTG, GSA, DTM and GSV) with a frequency of 1Hz. Press Enter when it is done. "
    )

    input("\n Turn on the oscilloscope and press Enter. ")

    sim.start()

    time.sleep(60)
    freq1Hz = input("\n Does the output rate of the navigation module data corresponds to the configured value of 1Hz on the oscilloscope? (Y/N) ")
    while freq1Hz != "Y" and freq1Hz != "N":
        freq1Hz = input(
            "\n Does the output rate of the navigation module data corresponds to the configured value of 1Hz on the oscilloscope? (Y/N) "
        )

    sim.stop()

    input(
        "\n Configure the stream of the NMEA data of the receiver (GGA, RMC, VTG, GSA, DTM and GSV) with a frequency of 2Hz. Press Enter when it is done. "
    )

    sim.start()

    time.sleep(60)
    freq2Hz = input("\n Does the output rate of the navigation module data corresponds to the configured value of 2Hz on the oscilloscope? (Y/N) ")
    while freq2Hz != "Y" and freq2Hz != "N":
        freq2Hz = input(
            "\n Does the output rate of the navigation module data corresponds to the configured value of 2Hz on the oscilloscope? (Y/N) "
        )

    sim.stop()

    input(
        "\n Configure the stream of the NMEA data of the receiver (GGA, RMC, VTG, GSA, DTM and GSV) with a frequency of 5Hz. Press Enter when it is done. "
    )

    sim.start()

    time.sleep(60)
    freq5Hz = input("\n Does the output rate of the navigation module data corresponds to the configured value of 5Hz on the oscilloscope? (Y/N) ")
    while freq5Hz != "Y" and freq5Hz != "N":
        freq5Hz = input(
            "\n Does the output rate of the navigation module data corresponds to the configured value of 5Hz on the oscilloscope? (Y/N) "
        )

    sim.stop()

    input(
        "\n Configure the stream of the NMEA data of the receiver (GGA, RMC, VTG, GSA, DTM and GSV) with a frequency of 10Hz. Press Enter when it is done. "
    )

    sim.start()

    time.sleep(60)
    freq10Hz = input("\n Does the output rate of the navigation module data corresponds to the configured value of 10Hz on the oscilloscope? (Y/N) ")
    while freq10Hz != "Y" and freq10Hz != "N":
        freq10Hz = input(
            "\n Does the output rate of the navigation module data corresponds to the configured value of 10Hz on the oscilloscope? (Y/N) "
        )

    sim.stop()

    sim.disconnect()

    if freq1Hz == "Y" and freq2Hz == "Y" and freq5Hz == "Y" and freq10Hz == "Y":
        return "Success"


####################### Test 5.14 #######################


def testCutOff(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl):
    """Check the cutoff angle for the receiver signal reception.

    Args:
        PortName :: string 
            DUT port name
        BaudRate :: string
            Data baud rate of the serial port (1200 / 2400 / 4800 / 9600 / 19200 / 38400 / 57600 / 115200 / 460800)
        DataBits :: string
            Number of data bits used by the serial port (from 5 to 8)
        Parity :: string
            Parity scheme used by the serial port (0 : NoParity / 1 : Even / 2 : Odd / 3 : Space / 4 : Mark)
        StopBits :: string
            Number of stop bits used by the serial port (1 / 2)
        FlowControl :: string
            Flow control used by the serial port (0 : NoFlowControl / 1 : Hardware / 2 : Software)

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    sim = scr.Case1("GPS&GLONASS")
    input(
        "\n Set the GNSS_MIN_ELEVATION parameter (minimum NSC elevation, or cut-off angle) to 5° in the receiver parameters. Press Enter when it is done. "
    )
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input('\n On Skydel, in the constellation tab, check the "Show Receiver" box. Press Enter when it is done. ')

    input(
        "\n During the simulation, check on Skydel that the satellite GLONASS 12 is excluded from processing after 1min and check that the satellite GPS 16 is excluded from processing after 2min and 20sec. Press Enter to start the simulation. "
    )

    sim.start()

    sim.stop(180)

    succ5deg = input("\n Were the two satellites excluded from processing? (Y/N) ")
    while succ5deg != "Y" and succ5deg != "N":
        succ5deg = input("\n Were the two satellites excluded from processing? (Y/N) ")

    input(
        "\n Set the GNSS_MIN_ELEVATION parameter (minimum NSC elevation, or cut-off angle) to 10° in the receiver parameters. Press Enter when it is done. "
    )
    sim.call(
        ConnectSerialPortReceiver(
            PortName,
            int(BaudRate),
            int(DataBits),
            int(Parity),
            int(StopBits),
            int(FlowControl),
        )
    )

    input('\n On Skydel, in the constellation tab, check the "Show Receiver " box. Press Enter when it is done. ')

    input(
        "\n During the simulation, check on Skydel that the satellite GPS 4 is excluded from processing after 16min and 50s. Press Enter to start the simulation. "
    )

    sim.start()

    sim.stop(1080)

    succ10deg = input("\n Was the satellite excluded from processing? (Y/N) ")
    while succ10deg != "Y" and succ10deg != "N":
        succ10deg = input("\n Was the satellite excluded from processing? (Y/N) ")

    sim.disconnect()

    if succ5deg == "Y" and succ10deg == "Y":
        return "Success"


####################### Test 5.15 #######################


def testOffTime():
    """Check that the receiver power-off is the same as configured.

    Returns:
        'Success' if the test is successful, nothing if it is not
    
    """

    input("\n Configure the receiver with a GNSS_POWER_OFF_TIME equal to 10 s. Press Enter when it is done. ")
    success = input(
        "\n Turn off the receiver and record its actual power-off time as observed by the state of the system status indicator. Does it correspond to the power-off time? (Y/N) "
    )
    while success != "Y" and success != "N":
        success = input(
            "\n Turn off the receiver and record its actual power-off time as observed by the state of the system status indicator. Does it correspond to the power-off time? (Y/N) "
        )

    if success == "Y":
        return "Success"


####################### Launch ERA-GLONASS #######################


def startpart():
    # Start Era Glonass Test
    print("\n ***** Start the test part by part ***** \n")

    print("\n                Open a Skydel instance                 \n"
          "\n    Check that your receiver is connected to the GSG-7    \n"
          "\n Check that you filled correctly the PORT_CONFIG.txt file \n")

    f = open("PORT_CONFIG.txt", "r")

    dico_port = {}

    for line in f.readlines():
        if "=" in line:
            element = line.split(" = ")
            dico_port[element[0]] = element[1][:-1]

    PortName = dico_port.get("PortName")
    BaudRate = dico_port.get("BaudRate")
    DataBits = dico_port.get("DataBits")
    Parity = dico_port.get("Parity")
    StopBits = dico_port.get("StopBits")
    FlowControl = dico_port.get("FlowControl")

    # # Test Case 5.1
    print("\n")
    continue_test = input("Do you want to start the 5.1 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.1 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result51 = testPrecision(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GLONASS")
            if result51 == "Success":
                print("\n")
                print("Test 5.1 succeded")
            else:
                print("\n")
                print("Test 5.1 failed")

            print("\n")
            replay = input("Do you want to replay the 5.1 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.1 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.1")

    # Test Case 5.2
    print("\n")
    continue_test = input("Do you want to start the 5.2 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.2 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result52 = testPrecision(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS")
            if result52 == "Success":
                print("\n")
                print("Test 5.2 succeded")
            else:
                print("\n")
                print("Test 5.2 failed")

            print("\n")
            replay = input("Do you want to replay the 5.2 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.2 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.2")

    # Test Case 5.3
    print("\n")
    continue_test = input("Do you want to start the 5.3 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.3 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result53 = testPrecision(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS&GLONASS")
            if result53 == "Success":
                print("\n")
                print("Test 5.3 succeded")
            else:
                print("\n")
                print("Test 5.3 failed")

            print("\n")
            replay = input("Do you want to replay the 5.3 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.3 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.3")

    # Test Case 5.4
    print("\n")
    continue_test = input("Do you want to start the 5.4 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.4 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result54 = testNmea(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl)
            if result54 == "Success":
                print("\n")
                print("Test 5.4 succeded")
            else:
                print("\n")
                print("Test 5.4 failed")

            print("\n")
            replay = input("Do you want to replay the 5.4 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.4 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.4")

    # Test Case 5.5
    print("\n")
    continue_test = input("Do you want to start the 5.5 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.5 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result55 = testEphError(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl)
            if result55 == "Success":
                print("\n")
                print("Test 5.5 succeded")
            else:
                print("\n")
                print("Test 5.5 failed")

            print("\n")
            replay = input("Do you want to replay the 5.5 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.5 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.5")

    # Test Case 5.6
    print("\n")
    continue_test = input("Do you want to start the 5.6 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.6 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result56 = testNavParam(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl)
            if result56 == "Success":
                print("\n")
                print("Test 5.6 succeded")
            else:
                print("\n")
                print("Test 5.6 failed")

            print("\n")
            replay = input("Do you want to replay the 5.6 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.6 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.6")

    # Test Case 5.7
    print("\n")
    continue_test = input("Do you want to start the 5.7 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.7 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            input(
                "\n Set the GNSS_MIN_ELEVATION parameter (minimum NSC elevation, or cut-off angle) to 5° in the receiver parameters. Press Enter when it is done. "
            )
            input(
                "\n Configure the stream of the NMEA data of the receiver (GGA, RMC, VTG, GSA, DTM and GSV) with a frequency of 1Hz. Press Enter when it is done. "
            )
            succ_gps, gga_gps = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS", False, scr.Case1)
            succ_glonass, gga_glonass = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GLONASS", False, scr.Case1)
            succ_gg, gga_gg = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS&GLONASS", False, scr.Case1)
            if succ_gps == "Success" and succ_glonass == "Success" and succ_gg == "Success":
                print("\n")
                print("Test 5.7 succeded")
            else:
                print("\n")
                print("Test 5.7 failed")

            print("\n")
            replay = input("Do you want to replay the 5.7 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.7 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.7")

    # Test Case 5.8
    print("\n")
    continue_test = input("Do you want to start the 5.8 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.8 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            input(
                "\n Set the GNSS_MIN_ELEVATION parameter (minimum NSC elevation, or cut-off angle) to 5° in the receiver parameters. Press Enter when it is done. "
            )
            input(
                "\n Configure the stream of the NMEA data of the receiver (GGA, RMC, VTG, GSA, DTM and GSV) with a frequency of 1Hz. Press Enter when it is done. \n"
            )
            result_vel_gps, gga_vel_gps = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS", True, scr.Case2)
            result_vel_glonass, gga_vel_glonass = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GLONASS", True, scr.Case2)
            result_vel_gg, gga_vel_gg = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS&GLONASS", True, scr.Case2)
            result_man_gps, gga_man_gps = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS", True, scr.Case3)
            result_man_glonass, gga_man_glonass = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GLONASS", True, scr.Case3)
            result_man_gg, gga_man_gg = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS&GLONASS", True, scr.Case3)
            result_block_gps, gga_block_gps = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS", True, scr.Case4)
            result_block_glonass, gga_block_glonass = testErrPos(
                PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GLONASS", True, scr.Case4
            )
            result_block_gg, gga_block_gg = testErrPos(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, "GPS&GLONASS", True, scr.Case4)
            list_gga = [gga_man_gps, gga_man_glonass, gga_man_gg, gga_block_gps, gga_block_glonass, gga_block_gg]
            if (
                result_vel_gps == "Success"
                and result_vel_glonass == "Success"
                and result_vel_gg == "Success"
                and result_man_gps == "Success"
                and result_man_glonass == "Success"
                and result_man_gg == "Success"
                and result_block_gps == "Success"
                and result_block_glonass == "Success"
                and result_block_gg == "Success"
            ):
                print("\n")
                print("Test 5.8 succeded")
            else:
                print("\n")
                print("Test 5.8 failed")

            print("\n")
            replay = input("Do you want to replay the 5.8 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.8 test ? (Y/N) ")

        print("\n")
        continue_test = input("Do you want to start the 5.9 test ? (Y/N) ")
        while continue_test != "Y" and continue_test != "N":
            print("\n")
            continue_test = input("Do you want to start the 5.9 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.8")

    # Test Case 5.9
    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            input(
                "\n Be careful for this test the acceleration velocity tajectory was not taken in account because the vehicle was stopping sometimes "
            )
            result59 = testTimeInter(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl, list_gga)
            if result59 == "Success":
                print("\n")
                print("Test 5.9 succeded")
            else:
                print("\n")
                print("Test 5.9 failed")

            print("\n")
            replay = input("Do you want to replay the 5.9 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.9 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.9")

    # Test Case 5.10
    print("\n")
    continue_test = input("Do you want to start the 5.10 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.10 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result510 = testRecovery(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl)
            if result510 == "Success":
                print("\n")
                print("Test 5.10 succeded")
            else:
                print("\n")
                print("Test 5.10 failed")

            print("\n")
            replay = input("Do you want to replay the 5.10 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.10 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.10")

    # Test Case 5.11
    print("\n")
    continue_test = input("Do you want to start the 5.11 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.11 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result511 = testTimeFix(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl)
            if result511 == "Success":
                print("\n")
                print("Test 5.11 succeded")
            else:
                print("\n")
                print("Test 5.11 failed")

            print("\n")
            replay = input("Do you want to replay the 5.11 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.11 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.11")

    # Test Case 5.12
    print("\n")
    continue_test = input("Do you want to start the 5.12 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.12 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result512 = testSensitivity(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl)
            if result512 == "Success":
                print("\n")
                print("Test 5.12 succeded")
            else:
                print("\n")
                print("Test 5.12 failed")

            print("\n")
            replay = input("Do you want to replay the 5.12 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.12 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.12")

    # Test Case 5.13
    print("\n")
    continue_test = input("Do you want to start the 5.13 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.13 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result513 = testRate(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl)
            if result513 == "Success":
                print("\n")
                print("Test 5.13 succeded")
            else:
                print("\n")
                print("Test 5.13 failed")

            print("\n")
            replay = input("Do you want to replay the 5.13 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.13 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.13")

    # Test Case 5.14
    print("\n")
    continue_test = input("Do you want to start the 5.14 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.14 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result514 = testCutOff(PortName, BaudRate, DataBits, Parity, StopBits, FlowControl)
            if result514 == "Success":
                print("\n")
                print("Test 5.14 succeded")
            else:
                print("\n")
                print("Test 5.14 failed")

            print("\n")
            replay = input("Do you want to replay the 5.14 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.14 test ? (Y/N) ")

    else:
        print("\n")
        print("The user stopped the test 5.14")

    # Test Case 5.15
    print("\n")
    continue_test = input("Do you want to start the 5.15 test ? (Y/N) ")
    while continue_test != "Y" and continue_test != "N":
        print("\n")
        continue_test = input("Do you want to start the 5.15 test ? (Y/N) ")

    if continue_test == "Y":
        replay = "Y"
        while replay == "Y":
            result515 = testOffTime()
            if result515 == "Success":
                print("\n")
                print("Test 5.15 succeded")
            else:
                print("\n")
                print("Test 5.15 failed")

            print("\n")
            replay = input("Do you want to replay the 5.15 test ? (Y/N) ")
            while replay != "Y" and replay != "N":
                print("\n")
                replay = input("Do you want to replay the 5.15 test ? (Y/N) ")
    else:
        print("\n")
        print("The user stopped the test 5.15")
