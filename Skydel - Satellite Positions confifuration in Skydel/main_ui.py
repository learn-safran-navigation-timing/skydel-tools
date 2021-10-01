"""
Skydel Extrapolator for Rinex GLONASS Navigation File - Main QT application class.
Created on 14 06 2021
:author: Grace Oulai
:copyright: Skydel © 2021
:Version: 21.8.0
"""
# Import
import glob
import csv
import sys
import subprocess
import shutil
import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui, QtCore
from decimal import Decimal
from PyQt5.QtWidgets import QLineEdit, QLabel, QDesktopWidget, QFileDialog, QMenuBar, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QLabel, QDesktopWidget, QFileDialog, QFormLayout, QGroupBox, QComboBox, QMenuBar
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import math
from datetime import datetime
from datetime import date
from skydelsdx import *
from skydelsdx.commands import *
from csv import reader
import math

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import rc, grid, figure, plot, rcParams, savefig
from math import radians

from astropy.time import Time
import numpy as np
import astropy.units as unit
import os
from astroplan.plots import plot_sky
from astroplan import FixedTarget
from astroplan import FixedTarget
from astropy.coordinates import SkyCoord
import astropy.units as uni
from astroplan import Observer

def quit_app():
    sys.exit()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.M_0 = 0
        self.filename = "sat_out.csv"


        self.gpsKeplerian = dict({"PRN": 0, "T_OC": 0, "T_OE": 0, "SQRTA": 0, "E": 0, "M_0": 0, "I_0": 0,
                                  "OMEGA_0": 0, "OMEGA": 0, "OMEGA_DOT": 0, "I_DOT": 0, "DELTA_N": 0})
        self.setStyleSheet("""QToolTip {
                                   background-color: #232b2b;
                                   color: white;
                                   border: #232b2b solid 1px
                                   }""")

        hlay = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('resources/Skydel-NewLogo.png')
        label.resize(85, 85)
        label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio))
        hlay.addWidget(label, 0)

        '''This part is the implementation of the Ui view'''
        # ******************************* Menubar
        self.setStyleSheet("""QToolTip {
                                   background-color: #232b2b;
                                   color: white;
                                   border: #232b2b solid 1px
                                   }""")
        menubar = QMenuBar()
        actionFile2 = menubar.addMenu("Exit")
        actionFile2.addAction("Quit")
        actionFile2.triggered.connect(quit_app)

        # Studio view to Skydel View

        self.title1 = QLabel("Orbits generation")
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setFont(QFont('Arial', 14))
        self.title1.setStyleSheet("background-color:#545759; border-radius:5px")

        self.file_path_1 = QLineEdit()
        self.file_path_1.setFont(QFont('Arial', 10))

        self.file_save_path_1 = QLineEdit()
        self.file_save_path_1.setText("File save here:")
        self.file_save_path_1.setEnabled(False)
        self.file_save_path_1.setFont(QFont('Arial', 10))

        self.button_layout = QtWidgets.QHBoxLayout()
        self.skyplot_button = QtWidgets.QPushButton('Show Skyplot')
        self.skyplot_button.setFont(QFont('Arial', 10))
        self.skyplot_button.clicked.connect(self.main_func)
        self.skyplot_button.setEnabled(True)
        self.button_layout.setAlignment(Qt.AlignCenter)
        self.button_layout.addWidget(self.skyplot_button)

        self.api_button = QtWidgets.QPushButton('Send to Skydel')
        self.api_button.setFont(QFont('Arial', 10))
        self.api_button.clicked.connect(self.skydel_api)
        self.api_button.setEnabled(True)
        self.button_layout.setAlignment(Qt.AlignCenter)
        self.button_layout.addWidget(self.api_button)

        self.end_process = QLabel()
        self.end_process.setFont(QFont('Arial', 10))

        layout_start_time = QFormLayout()
        groupBox = QGroupBox("Enter satellites data")
        groupBox.setFont(QFont('Arial', 11))
        groupBox.setAlignment(Qt.AlignCenter)

        self.sat_no = QLineEdit()
        self.sat_no.setPlaceholderText("2")
        self.sat_el = QLineEdit()
        self.sat_el.setPlaceholderText("10 20")
        self.sat_az = QLineEdit()
        self.sat_az.setPlaceholderText("20 40")

        layout_start_time.addRow("Satellites number", self.sat_no)
        layout_start_time.addRow("Elevation (degree)", self.sat_el)
        layout_start_time.addRow("Azimuth (degree)", self.sat_az)

        self.frame1 = QtWidgets.QFrame(self)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Plain)

        self.frame2 = QtWidgets.QFrame(self)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Plain)

        # self.save_button_1_layout.addWidget(self.file_save_path_1)
        spacerItem0 = QtWidgets.QSpacerItem(50, 30, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout1 = QtWidgets.QVBoxLayout()
        layout1.addWidget(menubar, 0)
        layout1.addItem(spacerItem1)
        layout1.addWidget(self.title1, 0)
        layout1.addItem(spacerItem0)
        # layout1.addLayout(self.load_button_1_layout, 1)
        layout1.addItem(spacerItem1)
        layout1.addLayout(layout_start_time, 2)
        layout1.addLayout(self.button_layout)
        layout1.addWidget(self.end_process)
        # **************************************************************************************************************
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(layout1)
        layout_final = QtWidgets.QVBoxLayout()
        layout_final.addLayout(hlay, 0)
        layout_final.addLayout(layout, 1)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout_final)
        self.resize(700, 400)
        self.setCentralWidget(widget)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def main_func(self):
        print("Nothing")

        nb_sat = int(self.sat_no.text())
        list_elevation = self.sat_el.text()
        list_elevation = list_elevation.split(" ")
        print(list_elevation)
        list_azimuth = self.sat_az.text()
        list_azimuth = list_azimuth.split(" ")
        print(list_azimuth)
        print(len(list_elevation))

        rc('grid', color='#979ba1', linewidth=1, linestyle='-')
        rc('xtick', labelsize=10)
        rc('ytick', labelsize=10)

        # force square figure and square axes looks better for polar, IMO
        width, height = rcParams['figure.figsize']
        size = min(width, height)

        # make a square figure
        fig = plt.figure(figsize=(size, size))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)

        file = open(self.filename, "w")
        file.write('PRN'+","+"t_oc"+","+"t_oe"+","+"sqrtA"+","+"e"+","+"omega"+","+"M_0"+","+"i_0"+","+"omega_0"+","+"omega_dot"+","+"i_dot"+","+"delta_n"+"\n")
        for i in range(nb_sat):
            el = int(list_elevation[i])
            az = int(list_azimuth[i])
            prn = i + 1

            ax.annotate(str(prn),
                        xy=(radians(az), 90 - el),  # theta, radius
                        bbox=dict(boxstyle="round", fc='dodgerblue', alpha=0.5),
                        horizontalalignment='center',
                        verticalalignment='center')

            gpsKeplerian_dict = self.keplerian_func(el, az, prn)
            self.csv_file(gpsKeplerian_dict, file)

        ax.set_yticks(range(0, 90 + 10, 10))  # Define the yticks
        yLabel = ['90', '', '', '60', '', '', '30', '', '', '']
        ax.set_yticklabels(yLabel)

        file.close()
        grid(True)
        plt.show()

    def keplerian_func(self, elevation, azimute, prn):

        # Conditions

        if azimute > 180:
            azimute = (azimute - 360)

        if (azimute >= 0) and (azimute <= 90):
            # Recompute elevation/azimute
            azimute = 90 - azimute
            elevation = elevation - 90

            # Ascending node
            self.omega_0 = 0

            # Define semi - major axes
            self.sqrtA = 5153

            # Eccentricity
            self.e = 0

            self.i_0 = 0

            # Argument of perigee
            self.omega = math.pi / 2

            # Compute M0
            R_earth = 6378137.0
            R_sat = self.sqrtA * self.sqrtA
            phi_a = math.asin(R_earth * math.sin(elevation / 180 * math.pi) / R_sat)
            phi_a = math.pi - phi_a
            M0_deg = 180 - (90 + elevation + phi_a / math.pi * 180)
            self.M_0 = M0_deg / 180 * math.pi

            # Inclination
            self.i_0 = azimute / 180 * math.pi

        if (azimute > -180) and (azimute <= -90):
            # Recompute elevation / azimute
            azimute = 180 + azimute
            azimute = 90 - azimute
            elevation = 90 - elevation

            # Ascending node
            self.omega_0 = 0

            # Semi - major access
            self.sqrtA = 5153

            # Eccentricity
            self.e = 0

            # Argument of perigee
            self.omega = math.pi / 2

            # Compute M0
            R_earth = 6378137.0
            R_sat = self.sqrtA * self.sqrtA
            phi_a = math.asin(R_earth * math.sin(elevation / 180 * math.pi) / R_sat)
            phi_a = math.pi - phi_a
            M0_deg = 180 - (90 + elevation + phi_a / math.pi * 180)
            self.M_0 = M0_deg / 180 * math.pi

            # Inclination
            self.i_0 = azimute / 180 * math.pi

        if (azimute > -90) and (azimute < 0):
            # Recompute elevation / azimute
            azimute = 90 + azimute
            elevation = 90 - elevation

            # Ascending node
            self.omega_0 = math.pi

            # Semi - major acces
            self.sqrtA = 5153

            # Eccentricity
            self.e = 0

            # Argument of perigee
            self.omega = math.pi / 2

            # Compute M0
            R_earth = 6378137.0
            R_sat = self.sqrtA * self.sqrtA
            phi_a = math.asin(R_earth * math.sin(elevation / 180 * math.pi) / R_sat)
            phi_a = math.pi - phi_a
            M0_deg = 180 - (90 + elevation + phi_a / math.pi * 180)
            M0_deg = (M0_deg - 180)
            self.M_0 = M0_deg / 180 * math.pi

            # Inclination
            self.i_0 = azimute / 180 * math.pi

        if (azimute > 90) and (azimute <= 180):
            # Recompute
            elevation / azimute
            azimute = azimute - 90
            elevation = elevation - 90

            # Ascending node
            self.omega_0 = math.pi

            # Semi - major access
            self.sqrtA = 5153

            # Eccentricity
            self.e = 0

            # Argument of perigee
            self.omega = math.pi / 2

            # Compute M0
            R_earth = 6378137.0
            R_sat = self.sqrtA * self.sqrtA
            phi_a = math.asin(R_earth * math.sin(elevation / 180 * math.pi) / R_sat)
            phi_a = math.pi - phi_a
            M0_deg = 180 - (90 + elevation + phi_a / math.pi * 180)
            M0_deg = (M0_deg - 180)
            self.M_0 = M0_deg / 180 * math.pi

            # Inclination
            self.i_0 = azimute / 180 * math.pi

        self.gpsKeplerian["PRN"] = prn
        self.gpsKeplerian["T_OC"] = 0
        self.gpsKeplerian["T_OE"] = 0

        self.gpsKeplerian["SQRTA"] = self.sqrtA
        self.gpsKeplerian["E"] = self.e
        self.gpsKeplerian["OMEGA"] = self.omega

        if self.M_0 < -math.pi:
            self.M_0 = 2 * math.pi + self.M_0

        if self.M_0 > math.pi:
            self.M_0 = -2 * math.pi + self.M_0

        # Radians
        self.gpsKeplerian["M_0"] = self.M_0 / math.pi
        self.gpsKeplerian["I_0"] = self.i_0 / math.pi
        self.gpsKeplerian["OMEGA_0"] = self.omega_0 / math.pi
        self.gpsKeplerian["OMEGA"] = self.omega / math.pi
        self.gpsKeplerian["OMEGA_DOT"] = 0
        self.gpsKeplerian["I_DOT"] = 0
        self.gpsKeplerian["DELTA_N"] = 0

        print(self.gpsKeplerian)

        return self.gpsKeplerian

    def csv_file(self, gpsKeplerian, file):

        data = [gpsKeplerian["PRN"], ",", gpsKeplerian["T_OC"], ",", gpsKeplerian["T_OE"], ",", gpsKeplerian["SQRTA"],
                ",",
                gpsKeplerian["E"], ",", gpsKeplerian["OMEGA"], ",", gpsKeplerian["M_0"], ",", gpsKeplerian["I_0"], ",",
                gpsKeplerian["OMEGA_0"], ",", gpsKeplerian["OMEGA_DOT"], ",", gpsKeplerian["I_DOT"], ",",
                gpsKeplerian["DELTA_N"]]

        print("Write multiple rows")
        data = " ".join(str(x) for x in data)
        print(data)
        data = data.replace(" ", "")
        file.write(data + "\n")

    def skydel_api(self):
        sim = RemoteSimulator(True)
        sim.connect()
        sim.call(New(True, True))
        sim.call(SaveAs("C:/Users/Jean-GraceOulai/Documents/Skydel-SDX/Configurations/test_automation.py", True))
        sim.call(SetModulationTarget("NoneRT", "", "", True, "{d3c0efea-6689-426c-909a-792afc0c732b}"))
        sim.call(ChangeModulationTargetSignals(0, 1250000, 100000000, "UpperL", "L1CA", 0, False,
                                               "{d3c0efea-6689-426c-909a-792afc0c732b}", None))
        sim.call(SetVehicleTrajectoryFixEcef("Fix", 6378137, 0, 0, 0, 0, 0))
        sim.call(SetGpsStartTime(datetime(2020, 3, 29, 0, 0, 0)))

        with open(self.filename, 'r') as read_obj:

            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                print(row)
                PRN = int(row[0])
                T_OC = row[1]
                T_OE = row[2]
                SQRT_A = float(row[3])
                E = float(row[4])
                OMEGA = float(row[5]) * math.pi
                M_O = round(float(row[6]) * math.pi, 15)
                I_O = float(row[7]) * math.pi
                OMEGA_O = float(row[8]) * math.pi
                OMEGA_DOT = float(row[9]) * math.pi
                I_DOT = float(row[10]) * math.pi
                DELTA_N = float(row[11]) * math.pi

                sim.call(SetEphemerisReferenceTimeForSV("GPS", PRN, datetime(2020, 3, 29, 0, 0, 0)))
                sim.call(SetGpsEphDoubleParamForSV(PRN, "SqrtA", SQRT_A))  # Root semi major axis
                sim.call(SetGpsEphDoubleParamForSV(PRN, "Eccentricity", E))  # Eccentricity
                sim.call(SetGpsEphDoubleParamForSV(PRN, "LittleOmega", OMEGA))  # Argument of perigee
                sim.call(SetGpsEphDoubleParamForSV(PRN, "M0", M_O))  # Mean anomaly
                sim.call(SetGpsEphDoubleParamForSV(PRN, "I0", I_O))  # Inclination
                sim.call(SetGpsEphDoubleParamForSV(PRN, "BigOmega", OMEGA_O))  # Longitude of ascending node
                sim.call(SetGpsEphDoubleParamForSV(PRN, "DeltaN", DELTA_N))  # Mean motion difference
                sim.call(SetGpsEphDoubleParamForSV(PRN, "Idot", I_DOT))  # Inclination rate
                sim.call(SetGpsEphDoubleParamForSV(PRN, "BigOmegaDot", OMEGA_DOT))  # Right ascension rate
                sim.call(SetGpsEphDoubleParamForSV(PRN, "Adot", 0))  # Semi-major axis rate
                sim.call(SetGpsEphDoubleParamForSV(PRN, "DeltaN0dot", 0))  # Rate of mean motion difference

        last_prn = PRN
        GPS_Max = 32

        for sat_number in range(last_prn + 1, GPS_Max + 1, 1):
            sim.call(EnableSV("GPS", sat_number, False))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    qtmodern.styles.light(app)
    mw = qtmodern.windows.ModernWindow(w)
    mw.show()
    app.exec_()
