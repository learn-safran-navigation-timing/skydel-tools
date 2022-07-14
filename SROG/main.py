"""
SROG: Skydel Rinex Observation Generator
GENERATOR of Rinex Observation from Skydel Raw DATA - Main QT application class.

Created on 16 06 2021

:author: Grace Oulai
:copyright: Skydel © 2021
:Version: 21.6.1
"""

# Import

import csv
import datetime
import glob
import os
import os.path
import subprocess
import sys
import numpy as np
import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QLabel, QDesktopWidget, QFileDialog, QFormLayout, QGroupBox, QComboBox, QMenuBar
from about import UiAboutDialog


def quit_app():
    """
    Function to quit application
    """
    sys.exit()


def openFile():
    """
    Function to open the User Manual
    """
    file = "SERGN_User_Manual.pdf"
    subprocess.Popen([file], shell=True)


class MainWindow(QtWidgets.QMainWindow):
    """
    Main application class
    """

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)

        hlay = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('resources/Skydel-NewLogo.png')
        label.resize(85, 85)
        label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio))
        hlay.addWidget(label, 0)

        self.direc = "future"
        self.file = str()
        self.path = str()
        self.new_rinex = str()
        self.count = int()
        self.time_row = list()
        self.minute_count = int()
        self.sat_id = ""
        self.csv_files_GPS_L1CA = list()
        self.csv_files_GPS_L1C = list()
        self.csv_files_GPS_L2C = list()
        self.csv_files_GLONASS_G1 = list()
        self.csv_files_GLONASS_G2 = list()
        self.csv_files_GALILEO_E1 = list()
        self.csv_files_BEIDOU_B1 = list()
        self.csv_files_BEIDOU_B1C = list()
        self.csv_files_BEIDOU_B2 = list()
        self.csv_files_GALILEO_E5a = list()
        self.csv_files_GALILEO_E5b = list()
        self.csv_files_SBAS_L1 = list()
        self.csv_files_SBAS_L5 = list()
        self.csv_files = list()
        self.csv_files_SBAS = list()
        self.sat_rinex_code = int()
        self.N_list = list()
        self.Time_0 = list()
        self.Sat_data_dict_0 = dict()
        self.Sat_data_dict_1 = dict()
        self.Sat_data_dict_2 = dict()
        self.header_name = str()
        self.directory_path = str()
        self.ui_about = UiAboutDialog()
        self.year_count = int()
        self.month_count = int()
        self.day_count = int()
        self.hour_count = int()
        self.sat_code = str()
        self.curr_sat = str()
        self.csv_files_1 = list()
        self.csv_files_2 = list()
        self.csv_files_SBASL1 = list()
        self.time_step_list = list()
        self.count_line_sat_1 = int()

        self.Sat_data_dict_0 = {
            "T_SAT": list(),
            "PSR": [],
            "ADR": [],
            "TIME": [],
            "SAT_CODE_BAND": []
        }

        self.Sat_data_dict_1 = {
            "T_SAT": list(),
            "PSR": [],
            "ADR": [],
            "TIME": [],
            "SAT_CODE_BAND": []
        }

        self.Sat_data_dict_2 = {
            "T_SAT": list(),
            "PSR": [],
            "ADR": [],
            "TIME": [],
            "SAT_CODE_BAND": []
        }

        ''' This part is the implementation of the Ui view'''
        # *************************************************************************************************************
        # ******************************* Menubar
        self.setStyleSheet("""QToolTip {
                                   background-color: #232b2b;
                                   color: white;
                                   border: #232b2b solid 1px
                                   }""")
        menubar = QMenuBar()
        actionFile2 = menubar.addMenu("Help")
        self.about_ui = actionFile2.addAction("About")
        self.about_ui.triggered.connect(self.show_about)
        actionFile2.addSeparator()
        self.user_manuel = actionFile2.addAction("User manual")
        self.user_manuel.triggered.connect(openFile)
        actionFile2 = menubar.addMenu("Exit")
        actionFile2.addAction("Quit")
        actionFile2.triggered.connect(quit_app)

        # *************************************************************************************************************
        # Studio view to Skydel View
        self.title1 = QLabel("Skydel Rinex Observation Generator")
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setFont(QFont('Arial', 16))
        self.title1.setStyleSheet("background-color:#3f839d; border-radius:5px")

        self.first_layout = QtWidgets.QHBoxLayout()
        self.select_dir_button = QtWidgets.QPushButton('Select directory')
        self.select_dir_button.clicked.connect(self.load_rinex)
        self.select_dir_button.setFont(QFont('Arial', 11))

        self.dir_path = QLineEdit()
        self.dir_path.setFont(QFont('Arial', 11))

        self.reset_button = QtWidgets.QPushButton('Reset')
        self.reset_button.setFont(QFont('Arial', 11))
        self.reset_button.clicked.connect(self.reset_func)

        self.first_layout.addWidget(self.select_dir_button)
        self.first_layout.addWidget(self.dir_path)
        self.first_layout.addWidget(self.reset_button)

        self.second_layout = QtWidgets.QVBoxLayout()

        self.generate_rinex_button = QtWidgets.QPushButton('Generate Rinex')
        self.generate_rinex_button.setFont(QFont('Arial', 11))
        self.generate_rinex_button.clicked.connect(self.main_func)
        self.generate_rinex_button.setEnabled(False)

        combo1 = QComboBox(self)
        sat_id_list = ["G: GPS", "R: GLONASS", "E: GALILEO", "J: QZSS", "C: BDS", "I: IRNSS", "S: SBAS", "M: Mixed"]
        combo1.addItems(sat_id_list)
        combo1.setCurrentIndex(0)
        combo1.activated[str].connect(self.onsatchanged1)
        self.sat_id = "G: GPS"

        combo2 = QComboBox(self)
        sat_id_list = ["L1", "L1/L2"]
        combo2.addItems(sat_id_list)
        combo2.setCurrentIndex(0)
        combo2.activated[str].connect(self.onsatchanged2)
        self.band_id = "L1"

        self.end_process = QLabel()
        self.end_process.setFont(QFont('Arial', 10))
        self.end_process = QLabel()
        self.end_process.setFont(QFont('Arial', 11))

        self.second_layout.setAlignment(Qt.AlignCenter)
        self.second_layout.addWidget(combo1, 0)
        self.second_layout.addWidget(combo2, 0)
        self.second_layout.addWidget(self.generate_rinex_button, 1)

        spacerItem1 = QtWidgets.QSpacerItem(60, 45, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        layout1 = QtWidgets.QVBoxLayout()
        layout1.addWidget(menubar, 0)
        layout1.addItem(spacerItem1)

        layout1.addWidget(self.title1, 0)
        layout1.addItem(spacerItem1)
        layout1.addLayout(self.first_layout)

        layout_start_time = QFormLayout()
        groupBox = QGroupBox("Enter start time")
        groupBox.setFont(QFont('Arial', 11))
        groupBox.setAlignment(Qt.AlignCenter)

        self.year = QLineEdit()
        self.year.setText("2021")

        self.month = QLineEdit()
        self.month.setText("4")

        self.day = QLineEdit()
        self.day.setText("20")

        self.hour = QLineEdit()
        self.hour.setText("10")

        self.minutes = QLineEdit()
        self.minutes.setText("48")

        self.secondes = QLineEdit()
        self.secondes.setText("35")

        layout_start_time.addRow("Year", self.year)
        layout_start_time.addRow("Month", self.month)
        layout_start_time.addRow("Day", self.day)
        layout_start_time.addRow("Hour", self.hour)
        layout_start_time.addRow("Minutes", self.minutes)
        layout_start_time.addRow("Seconds (s)", self.secondes)

        layout10 = QtWidgets.QHBoxLayout()
        self.frame1 = QtWidgets.QFrame(self)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Plain)

        self.frame2 = QtWidgets.QFrame(self)
        self.frame2.setFrameShadow(QtWidgets.QFrame.Plain)

        layout10.addWidget(self.frame1, 8)
        layout10.addLayout(layout_start_time, 9)
        layout10.addWidget(self.frame2, 10)

        groupBox.setLayout(layout10)

        # **************************************************************************************************************
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(layout1, 1)

        layout_final = QtWidgets.QVBoxLayout()
        layout_final.addLayout(hlay, 0)
        layout_final.addLayout(layout, 1)
        layout_final.addItem(spacerItem1)
        layout_final.addWidget(groupBox)
        layout_final.addItem(spacerItem1)
        layout_final.addLayout(self.second_layout, 3)
        layout_final.addWidget(self.end_process)

        layout_final.addItem(spacerItem1)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout_final)
        self.resize(750, 450)
        self.setCentralWidget(widget)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def load_rinex(self):
        """
        select skydel CSV raw data
        """
        self.directory_path = QFileDialog.getExistingDirectory(self, "Choose Directory", "E:\\")
        self.dir_path.setText(self.directory_path)
        self.generate_rinex_button.setEnabled(True)

    def show_about(self):
        """
        Show About dialog
        """
        self.ui_about.show()

    def on_file_saved_2(self):
        """
        Save rinex
        :return: selected file
        """
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "ObsGNSS",
                                                  "All Files (*);;Text Files (*.rnx)", options=options)
        return fileName

    def main_func(self):
        """
        Main function
        """
        # Variables
        list_sat = []
        list_sat_1 = []
        list_sat_2 = []
        self.end_process.setText("Processing...")
        np.random.seed(1234)

        # Set start time
        self.year_count = int(self.year.text())
        self.month_count = int(self.month.text())
        self.day_count = int(self.day.text())
        self.hour_count = int(self.hour.text())
        self.minute_count = int(self.minutes.text())
        second_0 = float(self.secondes.text())
        delta_ms = ((second_0 * 1000) + 500) / 1000
        date_and_time = datetime.datetime(self.year_count, self.month_count, self.day_count, self.hour_count,
                                          self.minute_count)
        self.new_time = date_and_time
        self.time_change = datetime.timedelta(minutes=+0)
        self.fid_w_name = self.on_file_saved_2()
        self.fid_w = open(self.fid_w_name, 'w+')
        path = str(self.directory_path)

        """
        Rinex Obs header
        """
        if self.sat_id == "G: GPS":
            self.sat_code = "G"
            self.csv_files_GPS_L1CA = glob.glob(os.path.join(path, "L1CA*.csv"))
            self.csv_files_GPS_L1C = glob.glob(os.path.join(path, "L1C *.csv"))
            self.csv_files_GPS_L2C = glob.glob(os.path.join(path, "L2C *.csv"))

            if self.band_id == "L1":
                self.header_name = 'resources/L1C_header.rnx'
                self.csv_files = self.csv_files_GPS_L1CA  # + self.csv_files_GPS_L1C

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

            elif self.band_id == "L1/L2":
                self.header_name = 'resources/GPS_L1_L2_header.rnx'
                self.csv_files_1 = self.csv_files_GPS_L1CA  # + self.csv_files_GPS_L1C
                self.csv_files_2 = self.csv_files_GPS_L2C
                self.csv_files = self.csv_files_GPS_L1CA + self.csv_files_GPS_L2C  # + self.csv_files_GPS_L1C +

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

                for path_file_1 in self.csv_files_1:
                    basename = os.path.basename(path_file_1)
                    list_sat_1.append(basename)

                for path_file_2 in self.csv_files_2:
                    basename = os.path.basename(path_file_2)
                    list_sat_2.append(basename)

        elif self.sat_id == "R: GLONASS":
            self.sat_code = "R"
            self.csv_files_GLONASS_G1 = glob.glob(os.path.join(path, "G1 *.csv"))
            self.csv_files_GLONASS_G2 = glob.glob(os.path.join(path, "G2 *.csv"))

            if self.band_id == "L1":
                self.header_name = 'resources/GLONASS_G1_header.rnx'
                self.csv_files = self.csv_files_GLONASS_G1

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

            elif self.band_id == "L1/L2":
                self.header_name = 'resources/GLONASS_L1_L2_header.rnx'
                self.csv_files = self.csv_files_1 + self.csv_files_2

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

                for path_file_1 in self.csv_files_1:
                    basename = os.path.basename(path_file_1)
                    list_sat_1.append(basename)

                for path_file_2 in self.csv_files_2:
                    basename = os.path.basename(path_file_2)
                    list_sat_2.append(basename)
            # else:
            #     self.header_name = 'resources/GLONASS_G2_header.rnx'
            #     self.csv_files_GLONASS_G2 = glob.glob(os.path.join(path, "G2 *.csv"))
            #     self.csv_files = self.csv_files_GLONASS_G2
            #
            #     for path_file in self.csv_files:
            #         basename = os.path.basename(path_file)
            #         list_sat.append(basename)

        elif self.sat_id == "E: GALILEO":
            self.sat_code = "E"
            self.csv_files_GALILEO_E1 = glob.glob(os.path.join(path, "E1 *.csv"))
            self.csv_files_GALILEO_E5a = glob.glob(os.path.join(path, "E5a *.csv"))

            if self.band_id == "L1":
                self.header_name = 'resources/GALILEO_E1_header.rnx'
                self.csv_files = self.csv_files_GALILEO_E1

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

            elif self.band_id == "L2":
                self.header_name = 'resources/GALILEO_E5.rnx'
                self.csv_files = self.csv_files_GALILEO_E5a
                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

            else:
                self.header_name = 'resources/GALILEO_E1_E5_header.rnx'
                self.csv_files_1 = self.csv_files_GALILEO_E1
                self.csv_files_2 = self.csv_files_GALILEO_E5a
                self.csv_files = self.csv_files_GALILEO_E1 + self.csv_files_GALILEO_E5a

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

                for path_file_1 in self.csv_files_1:
                    basename = os.path.basename(path_file_1)
                    list_sat_1.append(basename)

                for path_file_2 in self.csv_files_2:
                    basename = os.path.basename(path_file_2)
                    list_sat_2.append(basename)

        elif self.sat_id == "J: QZSS":
            self.sat_code = "J"
            self.csv_files_GALILEO_E1 = glob.glob(os.path.join(path, "E1 *.csv"))
            self.csv_files_GALILEO_E5a = glob.glob(os.path.join(path, "E5a *.csv"))
            self.csv_files_GALILEO_E5b = glob.glob(os.path.join(path, "E5b *.csv"))

            self.header_name = 'resources/L1C_header.rnx'
            if self.band_id == "L1":
                self.header_name = 'resources/QZSS_L1.rnx'
                for path_file in self.csv_files_GALILEO_E1:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)
            elif self.band_id == "L1/l2":
                self.header_name = 'resources/QZSS_L1_L2.rnx'
                for path_file in self.csv_files_GALILEO_E5a:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

        elif self.sat_id == "C: BDS":
            self.sat_code = "C"
            self.csv_files_BEIDOU_B1 = glob.glob(os.path.join(path, "B1 *.csv"))
            self.csv_files_BEIDOU_B1C = glob.glob(os.path.join(path, "B1C *.csv"))
            self.csv_files_BEIDOU_B2 = glob.glob(os.path.join(path, "B2 *.csv"))

            if self.band_id == "L1":
                self.header_name = 'resources/BEIDOU_B1.rnx'
                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

            elif self.band_id == "L1/l2":
                self.header_name = 'resources/BEIDOU_B1_B2.rnx'
                self.csv_files_1 = self.csv_files_BEIDOU_B1C + self.csv_files_BEIDOU_B1
                self.csv_files_2 = self.csv_files_BEIDOU_B2
                self.csv_files = self.csv_files_BEIDOU_B1C + self.csv_files_BEIDOU_B1 + self.csv_files_BEIDOU_B2

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

                for path_file_1 in self.csv_files_1:
                    basename = os.path.basename(path_file_1)
                    list_sat_1.append(basename)

                for path_file_2 in self.csv_files_2:
                    basename = os.path.basename(path_file_2)
                    list_sat_2.append(basename)

        elif self.sat_id == "I: IRNSS":
            self.sat_code = "I"
            self.header_name = 'resources/L1C_header.rnx'

        elif self.sat_id == "S: SBAS":

            self.csv_files_SBAS_L1 = glob.glob(os.path.join(path, "SBASL1 *.csv"))
            self.csv_files_SBAS_L5 = glob.glob(os.path.join(path, "SBASL5 *.csv"))

            if self.band_id == "L1":
                self.header_name = 'resources/SBAS_L1_header.rnx'
                self.csv_files = self.csv_files_SBAS_L1

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

            elif self.band_id == "L1/L2":

                self.header_name = 'resources/SBAS_L1_L2_header.rnx'
                self.csv_files_1 = self.csv_files_SBAS_L1
                self.csv_files_2 = self.csv_files_SBAS_L5
                self.csv_files = self.csv_files_SBAS_L1 + self.csv_files_SBAS_L5

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

                for path_file_1 in self.csv_files_1:
                    basename = os.path.basename(path_file_1)
                    list_sat_1.append(basename)

                for path_file_2 in self.csv_files_2:
                    basename = os.path.basename(path_file_2)
                    list_sat_2.append(basename)

        elif self.sat_id == "M: Mixed":
            self.sat_code = "M"

            if self.band_id == "L1":
                self.csv_files_GPS_L1CA = glob.glob(os.path.join(path, "L1CA *.csv"))
                self.csv_files_GPS_L1C = glob.glob(os.path.join(path, "L1C *.csv"))
                self.csv_files_GLONASS_G1 = glob.glob(os.path.join(path, "G1 *.csv"))
                self.csv_files_GALILEO_E1 = glob.glob(os.path.join(path, "E1 *.csv"))
                self.csv_files_BEIDOU_B1 = glob.glob(os.path.join(path, "B1 *.csv"))
                self.csv_files_BEIDOU_B1C = glob.glob(os.path.join(path, "B1C *.csv"))
                self.csv_files_SBASL1 = glob.glob(os.path.join(path, "SBASL1 *.csv"))
                self.csv_files = self.csv_files_GPS_L1CA + self.csv_files_GPS_L1C + self.csv_files_GLONASS_G1 + \
                                 self.csv_files_GALILEO_E1 + self.csv_files_BEIDOU_B1 + self.csv_files_BEIDOU_B1C + \
                                 self.csv_files_SBASL1

                if self.csv_files_GLONASS_G1:
                    self.header_name = 'resources/GPS_GLONASS_L1.rnx'

                    if self.csv_files_GALILEO_E1:
                        self.header_name = 'resources/GPS_GLONASS_GALILEO_L1.rnx'

                        if self.csv_files_BEIDOU_B1:
                            self.header_name = 'resources/GPS_GLONASS_GALILEO_BEIDOU_L1.rnx'

                            if self.csv_files_SBASL1:
                                self.header_name = 'resources/GPS_GLONASS_GALILEO_BEIDOU_QZSS_L1.rnx'

                            else:
                                self.header_name = 'resources/SBAS_S1_header.rnx'

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

            elif self.band_id == "L1/L2":
                self.csv_files_GPS_L1CA = glob.glob(os.path.join(path, "L1CA *.csv"))
                self.csv_files_GPS_L1C = glob.glob(os.path.join(path, "L1C *.csv"))
                self.csv_files_GPS_L2C = glob.glob(os.path.join(path, "L2C *.csv"))
                self.csv_files_GLONASS_G1 = glob.glob(os.path.join(path, "G1 *.csv"))
                self.csv_files_GLONASS_G2 = glob.glob(os.path.join(path, "G2 *.csv"))
                self.csv_files_GALILEO_E1 = glob.glob(os.path.join(path, "E1 *.csv"))
                self.csv_files_BEIDOU_B1 = glob.glob(os.path.join(path, "B1 *.csv"))
                self.csv_files_BEIDOU_B1C = glob.glob(os.path.join(path, "B1C *.csv"))
                self.csv_files_BEIDOU_B2 = glob.glob(os.path.join(path, "B2 *.csv"))
                self.csv_files_SBASL1 = glob.glob(os.path.join(path, "SBASL1 *.csv"))
                self.csv_files = self.csv_files_GPS_L1CA + self.csv_files_GPS_L1C + self.csv_files_GPS_L2C + \
                                 self.csv_files_GLONASS_G1 + self.csv_files_GLONASS_G2 + self.csv_files_GALILEO_E1 + \
                                 self.csv_files_BEIDOU_B1 + self.csv_files_BEIDOU_B1C + self.csv_files_BEIDOU_B2 + \
                                 self.csv_files_SBASL1

                self.csv_files_1 = self.csv_files_GPS_L1CA + self.csv_files_GPS_L1C + self.csv_files_GLONASS_G1 + \
                                   self.csv_files_GALILEO_E1 + self.csv_files_BEIDOU_B1 + self.csv_files_BEIDOU_B1C + \
                                   self.csv_files_SBASL1
                self.csv_files_2 = self.csv_files_GPS_L2C + self.csv_files_GLONASS_G2 + self.csv_files_BEIDOU_B2

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

                for path_file_1 in self.csv_files_1:
                    basename = os.path.basename(path_file_1)
                    list_sat_1.append(basename)

                for path_file_2 in self.csv_files_2:
                    basename = os.path.basename(path_file_2)
                    list_sat_2.append(basename)

                if self.csv_files_GLONASS_G1 != [] and self.csv_files_GLONASS_G2 != []:
                    self.header_name = 'resources/GPS_GLONASS_L1_L2.rnx'

                    if self.csv_files_GALILEO_E1:
                        self.header_name = 'resources/SBAS_S1_header.rnx'

                        if self.csv_files_BEIDOU_B1:
                            self.header_name = 'resources/SBAS_S1_header.rnx'

                            if self.csv_files_SBASL1:
                                self.header_name = 'resources/SBAS_S1_header.rnx'

                            else:
                                self.header_name = 'resources/SBAS_S1_header.rnx'
                else:
                    self.header_name = 'resources/GPS_GLONASS_L1.rnx'

            else:
                self.csv_files_GPS_L2C = glob.glob(os.path.join(path, "L2C *.csv"))
                self.csv_files_GLONASS_G2 = glob.glob(os.path.join(path, "G2 *.csv"))
                self.csv_files_BEIDOU_B2 = glob.glob(os.path.join(path, "B2 *.csv"))
                self.csv_files = self.csv_files_GPS_L2C + self.csv_files_GLONASS_G2 + self.csv_files_BEIDOU_B2

                for path_file in self.csv_files:
                    basename = os.path.basename(path_file)
                    list_sat.append(basename)

        self.write_header(delta_ms, second_0)

        sat_visible = list_sat
        if self.band_id == "L1":
            self.Sat_data_dict_0 = self.main_func_2(sat_visible, path)

            self.main_func_3(date_and_time, delta_ms, sat_visible, self.Sat_data_dict_0)

        elif self.band_id == "L1/L2":
            sat_visible_1 = list_sat_1
            sat_visible_2 = list_sat_2

            self.Sat_data_dict_1 = self.main_func_2(sat_visible_1, path)

            self.Sat_data_dict_2 = self.main_func_2(sat_visible_2, path)

            self.main_func_4(date_and_time, delta_ms, sat_visible_1, sat_visible_2, self.Sat_data_dict_1,
                             self.Sat_data_dict_2)

        self.end_process.setText("Done!")

        self.fid_w.close()

    def reset_func(self):
        """
        Reset function
        """
        self.end_process.setText("")
        self.dir_path.setText("")
        self.year.setText("2021")
        self.month.setText("4")
        self.day.setText("20")
        self.hour.setText("10")
        self.minutes.setText("48")
        self.secondes.setText("35")

    def onsatchanged1(self, text):
        """

        :param text: 
        """
        self.sat_id = text

    def onsatchanged2(self, text):
        """

        :param text: 
        """
        self.band_id = text

    def write_header(self, second, second_0):
        """

        :param second: 
        :param second_0: 
        """
        with open(self.header_name) as handler:

            for i, line in enumerate(handler):

                if 'OBSERVATION DATA' in line:
                    line_obs = "     3.04" + "           OBSERVATION DATA    " + str(
                        self.sat_code) + "                   RINEX VERSION / TYPE"
                    self.fid_w.write(line_obs)
                    self.fid_w.write('\n')

                elif 'TIME OF FIRST' in line:

                    if self.month_count < 10:
                        month_space = str('     ')
                    else:
                        month_space = str('    ')

                    if self.day_count < 10:
                        day_space = str('     ')
                    else:
                        day_space = str('    ')

                    if self.hour_count < 10:
                        hour_space = str('     ')
                    else:
                        hour_space = str('    ')

                    if self.hour_count < 10:
                        minute_space = str('     ')
                    else:
                        minute_space = str('    ')

                    if second_0 < 10:
                        second_space = str('    ')
                    else:
                        second_space = str('   ')

                    line_date = str('  ') + '{:0<4.0f}'.format(self.year_count) + month_space + str(
                        self.month_count) + day_space + str(self.day_count) + hour_space + str(self.hour_count) + \
                                minute_space + str(self.minute_count) + second_space + '{:0<2.7f}'.format(second_0) + \
                                str('     ') + str('GPS') + str('         ') + str(
                        'TIME OF FIRST OBS')

                    self.fid_w.write(line_date)
                    self.fid_w.write('\n')

                else:
                    self.fid_w.write(line)

                if 'END OF HEADER' in line:
                    self.fid_w.write('\n')
                    break

    def main_func_2(self, sat_visible, path):
        """

        :param sat_visible: 
        :param path: 
        :return: 
        """
        lines = []

        count_line = 0

        Sat_data_dict = {
            "T_SAT": [],
            "PSR": [],
            "ADR": [],
            "TIME": [],
            "SAT_CODE_BAND": []
        }

        for sat in sat_visible:

            basename = sat.split(" ")
            sat_band = basename[0]

            sat_int = basename[1]
            basename = sat_int.split(".")
            m = int(basename[0])
            name = path + "/" + str(sat_band) + ' ' + "{:02d}".format(int(m)) + ".csv"
            with open(name, 'r') as fid_sat:
                print(name, "is open")
                reader = csv.reader(fid_sat)
                next(reader)
                for row in reader:
                    count_line = count_line + 1
                    t0 = int(row[0])
                    t1 = next(reader)
                    t1 = int(t1[0])
                    time_step = (t1 - t0) / 1000
                    self.time_step_list.append(time_step)
                    break

        for sat in sat_visible:

            basename = sat.split(" ")
            sat_band = basename[0]

            code_band = list(sat_band)
            code_band = code_band[1]

            sat_int = basename[1]
            basename = sat_int.split(".")
            m = int(basename[0])
            name = path + "/" + str(sat_band) + ' ' + "{:02d}".format(int(m)) + ".csv"
            with open(name, 'r') as fid_sat:

                t_sat = []
                psr = []
                adr = []
                t_time = []
                data_band = []

                reader = csv.reader(fid_sat)
                next(reader)

                for row in reader:
                    lines.append(row)
                    temp_num_line = row
                    data_band.append(int(code_band))
                    t_time.append(int(temp_num_line[0]))
                    t_sat.append(float(temp_num_line[29]))
                    psr.append(float(temp_num_line[10]))
                    adr.append(float(temp_num_line[11]))

            Sat_data_dict["T_SAT"].append(t_sat)
            Sat_data_dict["PSR"].append(psr)
            Sat_data_dict["ADR"].append(adr)
            Sat_data_dict["TIME"].append(t_time)
            Sat_data_dict["SAT_CODE_BAND"].append(data_band)

        return Sat_data_dict

    def main_func_3(self, date_and_time, second, sat_visible, Sat_data_dict_0):

        """
        :param date_and_time: 
        :param second: 
        :param sat_visible: 
        :param Sat_data_dict_0: 
        """

        for k in range(0, len(Sat_data_dict_0["T_SAT"]), 1):
            N = len(Sat_data_dict_0["T_SAT"][k])
            self.N_list.append(N)
        N = max(self.N_list)

        time_comp = 500
        List_month_30 = [1, 4, 6, 9, 11]
        List_month_31 = [3, 5, 7, 8, 10, 12]
        
        for n in range(0, N, 1):

            if int(second) >= 59.9:
                                
                if self.minute_count == 59:
                    self.minute_count = 0
                    self.hour_count = self.hour_count + 1
                else:
                    self.minute_count = self.minute_count + 1

                # self.time_change = datetime.timedelta(minutes=self.minute_count)
                # self.new_time = date_and_time + self.time_change
                # self.minute_count = self.new_time.minute
                # self.hour_count = self.new_time.hour
                # self.day_count = self.new_time.day
            # self.month_count = self.new_time.month
            # self.year_count = self.new_time.year

                # self.time_change = datetime.timedelta(hours=self.hour_count)
                # self.new_time = date_and_time + self.time_change
                # self.minute_count = self.new_time.minute
                # self.hour_count = self.new_time.hour
                # self.day_count = self.new_time.day
                # self.month_count = self.new_time.month
                # self.year_count = self.new_time.year

            if self.hour_count >= 24:
                self.hour_count = int(self.hour_count) - 24
                self.day_count = int(self.day_count) + 1

            if int(self.day_count) == 30:
                if int(self.month_count) in List_month_30:
                    self.day_count = 1
                    self.month_count = self.month_count + 1

                    if int(self.month_count) >= 12:
                        self.month_count = 1
                        self.year_count = self.year_count + 1

            if int(self.day_count) > 31:
                if int(self.month_count) in List_month_31:
                    self.day_count = 1
                    self.month_count = self.month_count + 1

                    if int(self.month_count) >= 12:
                        self.month_count = 1
                        self.year_count = self.year_count + 1

            if int(self.day_count) == 28:
                if int(self.month_count) == 2:
                    self.month_count = self.month_count + 1
    
            second = np.mod(second, 60)
            count_time_table_1 = 0
            self.count_line_sat_1 = 0

            for sat_counter in sat_visible:
                try:
                    table_time = Sat_data_dict_0["TIME"][count_time_table_1][n]
                    if int(table_time) == int(time_comp):
                        self.count_line_sat_1 += 1
                except IndexError:
                    print("")
                count_time_table_1 += 1

            tline = str('> ') + '{:0<4.0f}'.format(self.year_count) + str(' ') + "{:02d}".format(
                self.month_count) + str(' ') + "{:02d}".format(
                self.day_count) + str(' ') + "{:02d}".format(self.hour_count) + str(' ') + str(
                "{0:0=2d}".format(self.minute_count)) + str(
                ' ') + '{:0<10.7f}'.format(second) + str('  0 ') + "{:02d}".format(self.count_line_sat_1)

            self.fid_w.write(tline)
            self.fid_w.write('\n')

            second = second + self.time_step_list[0]
            count_time_table = 0
            list_band = []
            for sat in sat_visible:

                basename = sat.split(" ")
                sat_band = basename[0]
                sat_int = basename[1]
                basename = sat_int.split(".")
                m = int(basename[0])

                # GPS
                if sat_band == "L1CA" or sat_band == "L1C" or sat_band == "L2C":
                    self.sat_rinex_code = "G"
                # BEIDOU
                if sat_band == "B1" or sat_band == "B2" or sat_band == "B1C":
                    self.sat_rinex_code = "B"
                # GLONASS
                if sat_band == "G1" or sat_band == "G2":
                    self.sat_rinex_code = "R"
                # GALILEO
                if sat_band == "E1" or sat_band == "E2":
                    self.sat_rinex_code = "E"
                # SBAS
                if sat_band == "SBASL1 ":
                    self.sat_rinex_code = "S"

                try:
                    self.curr_sat = self.sat_rinex_code + "{:02d}".format(int(m))
                    table_time = Sat_data_dict_0["TIME"][count_time_table][n]
                    list_band.append(self.curr_sat)

                    if int(table_time) == int(time_comp):

                        band_0 = '{:0<9.5f}'.format(Sat_data_dict_0["ADR"][count_time_table][n])

                        if len(band_0) == 10:
                            space_0 = ' 7      '
                        elif len(band_0) == 11:
                            space_0 = ' 7     '
                        elif len(band_0) == 12:
                            space_0 = ' 7    '
                        elif len(band_0) == 13:
                            space_0 = ' 7   '
                        elif len(band_0) == 14:
                            space_0 = ' 7  '
                        else:
                            space_0 = ' 7 '

                        tline = self.sat_rinex_code + "{:02d}".format(int(m)) + '  ' + '{:0<8.3f}'.format(
                            Sat_data_dict_0["PSR"][count_time_table][n]) + space_0 + '{:0<9.5f}'.format(
                            Sat_data_dict_0["ADR"][count_time_table][n])
                        self.fid_w.write(tline)
                        self.fid_w.write('\n')

                except IndexError:
                    print("")

                count_time_table += 1

            time_comp = time_comp + 100

    def main_func_4(self, date_and_time, second, sat_visible_1, sat_visible_2, Sat_data_dict_1, Sat_data_dict_2)
        """

        :param date_and_time:
        :param second:
        :param sat_visible_1:
        :param sat_visible_2:
        :param Sat_data_dict_1:
        :param Sat_data_dict_2:
        """
        sat_twin = str()
        sat_twin_2 = str()
        for k in range(0, len(Sat_data_dict_1["T_SAT"]), 1):
            N = len(Sat_data_dict_1["T_SAT"][k])
            self.N_list.append(N)
        N = max(self.N_list)

        time_comp = 500
        list_band = []
        list_sat_2 = []
        list_sat_twin_2 = []

        for sat_2 in sat_visible_2:
            basename_2 = sat_2.split(" ")
            sat_band_2 = basename_2[0]
            sat_int_2 = basename_2[1]
            basename_2 = sat_int_2.split(".")
            m2 = int(basename_2[0])
            list_sat_2.append(m2)

            # GPS
            if sat_band_2 == "L1CA" or sat_band_2 == "L1C" or sat_band_2 == "L2C":
                sat_rinex_code_2 = "G"
                sat_twin_2 = sat_rinex_code_2 + str(m2)

            # BEIDOU
            elif sat_band_2 == "B1" or sat_band_2 == "B2" or sat_band_2 == "B1C":
                sat_rinex_code_2 = "B"
                sat_twin_2 = sat_rinex_code_2 + str(m2)

            # GLONASS
            elif sat_band_2 == "G1" or sat_band_2 == "G2":
                sat_rinex_code_2 = "R"
                sat_twin_2 = sat_rinex_code_2 + str(m2)

            # GALILEO
            elif sat_band_2 == "E1" or sat_band_2 == "E5a" or sat_band_2 == "E5b":
                sat_rinex_code_2 = "E"
                sat_twin_2 = sat_rinex_code_2 + str(m2)

            # SBAS
            else:
                if sat_band_2 == "SBASL1 ":
                    sat_rinex_code_2 = "S"
                    sat_twin_2 = sat_rinex_code_2 + str(m2)

            list_sat_twin_2.append(sat_twin_2)

        List_month_30 = [1, 4, 6, 9, 11]
        List_month_31 = [3, 5, 7, 8, 10, 12]

        for n in range(0, N, 1):

            if int(second) >= 59.9:
                                
                if self.minute_count == 59:
                    self.minute_count = 0
                    self.hour_count = self.hour_count + 1
                else:
                    self.minute_count = self.minute_count + 1


                # self.time_change = datetime.timedelta(minutes=self.minute_count)
                # self.new_time = date_and_time + self.time_change
                # self.minute_count = self.new_time.minute
                # self.hour_count = self.new_time.hour
                # self.day_count = self.new_time.day
            # self.month_count = self.new_time.month
            # self.year_count = self.new_time.year

                
                # self.time_change = datetime.timedelta(hours=self.hour_count)
                # self.new_time = date_and_time + self.time_change
                # self.minute_count = self.new_time.minute
                # self.hour_count = self.new_time.hour
                # self.day_count = self.new_time.day
                # self.month_count = self.new_time.month
                # self.year_count = self.new_time.year

            if self.hour_count >= 24:
                self.hour_count = self.hour_count - 24
                self.day_count = self.day_count + 1

            if int(self.day_count) == 30:
                if int(self.month_count) in List_month_30:
                    self.day_count = 1
                    self.month_count = self.month_count + 1

                    if int(self.month_count) >= 12:
                        self.month_count = 1
                        self.year_count = self.year_count + 1

            if int(self.day_count) > 31:
                if int(self.month_count) in List_month_31:
                    self.day_count = 1
                    self.month_count =self.month_count + 1

                    if int(self.month_count) >= 12:
                        self.month_count = 1
                        self.year_count = self.year_count + 1

            if int(self.day_count) == 28:
                if int(self.month_count) == 2:
                    self.month_count = self.month_count + 1

            second = np.mod(second, 60)

            count_time_table_0 = 0
            count_line_sat_0 = 0

            for sat_1 in sat_visible_1:
                basename = sat_1.split(" ")
                sat_band = basename[0]
                sat_int = basename[1]
                basename = sat_int.split(".")
                m1 = int(basename[0])

                # GPS
                if sat_band == "L1CA" or sat_band == "L1C" or sat_band == "L2C":
                    self.sat_rinex_code = "G"
                    sat_twin = self.sat_rinex_code + str(m1)

                # BEIDOU
                elif sat_band == "B1" or sat_band == "B2" or sat_band == "B1C":
                    self.sat_rinex_code = "B"
                    sat_twin = self.sat_rinex_code + str(m1)

                # GLONASS
                elif sat_band == "G1" or sat_band == "G2":
                    self.sat_rinex_code = "R"
                    sat_twin = self.sat_rinex_code + str(m1)

                # GALILEO
                elif sat_band == "E1" or sat_band == "E5a" or sat_band == "E5b":
                    self.sat_rinex_code = "E"
                    sat_twin = self.sat_rinex_code + str(m1)

                # SBAS
                else:
                    if sat_band == "SBASL1 ":
                        self.sat_rinex_code = "S"
                        sat_twin = self.sat_rinex_code + str(m1)

                if sat_twin in list_sat_twin_2:
                    i2 = list_sat_2.index(m1)

                    self.curr_sat = str(self.sat_rinex_code) + str("{:02d}".format(int(m1)))
                    try:
                        table_time = Sat_data_dict_1["TIME"][count_time_table_0][n]

                        list_band.append(self.curr_sat)

                        if int(table_time) == int(time_comp):

                            band_1 = '{:0<9.5f}'.format(Sat_data_dict_1["ADR"][count_time_table_0][n])
                            band_2 = '{:0<9.5f}'.format(Sat_data_dict_2["ADR"][i2][n])

                            if len(band_1) == 10:
                                space_1 = ' 7      '
                            elif len(band_1) == 11:
                                space_1 = ' 7     '
                            elif len(band_1) == 12:
                                space_1 = ' 7    '
                            elif len(band_1) == 13:
                                space_1 = ' 7   '
                            elif len(band_1) == 14:
                                space_1 = ' 7  '
                            else:
                                space_1 = ' 7 '

                            if len(band_2) == 10:
                                space_2 = ' 7      '
                            elif len(band_2) == 11:
                                space_2 = ' 7     '
                            elif len(band_2) == 12:
                                space_2 = ' 7    '
                            elif len(band_2) == 13:
                                space_2 = ' 7   '
                            elif len(band_2) == 14:
                                space_2 = ' 7  '
                            else:
                                space_2 = ' 7 '

                            tline = str(self.sat_rinex_code) + str("{:02d}".format(int(m1))) + str('  ') + str(
                                '{:0<8.3f}'.format(
                                    Sat_data_dict_1["PSR"][count_time_table_0][n])) + str(space_1) + str(
                                '{:0<9.5f}'.format(
                                    Sat_data_dict_1["ADR"][count_time_table_0][n])) + str('  ') + str(
                                '{:0<8.3f}'.format(
                                    Sat_data_dict_2["PSR"][i2][n])) + str(space_2) + str('{:0<9.5f}'.format(
                                Sat_data_dict_2["ADR"][i2][n]))

                            count_line_sat_0 += 1

                    except IndexError as err:
                        print(err)

                else:

                    try:
                        self.curr_sat = str(self.sat_rinex_code) + str("{:02d}".format(int(m1)))
                        table_time = Sat_data_dict_1["TIME"][count_time_table_0][n]
                        list_band.append(self.curr_sat)
                        if int(table_time) == int(time_comp):

                            band_1 = str('{:0<9.5f}'.format(Sat_data_dict_1["ADR"][count_time_table_0][n]))

                            if len(band_1) == 10:
                                space_1 = ' 7      '
                            elif len(band_1) == 11:
                                space_1 = ' 7     '
                            elif len(band_1) == 12:
                                space_1 = ' 7    '
                            elif len(band_1) == 13:
                                space_1 = ' 7   '
                            elif len(band_1) == 14:
                                space_1 = ' 7  '
                            else:
                                space_1 = ' 7 '

                            tline = str(self.sat_rinex_code) + str("{:02d}".format(int(m1))) + str('  ') + str(
                                '{:0<8.3f}'.format(
                                    Sat_data_dict_1["PSR"][count_time_table_0][n])) + str(space_1) + str(
                                '{:0<9.5f}'.format(
                                    Sat_data_dict_1["ADR"][count_time_table_0][n]))

                            count_line_sat_0 += 1

                    except IndexError as err:
                        print(err)

                count_time_table_0 += 1

            tline = str('> ') + '{:0<4.0f}'.format(self.year_count) + str(' ') + "{:02d}".format(
                self.month_count) + str(' ') + "{:02d}".format(
                self.day_count) + str(' ') + "{:02d}".format(self.hour_count) + str(' ') + str(
                "{0:0=2d}".format(self.minute_count)) + str(
                ' ') + '{:0<10.7f}'.format(second) + str('  0 ') + "{:02d}".format(count_line_sat_0)

            self.fid_w.write(tline)
            self.fid_w.write('\n')

            second = second + self.time_step_list[0]
            count_time_table = 0
            count_line_sat_2 = 0

            for sat_1 in sat_visible_1:
                basename = sat_1.split(" ")
                sat_band = basename[0]
                sat_int = basename[1]
                basename = sat_int.split(".")
                m1 = int(basename[0])

                # GPS
                if sat_band == "L1CA" or sat_band == "L1C" or sat_band == "L2C":
                    self.sat_rinex_code = "G"
                    sat_twin = self.sat_rinex_code + str(m1)

                # BEIDOU
                elif sat_band == "B1" or sat_band == "B2" or sat_band == "B1C":
                    self.sat_rinex_code = "B"
                    sat_twin = self.sat_rinex_code + str(m1)

                # GLONASS
                elif sat_band == "G1" or sat_band == "G2":
                    self.sat_rinex_code = "R"
                    sat_twin = self.sat_rinex_code + str(m1)

                # GALILEO
                elif sat_band == "E1" or sat_band == "E5a" or sat_band == "E5b":
                    self.sat_rinex_code = "E"
                    sat_twin = self.sat_rinex_code + str(m1)

                # SBAS
                else:
                    if sat_band == "SBASL1 ":
                        self.sat_rinex_code = "S"
                        sat_twin = self.sat_rinex_code + str(m1)

                if sat_twin in list_sat_twin_2:
                    i2 = list_sat_2.index(m1)
                    self.curr_sat = str(self.sat_rinex_code) + str("{:02d}".format(int(m1)))
                    try:
                        table_time = Sat_data_dict_1["TIME"][count_time_table][n]

                        list_band.append(self.curr_sat)

                        if int(table_time) == int(time_comp):

                            band_1 = '{:0<9.5f}'.format(Sat_data_dict_1["ADR"][count_time_table][n])
                            band_2 = '{:0<9.5f}'.format(Sat_data_dict_2["ADR"][i2][n])

                            if len(band_1) == 10:
                                space_1 = ' 7      '
                            elif len(band_1) == 11:
                                space_1 = ' 7     '
                            elif len(band_1) == 12:
                                space_1 = ' 7    '
                            elif len(band_1) == 13:
                                space_1 = ' 7   '
                            elif len(band_1) == 14:
                                space_1 = ' 7  '
                            else:
                                space_1 = ' 7 '

                            if len(band_2) == 10:
                                space_2 = ' 7      '
                            elif len(band_2) == 11:
                                space_2 = ' 7     '
                            elif len(band_2) == 12:
                                space_2 = ' 7    '
                            elif len(band_2) == 13:
                                space_2 = ' 7   '
                            elif len(band_2) == 14:
                                space_2 = ' 7  '
                            else:
                                space_2 = ' 7 '

                            tline = str(self.sat_rinex_code) + str("{:02d}".format(int(m1))) + str('  ') + str(
                                '{:0<8.3f}'.format(
                                    Sat_data_dict_1["PSR"][count_time_table][n])) + str(space_1) + str(
                                '{:0<9.5f}'.format(
                                    Sat_data_dict_1["ADR"][count_time_table][n])) + str('  ') + str('{:0<8.3f}'.format(
                                Sat_data_dict_2["PSR"][i2][n])) + str(space_2) + str('{:0<9.5f}'.format(
                                Sat_data_dict_2["ADR"][i2][n]))
                            self.fid_w.write(tline)
                            self.fid_w.write('\n')

                            count_line_sat_2 += 1

                    except IndexError as err:
                        print(err)

                else:

                    try:
                        self.curr_sat = str(self.sat_rinex_code) + str("{:02d}".format(int(m1)))
                        table_time = Sat_data_dict_1["TIME"][count_time_table][n]
                        list_band.append(self.curr_sat)
                        if int(table_time) == int(time_comp):

                            band_1 = str('{:0<9.5f}'.format(Sat_data_dict_1["ADR"][count_time_table][n]))

                            if len(band_1) == 10:
                                space_1 = ' 7      '
                            elif len(band_1) == 11:
                                space_1 = ' 7     '
                            elif len(band_1) == 12:
                                space_1 = ' 7    '
                            elif len(band_1) == 13:
                                space_1 = ' 7   '
                            elif len(band_1) == 14:
                                space_1 = ' 7  '
                            else:
                                space_1 = ' 7 '

                            tline = str(self.sat_rinex_code) + str("{:02d}".format(int(m1))) + str('  ') + str(
                                '{:0<8.3f}'.format(
                                    Sat_data_dict_1["PSR"][count_time_table][n])) + str(space_1) + str(
                                '{:0<9.5f}'.format(
                                    Sat_data_dict_1["ADR"][count_time_table][n]))

                            self.fid_w.write(tline)
                            self.fid_w.write('\n')

                            count_line_sat_2 += 1

                    except IndexError:
                        print(count_time_table, n, N)

                count_time_table += 1

            time_comp = time_comp + 100

            if int(count_line_sat_0) == int(count_line_sat_2):
                print("ok")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(w)
    mw.show()
    w.show()
    app.exec_()
