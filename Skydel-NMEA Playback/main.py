import codecs
import csv
import os
import sys
import time
from datetime import datetime

import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget
from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtWidgets import QMenuBar, QMessageBox, QGroupBox, QCheckBox

import pynmea2
import skydelsdx
from skydelsdx.commands import *
from skydelsdx.units import *


def quit_app():
    """Close the application"""
    quit()


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.nmea_file_name = None
        self.gsv_file_open = None
        self.gsv_filename = None
        self.gsa_file_open = None
        self.traj_file = None
        self.gsv_file = None
        self.gsa_file = None
        self.sim = None
        self.traj_filename = None
        self.traj_file_open = None
        self.gga_time_open = None

        self.gsv_csvfile_writer = None
        self.gsa_csvfile_writer = None
        self.gsa_filename = None
        self.gga_time_writer = None
        self.rmc_csvfile_writer = None
        self.rmc_file_open = None
        self.gga_time_filename = None
        self.rmc_filename = None
        self.rmc_file = None
        self.traj_csvfile_writer = None
        self.elapsed_gga = None
        """Variables initialization and UI items definition"""
        self.table_gga_elapsed = []
        self.table_rmc_elapsed = []
        self.table_gga_time = []
        self.table_rmc_elapsed = []
        self.table_date_rmc = []
        self.table_rmc = []
        self.elapsed_second = 0
        self.running_mode = str()
        self.testfilename = ""
        self.save_folder = ""
        self.load_folder = ""
        self.running_stop = False
        self.list_GNSS_ID = []
        self.ind = 0
        self.global_output_val = "None"

        # Safran Logo setting
        hlay = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('LOGO_SAFRAN_rvb.png')
        label.resize(165, 165)
        label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio))
        hlay.addWidget(label, 0)

        # MenuBar setting
        menubar = QMenuBar()
        actionfile00 = menubar.addMenu("File")
        actionfile00.addAction("Quit")
        actionfile00.triggered.connect(self.close)
        frame1 = QtWidgets.QFrame(self)
        frame1.setFrameShadow(QtWidgets.QFrame.Plain)

        # Layout spacer definition
        spaceritem = QtWidgets.QSpacerItem(102, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # Load NMEA file settings
        self.load_file_button_layout = QtWidgets.QHBoxLayout()
        self.load_file_button = QtWidgets.QPushButton('Load NMEA file')
        self.load_file_button.setFont(QFont('Arial', 10))
        self.load_file_button.clicked.connect(self.load_nmea_file)
        self.load_file_button_layout.setAlignment(Qt.AlignCenter)
        self.load_file_button_layout.addWidget(self.load_file_button)

        self.file_group = QGroupBox("File settings")
        self.file_group.setFont(QFont('Arial', 9))
        self.file_group_layout = QtWidgets.QVBoxLayout()
        self.file_group.setLayout(self.file_group_layout)
        self.file_group_layout.addLayout(self.load_file_button_layout)

        # Save parsed NMEA Data settings
        self.save_checkbox = QCheckBox("Save CSV.")
        self.labelA = QLabel("")
        self.labelA.setText("Not saving.")
        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.setFont(QFont('Arial', 10))
        self.start_button.pressed.connect(self.pre_start)
        self.start_button.setEnabled(False)

        save_group = QGroupBox("Save Options")
        save_group.setFont(QFont('Arial', 9))
        save_layout = QtWidgets.QVBoxLayout()
        save_group.setLayout(save_layout)
        save_layout.addWidget(self.labelA, 1)
        save_layout.addWidget(self.start_button, 1)

        # Playback in NMEA settings
        self.playback_button_layout = QtWidgets.QVBoxLayout()
        self.playback_button = QtWidgets.QPushButton('Arm / Start')
        self.playback_button.setFont(QFont('Arial', 9))
        self.playback_button.pressed.connect(self.playback_skydel_2)
        self.playback_button.setEnabled(False)

        self.Skydel_output_label = QLabel("")
        self.Skydel_output_label.setText("Output type")

        self.output_selection_comboBox = QtWidgets.QComboBox()
        self.output_selection_comboBox.addItem("None")
        self.output_selection_comboBox.addItem("NoneRT")
        self.output_selection_comboBox.addItem("DTA-2115B")
        self.output_selection_comboBox.addItem("DTA-2116")
        # self.output_selection_comboBox.addItem("X300")
        # self.output_selection_comboBox.addItem("N310")

        # Skydel Logo setting
        skydel_logo = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('LOGO_SKYDEL.png')
        skydel_logo.resize(175, 175)
        skydel_logo.setAlignment(Qt.AlignCenter)
        skydel_logo.setPixmap(pixmap.scaled(skydel_logo.size(), QtCore.Qt.KeepAspectRatio))

        self.output_selection_comboBox.activated[str].connect(self.output_type)

        self.layout_output_type = QtWidgets.QHBoxLayout()
        self.layout_output_type.addWidget(self.Skydel_output_label, 0)
        self.layout_output_type.addWidget(self.output_selection_comboBox, 1)

        skydel_group = QGroupBox("Playback in Skydel")
        skydel_group.setFont(QFont('Arial', 9))
        skydel_group_layout = QtWidgets.QVBoxLayout()
        skydel_group.setLayout(skydel_group_layout)
        skydel_group_layout.addWidget(skydel_logo, 0)
        skydel_group_layout.addLayout(self.layout_output_type, 1)
        skydel_group_layout.addItem(spaceritem)
        skydel_group_layout.addWidget(self.playback_button, 2)

        layout4 = QtWidgets.QVBoxLayout()
        layout4.addWidget(menubar, 0)
        layout4.addItem(spaceritem)
        layout4.addWidget(self.file_group, 1)
        layout4.addItem(spaceritem)
        layout4.addWidget(save_group, 2)
        layout4.addItem(spaceritem)
        layout4.addWidget(skydel_group, 3)

        # Message parsing section setting
        self.layout3 = QtWidgets.QHBoxLayout()
        self.title1 = QLabel("NMEA MESSAGE PARSING")
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setFont(QFont('Arial', 10))
        self.title1.setStyleSheet("background-color:#0f60a7; border-radius:5px")
        self.stop_button = QtWidgets.QPushButton('Stop parsing')
        self.stop_button.setFont(QFont('Arial', 10))
        self.stop_button.clicked.connect(self.stop_streaming_func)
        self.layout3.addWidget(self.title1, 4)
        layout2 = QtWidgets.QHBoxLayout()
        self.show_message = QtWidgets.QTextEdit()
        self.show_message.setFont(QFont('Arial', 9))
        self.cursor = self.show_message.textCursor()
        self.cursor.insertText("NMEA STREAMING BOARD")
        self.show_other_message = QtWidgets.QTextEdit()
        self.show_other_message.setFont(QFont('Arial', 9))
        layout2.addWidget(self.show_other_message, 0)
        layout2.addWidget(self.show_message, 1)
        layout1 = QtWidgets.QVBoxLayout()
        layout1.addLayout(self.layout3, 0)
        layout1.addLayout(layout2, 1)
        layout = QtWidgets.QHBoxLayout()
        layout.addLayout(layout4, 0)
        layout.addLayout(layout1, 1)
        layout_final = QtWidgets.QVBoxLayout()
        layout_final.addLayout(hlay, 0)
        layout_final.addLayout(layout, 1)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout_final)
        self.resize(1324, 924)
        self.setCentralWidget(widget)
        qtrectangle = self.frameGeometry()
        centerpoint = QDesktopWidget().availableGeometry().center()
        qtrectangle.moveCenter(centerpoint)
        self.move(qtrectangle.topLeft())

    def load_nmea_file(self):
        """
        :return: This function allow user to select an NMEA file with the following extension *.txt, *.csv, *.log, 
        *.nmea, *.ubx
        """
        
        self.nmea_file_name, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + " DATA Files", ".",
                                                                             "(*.txt *.csv *.log *.nmea *.ubx)")
        
        if self.nmea_file_name:
            self.screen_1("\n")
            self.screen_1("FILE MODE:")
            self.screen_1(self.nmea_file_name)  # Display of the NMEA file name on the
            self.start_button.setEnabled(True)
        else:
            QMessageBox.about(self, "Load NMEA file error", "File not found.")

    def savecsv_checkaction_2(self):

        folder_selection = 0

        self.save_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if self.save_folder == "":
            QMessageBox.about(self, "CSV FOLDER PATH", "THE FOLDER PATH IS EMPTY.")
            self.save_checkbox.setChecked(False)

        elif not os.path.exists(self.save_folder):
            QMessageBox.about(self, "CSV FOLDER PATH", "THE SPECIFIED FOLDER IS NOT VALID")

        elif self.save_folder:
            self.screen_1("\n")
            self.screen_1("CSV FILE SAVED HERE:")
            self.screen_1(self.save_folder)
            return self.save_folder

        if folder_selection == 0:
            return 0

    def bad_folder(self):
        """
        :return: This fonction will be call when an error occur while selecting the save csv folder
        """
        buttonreply = QMessageBox.question(self, 'Folder selection', "Do you want to select a new folder?",
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                           QMessageBox.Cancel)

        if buttonreply == QMessageBox.Yes:
            print('Yes clicked.')
            self.savecsv_checkaction_2()
            # folder_action = "No"

        if buttonreply == QMessageBox.No:
            print('No clicked.')
            folder_action = "No"
            return folder_action

        if buttonreply == QMessageBox.Cancel:
            print('Cancel')
            folder_action = "Cancel"
            return folder_action

    def load_csv_skydel(self):
        """
        :return: This fonction allow the user to parse the selected NMEA file and generate the data into CSV files
        """

        self.load_folder = ""

        if self.load_folder == "":
            self.load_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            self.screen_1("\n")
            self.screen_1("CSV FILE SAVED HERE:")
            self.screen_1(self.load_folder)
            return self.load_folder

        if self.load_folder:
            self.screen_1("\n")
            self.screen_1("CSV FILE WILL BE LOADED HERE:")
            self.screen_1(self.load_folder)
            return self.load_folder

    def delete_folder(self, folder):
        """
        :param folder: This function will delete all csv file in the selected NMEA folder
        :return:
        """
        if folder:
            files_in_directory = os.listdir(folder)
            filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
            for file in filtered_files:
                path_to_file = os.path.join(folder, file)
                try:
                    os.remove(path_to_file)
                    print("Removing file:", path_to_file)
                except PermissionError as err:
                    print(err)
                    QMessageBox.about(self, "DELETING CSV FILE ERROR", str(err))

    def pre_start(self):

        self.table_gga_elapsed = []
        self.table_gga_time = []
        self.table_rmc_elapsed = []
        self.table_rmc = []
        self.table_rmc_elapsed = []
        self.table_date_rmc = []
        self.elapsed_second = 0
        self.running_mode = str()

        self.running_stop = False
        self.list_GNSS_ID = []
        print("--- self.Streaming START")
        self.screen_1("\n")
        self.screen_1("--- Streaming START")

        self.layout3.addWidget(self.stop_button, 1)

        self.layout3.addWidget(self.title1, 4)
        self.start()
        self.screen_1("\n")
        self.screen_1("--- Streaming END.")
        # self.running_stop = False
        self.stop_streaming_func()

    def start(self):

        self.labelA.setText("Saving.")

        folder_selection = 0

        self.save_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if self.save_folder == "":
            QMessageBox.about(self, "CSV FOLDER PATH", "THE FOLDER PATH IS EMPTY.")
            self.save_checkbox.setChecked(False)

        elif not os.path.exists(self.save_folder):
            QMessageBox.about(self, "CSV FOLDER PATH", "THE SPECIFIED FOLDER IS NOT VALID")

        elif self.save_folder:
            folder_selection = 1

            self.screen_1("\n")
            self.screen_1("CSV FILE SAVED HERE:")
            self.screen_1(self.save_folder)

        self.running_stop = False

        if folder_selection == 0:
            folder_choice = self.bad_folder()

            if folder_choice == "No":
                pass

            elif folder_choice == "Cancel":
                pass

        else:
            try:
                self.screen_1("\n")  # MY_FUNCTION_CALL
                self.screen_1("--- Streaming ...")  # MY_FUNCTION_CALL
                # file = open(self.nmea_file_name,
                #             encoding='utf-8')

                file = codecs.open(self.nmea_file_name, 'r', encoding='utf-8',
                                   errors='ignore')

                rmc_fieldnames = ['Elapsed time (ms)', 'Timestamp', 'Status', 'Latitude', 'Latitude Direction',
                                  'Longitude',
                                  'Longitude Direction',
                                  'Speed Over Ground', 'True Course', 'Datestamp', 'Magnetic Variation',
                                  'Magnetic Variation Direction',
                                  'Mode Indicator', 'Navigational Status']

                gga_time_fieldnames = ['True date', 'Calculated date', 'True seconds', 'Calculated seconds']

                self.rmc_filename = self.save_folder + "/" + 'RMC' + '.csv'
                self.gga_time_filename = self.save_folder + "/" + 'GGA_Time' + '.csv'

                self.rmc_file_open = open(self.rmc_filename, 'w', newline='')
                self.rmc_csvfile_writer = csv.DictWriter(self.rmc_file_open, fieldnames=rmc_fieldnames)
                self.rmc_csvfile_writer.writeheader()

                self.gga_time_open = open(self.gga_time_filename, 'w', newline='')
                self.gga_time_writer = csv.DictWriter(self.gga_time_open, fieldnames=gga_time_fieldnames)
                self.gga_time_writer.writeheader()

                traj_fieldnames = ['Elapsed time (ms)', 'TimeStamp', 'Latitude', 'Longitude',
                                   'Antenna Alt above sea level (mean)']
                self.traj_filename = self.save_folder + "/" + 'trajectory' + '.csv'
                self.traj_file_open = open(self.traj_filename, 'w', newline='')
                self.traj_csvfile_writer = csv.DictWriter(self.traj_file_open, fieldnames=traj_fieldnames)
                self.traj_csvfile_writer.writeheader()

                gsa_fieldnames = ['Mode', "sv_id_1", "sv_id_2", "sv_id_3", "sv_id_4", "sv_id_5", "sv_id_6", "sv_id_7",
                                  "sv_id_8", "sv_id_9", "sv_id_10", "sv_id_11", "sv_id_12",
                                  'Mode fix type', 'PDOP (Dilution of precision)',
                                  'HDOP (Horizontal DOP)',
                                  'VDOP (Vertical DOP)']
                self.gsa_filename = self.save_folder + "/" + 'GSA' + '.csv'
                self.gsa_file_open = open(self.gsa_filename, 'w', newline='')
                self.gsa_csvfile_writer = csv.DictWriter(self.gsa_file_open, fieldnames=gsa_fieldnames)
                self.gsa_csvfile_writer.writeheader()

                gsv_fieldnames = ["Elapsed time", "GNSS ID", 'Number of messages of type in cycle',
                                  'Message Number',
                                  'Total number of SVs in view',
                                  'sv_prn_num_1', 'elevation_deg_1', 'azimuth_1', 'snr_1', 'sv_prn_num_2',
                                  'elevation_deg_2',
                                  'azimuth_2', 'snr_2', 'sv_prn_num_3', 'elevation_deg_3', 'azimuth_3',
                                  'snr_3', 'sv_prn_num_4',
                                  'elevation_deg_4', 'azimuth_4', 'snr_4', 'sv_prn_num_5',
                                  'elevation_deg_5', 'azimuth_5',
                                  'snr_5',
                                  'sv_prn_num_6', 'elevation_deg_6', 'azimuth_6', 'snr_6', 'sv_prn_num_7',
                                  'elevation_deg_7',
                                  'azimuth_7', 'snr_7', 'sv_prn_num_8', 'elevation_deg_8', 'azimuth_8',
                                  'snr_8', 'sv_prn_num_9',
                                  'elevation_deg_9', 'azimuth_9', 'snr_9']

                self.gsv_filename = self.save_folder + "/" + 'GSV' + '.csv'
                self.gsv_file_open = open(self.gsv_filename, 'w', newline='')
                self.gsv_csvfile_writer = csv.DictWriter(self.gsv_file_open, fieldnames=gsv_fieldnames)
                self.gsv_csvfile_writer.writeheader()

                try:
                    for line in file.readlines():
                        if self.running_stop:
                            break

                        try:

                            msg = pynmea2.parse(line)

                            self.parsing_screen_2(repr(msg))  # MY_FUNCTION_CALL
                            self.parsing_screen_2("\n")  # MY_FUNCTION_CALL

                            self.save_parsed_data(msg)

                        except pynmea2.ParseError as e:
                            print('Parse error: {}'.format(e))
                            self.parsing_screen_2('Parse error: {}'.format(e))  # MY_FUNCTION_CALL
                            self.parsing_screen_2("\n")  # MY_FUNCTION_CALL
                            continue
                        except UnicodeDecodeError as uni_err:
                            print(uni_err)
                            continue
                    self.rmc_file_open.close()
                    self.gsa_file_open.close()
                    self.gsv_file_open.close()
                    self.traj_file_open.close()

                except UnicodeDecodeError as uni_er:
                    self.running_stop = False
                    QMessageBox.about(self, "PARSE ERROR", str(uni_er))

            except PermissionError as perm_err:
                self.running_stop = False
                QMessageBox.about(self, "PARSE ERROR", str(perm_err) + ". Please close this file to continue.")

            except FileNotFoundError as fil_err:
                QMessageBox.about(self, "FILE ERROR", str(fil_err) + ". Please make sure you selected a file.")

        self.labelA.setText("Not saving.")

    def save_parsed_data(self, msg):

        """This function will save each NMEA message read on the NMEA file into the corrresponding csv file"""

        # 'Number of messages of type in cycle','Message Number', 'Total number of SVs in view', 'SV PRN number 1', 
        # 'Elevation in degrees 1', 'Azimuth, deg from true north 1', SNR_1, 'SV PRN number 2', 'sv_prn_num_2', 
        # ('Elevation in degrees 2', 'elevation_deg_2'), ('Azimuth, deg from true north 2', 'azimuth_2'), ('SNR 2', 
        # 'snr_2'), ('SV PRN number 3', 'sv_prn_num_3'), ('Elevation in degrees 3', 'elevation_deg_3'), ('Azimuth, 
        # deg from true north 3', 'azimuth_3'), ('SNR 3', 'snr_3'), ('SV PRN number 4', 'sv_prn_num_4'), ('Elevation 
        # in degrees 4', 'elevation_deg_4'), ('Azimuth, deg from true north 4', 'azimuth_4'), ('SNR 4', 'snr_4'))
        gnss_id = str()
        try:

            if msg.sentence_type == 'RMC':
                print(repr(msg))

                if msg.timestamp is None or msg.datestamp is None:
                    pass
                else:

                    date_rmc = msg.datetime.replace(tzinfo=None)
                    time_rmc = (str(date_rmc)).split(" ")
                    time_rmc = str(time_rmc[1])
                    self.table_rmc.append(date_rmc)
                    date = date_rmc - self.table_rmc[0]
                    seconds = (date.total_seconds())
                    print(seconds)
                    # milliseconds = round(seconds * 1000)
                    self.elapsed_second = seconds

                    self.table_rmc_elapsed.append(self.elapsed_second)

                    rmc_status = msg.status
                    rmc_lat = msg.latitude
                    rmc_lat_dir = msg.lat_dir
                    rmc_lon = msg.longitude
                    rmc_lon_dir = msg.lon_dir
                    rmc_spd_over_grnd = msg.spd_over_grnd
                    rmc_true_course = msg.true_course
                    rmc_datestamp = msg.datestamp
                    rmc_mag_variation = msg.mag_variation
                    rmc_mag_var_dir = msg.mag_var_dir
                    rmc_mode_indicator = msg.mode_indicator
                    rmc_nav_status = msg.nav_status

                    rmc_dict_values = {'Elapsed time (ms)': self.elapsed_second,
                                       "Timestamp": time_rmc,
                                       'Status': rmc_status,
                                       'Latitude': rmc_lat, 'Latitude Direction': rmc_lat_dir, 'Longitude': rmc_lon,
                                       'Longitude Direction': rmc_lon_dir,
                                       'Speed Over Ground': rmc_spd_over_grnd, 'True Course': rmc_true_course,
                                       'Datestamp': rmc_datestamp, 'Magnetic Variation': rmc_mag_variation,
                                       'Magnetic Variation Direction': rmc_mag_var_dir,
                                       'Mode Indicator': rmc_mode_indicator, 'Navigational Status': rmc_nav_status}

                    self.rmc_csvfile_writer.writerow(rmc_dict_values)

            if msg.sentence_type == 'GGA':
                print(repr(msg))

                gga_timestamp = str(msg.timestamp)

                if str(gga_timestamp) == "None":
                    pass
                else:
                    print(self.ind)

                    start_time = gga_timestamp.split(":")
                    print(gga_timestamp)

                    gga_hour = start_time[0]
                    gga_minute = start_time[1]
                    gga_s = start_time[2].split("+")

                    # gga_sec = int(round(float(gga_s[0])))
                    # gga_milli_sec = float(gga_s[0]) * 1000

                    gga_total_millisec = ((int(gga_hour) * 60 + int(gga_minute)) * 60) * 1000 + float(gga_s[0]) * 1000

                    self.table_gga_elapsed.append(gga_total_millisec)

                    print(self.table_gga_elapsed, self.table_gga_elapsed[self.ind], self.ind)

                    if self.ind == 0:
                        pass
                    else:
                        if self.table_gga_elapsed[self.ind] <= self.table_gga_elapsed[self.ind - 1]:
                            print(self.table_gga_elapsed)
                            self.table_gga_elapsed.clear()
                            self.ind = -1
                            print(self.table_gga_elapsed)
                            self.table_gga_elapsed.append(gga_total_millisec)

                            traj_fieldnames = ['Elapsed time (ms)', 'TimeStamp', 'Latitude', 'Longitude',
                                               'Antenna Alt above sea level (mean)']

                            self.traj_file_open = open(self.traj_filename, 'w', newline='')
                            self.traj_csvfile_writer = csv.DictWriter(self.traj_file_open, fieldnames=traj_fieldnames)
                            self.traj_csvfile_writer.writeheader()

                    self.elapsed_gga = gga_total_millisec - self.table_gga_elapsed[0]
                    self.table_gga_time.append(gga_timestamp)

                    gga_time_dict = {'True date': start_time, "Calculated date": gga_timestamp,
                                     "True seconds": gga_total_millisec,
                                     "Calculated seconds": self.elapsed_gga
                                     }

                    self.gga_time_writer.writerow(gga_time_dict)

                    gga_lat = msg.latitude
                    gga_lon = msg.longitude
                    gga_altitude = msg.altitude
                    # gga_lat_dir = msg.lat_dir
                    # gga_lon_dir = msg.lon_dir
                    # gga_gps_qual = msg.gps_qual
                    # gga_num_sats = msg.num_sats
                    # gga_horizontal_dil = msg.horizontal_dil
                    # gga_altitude_units = msg.altitude_units
                    # gga_geo_sep = msg.geo_sep
                    # gga_geo_sep_units = msg.geo_sep_units
                    # gga_age_gps_data = msg.age_gps_data
                    # gga_ref_station_id = msg.ref_station_id

                    self.traj_csvfile_writer.writerow(
                        {'Elapsed time (ms)': self.elapsed_gga, 'TimeStamp': gga_timestamp, 'Latitude': gga_lat,
                         'Longitude': gga_lon,
                         'Antenna Alt above sea level (mean)': gga_altitude})

                    # gga_time_temp = gga_total_millisec
                    self.ind = self.ind + 1

                '''https://receiverhelp.trimble.com/alloy-gnss/en-us/NMEA-0183messages_GSV.html

                $GPGSV indicates GPS and SBAS satellites. If the PRN is greater than 32, this indicates an SBAS PRN, 
                87 should be added to the GSV PRN number to determine the SBAS PRN number.

                $GLGSV indicates GLONASS satellites. 64 should be subtracted from the GSV PRN number to determine the 
                GLONASS PRN number.

                $GBGSV indicates BeiDou satellites. 100 should be subtracted from the GSV PRN number to determine the 
                BeiDou PRN number.

                $GAGSV indicates Galileo satellites.

                $GQGSV indicates QZSS satellites.'''

            if msg.sentence_type == 'GSV':

                if msg.talker == "GP":
                    gnss_id = "GPS"

                elif msg.talker == "GL":
                    gnss_id = "GLONASS"

                elif msg.talker == "GA":
                    gnss_id = "Galileo"

                elif msg.talker == "GB" or "BD":
                    gnss_id = "BeiDou"

                elif msg.talker == "GQ":
                    gnss_id = "QZSS"

                elif msg.talker == "GI":
                    gnss_id = "NavIC"

                if gnss_id not in self.list_GNSS_ID:
                    self.list_GNSS_ID.append(gnss_id)

                gsv_num_messages = msg.num_messages
                gsv_msg_num = msg.msg_num
                gsv_num_sv_in_view = msg.num_sv_in_view

                try:
                    sv_prn_num_1 = msg.sv_prn_num_1

                    if msg.talker == "GP":
                        if int(sv_prn_num_1) > 32:
                            sv_prn_num_1 = 87 + int(sv_prn_num_1) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        gnss_id = "GLONASS"
                        sv_prn_num_1 = int(sv_prn_num_1) - 64

                    elif msg.talker == "GB" or "BD":
                        gnss_id = "BeiDou"

                    elevation_deg_1 = msg.elevation_deg_1
                    azimuth_1 = msg.azimuth_1
                    snr_1 = msg.snr_1
                except AttributeError as er:
                    sv_prn_num_1 = ""
                    elevation_deg_1 = ""
                    azimuth_1 = ""
                    snr_1 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_1 = ""
                    elevation_deg_1 = ""
                    azimuth_1 = ""
                    snr_1 = ""
                    print(er)

                try:
                    sv_prn_num_2 = msg.sv_prn_num_2

                    if msg.talker == "GP":
                        if int(sv_prn_num_2) > 32:
                            sv_prn_num_1 = 87 + int(sv_prn_num_2) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        gnss_id = "GLONASS"
                        sv_prn_num_2 = int(sv_prn_num_2) - 64

                    elif msg.talker == "GB" or "BD":
                        gnss_id = "BeiDou"

                    elevation_deg_2 = msg.elevation_deg_2
                    azimuth_2 = msg.azimuth_2
                    snr_2 = msg.snr_2
                except AttributeError as er:
                    sv_prn_num_2 = ""
                    elevation_deg_2 = ""
                    azimuth_2 = ""
                    snr_2 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_2 = ""
                    elevation_deg_2 = ""
                    azimuth_2 = ""
                    snr_2 = ""
                    print(er)

                try:
                    sv_prn_num_3 = msg.sv_prn_num_3

                    if msg.talker == "GP":
                        if int(sv_prn_num_3) > 32:
                            sv_prn_num_3 = 87 + int(sv_prn_num_3) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        gnss_id = "GLONASS"
                        sv_prn_num_3 = int(sv_prn_num_3) - 64

                    elif msg.talker == "GB" or "BD":
                        gnss_id = "BeiDou"

                    elevation_deg_3 = msg.elevation_deg_3
                    azimuth_3 = msg.azimuth_3
                    snr_3 = msg.snr_3
                except AttributeError as er:
                    sv_prn_num_3 = ""
                    elevation_deg_3 = ""
                    azimuth_3 = ""
                    snr_3 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_3 = ""
                    elevation_deg_3 = ""
                    azimuth_3 = ""
                    snr_3 = ""
                    print(er)

                try:
                    sv_prn_num_4 = msg.sv_prn_num_4

                    if msg.talker == "GP":
                        if int(sv_prn_num_4) > 32:
                            sv_prn_num_1 = 87 + int(sv_prn_num_4) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        gnss_id = "GLONASS"
                        sv_prn_num_4 = int(sv_prn_num_4) - 64

                    elif msg.talker == "GB" or "BD":
                        gnss_id = "BeiDou"

                    elevation_deg_4 = msg.elevation_deg_4
                    azimuth_4 = msg.azimuth_4
                    snr_4 = msg.snr_4
                except AttributeError as er:
                    sv_prn_num_4 = ""
                    elevation_deg_4 = ""
                    azimuth_4 = ""
                    snr_4 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_4 = ""
                    elevation_deg_4 = ""
                    azimuth_4 = ""
                    snr_4 = ""
                    print(er)

                try:
                    sv_prn_num_5 = msg.sv_prn_num_5

                    if msg.talker == "GP":
                        if int(sv_prn_num_5) > 32:
                            sv_prn_num_1 = 87 + int(sv_prn_num_5) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        gnss_id = "GLONASS"
                        sv_prn_num_5 = int(sv_prn_num_5) - 64

                    elif msg.talker == "GB" or "BD":
                        # print("BeiDou")
                        gnss_id = "BeiDou"
                        # sv_prn_num_5 = int(sv_prn_num_5) - 100

                    elevation_deg_5 = msg.elevation_deg_5
                    azimuth_5 = msg.azimuth_5
                    snr_5 = msg.snr_5
                except AttributeError as er:
                    sv_prn_num_5 = ""
                    elevation_deg_5 = ""
                    azimuth_5 = ""
                    snr_5 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_5 = ""
                    elevation_deg_5 = ""
                    azimuth_5 = ""
                    snr_5 = ""
                    print(er)

                try:
                    sv_prn_num_6 = msg.sv_prn_num_6

                    if msg.talker == "GP":
                        # print("GPS")
                        if int(sv_prn_num_6) > 32:
                            sv_prn_num_6 = 87 + int(sv_prn_num_6) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        # print("GLONASS")
                        gnss_id = "GLONASS"
                        sv_prn_num_6 = int(sv_prn_num_6) - 64

                    elif msg.talker == "GB" or "BD":
                        # print("BeiDou")
                        gnss_id = "BeiDou"

                    elevation_deg_6 = msg.elevation_deg_6
                    azimuth_6 = msg.azimuth_6
                    snr_6 = msg.snr_6
                except AttributeError as er:
                    sv_prn_num_6 = ""
                    elevation_deg_6 = ""
                    azimuth_6 = ""
                    snr_6 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_6 = ""
                    elevation_deg_6 = ""
                    azimuth_6 = ""
                    snr_6 = ""
                    print(er)

                try:
                    sv_prn_num_7 = msg.sv_prn_num_7

                    if msg.talker == "GP":
                        # print("GPS")
                        if int(sv_prn_num_7) > 32:
                            sv_prn_num_7 = 87 + int(sv_prn_num_7) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        # print("GLONASS")
                        gnss_id = "GLONASS"
                        sv_prn_num_7 = int(sv_prn_num_7) - 64

                    elif msg.talker == "GB" or "BD":
                        # print("BeiDou")
                        gnss_id = "BeiDou"

                    elevation_deg_7 = msg.elevation_deg_7
                    azimuth_7 = msg.azimuth_7
                    snr_7 = msg.snr_7

                except AttributeError as er:
                    sv_prn_num_7 = ""
                    elevation_deg_7 = ""
                    azimuth_7 = ""
                    snr_7 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_7 = ""
                    elevation_deg_7 = ""
                    azimuth_7 = ""
                    snr_7 = ""
                    print(er)

                try:
                    sv_prn_num_8 = msg.sv_prn_num_8

                    if msg.talker == "GP":
                        # print("GPS")
                        if int(sv_prn_num_8) > 32:
                            sv_prn_num_8 = 87 + int(sv_prn_num_8) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        # print("GLONASS")
                        gnss_id = "GLONASS"
                        sv_prn_num_8 = int(sv_prn_num_8) - 64

                    elif msg.talker == "GB" or "BD":
                        gnss_id = "BeiDou"
                    # sv_prn_num_8 = int(sv_prn_num_8) - 100

                    elevation_deg_8 = msg.elevation_deg_8
                    azimuth_8 = msg.azimuth_8
                    snr_8 = msg.snr_8

                except AttributeError as er:
                    sv_prn_num_8 = ""
                    elevation_deg_8 = ""
                    azimuth_8 = ""
                    snr_8 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_8 = ""
                    elevation_deg_8 = ""
                    azimuth_8 = ""
                    snr_8 = ""
                    print(er)

                try:
                    sv_prn_num_9 = msg.sv_prn_num_9

                    if msg.talker == "GP":
                        if int(sv_prn_num_9) > 32:
                            sv_prn_num_9 = (87 + int(sv_prn_num_9)) - 119
                            gnss_id = "SBAS"
                        else:
                            gnss_id = "GPS"

                    elif msg.talker == "GL":
                        gnss_id = "GLONASS"
                        sv_prn_num_9 = int(sv_prn_num_9) - 64

                    elif msg.talker == "GB" or "BD":
                        gnss_id = "BeiDou"

                    elevation_deg_9 = msg.elevation_deg_9
                    azimuth_9 = msg.azimuth_9
                    snr_9 = msg.snr_9
                except AttributeError as er:
                    sv_prn_num_9 = ""
                    elevation_deg_9 = ""
                    azimuth_9 = ""
                    snr_9 = ""
                    print(er)
                except ValueError as er:
                    sv_prn_num_9 = ""
                    elevation_deg_9 = ""
                    azimuth_9 = ""
                    snr_9 = ""
                    print(er)

                print(self.elapsed_second)
                print(self.elapsed_gga)

                gsv_dict_values = {'Elapsed time': self.elapsed_gga, "GNSS ID": gnss_id,
                                   'Number of messages of type in cycle': gsv_num_messages,
                                   'Message Number': gsv_msg_num,
                                   'Total number of SVs in view': gsv_num_sv_in_view,
                                   'sv_prn_num_1': sv_prn_num_1, 'elevation_deg_1': elevation_deg_1,
                                   'azimuth_1': azimuth_1, 'snr_1': snr_1, 'sv_prn_num_2': sv_prn_num_2,
                                   'elevation_deg_2': elevation_deg_2,
                                   'azimuth_2': azimuth_2, 'snr_2': snr_2, 'sv_prn_num_3': sv_prn_num_3,
                                   'elevation_deg_3': elevation_deg_3, 'azimuth_3': azimuth_3, 'snr_3': snr_3,
                                   'sv_prn_num_4': sv_prn_num_4,
                                   'elevation_deg_4': elevation_deg_4, 'azimuth_4': azimuth_4, 'snr_4': snr_4,
                                   'sv_prn_num_5': sv_prn_num_5, 'elevation_deg_5': elevation_deg_5,
                                   'azimuth_5': azimuth_5, 'snr_5': snr_5,
                                   'sv_prn_num_6': sv_prn_num_6, 'elevation_deg_6': elevation_deg_6,
                                   'azimuth_6': azimuth_6, 'snr_6': snr_6, 'sv_prn_num_7': sv_prn_num_7,
                                   'elevation_deg_7': elevation_deg_7,
                                   'azimuth_7': azimuth_7, 'snr_7': snr_7, 'sv_prn_num_8': sv_prn_num_8,
                                   'elevation_deg_8': elevation_deg_8, 'azimuth_8': azimuth_8, 'snr_8': snr_8,
                                   'sv_prn_num_9': sv_prn_num_9,
                                   'elevation_deg_9': elevation_deg_9, 'azimuth_9': azimuth_9, 'snr_9': snr_9}

                self.gsv_csvfile_writer.writerow(gsv_dict_values)

            if msg.sentence_type == 'GSA':
                print(repr(msg))
                """     GSA      Satellite status
     A        Auto selection of 2D or 3D fix (M = manual) 
     3        3D fix - values include: 1 = no fix
                                       2 = 2D fix
                                       3 = 3D fix
     04,05... PRNs of satellites used for fix (space for 12) 
     2.5      PDOP (dilution of precision) 
     1.3      Horizontal dilution of precision (HDOP) 
     2.1      Vertical dilution of precision (VDOP)
     *39      the checksum data, always begins with *"""

                gsa_mode = msg.mode
                gsa_mode_fix_type = msg.mode_fix_type
                gsa_sv_id01 = msg.sv_id01
                gsa_sv_id02 = msg.sv_id02
                gsa_sv_id03 = msg.sv_id03
                gsa_sv_id04 = msg.sv_id04
                gsa_sv_id05 = msg.sv_id05
                gsa_sv_id06 = msg.sv_id06
                gsa_sv_id07 = msg.sv_id07
                gsa_sv_id08 = msg.sv_id08
                gsa_sv_id09 = msg.sv_id09
                gsa_sv_id10 = msg.sv_id10
                gsa_sv_id11 = msg.sv_id11
                gsa_sv_id12 = msg.sv_id12
                gsa_pdop = msg.pdop
                gsa_hdop = msg.hdop
                gsa_vdop = msg.vdop

                if gsa_mode == "M":
                    gsa_mode_str = "Manual"
                else:
                    gsa_mode_str = "Automatic"

                if gsa_mode_fix_type == 0:
                    gsa_mode_fix_type_str = "No fix"
                    # print("no fix")
                elif gsa_mode_fix_type == 1:
                    gsa_mode_fix_type_str = "2D fix"
                    # print("2D fix")
                else:
                    # print("3D fix")
                    gsa_mode_fix_type_str = "3D fix"

                gsa_dict_values = {'Mode': gsa_mode_str, 'Mode fix type': gsa_mode_fix_type_str, "sv_id_1": gsa_sv_id01,
                                   "sv_id_2": gsa_sv_id02, "sv_id_3": gsa_sv_id03, "sv_id_4": gsa_sv_id04,
                                   "sv_id_5": gsa_sv_id05, "sv_id_6": gsa_sv_id06, "sv_id_7": gsa_sv_id07,
                                   "sv_id_8": gsa_sv_id08, "sv_id_9": gsa_sv_id09, "sv_id_10": gsa_sv_id10,
                                   "sv_id_11": gsa_sv_id11, "sv_id_12": gsa_sv_id12,
                                   'PDOP (Dilution of precision)': gsa_pdop, 'HDOP (Horizontal DOP)': gsa_hdop,
                                   'VDOP (Vertical DOP)': gsa_vdop}

                self.gsa_csvfile_writer.writerow(gsa_dict_values)

        except pynmea2.ParseError as e:
            print('Parse error: {}'.format(e))

        except KeyError as err:
            print(err)
            pass

        except AttributeError as att_err:
            print(att_err)
            pass

    def parsing_screen_2(self, mystring):
        """
        This function update the parsing screen with new data
        :param mystring
        :return: None
        """
        print("")
        self.cursor.insertText(str(mystring))
        self.cursor.setPosition(self.cursor.position())
        self.cursor.movePosition(self.cursor.Left, self.cursor.KeepAnchor, 0)
        self.show_message.setTextCursor(self.cursor)
        QApplication.processEvents()  # update gui for pyqt

    def screen_1(self, mystring):
        """
        This function update the screen 1 with new data
        :param mystring
        :return: None
        """
        print("")
        self.show_other_message.append(str(mystring))
        self.show_message.append('started appending %s' % mystring)  # append string
        QApplication.processEvents()  # update gui for pyqt

    def output_type(self, output_val):
        """
        This function update the screen 1 with new data
        :param output_val: selected Skydel output value on the combo box
        :return: output_val
        """
        self.playback_button.setEnabled(True)
        self.global_output_val = output_val
        print(self.global_output_val)
        return output_val

    def playback_skydel_2(self):

        load_folder = self.load_csv_skydel()

        cnt_line = 0
        cnt_no_track = 0

        if load_folder == "":
            QMessageBox.about(self, "CSV FOLDER PATH", "THE FOLDER PATH IS EMPTY.")
        else:

            try:
                # Connect to Skydel
                self.sim = skydelsdx.RemoteSimulator(True)
                self.sim.connect()
                self.sim.call(New(True, True))

                # Change configuration before starting the self.simulation

                if self.global_output_val == "None":
                    self.sim.call(SetModulationTarget("None", "", "", True, "uniqueId"))

                elif self.global_output_val == "NoneRT":
                    self.sim.call(SetModulationTarget("NoneRT", "", "", True, "uniqueId"))

                elif self.global_output_val == "DTA-2115B":
                    self.sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))

                elif self.global_output_val == "DTA-2116":
                    self.sim.call(SetModulationTarget("DTA-2116", "", "", True, "uniqueId"))

                else:
                    print(" No selected Output")

                self.rmc_file = load_folder + "/" + 'RMC.csv'
                self.gsv_file = load_folder + "/" + 'GSV.csv'
                self.gsa_file = load_folder + "/" + 'GSA.csv'
                self.traj_file = load_folder + "/" + 'trajectory.csv'

                rmc_time = open(self.rmc_file, encoding='utf-8')
                lines = rmc_time.readlines()

                len_lines = len(lines)

                if len_lines == 1:
                    print(
                        "NO RMC file was found, Chnage the time in the Skydel instance or Skydel will start at the "
                        "default time")
                    self.sim.call(SetVehicleTrajectory("Track"))

                else:

                    try:
                        lines.pop(0)
                    except IndexError as ind_err_11:
                        QMessageBox.about(self, "FILE ERROR", str(ind_err_11) + "The RMC file is empty")

                    start_date = str()
                    start_time = str()

                    for i in range(len(lines)):
                        if not lines[i]:
                            continue
                        else:
                            time_line = lines[i].split(",")
                            start_time = time_line[1]
                            start_date = time_line[9]
                            break

                    print("Start Time:", start_time)
                    print("Start date:", start_date)

                    if "-" in start_date:
                        start_date = start_date.split("-")
                    elif "/" in start_date:
                        start_date = start_date.split("/")

                    try:
                        print(start_date[0])
                        print(start_date[1])
                        print(start_date[2])
                    except IndexError as id_err:
                        print(id_err)

                    skydel_year = start_date[0]
                    skydel_month = start_date[1]
                    skydel_day = start_date[2]
                    start_time = start_time.split(":")

                    skydel_hour = start_time[0]
                    skydel_minute = start_time[1]
                    skydel_sec = start_time[2].split("+")

                    skydel_sec = int(round(float(skydel_sec[0])))

                    self.sim.call(SetGpsStartTime(
                        datetime(int(skydel_year), int(skydel_month), int(skydel_day), int(skydel_hour),
                                 int(skydel_minute),
                                 int(skydel_sec))))

                def push_track_node(sim, timestampsec, latdeg, londeg, altmet):
                    sim.pushTrackLla(timestampsec, Lla(toRadian(latdeg), toRadian(londeg), altmet))

                with open(self.traj_file, "r") as f:
                    reader = csv.reader(f, delimiter=",")
                    next(reader, None)  # skip the headers
                    self.sim.beginTrackDefinition()

                    for i, line in enumerate(reader):

                        cnt_line = cnt_line + 1
                        try:
                            print("traj:", int(float(line[0])), float(line[2]), float(line[3]), float(line[4]))
                        except ValueError as val_err:
                            print(val_err)
                            pass

                        if line[0] == "" or line[1] == "" or line[2] == "" or line[3] == "" or line[4] == "":
                            cnt_no_track = cnt_no_track + 1

                            pass

                        else:
                            push_track_node(self.sim, int(float(line[0])), float(line[2]), float(line[3]),
                                            float(line[4]))

                    self.sim.endTrackDefinition()

                if cnt_no_track == cnt_line and cnt_line != 0:
                    QMessageBox.about(self, "SKYDEL TRAJECTORY",
                                      "The trajectory file is empty. No trajectory was set on Skydel.")
                else:
                    QMessageBox.about(self, "SKYDEL SIGNAL",
                                      "The trajectory is ready. Please select your signals in Skydel and press the "
                                      "Arm/STart button.")

            except ConnectionRefusedError as skydel_connect_err:
                QMessageBox.about(self, "SKYDEL ERROR",
                                  str(skydel_connect_err) + ". Please make sure that a new Skydel instance is open "
                                                            "and try again.")

            except FileNotFoundError as fil_err:
                QMessageBox.about(self, "MISSING FILE ERROR",
                                  str(fil_err) + ". Please make sure your folder contains all playback files")

        self.screen_1("\n")
        self.screen_1("Arming Skydel...")
        gps_list_up = str()
        gal_list_up = str()
        glo_list_up = str()
        beid_list_up = str()
        gps_list_low = str()
        gal_list_low = str()
        glo_list_low = str()
        beid_list_low = str()
        sbas_list_up = str()
        sbas_list_low = str()

        try:
            gsv_open = open(self.gsv_file, 'r')
            gsv_gnss = csv.DictReader(gsv_open)
            # gsv_file_object = csv.reader(gsv_open)
            gnss = []

            for col in gsv_gnss:
                gnss.append(col['GNSS ID'])

            result = []
            [result.append(x) for x in gnss if x not in result]

            self.list_GNSS_ID = result
            sv_dict = {}

            self.screen_1("\n")
            self.screen_1("The GNSS Signals present in the NMEA data are:")
            self.screen_1(self.list_GNSS_ID)

            if not self.list_GNSS_ID:

                if self.global_output_val == "None":
                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "UpperL", "L1CA", 0, False, "uniqueId0",
                                                      None))
                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", "L2C", 0, False, "uniqueId1",
                                                      None))

                elif self.global_output_val == "NoneRT":
                    self.sim.call(
                        ChangeModulationTargetSignals(0, 12500000, 100000000, "UpperL", "L1CA", -1, False, "uniqueId0"))
                    self.sim.call(
                        ChangeModulationTargetSignals(0, 12500000, 100000000, "LowerL", "L2C", -1, False, "uniqueId1"))

                elif self.global_output_val == "DTA-2115B":
                    self.sim.call(
                        ChangeModulationTargetSignals(0, 12500000, 85000000, "UpperL", "L1CA", 50, True, "uniqueId0",
                                                      None))
                    self.sim.call(
                        ChangeModulationTargetSignals(0, 12500000, 85000000, "LowerL", "L2C", 50, True, "uniqueId1",
                                                      None))

                elif self.global_output_val == "DTA-2116":
                    self.sim.call(
                        ChangeModulationTargetSignals(0, 12500000, 125000000, "UpperL", "L1CA", 50, True,
                                                      "uniqueId0", None))
                    self.sim.call(
                        ChangeModulationTargetSignals(0, 12500000, 125000000, "LowerL", "L2C", 50, True,
                                                      "uniqueId1", None))
                else:
                    print(" No selected Output")

                # self.sim.call(
                #     ChangeModulationTargetSignals(0, 12500000, 100000000, "UpperL", "L1CA", -1, False, "uniqueId0"))
                # self.sim.call(
                #     ChangeModulationTargetSignals(0, 12500000, 100000000, "LowerL", "L2C", -1, False, "uniqueId2"))

            if "GPS" in self.list_GNSS_ID:
                gps_list_up = "L1CA" + "," + "L1C"
                gps_list_low = "L2C"
            if "GLONASS" in self.list_GNSS_ID:
                glo_list_up = "G1"
                glo_list_low = "G2"
            if "Galileo" in self.list_GNSS_ID:
                gal_list_up = "E1"
                gal_list_low = "E5b"
            if "BeiDou" in self.list_GNSS_ID:
                beid_list_up = "B1" + "," + "B1C"
                beid_list_low = "B2" + "," + "B2a"
            if "SBAS" in self.list_GNSS_ID:
                sbas_list_up = "SBASL1"
                sbas_list_low = "SBASL5"

            gnss_list_up = str(
                gps_list_up + "," + gal_list_up + "," + glo_list_up + "," + beid_list_up + "," + sbas_list_up)
            gnss_list_low = str(gps_list_low + "," + gal_list_low + "," + beid_list_low + "," + sbas_list_low)
            gnss_list_low_2 = str(glo_list_low)

            if self.global_output_val == "None":
                self.sim.call(SetModulationTarget("None", "", "", True, "uniqueId"))
                self.sim.call(
                    ChangeModulationTargetSignals(0, 1250000, 125000000, "UpperL", gnss_list_up, 0, False,
                                                  "uniqueId", None))

            elif self.global_output_val == "NoneRT":
                self.sim.call(SetModulationTarget("NoneRT", "", "", True, "uniqueId"))
                self.sim.call(
                    ChangeModulationTargetSignals(0, 1250000, 125000000, "UpperL", gnss_list_up, 0, False,
                                                  "uniqueId", None))

            elif self.global_output_val == "DTA-2115B":
                self.sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId"))
                self.sim.call(
                    ChangeModulationTargetSignals(0, 12500000, 85000000, "UpperL", gnss_list_up, 50, True, "uniqueId",
                                                  None))

            elif self.global_output_val == "DTA-2116":
                self.sim.call(SetModulationTarget("DTA-2116", "", "", True, "uniqueId"))
                self.sim.call(
                    ChangeModulationTargetSignals(0, 12500000, 125000000, "UpperL", gnss_list_up, 50, True,
                                                  "uniqueId", None))

            else:
                print(" No selected Output")

            # self.sim.call(
            #     ChangeModulationTargetSignals(0, 12500000, 100000000, "UpperL", gnss_list_up, -1, False, "uniqueId"))

            reader = csv.reader(open(self.gsv_file))
            row_count_gsv = len(list(reader))
            # row_count_gsv = len(gsv_open.readlines())
            print(row_count_gsv)

            if row_count_gsv <= 2:
                QMessageBox.about(self, "Skydel Notification", "Please make sure you selected signals in Skydel")

                buttonreply = QMessageBox.question(self, 'Skydel Notification',
                                                   "Are you ready to Start Skydel?",
                                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                                   QMessageBox.Cancel)

                if buttonreply == QMessageBox.Yes:
                    self.sim.start()
                    self.screen_1("\n")
                    self.screen_1("Starting Skydel...")

                if buttonreply == QMessageBox.No:
                    print('No Arm, no Start')

                if buttonreply == QMessageBox.Cancel:
                    print('Cancel - equivalent to No')
            else:
                self.sim.call(
                    SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L1, "Basic Antenna"))
                self.sim.call(
                    SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L2, "Basic Antenna"))
                self.sim.call(
                    SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.L5, "Basic Antenna"))
                self.sim.call(
                    SetVehicleAntennaGainCSV("", AntennaPatternType.AntennaNone, GNSSBand.E6, "Basic Antenna"))

                if not gnss_list_low:
                    pass
                else:

                    if self.global_output_val == "None":

                        self.sim.call(SetModulationTarget("None", "", "", True, "uniqueId1"))
                        self.sim.call(
                            ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", gnss_list_low, 0, False,
                                                          "uniqueId1",
                                                          None))

                        self.sim.call(SetModulationTarget("None", "", "", True, "uniqueId2"))
                        self.sim.call(
                            ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", gnss_list_low_2, 0, False,
                                                          "uniqueId2",
                                                          None))

                    elif self.global_output_val == "NoneRT":

                        self.sim.call(SetModulationTarget("NoneRT", "", "", True, "uniqueId1"))
                        self.sim.call(
                            ChangeModulationTargetSignals(0, 12500000, 100000000, "LowerL", gnss_list_low, -1, False,
                                                          "uniqueId1"))
                        self.sim.call(SetModulationTarget("NoneRT", "", "", True, "uniqueId2"))
                        self.sim.call(
                            ChangeModulationTargetSignals(0, 12500000, 100000000, "LowerL", gnss_list_low_2, -1, False,
                                                          "uniqueId2"))

                    elif self.global_output_val == "DTA-2115B":

                        self.sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId1"))
                        self.sim.call(
                            ChangeModulationTargetSignals(0, 12500000, 85000000, "LowerL", gnss_list_low, 50, True,
                                                          "uniqueId1",
                                                          None))

                        self.sim.call(SetModulationTarget("DTA-2115B", "", "", True, "uniqueId2"))
                        self.sim.call(
                            ChangeModulationTargetSignals(0, 12500000, 85000000, "LowerL", gnss_list_low_2, 50, True,
                                                          "uniqueId2",
                                                          None))

                    elif self.global_output_val == "DTA-2116":

                        self.sim.call(SetModulationTarget("DTA-2116", "", "", True, "uniqueId1"))
                        self.sim.call(
                            ChangeModulationTargetSignals(0, 12500000, 125000000, "LowerL", gnss_list_low, 50, True,
                                                          "uniqueId1",
                                                          None))

                        self.sim.call(SetModulationTarget("DTA-2116", "", "", True, "uniqueId2"))
                        self.sim.call(
                            ChangeModulationTargetSignals(0, 12500000, 125000000, "LowerL", gnss_list_low_2, 50, True,
                                                          "uniqueId2",
                                                          None))
                    else:
                        print(" No selected Output")

                    # self.sim.call(SetModulationTarget("NoneRT", "", "", True, "uniqueId1"))
                    # self.sim.call(
                    #     ChangeModulationTargetSignals(0, 12500000, 100000000, "LowerL", gnss_list_low, -1, False,
                    #                                   "uniqueId1"))
                    # self.sim.call(SetModulationTarget("NoneRT", "", "", True, "uniqueId2"))
                    # self.sim.call(
                    #     ChangeModulationTargetSignals(0, 12500000, 100000000, "LowerL", gnss_list_low_2, -1, False,
                    #                                   "uniqueId2"))

                """$GPGSV indicates GPS and SBAS satellites. If the PRN is greater than 32, this indicates an SBAS 
                PRN, 87 should be added to the GSV PRN number to determine the SBAS PRN number.
        
                $GLGSV indicates GLONASS satellites. 64 should be subtracted from the GSV PRN number to determine the 
                GLONASS PRN number.
        
                $GBGSV indicates BeiDou satellites. 100 should be subtracted from the GSV PRN number to determine the 
                BeiDou PRN number.
        
                $GAGSV indicates Galileo satellites.
        
                $GQGSV indicates QZSS satellites."""

                for GNSS in self.list_GNSS_ID:
                    list_sv = []

                    with open(self.gsv_file, "r") as f:
                        reader = csv.reader(f, delimiter=",")
                        next(reader, None)

                        for i, line in enumerate(reader):
                            if str(line[1]) == GNSS:
                                if str(line[5]) == "":
                                    pass
                                else:
                                    list_sv.append(str(line[5]))
                                if str(line[9]) == "":
                                    pass
                                else:
                                    list_sv.append(str(line[9]))
                                if str(line[13]) == "":
                                    pass
                                else:
                                    list_sv.append(str(line[13]))
                                if str(line[17]) == "":
                                    pass
                                else:
                                    list_sv.append(str(line[17]))
                                if str(line[21]) == "":
                                    pass
                                else:
                                    list_sv.append(str(line[21]))

                    s_v_result = []

                    [s_v_result.append(s_v) for s_v in list_sv if s_v not in s_v_result]

                    print(s_v_result)

                    for sv_2 in s_v_result:
                        #
                        if GNSS == "SBAS" and int(sv_2) > 39:
                            s_v_result.remove(str(sv_2))

                        if GNSS == "GPS":
                            if int(sv_2) < 1 or int(sv_2) > 32:
                                s_v_result.remove(str(sv_2))

                        if GNSS == "GLONASS":
                            if int(sv_2) < 1 or int(sv_2) > 24:
                                s_v_result.remove(str(sv_2))

                    sv_dict.update({str(GNSS): s_v_result})
                    print(s_v_result)
                    print(sv_dict)

                for GNSS in self.list_GNSS_ID:
                    self.sim.call(
                        EnableRFOutputForSV(str(GNSS), 0, False))

                    list_sv_enable = sv_dict[str(GNSS)]
                    print(GNSS, list_sv_enable)

                    for sv_to_enable in list_sv_enable:

                        if GNSS == "SBAS":
                            print(sv_to_enable)
                            if int(sv_to_enable) < 1 or int(sv_to_enable) > 39:
                                list_sv_enable.remove(str(sv_to_enable))
                                break

                        if GNSS == "GPS":
                            print(sv_to_enable)
                            if int(sv_to_enable) < 1 or int(sv_to_enable) > 32:
                                list_sv_enable.remove(str(sv_to_enable))
                                break

                        if GNSS == "GLONASS":
                            if int(sv_to_enable) < 1 or int(sv_to_enable) > 24:
                                list_sv_enable.remove(sv_to_enable)
                                break

                        self.sim.call(
                            EnableRFOutputForSV(str(GNSS), int(sv_to_enable), True))

                QMessageBox.about(self, "Skydel Notification", "Please make sure you selected signals in Skydel")

                buttonreply = QMessageBox.question(self, 'Skydel Notification',
                                                   "Are you ready to Arm and Start Skydel?",
                                                   QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                                   QMessageBox.Cancel)

                if buttonreply == QMessageBox.Yes:
                    self.sim.arm()

                    with open(self.gsv_file, "r") as f:
                        reader = csv.reader(f, delimiter=",")
                        next(reader, None)

                        for i, line in enumerate(reader):
                            if str(line[5]) == "" or str(line[8]) == "":
                                pass
                            else:
                                self.sim.post(
                                    SetManualPowerOffsetForSV(str(line[1]), int(line[5]), {"All": int(line[8]) - 44},
                                                              False),
                                    float(line[0]))

                            if str(line[9]) == "" or str(line[12]) == "":
                                pass
                            else:
                                self.sim.post(
                                    SetManualPowerOffsetForSV(str(line[1]), int(line[9]), {"All": int(line[12]) - 44},
                                                              False),
                                    float(line[0]))

                            if str(line[13]) == "" or str(line[16]) == "":
                                pass
                            else:
                                self.sim.post(
                                    SetManualPowerOffsetForSV(str(line[1]), int(line[13]), {"All": int(line[16]) - 44},
                                                              False),
                                    float(line[0]))

                            if str(line[17]) == "" or str(line[20]) == "":
                                pass
                            else:
                                self.sim.post(
                                    SetManualPowerOffsetForSV(str(line[1]), int(line[17]), {"All": int(line[20]) - 44},
                                                              False),
                                    float(line[0]))

                            if str(line[21]) == "" or str(line[24]) == "":
                                pass
                            else:
                                self.sim.post(
                                    SetManualPowerOffsetForSV(str(line[1]), int(line[21]), {"All": int(line[24]) - 44},
                                                              False),
                                    float(line[0]))

                    self.screen_1("\n")
                    self.screen_1("Skydel is now ready...")
                    time.sleep(5)
                    self.sim.start()
                    self.screen_1("\n")
                    self.screen_1("Starting Skydel...")

                if buttonreply == QMessageBox.No:
                    print('No Arm, no Start')

                if buttonreply == QMessageBox.Cancel:
                    print('Cancel - equivalent to No')

        except AttributeError as attr_err_10:
            print(attr_err_10)
            QMessageBox.about(self, "Parsing error",
                              "Oup! You maybe miss the first step, please click on Set Skydel to start")

        except FileNotFoundError as file_not_found_10:
            print(file_not_found_10)
            QMessageBox.about(self, "Parsing error",
                              str(file_not_found_10))

    def stop_streaming_func(self):

        self.running_stop = True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(w)
    mw.show()
    sys.exit(app.exec_())
