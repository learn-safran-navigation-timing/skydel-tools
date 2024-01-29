"""
SROG: Skydel Rinex Observation Generator
GENERATOR of Rinex Observation from Skydel Raw DATA - Main QT application class.
Created on 16 06 2021
:author: Grace Oulai
:copyright: Skydel © 2021
:Version: 23.12.1
"""

# Import

import csv
import datetime
from datetime import date
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
from PyQt5.QtGui import QFont, QStandardItemModel
from PyQt5.QtWidgets import QLineEdit, QLabel, QDesktopWidget, QFileDialog, QFormLayout, QGroupBox, QComboBox, QMenuBar, \
    QRadioButton, QCheckBox, QMessageBox
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

        self.Sat_data_dict_g_L1C = list()
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
        self.csv_files_GPS_L1P = list()
        self.csv_files_GPS_L2P = list()
        self.csv_files_GPS_L5 = list()

        self.csv_files_GLONASS_G1 = list()
        self.csv_files_GLONASS_G2 = list()

        self.csv_files_GALILEO_E1 = list()
        self.csv_files_GALILEO_E5a = list()
        self.csv_files_GALILEO_E5b = list()
        self.csv_files_GALILEO_E6BC = list()

        self.csv_files_BEIDOU_B1 = list()
        self.csv_files_BEIDOU_B1C = list()
        self.csv_files_BEIDOU_B2 = list()
        self.csv_files_BEIDOU_B2a = list()
        self.csv_files_BEIDOU_B3I = list()

        self.csv_files_QZSS_L1CA = list()
        self.csv_files_QZSS_L1CB = list()
        self.csv_files_QZSS_L1C = list()
        self.csv_files_QZSS_L1S = list()
        self.csv_files_QZSS_L2C = list()
        self.csv_files_QZSS_L5 = list()
        self.csv_files_QZSS_L5S = list()

        self.csv_files_KPS_L1CA = list()  # KPS
        self.csv_files_KPS_L1CB = list()  # KPS
        self.csv_files_KPS_L1C = list()  # KPS
        self.csv_files_KPS_L1S = list()  # KPS
        self.csv_files_KPS_L2C = list()  # KPS
        self.csv_files_KPS_L5 = list()  # KPS
        self.csv_files_KPS_L5S = list()  # KPS

        self.csv_files_NAVIC_L5 = list()

        self.csv_files_SBAS_L1 = list()
        self.csv_files_SBAS_L5 = list()

        self.csv_files = list()
        self.sat_rinex_code = int()
        self.Time_0 = list()
        self.header_name = str()
        self.directory_path = str()
        self.ui_about = UiAboutDialog()
        self.year_count = int()
        self.month_count = int()
        self.day_count = int()
        self.hour_count = int()
        self.sat_code = str()
        self.curr_sat = str()
        self.time_step_list = list()
        self.count_line_sat_1 = int()

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

        self.ubx_msg_class = []
        self.ubx_1 = QCheckBox('G: GPS')
        self.ubx_2 = QCheckBox('R: GLONASS')
        self.ubx_3 = QCheckBox('E: GALILEO')
        self.ubx_4 = QCheckBox('C: BEIDOU')
        self.ubx_5 = QCheckBox('J: QZSS')
        self.ubx_6 = QCheckBox('K: KPS')  # KPS
        self.ubx_7 = QCheckBox('I: IRNSS')
        self.ubx_8 = QCheckBox('S: SBAS')
        self.ubx_9 = QCheckBox('M: Mixed-ALL')

        self.ubx_1.stateChanged.connect(self.msg_type_handler)
        self.ubx_2.stateChanged.connect(self.msg_type_handler)
        self.ubx_3.stateChanged.connect(self.msg_type_handler)
        self.ubx_4.stateChanged.connect(self.msg_type_handler)
        self.ubx_5.stateChanged.connect(self.msg_type_handler)
        self.ubx_6.stateChanged.connect(self.msg_type_handler)  # KPS
        self.ubx_7.stateChanged.connect(self.msg_type_handler)
        self.ubx_8.stateChanged.connect(self.msg_type_handler)
        self.ubx_9.stateChanged.connect(self.msg_type_handler)

        ubx_msg_group = QGroupBox(" GNSS Signals")
        ubx_msg_group.setFont(QFont('Arial', 9))
        ubx_msg_layout = QtWidgets.QVBoxLayout()
        ubx_msg_group.setLayout(ubx_msg_layout)
        ubx_msg_layout.addWidget(self.ubx_1, 1)
        ubx_msg_layout.addWidget(self.ubx_2, 1)
        ubx_msg_layout.addWidget(self.ubx_3, 1)
        ubx_msg_layout.addWidget(self.ubx_4, 1)
        ubx_msg_layout.addWidget(self.ubx_5, 1)
        ubx_msg_layout.addWidget(self.ubx_6, 1)  # KPS
        ubx_msg_layout.addWidget(self.ubx_7, 1)
        ubx_msg_layout.addWidget(self.ubx_8, 1)
        ubx_msg_layout.addWidget(self.ubx_9, 1)

        self.end_process = QLabel()
        self.end_process.setFont(QFont('Arial', 10))
        self.end_process = QLabel()
        self.end_process.setFont(QFont('Arial', 11))

        self.second_layout.setAlignment(Qt.AlignCenter)
        self.second_layout.addWidget(ubx_msg_group, 0)
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
        self.year.setText("2023")

        self.month = QLineEdit()
        self.month.setText("9")

        self.day = QLineEdit()
        self.day.setText("14")

        self.hour = QLineEdit()
        self.hour.setText("12")

        self.minutes = QLineEdit()
        self.minutes.setText("00")

        self.secondes = QLineEdit()
        self.secondes.setText("00")

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

    def on_file_saved_2(self, const_str):
        """
        Save rinex
        :return: selected file
        """
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", str("ObsGNSS" + const_str),
                                                  "All Files (*);;Text Files (*.rnx)", options=options)
        return fileName

    def obs_type_writer(self, str_code, obs_type_list):
        header_str_tmp = str()
        cnt_1 = 0
        dict_str = list()
        new_sdr_dict = list()
        len_obs_type_list = len(obs_type_list)
        quot_len_list = len_obs_type_list // 13
        rem_len_list = len_obs_type_list % 13

        if quot_len_list == 0:
            pass
        else:
            for i in range(quot_len_list):
                for j in range(13):
                    header_str_tmp = header_str_tmp + str(obs_type_list[cnt_1]) + " "
                    cnt_1 += 1
                header_str_tmp = header_str_tmp + " SYS / # / OBS TYPES "
                dict_str.append(header_str_tmp)

                header_str_tmp = str()

        if rem_len_list == 0:
            pass
        else:
            for k in range(rem_len_list):
                header_str_tmp = header_str_tmp + str(obs_type_list[cnt_1]) + " "
                cnt_1 += 1
            header_str_tmp = header_str_tmp.ljust(53, " ")
            header_str_tmp = header_str_tmp + "SYS / # / OBS TYPES "
            dict_str.append(header_str_tmp)

        str_nb_code = str(len_obs_type_list)
        str_nb_code = str_nb_code.rjust(3, " ")

        try:
            header_str_11_00 = str_code + "  " + str_nb_code + " " + dict_str[0]
        except IndexError as err_indx_1:
            header_str_11_00 = str_code + "  " + str_nb_code + " "

        new_sdr_dict.append(header_str_11_00)

        if len(dict_str) > 1:
            for el in range(1, len(dict_str), 1):
                new_str_tmp = dict_str[el]
                header_str_tmp = new_str_tmp.rjust(80, " ")
                new_sdr_dict.append(header_str_tmp)
        return new_sdr_dict

    def msg_type_handler(self):

        if self.ubx_9.isChecked():
            self.ubx_1.setChecked(False)
            self.ubx_2.setChecked(False)
            self.ubx_3.setChecked(False)
            self.ubx_4.setChecked(False)
            self.ubx_5.setChecked(False)
            self.ubx_6.setChecked(False)
            self.ubx_7.setChecked(False)
            self.ubx_8.setChecked(False)

    def main_func(self):
        """
        Main function
        """
        # Variables
        list_sat = []
        list_dict_j = []
        list_band_j = []
        list_dict_k = []  # KPS
        list_band_k = []  # KPS
        list_dict_g = []
        list_band_g = []
        list_dict_r = []
        list_band_r = []
        list_dict_e = []
        list_band_e = []
        list_dict_c = []
        list_band_c = []
        list_dict_s = []
        list_band_s = []
        list_dict_i = []
        list_band_i = []
        list_dict_m = []
        list_band_m = []

        list_sat_g_l1ca = []
        list_sat_g_l1c = []
        list_sat_g_l1p = []
        list_sat_g_l2c = []
        list_sat_g_l2p = []
        list_sat_g_l5 = []

        list_sat_j_l1ca = []
        list_sat_j_l1cb = []
        list_sat_j_l1c = []
        list_sat_j_l1s = []
        list_sat_j_l2c = []
        list_sat_j_l5 = []
        list_sat_j_l5s = []

        list_sat_k_l1ca = []  # kps
        list_sat_k_l1cb = []  # kps
        list_sat_k_l1c = []  # kps
        list_sat_k_l1s = []  # kps
        list_sat_k_l2c = []  # kps
        list_sat_k_l5 = []  # kps
        list_sat_k_l5s = []  # kps

        list_sat_r_g1 = []
        list_sat_r_g2 = []

        list_sat_e_e1 = []
        list_sat_e_e5a = []
        list_sat_e_e5b = []
        list_sat_e_e6bc = []

        list_sat_c_b1 = []
        list_sat_c_b1c = []
        list_sat_c_b2 = []
        list_sat_c_b2a = []
        list_sat_c_b3i = []

        list_sat_s_l1 = []
        list_sat_s_l5 = []

        list_sat_i_l5 = []

        check_nb = 0

        self.obs_code_g = list()
        self.obs_code_j = list()
        self.obs_code_r = list()
        self.obs_code_e = list()
        self.obs_code_b = list()
        self.obs_code_c = list()
        self.obs_code_i = list()
        self.obs_code_s = list()
        self.obs_code_k = list()  # KPS

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
        const_str = ""
        if self.ubx_1.isChecked():
            const_str = const_str + "_GPS"
            self.sat_code = "G"
            check_nb += 1
        if self.ubx_2.isChecked():
            const_str = const_str + "_GLONASS"
            self.sat_code = "R"
            check_nb += 1
        if self.ubx_3.isChecked():
            const_str = const_str + "_GALILEO"
            self.sat_code = "E"
            check_nb += 1
        if self.ubx_4.isChecked():
            const_str = const_str + "_BEIDOU"
            self.sat_code = "C"
            check_nb += 1
        if self.ubx_5.isChecked():
            const_str = const_str + "_QZSS"
            self.sat_code = "J"
            check_nb += 1
        if self.ubx_6.isChecked():
            const_str = const_str + "_KPS"
            self.sat_code = "K"
            check_nb += 1
        if self.ubx_7.isChecked():
            const_str = const_str + "_IRNSS"
            self.sat_code = "I"
            check_nb += 1
        if self.ubx_8.isChecked():
            const_str = const_str + "_SBAS"
            self.sat_code = "S"
            check_nb += 1
        if self.ubx_9.isChecked() or check_nb >= 2:
            const_str = const_str + "_Mixed"
            self.sat_code = "M"

        self.fid_w_name = self.on_file_saved_2(const_str)
        try:
            self.fid_w = open(self.fid_w_name, 'w+')
            path = str(self.directory_path)

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

            header_str_12 = str('  ') + '{:0<4.0f}'.format(self.year_count) + month_space + str(
                self.month_count) + day_space + str(self.day_count) + hour_space + str(self.hour_count) + \
                            minute_space + '{:0<2.0f}'.format(self.minute_count) + second_space + '{:0<2.7f}'.format(
                second_0) + \
                            str('     ') + str('GPS') + str('         ') + str(
                'TIME OF FIRST OBS')

            header_str_1 = "     " + "3.04" + "           " + "OBSERVATION DATA    " + str(
                self.sat_code) + "                   " + "RINEX VERSION / TYPE"

            self.fid_w.write(header_str_1)
            self.fid_w.write('\n')

            today = date.today()

            date_now = today.strftime("%Y%m%d")
            time_now = datetime.datetime.now()
            time_now_str = time_now.strftime("%H%M%S")

            header_str_2 = "SROG                " + "SKYDEL              " + str(date_now) + " " + str(
                time_now_str) + " " + "UTC" + " " + "PGM / RUN BY / DATE"
            self.fid_w.write(header_str_2)
            self.fid_w.write('\n')

            header_str_3 = "SKYDEL                                                      " + "MARKER NAME"
            self.fid_w.write(header_str_3)
            self.fid_w.write('\n')

            header_str_4 = "Unknown             " + "                                        " + "MARKER NUMBER"
            self.fid_w.write(header_str_4)
            self.fid_w.write('\n')

            header_str_5 = "SAFRAN TRUSTED 4D   " + "                                        " + "OBSERVER / AGENCY"
            self.fid_w.write(header_str_5)
            self.fid_w.write('\n')

            header_str_6 = "THIS RINEX OBS HAS BEEN GENERATED WITH SKYDEL RAW DATA      " + "COMMENT"
            self.fid_w.write(header_str_6)
            self.fid_w.write('\n')

            header_str_7 = "Unknown             " + "Unknown              " + "                   " + "REC # / TYPE / VERS"
            self.fid_w.write(header_str_7)
            self.fid_w.write('\n')

            header_str_8 = "Unknown             " + "Unknown              " + "                   " + "ANT # / TYPE"
            self.fid_w.write(header_str_8)
            self.fid_w.write('\n')

            header_str_9 = "        0.0000" + "        0.0000" + "        0.0000" + "                  " + "APPROX POSITION XYZ"
            self.fid_w.write(header_str_9)
            self.fid_w.write('\n')

            header_str_10 = "        0.0000" + "        0.0000" + "        0.0000" + "                  " + "ANTENNA: DELTA H/E/N"
            self.fid_w.write(header_str_10)
            self.fid_w.write('\n')

            if self.ubx_9.isChecked():
                self.sat_code = "M"
                mixed_code = 1
            else:
                mixed_code = 0

            if self.ubx_1.isChecked() or mixed_code == 1:
                self.sat_code = "G"
                self.csv_files_GPS_L1CA = glob.glob(os.path.join(path, "L1CA*.csv"))
                self.csv_files_GPS_L1C = glob.glob(os.path.join(path, "L1C *.csv"))
                self.csv_files_GPS_L2C = glob.glob(os.path.join(path, "L2C *.csv"))
                self.csv_files_GPS_L1P = glob.glob(os.path.join(path, "L1P *.csv"))
                self.csv_files_GPS_L2P = glob.glob(os.path.join(path, "L2P *.csv"))
                self.csv_files_GPS_L5 = glob.glob(os.path.join(path, "L5 *.csv"))

                if self.csv_files_GPS_L1CA:
                    self.obs_code_g.append("C1C")
                    self.obs_code_g.append("L1C")
                    self.obs_code_g.append("D1C")
                    for path_file in self.csv_files_GPS_L1CA:
                        basename = os.path.basename(path_file)
                        list_sat_g_l1ca.append(basename)
                    self.Sat_data_dict_g_L1CA, self.sat_band_list_L1CA = self.main_func_2(list_sat_g_l1ca, path)
                    list_dict_g.append(self.Sat_data_dict_g_L1CA)
                    list_band_g.append(list_sat_g_l1ca)

                if self.csv_files_GPS_L1C:
                    self.obs_code_g.append("C1L")
                    self.obs_code_g.append("L1L")
                    self.obs_code_g.append("D1L")
                    for path_file in self.csv_files_GPS_L1C:
                        basename = os.path.basename(path_file)
                        list_sat_g_l1c.append(basename)
                    self.Sat_data_dict_g_L1C, self.sat_band_list_L1C = self.main_func_2(list_sat_g_l1c, path)
                    list_dict_g.append(self.Sat_data_dict_g_L1C)
                    list_band_g.append(list_sat_g_l1c)

                if self.csv_files_GPS_L1P:
                    self.obs_code_g.append("C1W")
                    self.obs_code_g.append("L1W")
                    self.obs_code_g.append("D1W")
                    for path_file in self.csv_files_GPS_L1P:
                        basename = os.path.basename(path_file)
                        list_sat_g_l1p.append(basename)
                    self.Sat_data_dict_g_L1P, self.sat_band_list_L1P = self.main_func_2(list_sat_g_l1p, path)
                    list_dict_g.append(self.Sat_data_dict_g_L1P)
                    list_band_g.append(list_sat_g_l1p)

                if self.csv_files_GPS_L2C:
                    self.obs_code_g.append("C2L")
                    self.obs_code_g.append("L2L")
                    self.obs_code_g.append("D2L")
                    for path_file in self.csv_files_GPS_L2C:
                        basename = os.path.basename(path_file)
                        list_sat_g_l2c.append(basename)
                    self.Sat_data_dict_g_L2C, self.sat_band_list_L2C = self.main_func_2(list_sat_g_l2c, path)
                    list_dict_g.append(self.Sat_data_dict_g_L2C)
                    list_band_g.append(list_sat_g_l2c)

                if self.csv_files_GPS_L2P:
                    self.obs_code_g.append("C2W")
                    self.obs_code_g.append("L2W")
                    self.obs_code_g.append("D2W")
                    for path_file in self.csv_files_GPS_L2P:
                        basename = os.path.basename(path_file)
                        list_sat_g_l2p.append(basename)
                    self.Sat_data_dict_g_L2P, self.sat_band_list_L2P = self.main_func_2(list_sat_g_l2p, path)
                    list_dict_g.append(self.Sat_data_dict_g_L2P)
                    list_band_g.append(list_sat_g_l2p)

                if self.csv_files_GPS_L5:
                    self.obs_code_g.append("C5Q")
                    self.obs_code_g.append("L5Q")
                    self.obs_code_g.append("D5Q")
                    for path_file in self.csv_files_GPS_L5:
                        basename = os.path.basename(path_file)
                        list_sat_g_l5.append(basename)
                    self.Sat_data_dict_g_L5, self.sat_band_list_L5 = self.main_func_2(list_sat_g_l5, path)
                    list_dict_g.append(self.Sat_data_dict_g_L5)
                    list_band_g.append(list_sat_g_l5)

                header_str_11_str = self.obs_type_writer(self.sat_code, self.obs_code_g)

                for el in header_str_11_str:
                    self.fid_w.write(el)
                    self.fid_w.write('\n')

            if self.ubx_2.isChecked() or mixed_code == 1:
                self.sat_code = "R"
                self.csv_files_GLONASS_G1 = glob.glob(os.path.join(path, "G1 *.csv"))
                self.csv_files_GLONASS_G2 = glob.glob(os.path.join(path, "G2 *.csv"))

                if self.csv_files_GLONASS_G1:
                    self.obs_code_r.append("C1P")
                    self.obs_code_r.append("L1P")
                    self.obs_code_r.append("D1P")
                    for path_file in self.csv_files_GLONASS_G1:
                        basename = os.path.basename(path_file)
                        list_sat_r_g1.append(basename)
                    self.Sat_data_dict_r_G1, self.sat_band_list_G1 = self.main_func_2(list_sat_r_g1, path)
                    list_dict_r.append(self.Sat_data_dict_r_G1)
                    list_band_r.append(list_sat_r_g1)

                if self.csv_files_GLONASS_G2:
                    self.obs_code_r.append("C2P")
                    self.obs_code_r.append("L2P")
                    self.obs_code_r.append("D2P")
                    for path_file in self.csv_files_GLONASS_G2:
                        basename = os.path.basename(path_file)
                        list_sat_r_g2.append(basename)
                    self.Sat_data_dict_r_G2, self.sat_band_list_G2 = self.main_func_2(list_sat_r_g2, path)
                    list_dict_r.append(self.Sat_data_dict_r_G2)
                    list_band_r.append(list_sat_r_g2)

                header_str_11_str = self.obs_type_writer(self.sat_code, self.obs_code_r)

                for el in header_str_11_str:
                    self.fid_w.write(el)
                    self.fid_w.write('\n')

            if self.ubx_3.isChecked() or mixed_code == 1:
                self.sat_code = "E"
                self.csv_files_GALILEO_E1 = glob.glob(os.path.join(path, "E1 *.csv"))
                self.csv_files_GALILEO_E5a = glob.glob(os.path.join(path, "E5a *.csv"))
                self.csv_files_GALILEO_E5b = glob.glob(os.path.join(path, "E5b *.csv"))
                self.csv_files_GALILEO_E6BC = glob.glob(os.path.join(path, "E6BC *.csv"))

                if self.csv_files_GALILEO_E1:
                    self.obs_code_e.append("C1C")
                    self.obs_code_e.append("L1C")
                    self.obs_code_e.append("D1C")
                    for path_file in self.csv_files_GALILEO_E1:
                        basename = os.path.basename(path_file)
                        list_sat_e_e1.append(basename)
                    self.Sat_data_dict_e_e1, self.sat_band_list_E1 = self.main_func_2(list_sat_e_e1, path)
                    list_dict_e.append(self.Sat_data_dict_e_e1)
                    list_band_e.append(list_sat_e_e1)

                if self.csv_files_GALILEO_E5a:
                    self.obs_code_e.append("C5Q")
                    self.obs_code_e.append("L5Q")
                    self.obs_code_e.append("D5Q")
                    for path_file in self.csv_files_GALILEO_E5a:
                        basename = os.path.basename(path_file)
                        list_sat_e_e5a.append(basename)
                    self.Sat_data_dict_e_e5a, self.sat_band_list_E5a = self.main_func_2(list_sat_e_e5a, path)
                    list_dict_e.append(self.Sat_data_dict_e_e5a)
                    list_band_e.append(list_sat_e_e5a)

                if self.csv_files_GALILEO_E5b:
                    self.obs_code_e.append("C7Q")
                    self.obs_code_e.append("L7Q")
                    self.obs_code_e.append("D7Q")
                    for path_file in self.csv_files_GALILEO_E5b:
                        basename = os.path.basename(path_file)
                        list_sat_e_e5b.append(basename)
                    self.Sat_data_dict_e_e5b, self.sat_band_list_E5b = self.main_func_2(list_sat_e_e5b, path)
                    list_dict_e.append(self.Sat_data_dict_e_e5b)
                    list_band_e.append(list_sat_e_e5b)

                if self.csv_files_GALILEO_E6BC:
                    self.obs_code_e.append("C6C")
                    self.obs_code_e.append("L6C")
                    self.obs_code_e.append("D6C")
                    for path_file in self.csv_files_GALILEO_E5b:
                        basename = os.path.basename(path_file)
                        list_sat_e_e6bc.append(basename)
                    self.Sat_data_dict_e_e6bcb, self.sat_band_list_E6BC = self.main_func_2(list_sat_e_e6bc, path)
                    list_dict_e.append(self.Sat_data_dict_e_e6bc)
                    list_band_e.append(list_sat_e_e6bc)

                header_str_11_str = self.obs_type_writer(self.sat_code, self.obs_code_e)

                for el in header_str_11_str:
                    self.fid_w.write(el)
                    self.fid_w.write('\n')

            if self.ubx_4.isChecked() or mixed_code == 1:
                self.sat_code = "C"
                self.csv_files_BEIDOU_B1 = glob.glob(os.path.join(path, "B1 *.csv"))
                self.csv_files_BEIDOU_B1C = glob.glob(os.path.join(path, "B1C *.csv"))
                self.csv_files_BEIDOU_B2 = glob.glob(os.path.join(path, "B2 *.csv"))
                self.csv_files_BEIDOU_B2a = glob.glob(os.path.join(path, "B2a *.csv"))
                self.csv_files_BEIDOU_B31 = glob.glob(os.path.join(path, "B3I *.csv"))

                if self.csv_files_BEIDOU_B1:
                    self.obs_code_c.append("C1C")
                    self.obs_code_c.append("L1C")
                    self.obs_code_c.append("D1C")
                    for path_file in self.csv_files_BEIDOU_B1:
                        basename = os.path.basename(path_file)
                        list_sat_c_b1.append(basename)
                    self.Sat_data_dict_c_b1, self.sat_band_list_B1 = self.main_func_2(list_sat_c_b1, path)
                    list_dict_c.append(self.Sat_data_dict_c_b1)
                    list_band_c.append(list_sat_c_b1)

                if self.csv_files_BEIDOU_B1C:
                    self.obs_code_c.append("C1P")
                    self.obs_code_c.append("L1P")
                    self.obs_code_c.append("D1P")
                    for path_file in self.csv_files_BEIDOU_B1C:
                        basename = os.path.basename(path_file)
                        list_sat_c_b1c.append(basename)
                    self.Sat_data_dict_c_b1c, self.sat_band_list_B1C = self.main_func_2(list_sat_c_b1c, path)
                    list_dict_c.append(self.Sat_data_dict_c_b1c)
                    list_band_c.append(list_sat_c_b1c)

                if self.csv_files_BEIDOU_B2:
                    self.obs_code_c.append("C7I")
                    self.obs_code_c.append("L7I")
                    self.obs_code_c.append("D7I")
                    for path_file in self.csv_files_BEIDOU_B2:
                        basename = os.path.basename(path_file)
                        list_sat_c_b2.append(basename)
                    self.Sat_data_dict_c_b2, self.sat_band_list_B2 = self.main_func_2(list_sat_c_b2, path)
                    list_dict_c.append(self.Sat_data_dict_c_b2)
                    list_band_c.append(list_sat_c_b2)

                if self.csv_files_BEIDOU_B2a:
                    self.obs_code_c.append("C5P")
                    self.obs_code_c.append("L5P")
                    self.obs_code_c.append("D5P")
                    for path_file in self.csv_files_BEIDOU_B2a:
                        basename = os.path.basename(path_file)
                        list_sat_c_b2a.append(basename)
                    self.Sat_data_dict_c_b2a, self.sat_band_list_B2a = self.main_func_2(list_sat_c_b2a, path)
                    list_dict_c.append(self.Sat_data_dict_c_b2a)
                    list_band_c.append(list_sat_c_b2a)

                if self.csv_files_BEIDOU_B3I:
                    self.obs_code_c.append("C6I")
                    self.obs_code_c.append("L6I")
                    self.obs_code_c.append("D6I")
                    for path_file in self.csv_files_BEIDOU_B3I:
                        basename = os.path.basename(path_file)
                        list_sat_c_b3i.append(basename)
                    self.Sat_data_dict_c_b3i, self.sat_band_list_B3I = self.main_func_2(list_sat_c_b3i, path)
                    list_dict_c.append(self.Sat_data_dict_c_b3i)
                    list_band_c.append(list_sat_c_b3i)

                header_str_11_str = self.obs_type_writer(self.sat_code, self.obs_code_c)

                for el in header_str_11_str:
                    self.fid_w.write(el)
                    self.fid_w.write('\n')

            if self.ubx_5.isChecked() or mixed_code == 1:
                self.sat_code = "J"
                self.csv_files_QZSS_L1CA = glob.glob(os.path.join(path, "QZSSL1CA*.csv"))
                self.csv_files_QZSS_L1CB = glob.glob(os.path.join(path, "QZSSL1CB*.csv"))
                self.csv_files_QZSS_L1C = glob.glob(os.path.join(path, "QZSSL1C *.csv"))
                self.csv_files_QZSS_L2C = glob.glob(os.path.join(path, "QZSSL2C *.csv"))
                self.csv_files_QZSS_L1S = glob.glob(os.path.join(path, "QZSSL1S *.csv"))
                self.csv_files_QZSS_L5S = glob.glob(os.path.join(path, "QZSSL5S *.csv"))
                self.csv_files_QZSS_L5 = glob.glob(os.path.join(path, "QZSSL5 *.csv"))

                if self.csv_files_QZSS_L1CA:
                    self.obs_code_j.append("C1C")
                    self.obs_code_j.append("L1C")
                    self.obs_code_j.append("D1C")
                    for path_file in self.csv_files_QZSS_L1CA:
                        basename = os.path.basename(path_file)
                        list_sat_j_l1ca.append(basename)
                    self.Sat_data_dict_j_L1CA, self.sat_band_list_L1CA = self.main_func_2(list_sat_j_l1ca, path)
                    list_dict_j.append(self.Sat_data_dict_j_L1CA)
                    list_band_j.append(list_sat_j_l1ca)

                if self.csv_files_QZSS_L1C:
                    self.obs_code_j.append("C1L")
                    self.obs_code_j.append("L1L")
                    self.obs_code_j.append("D1L")
                    # self.all_csv_j.append(self.csv_files_QZSS_L1C)
                    for path_file in self.csv_files_QZSS_L1C:
                        basename = os.path.basename(path_file)
                        list_sat_j_l1c.append(basename)
                    self.Sat_data_dict_j_L1C, self.sat_band_list_L1C = self.main_func_2(list_sat_j_l1c, path)
                    list_dict_j.append(self.Sat_data_dict_j_L1C)
                    list_band_j.append(list_sat_j_l1c)

                if self.csv_files_QZSS_L1S:
                    self.obs_code_j.append("C1Z")
                    self.obs_code_j.append("L1Z")
                    self.obs_code_j.append("D1Z")
                    # self.all_csv_j.append(self.csv_files_QZSS_L1S)

                if self.csv_files_QZSS_L2C:
                    self.obs_code_j.append("C2L")
                    self.obs_code_j.append("L2L")
                    self.obs_code_j.append("D2L")
                    # self.all_csv_j.append(self.csv_files_QZSS_L2C)
                    for path_file in self.csv_files_QZSS_L2C:
                        basename = os.path.basename(path_file)
                        list_sat_j_l2c.append(basename)
                    self.Sat_data_dict_j_L2C, self.sat_band_list_L1C = self.main_func_2(list_sat_j_l2c, path)
                    list_dict_j.append(self.Sat_data_dict_j_L2C)
                    list_band_j.append(list_sat_j_l2c)

                if self.csv_files_QZSS_L5:
                    self.obs_code_j.append("C5Q")
                    self.obs_code_j.append("L5Q")
                    self.obs_code_j.append("D5Q")
                    # self.all_csv_j.append(self.csv_files_QZSS_L5)
                    for path_file in self.csv_files_QZSS_L5:
                        basename = os.path.basename(path_file)
                        list_sat_j_l5.append(basename)
                    self.Sat_data_dict_j_L5, self.sat_band_list_L5 = self.main_func_2(list_sat_j_l5, path)
                    list_dict_j.append(self.Sat_data_dict_j_L5)
                    list_band_j.append(list_sat_j_l5)

                header_str_11_str = self.obs_type_writer(self.sat_code, self.obs_code_j)

                for el in header_str_11_str:
                    self.fid_w.write(el)
                    self.fid_w.write('\n')

            if self.ubx_6.isChecked() or mixed_code == 1:
                self.sat_code = "K"
                self.csv_files_KPS_L1CA = glob.glob(os.path.join(path, "OOO_CS_PSL_L1*.csv"))
                # self.csv_files_KPS_L1CB = glob.glob(os.path.join(path, "  *.csv"))
                # self.csv_files_KPS_L1C = glob.glob(os.path.join(path, "QZSSL1C *.csv"))
                self.csv_files_KPS_L2C = glob.glob(os.path.join(path, "OOO_CS_PSL_L2 *.csv"))
                # self.csv_files_KPS_L1S = glob.glob(os.path.join(path, "QZSSL1S *.csv"))
                # self.csv_files_KPS_L5S = glob.glob(os.path.join(path, "OOO_CS_PSL_S *.csv"))
                self.csv_files_KPS_L5 = glob.glob(os.path.join(path, "OOO_CS_PSL_L5 *.csv"))
                self.csv_files_KPS_S = glob.glob(os.path.join(path, "OOO_CS_PSL_S *.csv"))

                if self.csv_files_KPS_L1CA:
                    self.obs_code_k.append("C1C")
                    self.obs_code_k.append("L1C")
                    self.obs_code_k.append("D1C")
                    for path_file in self.csv_files_KPS_L1CA:
                        basename = os.path.basename(path_file)
                        list_sat_k_l1ca.append(basename)
                    self.Sat_data_dict_k_L1CA, self.sat_band_list_L1CA = self.main_func_2(list_sat_k_l1ca, path)
                    list_dict_k.append(self.Sat_data_dict_k_L1CA)
                    list_band_k.append(list_sat_k_l1ca)

                # if self.csv_files_QZSS_L1C:
                #     self.obs_code_j.append("C1L")
                #     self.obs_code_j.append("L1L")
                #     self.obs_code_j.append("D1L")
                #     # self.all_csv_j.append(self.csv_files_QZSS_L1C)
                #     for path_file in self.csv_files_QZSS_L1C:
                #         basename = os.path.basename(path_file)
                #         list_sat_j_l1c.append(basename)
                #     self.Sat_data_dict_j_L1C, self.sat_band_list_L1C = self.main_func_2(list_sat_j_l1c, path)
                #     list_dict_j.append(self.Sat_data_dict_j_L1C)
                #     list_band_j.append(list_sat_j_l1c)

                # if self.csv_files_QZSS_L1S:
                #     self.obs_code_j.append("C1Z")
                #     self.obs_code_j.append("L1Z")
                #     self.obs_code_j.append("D1Z")
                #     # self.all_csv_j.append(self.csv_files_QZSS_L1S)

                if self.csv_files_KPS_L2C:
                    self.obs_code_k.append("C2L")
                    self.obs_code_k.append("L2L")
                    self.obs_code_k.append("D2L")
                    for path_file in self.csv_files_KPS_L2C:
                        basename = os.path.basename(path_file)
                        list_sat_k_l2c.append(basename)
                    self.Sat_data_dict_k_L2C, self.sat_band_list_L1C = self.main_func_2(list_sat_k_l2c, path)
                    list_dict_k.append(self.Sat_data_dict_k_L2C)
                    list_band_k.append(list_sat_k_l2c)

                if self.csv_files_KPS_L5:
                    self.obs_code_k.append("C5Q")
                    self.obs_code_k.append("L5Q")
                    self.obs_code_k.append("D5Q")
                    # self.all_csv_j.append(self.csv_files_QZSS_L5)
                    for path_file in self.csv_files_KPS_L5:
                        basename = os.path.basename(path_file)
                        list_sat_k_l5.append(basename)
                    self.Sat_data_dict_k_L5, self.sat_band_list_L5 = self.main_func_2(list_sat_k_l5, path)
                    list_dict_k.append(self.Sat_data_dict_k_L5)
                    list_band_k.append(list_sat_k_l5)

                header_str_11_str = self.obs_type_writer(self.sat_code, self.obs_code_k)

                for el in header_str_11_str:
                    self.fid_w.write(el)
                    self.fid_w.write('\n')

            if self.ubx_7.isChecked() or mixed_code == 1:
                self.sat_code = "I"
                self.header_name = 'resources/L1C_header.rnx'
                self.csv_files_NAVIC_L5 = glob.glob(os.path.join(path, "NAVICL5 *.csv"))

                if self.csv_files_NAVIC_L5:
                    self.obs_code_i.append("C5A")
                    self.obs_code_i.append("L5A")
                    self.obs_code_i.append("D5A")
                    for path_file in self.csv_files_NAVIC_L5:
                        basename = os.path.basename(path_file)
                        list_sat_i_l5.append(basename)
                    self.Sat_data_dict_i_L5, self.sat_band_list_L5 = self.main_func_2(list_sat_i_l5, path)
                    list_dict_i.append(self.Sat_data_dict_i_L5)
                    list_band_i.append(list_sat_i_l5)

                header_str_11_str = self.obs_type_writer(self.sat_code, self.obs_code_i)

                for el in header_str_11_str:
                    self.fid_w.write(el)
                    self.fid_w.write('\n')

            if self.ubx_8.isChecked() or mixed_code == 1:
                self.sat_code = "S"
                self.csv_files_SBAS_L1 = glob.glob(os.path.join(path, "SBASL1 *.csv"))
                self.csv_files_SBAS_L5 = glob.glob(os.path.join(path, "SBASL5 *.csv"))

                if self.csv_files_SBAS_L1:
                    self.obs_code_s.append("C1C")
                    self.obs_code_s.append("L1C")
                    self.obs_code_s.append("D1C")
                    for path_file in self.csv_files_SBAS_L1:
                        basename = os.path.basename(path_file)
                        list_sat_s_l1.append(basename)
                    self.Sat_data_dict_s_L1, self.sat_band_list_L1 = self.main_func_2(list_sat_s_l1, path)
                    list_dict_s.append(self.Sat_data_dict_s_L1)
                    list_band_s.append(list_sat_s_l1)

                if self.csv_files_SBAS_L5:
                    self.obs_code_s.append("C5I")
                    self.obs_code_s.append("L5I")
                    self.obs_code_s.append("D5I")
                    for path_file in self.csv_files_SBAS_L5:
                        basename = os.path.basename(path_file)
                        list_sat_s_l5.append(basename)
                    self.Sat_data_dict_s_L5, self.sat_band_list_L5 = self.main_func_2(list_sat_s_l5, path)
                    list_dict_s.append(self.Sat_data_dict_s_L5)
                    list_band_s.append(list_sat_s_l5)

                header_str_11_str = self.obs_type_writer(self.sat_code, self.obs_code_s)

                for el in header_str_11_str:
                    self.fid_w.write(el)
                    self.fid_w.write('\n')

            self.fid_w.write(header_str_12)
            self.fid_w.write('\n')

            header_str_13 = "                                                            END OF HEADER"
            self.fid_w.write(header_str_13)
            self.fid_w.write('\n')

            self.main_func_5(delta_ms, list_dict_g, list_dict_r, list_dict_e, list_dict_c, list_dict_j, list_dict_k,
                             list_dict_s, list_dict_i, list_band_g, list_band_r, list_band_e, list_band_c, list_band_i,
                             list_band_s, list_band_j, list_band_k)
            self.end_process.setText("Done!")

            self.fid_w.close()
        except FileNotFoundError as err_file:
            print(err_file)
            QMessageBox.about(self, "File Not Found Error", "Please save a new file")
            pass

        except PermissionError as err_file:
            print(err_file)
            QMessageBox.about(self, "Permission Error", "Please save a new file")
            pass

    def main_func_2(self, sat_visible, path):
        """
        :param sat_visible:
        :param path:
        :return:
        """
        lines = []
        sat_band_list = []
        count_line = 0

        Sat_data_dict = {
            "T_SAT": [],
            "PSR": [],
            "ADR": [],
            "TIME": [],
            "DOP": [],
            "SAT_CODE_BAND": []
        }

        for sat in sat_visible:

            basename = sat.split(" ")

            sat_int = basename[1]
            basename = sat_int.split(".")
            m = int(basename[0])
            name = os.path.join(path, sat)
            with open(name, 'r') as fid_sat:
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

            name = os.path.join(path, sat)

            with open(name, 'r') as fid_sat:

                basename = sat.split(" ")
                sat_band = basename[0]

                t_sat = []
                psr = []
                adr = []
                dop = []
                t_time = []
                data_band = []

                reader = csv.reader(fid_sat)
                next(reader)

                for row in reader:
                    lines.append(row)
                    temp_num_line = row
                    data_band.append(str(sat_band))
                    t_time.append(int(temp_num_line[0]))
                    t_sat.append(float(temp_num_line[29]))
                    psr.append(float(temp_num_line[10]))
                    adr.append(float(temp_num_line[11]))
                    dop.append(float(temp_num_line[25]))

            Sat_data_dict["T_SAT"].append(t_sat)
            Sat_data_dict["PSR"].append(psr)
            Sat_data_dict["ADR"].append(adr)
            Sat_data_dict["TIME"].append(t_time)
            Sat_data_dict["DOP"].append(dop)
            Sat_data_dict["SAT_CODE_BAND"].append(data_band)

        return Sat_data_dict, sat_band_list

    def main_func_5(self, second, list_dict_g, list_dict_r, list_dict_e, list_dict_c, list_dict_j, list_dict_k,
                    list_dict_s, list_dict_i, list_band_g, list_band_r, list_band_e, list_band_c, list_band_i,
                    list_band_s, list_band_j, list_band_k):

        global N_g, N_j, N_e, N_r, N_i, N_s, N_c, N_k

        n_list_g = []
        if not list_dict_g:
            pass
            N_g = 0
        else:
            for dict_g in list_dict_g:
                for k_g in range(0, len(dict_g["T_SAT"]), 1):
                    N_g = len(dict_g["T_SAT"][k_g])
                    n_list_g.append(N_g)
                N_g = max(n_list_g)
                break
        count_line_sat_g = len(n_list_g)

        n_list_j = []
        if not list_dict_j:
            pass
            N_j = 0
        else:
            for dict_j in list_dict_j:
                for k_j in range(0, len(dict_j["T_SAT"]), 1):
                    N_j = len(dict_j["T_SAT"][k_j])
                    n_list_j.append(N_j)
                N_j = max(n_list_j)
                break
        count_line_sat_j = len(n_list_j)

        n_list_k = []
        if not list_dict_k:
            pass
            N_k = 0
        else:
            for dict_k in list_dict_k:
                for k_k in range(0, len(dict_k["T_SAT"]), 1):
                    N_k = len(dict_k["T_SAT"][k_k])
                    n_list_k.append(N_k)
                N_k = max(n_list_k)
                break
        count_line_sat_k = len(n_list_k)

        n_list_r = []
        if not list_dict_r:
            pass
            N_r = 0
        else:
            for dict_r in list_dict_r:
                for k_r in range(0, len(dict_r["T_SAT"]), 1):
                    N_r = len(dict_r["T_SAT"][k_r])
                    n_list_r.append(N_r)
                N_r = max(n_list_r)
                break
        count_line_sat_r = len(n_list_r)

        n_list_e = []
        if not list_dict_e:
            pass
            N_e = 0
        else:
            for dict_e in list_dict_e:
                for k_e in range(0, len(dict_e["T_SAT"]), 1):
                    N_e = len(dict_e["T_SAT"][k_e])
                    n_list_e.append(N_e)
                N_e = max(n_list_e)
                break
        count_line_sat_e = len(n_list_e)

        n_list_s = []
        if not list_dict_s:
            pass
            N_s = 0
        else:
            for dict_s in list_dict_s:
                for k_s in range(0, len(dict_s["T_SAT"]), 1):
                    N_s = len(dict_s["T_SAT"][k_s])
                    n_list_s.append(N_s)
                N_s = max(n_list_s)
                break
        count_line_sat_s = len(n_list_s)

        n_list_i = []
        if not list_dict_i:
            pass
            N_i = 0
        else:
            for dict_i in list_dict_i:
                for k_i in range(0, len(dict_i["T_SAT"]), 1):
                    N_i = len(dict_i["T_SAT"][k_i])
                    n_list_i.append(N_i)
                N_i = max(n_list_i)
                break
        count_line_sat_i = len(n_list_i)

        n_list_c = []
        if not list_dict_c:
            pass
            N_c = 0
        else:
            for dict_c in list_dict_c:
                for k_c in range(0, len(dict_c["T_SAT"]), 1):
                    N_c = len(dict_c["T_SAT"][k_c])
                    n_list_c.append(N_c)
                N_c = max(n_list_c)
                break
        count_line_sat_c = len(n_list_c)

        N = max([N_g, N_j, N_e, N_r, N_s, N_i, N_c, N_k])

        count_line_sat = (
                    count_line_sat_g + count_line_sat_j + count_line_sat_k + count_line_sat_e + count_line_sat_s + count_line_sat_r
                    + count_line_sat_c + count_line_sat_i)

        time_comp = 500
        List_month_30 = [1, 4, 6, 9, 11]
        List_month_31 = [3, 5, 7, 8, 10, 12]

        for n in range(0, N, 1):
            # *********************************************************************#
            if int(second) >= 59.9:

                if self.minute_count == 59:
                    self.minute_count = 0
                    self.hour_count = self.hour_count + 1
                else:
                    self.minute_count = self.minute_count + 1

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
                    self.month_count = self.month_count + 1

                    if int(self.month_count) >= 12:
                        self.month_count = 1
                        self.year_count = self.year_count + 1

            if int(self.day_count) == 28:
                if int(self.month_count) == 2:
                    self.month_count = self.month_count + 1

            second = np.mod(second, 60)

            tline = str('> ') + '{:0<4.0f}'.format(self.year_count) + str(' ') + "{:02d}".format(
                self.month_count) + str(' ') + "{:02d}".format(
                self.day_count) + str(' ') + "{:02d}".format(self.hour_count) + str(' ') + str(
                "{0:0=2d}".format(self.minute_count)) + str(
                ' ') + '{:0<10.7f}'.format(second) + str('  0 ') + "{:02d}".format(count_line_sat)

            self.fid_w.write(tline)
            self.fid_w.write('\n')

            second = second + self.time_step_list[0]

            # *********************************************************************#
            cnt_1 = 0

            if self.ubx_9.isChecked():
                mixed_code = 1
            else:
                mixed_code = 0

            if self.ubx_1.isChecked() or mixed_code == 1:
                if list_band_g:
                    for cnt_2 in range(len(list_band_g[cnt_1])):

                        m1 = list_band_g[cnt_1][cnt_2]
                        basename = m1.split(" ")
                        sat_band = basename[0]
                        sat_int = basename[1]
                        basename = sat_int.split(".")
                        m2 = int(basename[0])
                        tline_2 = "G" + str("{:02d}".format(int(m2)))

                        for dict_data in list_dict_g:

                            if time_comp in list(dict_data["TIME"][cnt_2]):
                                time_id = list(dict_data["TIME"][cnt_2]).index(time_comp)
                                psr = str('{: >14.3f}'.format(dict_data["PSR"][cnt_2][time_id]))
                                adr = str('{: >14.3f}'.format(dict_data["ADR"][cnt_2][time_id]))
                                dop = str('{: >14.3f}'.format(dict_data["DOP"][cnt_2][time_id]))

                                if not psr:
                                    psr = "              "
                                if not adr:
                                    adr = "              "
                                if not dop:
                                    dop = "              "

                                tline_temp = psr + " " + str(7) + adr + " " + str(7) + dop + " " + str(7)

                                tline_2 = tline_2 + tline_temp

                            else:
                                pass

                        if len(tline_2) <= 4:
                            pass
                        else:
                            self.fid_w.write(tline_2)
                            self.fid_w.write('\n')

            if self.ubx_2.isChecked() or mixed_code == 1:
                if list_band_r:
                   for cnt_2 in range(len(list_band_r[cnt_1])):
                    m1 = list_band_r[cnt_1][cnt_2]
                    basename = m1.split(" ")
                    sat_band = basename[0]
                    sat_int = basename[1]
                    basename = sat_int.split(".")
                    m2 = int(basename[0])

                    tline_2 = "R" + str("{:02d}".format(int(m2)))

                    for dict_data in list_dict_r:
                        if time_comp in list(dict_data["TIME"][cnt_2]):
                            time_id = list(dict_data["TIME"][cnt_2]).index(time_comp)

                            psr = str('{: >14.3f}'.format(dict_data["PSR"][cnt_2][time_id]))
                            adr = str('{: >14.3f}'.format(dict_data["ADR"][cnt_2][time_id]))
                            dop = str('{: >14.3f}'.format(dict_data["DOP"][cnt_2][time_id]))

                            if not psr:
                                psr = "              "
                            if not adr:
                                adr = "              "
                            if not dop:
                                dop = "              "

                            tline_temp = psr + " " + str(7) + adr + " " + str(7) + dop + " " + str(7)
                            tline_2 = tline_2 + tline_temp
                        else:
                            pass

                    if len(tline_2) <= 4:
                        pass
                    else:
                        self.fid_w.write(tline_2)
                        self.fid_w.write('\n')

            if self.ubx_3.isChecked() or mixed_code == 1:
                if list_band_e:
                    for cnt_2 in range(len(list_band_e[cnt_1])):
                        m1 = list_band_e[cnt_1][cnt_2]
                        basename = m1.split(" ")
                        sat_band = basename[0]
                        sat_int = basename[1]
                        basename = sat_int.split(".")
                        m2 = int(basename[0])

                        tline_2 = "E" + str("{:02d}".format(int(m2)))

                        for dict_data in list_dict_e:

                            if time_comp in list(dict_data["TIME"][cnt_2]):
                                time_id = list(dict_data["TIME"][cnt_2]).index(time_comp)

                                psr = str('{: >14.3f}'.format(dict_data["PSR"][cnt_2][time_id]))
                                adr = str('{: >14.3f}'.format(dict_data["ADR"][cnt_2][time_id]))
                                dop = str('{: >14.3f}'.format(dict_data["DOP"][cnt_2][time_id]))

                                if not psr:
                                    psr = "              "
                                if not adr:
                                    adr = "              "
                                if not dop:
                                    dop = "              "

                                tline_temp = psr + " " + str(7) + adr + " " + str(7) + dop + " " + str(7)
                                tline_2 = tline_2 + tline_temp
                            else:
                                pass

                        if len(tline_2) <= 4:
                            pass
                        else:
                            self.fid_w.write(tline_2)
                            self.fid_w.write('\n')

            if self.ubx_4.isChecked() or mixed_code == 1:
                if list_band_c:
                    for cnt_2 in range(len(list_band_c[cnt_1])):
                        m1 = list_band_c[cnt_1][cnt_2]
                        basename = m1.split(" ")
                        sat_band = basename[0]
                        sat_int = basename[1]
                        basename = sat_int.split(".")
                        m2 = int(basename[0])

                        tline_2 = "C" + str("{:02d}".format(int(m2)))

                        for dict_data in list_dict_c:
                            if time_comp in list(dict_data["TIME"][cnt_2]):
                                time_id = list(dict_data["TIME"][cnt_2]).index(time_comp)
                                psr = str('{: >14.3f}'.format(dict_data["PSR"][cnt_2][time_id]))
                                adr = str('{: >14.3f}'.format(dict_data["ADR"][cnt_2][time_id]))
                                dop = str('{: >14.3f}'.format(dict_data["DOP"][cnt_2][time_id]))

                                if not psr:
                                    psr = "              "
                                if not adr:
                                    adr = "              "
                                if not dop:
                                    dop = "              "

                                tline_temp = psr + " " + str(7) + adr + " " + str(7) + dop + " " + str(7)
                                tline_2 = tline_2 + tline_temp

                            else:
                                pass
                        if len(tline_2) <= 4:
                            pass
                        else:
                            self.fid_w.write(tline_2)
                            self.fid_w.write('\n')

            if self.ubx_5.isChecked() or mixed_code == 1:
                if list_band_j:
                    for cnt_2 in range(len(list_band_j[cnt_1])):
                        m1 = list_band_j[cnt_1][cnt_2]
                        basename = m1.split(" ")
                        sat_band = basename[0]
                        sat_int = basename[1]
                        basename = sat_int.split(".")
                        m2 = int(basename[0])

                        tline_2 = "J" + str("{:02d}".format(int(m2)))

                        for dict_data in list_dict_c:

                            if time_comp in list(dict_data["TIME"][cnt_2]):
                                time_id = list(dict_data["TIME"][cnt_2]).index(time_comp)
                                psr = str('{: >14.3f}'.format(dict_data["PSR"][cnt_2][time_id]))
                                adr = str('{: >14.3f}'.format(dict_data["ADR"][cnt_2][time_id]))
                                dop = str('{: >14.3f}'.format(dict_data["DOP"][cnt_2][time_id]))

                                if not psr:
                                    psr = "              "
                                if not adr:
                                    adr = "              "
                                if not dop:
                                    dop = "              "

                                tline_temp = psr + " " + str(7) + adr + " " + str(7) + dop + " " + str(7)
                                tline_2 = tline_2 + tline_temp

                            else:
                                pass

                        if len(tline_2) <= 4:
                            pass
                        else:
                            self.fid_w.write(tline_2)
                            self.fid_w.write('\n')

            if self.ubx_6.isChecked() or mixed_code == 1:
                if list_band_k:
                    for cnt_2 in range(len(list_band_k[cnt_1])):
                        m1 = list_band_k[cnt_1][cnt_2]
                        basename = m1.split(" ")
                        sat_band = basename[0]
                        sat_int = basename[1]
                        basename = sat_int.split(".")
                        m2 = int(basename[0])

                        tline_2 = "K" + str("{:02d}".format(int(m2)))

                        for dict_data in list_dict_k:

                            if time_comp in list(dict_data["TIME"][cnt_2]):
                                time_id = list(dict_data["TIME"][cnt_2]).index(time_comp)
                                psr = str('{: >14.3f}'.format(dict_data["PSR"][cnt_2][time_id]))
                                adr = str('{: >14.3f}'.format(dict_data["ADR"][cnt_2][time_id]))
                                dop = str('{: >14.3f}'.format(dict_data["DOP"][cnt_2][time_id]))

                                if not psr:
                                    psr = "              "
                                if not adr:
                                    adr = "              "
                                if not dop:
                                    dop = "              "

                                tline_temp = psr + " " + str(7) + adr + " " + str(7) + dop + " " + str(7)
                                tline_2 = tline_2 + tline_temp

                            else:
                                pass
                        if len(tline_2) <= 4:
                            pass
                        else:
                            self.fid_w.write(tline_2)
                            self.fid_w.write('\n')

            if self.ubx_7.isChecked() or mixed_code == 1:
                if list_band_i:
                    for cnt_2 in range(len(list_band_i[cnt_1])):
                        m1 = list_band_i[cnt_1][cnt_2]
                        basename = m1.split(" ")
                        sat_band = basename[0]
                        sat_int = basename[1]
                        basename = sat_int.split(".")
                        m2 = int(basename[0])

                        tline_2 = "I" + str("{:02d}".format(int(m2)))

                        for dict_data in list_dict_i:
                            if time_comp in list(dict_data["TIME"][cnt_2]):
                                time_id = list(dict_data["TIME"][cnt_2]).index(time_comp)

                                psr = str('{: >14.3f}'.format(dict_data["PSR"][cnt_2][time_id]))
                                adr = str('{: >14.3f}'.format(dict_data["ADR"][cnt_2][time_id]))
                                dop = str('{: >14.3f}'.format(dict_data["DOP"][cnt_2][time_id]))

                                if not psr:
                                    psr = "              "
                                if not adr:
                                    adr = "              "
                                if not dop:
                                    dop = "              "

                                tline_temp = psr + " " + str(7) + adr + " " + str(7) + dop + " " + str(7)
                                tline_2 = tline_2 + tline_temp

                                if len(tline_2) <= 4:
                                    pass
                                else:
                                    self.fid_w.write(tline_2)
                                    self.fid_w.write('\n')
                            else:
                                pass

            if self.ubx_8.isChecked() or mixed_code == 1:
                if list_band_s:
                    for cnt_2 in range(len(list_band_s[cnt_1])):
                        m1 = list_band_s[cnt_1][cnt_2]
                        basename = m1.split(" ")
                        sat_band = basename[0]
                        sat_int = basename[1]
                        basename = sat_int.split(".")
                        m2 = int(basename[0])

                        tline_2 = "S" + str("{:02d}".format(int(m2)))
                        for dict_data in list_dict_s:
                            if time_comp in list(dict_data["TIME"][cnt_2]):
                                time_id = list(dict_data["TIME"][cnt_2]).index(time_comp)
                                psr = str('{: >14.3f}'.format(dict_data["PSR"][cnt_2][time_id]))
                                adr = str('{: >14.3f}'.format(dict_data["ADR"][cnt_2][time_id]))
                                dop = str('{: >14.3f}'.format(dict_data["DOP"][cnt_2][time_id]))

                                if not psr:
                                    psr = "              "
                                if not adr:
                                    adr = "              "
                                if not dop:
                                    dop = "              "

                                tline_temp = psr + " " + str(7) + adr + " " + str(7) + dop + " " + str(7)
                                tline_2 = tline_2 + tline_temp

                            else:
                                pass
                        if len(tline_2) <= 4:
                            pass
                        else:
                            self.fid_w.write(tline_2)
                            self.fid_w.write('\n')

            time_comp = time_comp + 100

    def reset_func(self):
        """
        Reset function
        """
        self.end_process.setText("")
        self.dir_path.setText("")
        self.year.setText("2023")
        self.month.setText("9")
        self.day.setText("14")
        self.hour.setText("12")
        self.minutes.setText("0")
        self.secondes.setText("0")

        self.ubx_1.setChecked(False)
        self.ubx_2.setChecked(False)
        self.ubx_3.setChecked(False)
        self.ubx_4.setChecked(False)
        self.ubx_5.setChecked(False)
        self.ubx_6.setChecked(False)
        self.ubx_7.setChecked(False)
        self.ubx_8.setChecked(False)
        self.ubx_9.setChecked(False)

        self.generate_rinex_button.setEnabled(False)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    qtmodern.styles.light(app)
    mw = qtmodern.windows.ModernWindow(w)
    mw.show()
    w.show()
    app.exec_()
