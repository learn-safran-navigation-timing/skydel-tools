"""
Skydel Extrapolator for Rinex GLONASS Navigation File - Main QT application class.

Created on 14 06 2021

:author: Grace Jean
:copyright: Skydel © 2021
:Version: 24.1.1
"""

import glob
import csv
import re
import os
import sys
import subprocess
import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore
from get_sat_navigation import RinexReader
from Runge_Kutta_4 import RungeKutta4
from decimal import Decimal
from PyQt5.QtWidgets import QLineEdit, QLabel, QDesktopWidget, QFileDialog, QMenuBar, QMessageBox, QGroupBox, \
    QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from about import UiAboutDialog

ephemeris_reader = RinexReader()  # Load Rinex reader function
range_kutta = RungeKutta4()  #

def find_pos(line):
    # This function read the data in the temp directory for each satellite and each line and then get the data into 
    # variables.

    """'Sat_ID': sv_name, 'year': sv_year, 'month': sv_month, 'day': sv_day, 'hour': sv_hour,
     'min': sv_minutes, 'sec': sv_secondes, 'totalsec': totalsec,
     'bias': float(sv_clock_bias), 'freq': float(sv_freq_draft), 'frame': float(sv_frame_time),
     'x': float(sv_x_position), 'y': float(sv_y_position), 'z': float(sv_z_position),
     'vx': float(sv_x_velocity), 'vy': float(sv_y_velocity), 'vz': float(sv_z_velocity),
     'ax': float(sv_x_acceleration), 'ay': float(sv_y_acceleration), 'az': float(sv_z_acceleration),
     'health': float(sv_x_health), 'freq_num': float(sv_y_health), 'age': float(sv_z_health)"""

    sv_name = str(line[0])  # Sat ID = 1
    sv_date = [str(line[1]), str(line[2]), str(line[3])]  # date of the line [year, month, day]
    sv_time = [str(line[4]), str(line[5]), str(line[6])]  # time of the line [hour, minutes, secs]
    time = int(line[7])  # time ( hour + minutes + sec) converted in s
    sv_others = [float(line[8]), float(line[9]), float(line[10])]  # others satellite data
    Position0 = [float(line[11]), float(line[12]), float(line[13])]
    velocity0 = [float(line[14]), float(line[15]), float(line[16])]
    acceleration0 = [float(line[17]), float(line[18]), float(line[19])]
    info = [float(line[20]), float(line[21]), float(line[22])]
    return time, sv_name, sv_date, sv_time, Position0, velocity0, acceleration0, sv_others, info


def sec_to_hours(seconds):
    a = str(seconds // 3600)
    b = str((seconds % 3600) // 60)
    c = str((seconds % 3600) % 60)
    """ d = ["{} hours {} mins {} seconds".format(a, b, c)]"""

    return a, b, c


def quit_app():
    sys.exit()


def openFile():
    file = "SERGN_User_Manual.pdf"
    subprocess.Popen([file], shell=True)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Variables initialization
        self.custom_year = None
        self.max_time = None
        self.custom_second = None
        self.custom_time_future_end = None
        self.custom_time_past_end = None
        self.custom_time_start = None
        self.custom_month = None
        self.custom_date = None
        self.custom_minute = None
        self.custom_hour = None
        self.user_custom_date = None
        self.header_info = None
        self.sv_date_1 = None
        self.sv_day_1 = None
        self.sv_second_1 = None
        self.time_temp_1 = None
        self.sv_year_1 = None
        self.totalsec_1 = None
        self.sv_minutes_1 = None
        self.sv_hour_1 = None
        self.sv_month_1 = None
        self.sv_name = None
        self.header_info_1 = None
        self.rinex_version = None
        self.extrapol_direct = "future"  # Default direction for extrapolation is set in the future
        self.file = str()  # This is the rinex file to be loaded on Skydel
        self.path = str()  # directory path to save temp Rinex data. So the tool will read the data already in your
        # rinex and save them in the temporay folder for each satellite.
        self.new_rinex = str()  # New rinex path, this path will be set by the user
        self.count = int()
        self.time_row = list()
        self.rows = list()
        self.is_folder = 1
        self.time_stop = 0
        self.time_change_end_2 = 0
        self.setStyleSheet("""QToolTip {
                                   background-color: #232b2b;
                                   color: white;
                                   border: #232b2b solid 1px
                                   }""")
        self.ui_about = UiAboutDialog()

        hlay = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('resources/Skydel-NewLogo.png')
        label.resize(85, 85)
        label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio))
        hlay.addWidget(label, 0)

        ''' This part is the implementation of the Ui view'''

        # ******************************* Menubar **********************************************************************
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

        self.title1 = QLabel("Skydel Extrapolator for Rinex GLONASS Navigation")
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setFont(QFont('Arial', 14))
        self.title1.setStyleSheet("background-color:#1f6c8e ; border-radius:5px")

        self.file_path_1 = QLineEdit()
        self.file_path_1.setFont(QFont('Arial', 10))

        self.load_button_1_layout = QtWidgets.QHBoxLayout()
        self.load_button1 = QtWidgets.QPushButton('Load Rinex')
        self.load_button1.clicked.connect(self.load_rinex)

        self.load_button1.setFont(QFont('Arial', 10))
        self.load_button_1_layout.addWidget(self.load_button1)
        self.load_button_1_layout.addWidget(self.file_path_1)

        self.file_save_path_1 = QLineEdit()
        self.file_save_path_1.setText("File save here:")
        self.file_save_path_1.setEnabled(False)
        self.file_save_path_1.setFont(QFont('Arial', 10))

        self.save_button_1_layout = QtWidgets.QHBoxLayout()
        self.save_button1 = QtWidgets.QPushButton('Create new Rinex')
        self.save_button1.setFont(QFont('Arial', 10))

        self.save_button1.clicked.connect(self.main_func)
        self.save_button1.setEnabled(False)

        self.save_button_1_layout.setAlignment(Qt.AlignCenter)
        self.save_button_1_layout.addWidget(self.save_button1)

        self.set_custom_time_label = QLabel("Set custom time")
        self.set_custom_time_label.setAlignment(Qt.AlignCenter)
        self.set_custom_time_label.setFont(QFont('Arial', 10))

        self.set_custom_date_label = QLabel("Set custom date")
        self.set_custom_date_label.setAlignment(Qt.AlignCenter)
        self.set_custom_date_label.setFont(QFont('Arial', 10))

        self.custom_hour_edit = QLineEdit()
        self.custom_hour_edit.setEnabled(False)
        self.custom_hour_edit.setFont(QFont('Arial', 10))

        self.custom_minute_edit = QLineEdit()
        self.custom_minute_edit.setEnabled(False)
        self.custom_minute_edit.setFont(QFont('Arial', 10))

        self.custom_second_edit = QLineEdit()
        self.custom_second_edit.setEnabled(False)
        self.custom_second_edit.setFont(QFont('Arial', 10))

        self.custom_date_edit = QLineEdit()
        self.custom_date_edit.setEnabled(False)
        self.custom_date_edit.setFont(QFont('Arial', 10))

        self.custom_month_edit = QLineEdit()
        self.custom_month_edit.setEnabled(False)
        self.custom_month_edit.setFont(QFont('Arial', 10))

        self.custom_year_edit = QLineEdit()
        self.custom_year_edit.setEnabled(False)
        self.custom_year_edit.setFont(QFont('Arial', 10))

        self.custom_hour_edit.setText("hh")
        self.custom_minute_edit.setText("mm")
        self.custom_second_edit.setText("ss")

        self.custom_date_edit.setText("DD")
        self.custom_month_edit.setText("MM")
        self.custom_year_edit.setText("YYYY")

        custom_time_layout = QtWidgets.QHBoxLayout()
        custom_time_layout.addWidget(self.set_custom_time_label)
        custom_time_layout.addWidget(self.custom_hour_edit)
        custom_time_layout.addWidget(self.custom_minute_edit)
        custom_time_layout.addWidget(self.custom_second_edit)

        custom_date_layout = QtWidgets.QHBoxLayout()

        custom_date_layout.addWidget(self.set_custom_date_label)
        custom_date_layout.addWidget(self.custom_date_edit)
        custom_date_layout.addWidget(self.custom_month_edit)
        custom_date_layout.addWidget(self.custom_year_edit)

        self.rinex_info_label = QLabel("                Rinex timing Info               ")
        self.rinex_info_label.setAlignment(Qt.AlignCenter)
        self.rinex_info_label.setFont(QFont('Arial', 10))

        self.rinex_date_edit = QLineEdit()
        self.rinex_date_edit.setAlignment(Qt.AlignCenter)
        self.rinex_date_edit.setEnabled(False)
        self.rinex_date_edit.setFont(QFont('Arial', 10))

        self.rinex_time_edit = QLineEdit()
        self.rinex_time_edit.setAlignment(Qt.AlignCenter)
        self.rinex_time_edit.setEnabled(False)
        self.rinex_time_edit.setFont(QFont('Arial', 10))

        self.customer_info = QPlainTextEdit()
        self.customer_info.setEnabled(True)
        self.customer_info.setFont(QFont('Arial', 10))

        rinex_info_layout = QtWidgets.QVBoxLayout()
        rinex_info_layout.addWidget(self.rinex_info_label)
        rinex_info_layout.addWidget(self.rinex_date_edit)
        rinex_info_layout.addWidget(self.rinex_time_edit)
        rinex_info_layout.addWidget(self.customer_info)

        self.end_process = QLabel()
        self.end_process.setFont(QFont('Arial', 10))

        spacerItem0 = QtWidgets.QSpacerItem(50, 30, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        layout1 = QtWidgets.QVBoxLayout()
        layout1.addWidget(menubar, 0)
        layout1.addItem(spacerItem1)
        layout1.addWidget(self.title1, 0)
        layout1.addItem(spacerItem0)
        layout1.addLayout(self.load_button_1_layout, 1)

        layout1.addLayout(custom_time_layout)
        layout1.addLayout(custom_date_layout)

        layout1.addItem(spacerItem1)
        layout1.addItem(spacerItem1)
        layout1.addLayout(self.save_button_1_layout)

        layout1.addWidget(self.end_process)

        groupbox_time = QGroupBox("")
        groupbox_time.setCheckable(False)

        layout_time = QtWidgets.QVBoxLayout()
        groupbox_time.setLayout(rinex_info_layout)

        # ***************************************************************************************************************
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(groupbox_time)

        layout.addLayout(layout1)
        layout_final = QtWidgets.QVBoxLayout()

        layout_final.addLayout(hlay, 0)
        layout_final.addLayout(layout, 1)
        layout_final.addLayout(layout_time, 2)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout_final)

        self.resize(800, 400)
        self.setCentralWidget(widget)
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def show_about(self):
        self.ui_about.show()

    def load_rinex(self):

        self.file, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + " DATA Files", ".",
                                                                   "(*.rnx *.csv *.txt *.**g)")
        self.path = "tmp"

        try:
            os.rmdir(self.path)
        except OSError:
            print("Deletion of the temporary directory %s failed" % self.path)
        else:
            print("Successfully deleted the temporary directory %s" % self.path)

        if self.file:  # if the file is loaded

            skip_header, rin_detec, self.header_info = ephemeris_reader.find_header(self.file)

            try:
                self.end_process.setText("Loading...")

                new_lines, length_skipline = ephemeris_reader.readRinex(self.file, skip_header)

                self.sv_date_1 = str(new_lines[0])

                if "R" in self.sv_date_1:
                    str_sv = str(self.sv_date_1)
                    self.sv_name = str_sv[:3]
                    self.sv_name = self.sv_name.replace(" ", "")
                    pattern = r'\d+'
                    self.sv_name = re.split(pattern, self.sv_name)
                    self.sv_name = self.sv_name[1]

                else:
                    str_sv = str(self.sv_date_1)
                    self.sv_name = str_sv[:3]
                    self.sv_name = self.sv_name.replace(" ", "")

                self.sv_date_1 = self.sv_date_1[3:]

                self.sv_date_1 = self.sv_date_1.replace('e', 'E')
                self.sv_date_1 = self.sv_date_1.replace('D', 'E')
                self.sv_date_1 = self.sv_date_1.replace('E-', 'Eneg').replace('-', ' -').split()
                self.sv_date_1 = [item.replace('Eneg', 'E-') for item in self.sv_date_1]

                self.sv_year_1 = self.sv_date_1[0]
                self.sv_month_1 = self.sv_date_1[1]
                self.sv_day_1 = self.sv_date_1[2]
                self.sv_hour_1 = self.sv_date_1[3]
                self.sv_minutes_1 = self.sv_date_1[4]
                self.sv_second_1 = self.sv_date_1[5]

                self.totalsec_1 = int(self.sv_hour_1) * 3600 + int(self.sv_minutes_1) * 60 + int(
                    float(self.sv_second_1))

                if len(self.sv_year_1) == 2:
                    self.sv_year_1 = "20" + str(self.sv_year_1)

                self.custom_year_edit.setText(str(self.sv_year_1))
                self.custom_month_edit.setText(str(self.sv_month_1))
                self.custom_date_edit.setText(str(self.sv_day_1))

                self.custom_hour_edit.setText(str(self.sv_hour_1))
                self.custom_minute_edit.setText(str(self.sv_minutes_1))
                self.custom_second_edit.setText(str(int(float(self.sv_second_1))))

                date_info = "Date (first SV ephemeris) : " + self.sv_day_1 + "-" + self.sv_month_1 + "-" + self.sv_year_1
                time_info = "Time (first SV ephemeris) : " + self.sv_hour_1 + ":" + self.sv_minutes_1 + ":" + self.sv_second_1

                self.sv_second_1 = self.sv_second_1.split('.')
                self.sv_second_1 = self.sv_second_1[0]

                self.time_temp_1 = abs(self.totalsec_1 - 24 * 60 * 60)

                self.rinex_date_edit.setText(date_info)
                self.rinex_time_edit.setText(time_info)

                user_infos = "..."

                self.customer_info.insertPlainText(user_infos)
                self.customer_info.insertPlainText("\r")
                self.customer_info.insertPlainText("\n")

                self.custom_hour_edit.setEnabled(True)
                self.custom_minute_edit.setEnabled(True)
                self.custom_second_edit.setEnabled(True)

                self.custom_date_edit.setEnabled(True)
                self.custom_month_edit.setEnabled(True)
                self.custom_year_edit.setEnabled(True)

                ephemeris_reader.readline(new_lines, length_skipline)
                self.file_path_1.setText(self.file)
                self.save_button1.setEnabled(True)

            except IndexError as ind_err_1:
                self.end_process.setText(" ")
                print(ind_err_1)

                QMessageBox.about(self, "Rinex Format Error", "The loaded file is not a Rinex Navigation GLONASS.")
        self.end_process.setText(" ")

    def on_file_saved_2(self):

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "New_Rinex",
                                                  "All Files (*);;Text Files (*.rnx)", options=options)

        if fileName:

            return fileName
        else:
            self.is_folder = 0

    def find_max_time(self, line):
        """'Sat_ID': sv_name, 'year': sv_year, 'month': sv_month, 'day': sv_day, 'hour': sv_hour,
         'min': sv_minutes, 'sec': sv_secondes, 'totalsec': totalsec,
         'bias': float(sv_clock_bias), 'freq': float(sv_freq_draft), 'frame': float(sv_frame_time),
         'x': float(sv_x_position), 'y': float(sv_y_position), 'z': float(sv_z_position),
         'vx': float(sv_x_velocity), 'vy': float(sv_y_velocity), 'vz': float(sv_z_velocity),
         'ax': float(sv_x_acceleration), 'ay': float(sv_y_acceleration), 'az': float(sv_z_acceleration),
         'health': float(sv_x_health), 'freq_num': float(sv_y_health), 'age': float(sv_z_health)"""

        time = int(line[7])

        if time >= self.max_time:
            self.max_time = time

    def main_func(self):
        global step_time

        self.max_time = 0

        sv_list = []

        self.user_custom_date = self.custom_date_edit.text()

        self.custom_hour = self.custom_hour_edit.text()
        self.custom_minute = self.custom_minute_edit.text()
        self.custom_second = self.custom_second_edit.text()

        self.custom_date = self.custom_date_edit.text()
        self.custom_month = self.custom_month_edit.text()
        self.custom_year = self.custom_year_edit.text()

        if len(self.custom_hour) > 2:
            QMessageBox.about(self, "Custom time error", "Please enter the hour in 2 digits hh.")
            return

        if len(self.custom_minute) > 2:
            QMessageBox.about(self, "Custom time error", "Please enter the minute in 2 digits mm.")
            return

        if str(self.custom_minute) not in ["45", "15"]:
            QMessageBox.about(self, "Custom time error", "Please enter 15 or 45 as the value for the minutes.")
            return

        if len(self.custom_second) > 2:
            QMessageBox.about(self, "Custom time error", "Please enter the second in 2 digits ss.")
            return

        if len(self.custom_date) > 2:
            QMessageBox.about(self, "Custom time error", "Please enter the date in 1 or 2 digits.")
            return

        if len(self.custom_month) > 2:
            QMessageBox.about(self, "Custom time error", "Please enter the month in 2 digits MM.")
            return

        if len(self.custom_year) != 4:
            QMessageBox.about(self, "Custom time error", "Please enter the year in 4 digits YYYY.")
            return

        self.end_process.setText("Processing...")

        self.custom_time_start = int(self.custom_hour) * 3600 + int(self.custom_minute) * 60 + int(
            float(self.custom_second))
        self.custom_time_past_end = self.custom_time_start + 23 * 3600 + 45 * 60
        self.custom_time_future_end = self.custom_time_start

        self.new_rinex = self.on_file_saved_2()

        self.customer_info.insertPlainText("New rinex path: ")
        self.customer_info.insertPlainText(self.new_rinex)
        self.customer_info.insertPlainText("\r")
        self.customer_info.insertPlainText("\n")


        if self.is_folder == 1:

            f = open(self.new_rinex, "w")

            with open(self.file) as handler:
                for i, line in enumerate(handler):
                    f.write(line)
                    if 'END OF HEADER' in line:
                        break

            for filename in glob.glob((os.path.join(self.path, '*.csv'))):
                with open(os.path.join(os.getcwd(), filename), 'r') as f:  # open in readonly mode
                    reader = csv.reader(f)
                    next(reader)
                    true_data = next(reader)
                    self.find_max_time(true_data)

            for filename in glob.glob((os.path.join(self.path, '*.csv'))):

                self.count = 0

                self.time_row = []
                with open(os.path.join(os.getcwd(), filename), 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)
                    # Reads header row as a list
                    self.rows = list(reader)

                    for row in self.rows:
                        self.time_row.append(row[7])

                with open(os.path.join(os.getcwd(), filename), 'r') as f:  # open in readonly mode
                    reader = csv.reader(f)
                    next(reader)
                    true_data = next(reader)

                    true_time, sv_name, sv_date, sv_time, Position0, Velocity0, Acceleration0, sv_others, info = find_pos(
                        true_data)

                    curr_time = int(true_time)
                    step_time = 900 + 900
                    end_time = 23 * 3600 + 45 * 60

                    self.new_version_main_func(true_time, sv_name, sv_date, Position0, Velocity0, Acceleration0,
                                               sv_others, info, curr_time, step_time, end_time)

                    sv_list.append(sv_name)

            self.path = "tmp"

            try:
                os.rmdir(self.path)
            except OSError:
                print("Deletion of the temporary directory %s failed" % self.path)
            else:
                print("Successfully deleted the temporary directory %s" % self.path)

            self.end_process.setText("The new rinex has been successfully generated.")

        else:
            if self.new_rinex == "":
                QMessageBox.about(self, "Error", "No folder selected!")

            self.end_process.setText(" ")

            self.is_folder = 1

    def new_version_main_func(self, true_time, sv_name, sv_date, Position0, Velocity0, Acceleration0, sv_others,
                              infos, curr_time, step_time, end_time):

        global str_date, str_x, str_y, str_z

        date_1 = int(sv_date[2])  # date of the current satellite ephemeris
        date_2 = int(self.custom_date)  # custom date enter by the user in the UI

        month_1 = int(sv_date[1])
        month_2 = int(self.custom_month)

        year_1 = str(sv_date[0])
        year_2 = int(self.custom_year)

        if len(str(year_2)) == 2:
            year_2 = "20" + str(year_2)

        if len(str(year_1)) == 2:
            year_1 = "20" + str(year_1)

        year_1 = int(year_1)
        year_2 = int(year_2)

        diff_year = year_1 - year_2

        List_month_30 = [1, 4, 6, 9, 11]
        List_month_31 = [3, 5, 7, 8, 10, 12]
        # List_month_28 = [2]

        if diff_year < 0:  # futur
            delta_month = month_1 + month_2
            if delta_month % 12 == 1:

                if month_1 in List_month_30:
                    delta_day = (30 - date_1) + date_2
                elif month_1 in List_month_31:
                    delta_day = (31 - date_1) + date_2
                else:
                    delta_day = (28 - date_1) + date_2

                if len(str(self.custom_year)) == 4:
                    self.custom_year = str(self.custom_year).split("0")
                    self.custom_year = self.custom_year[1]

                extrapol_total_time = (int(delta_day)) * 24 * 60 * 60 + (
                        (int(self.custom_hour) * 60 * 60 + int(self.custom_minute) * 60 + int(
                            self.custom_second)) - curr_time)

                sv_date = [str(self.custom_year), str(self.custom_month), str(self.custom_date)]

                counter = 0

                for time in range(0, extrapol_total_time - 1800, step_time):
                    counter = counter + 1
                    self.extrapol_direct = "future"

                    next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                          Position0,
                                                                                          Velocity0,
                                                                                          Acceleration0)

                last_time_extrapol = self.custom_time_start + 23 * 3600 + 45 * 60

                for time in range(self.custom_time_start, last_time_extrapol, step_time):

                    self.extrapol_direct = "future"

                    res2, self.time_row = self.middle_func(self.time_row, time, sv_date[2])

                    if res2 == 0:
                        next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                              Position0,
                                                                                              Velocity0,
                                                                                              Acceleration0)

                        self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                          Acceleration0, sv_others, infos, self.new_rinex)

            else:
                QMessageBox.about(self, "Extrapolation limit",
                                  "It is not possible to extrapolate this far. Please choose another date")

        elif diff_year > 0:  # past

            delta_month = month_1 + month_2
            if delta_month % 12 == 1:

                if month_2 in List_month_30:
                    delta_day = date_1 + (30 - date_2)

                elif month_2 in List_month_31:
                    delta_day = date_1 + (31 - date_2)

                else:
                    delta_day = date_1 + (28 - date_2)

                extrapol_total_time = (int(delta_day)) * 24 * 60 * 60 - ((int(self.custom_hour) * 60 * 60 + int(
                    self.custom_minute) * 60 + int(
                    self.custom_second)) - curr_time)

                if len(str(self.custom_year)) == 4:
                    self.custom_year = str(self.custom_year).split("0")
                    self.custom_year = self.custom_year[1]

                sv_date = [str(self.custom_year), str(self.custom_month), str(self.custom_date)]

                cnt = 0

                for time in range(extrapol_total_time + 1800, 0, -step_time):
                    cnt = cnt + 1
                    self.extrapol_direct = "past"

                    next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                          Position0,
                                                                                          Velocity0,
                                                                                          Acceleration0)

                last_time_extrapol = self.custom_time_start + 23 * 3600 + 45 * 60

                for time in range(self.custom_time_start, last_time_extrapol, step_time):
                    self.extrapol_direct = "future"

                    next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                          Position0,
                                                                                          Velocity0,
                                                                                          Acceleration0)

                    self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                      Acceleration0, sv_others, infos, self.new_rinex)

            else:
                QMessageBox.about(self, "Extrapolation limit",
                                  "It is not possible to extrapolate this far. Choose another date")

        else:
            if date_1 == date_2:

                sv_date = [str(self.custom_year), str(self.custom_month), str(self.custom_date)]

                if self.custom_time_start == curr_time:
                    #              0h15       0h15

                    end_time_1 = self.custom_time_start + 23 * 3600 + 45 * 60

                    for time in range(curr_time, end_time_1, step_time):

                        self.extrapol_direct = "future"

                        res2, self.time_row = self.middle_func(self.time_row, time, sv_date[2])

                        if res2 == 0:
                            next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                                  Position0,
                                                                                                  Velocity0,
                                                                                                  Acceleration0)

                            self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                              Acceleration0, sv_others, infos, self.new_rinex)

                # 12h                      10h
                # elif self.custom_time_start > curr_time:
                # 23h45                    01h15
                elif self.custom_time_start < curr_time:
                    #                23h45       0h15

                    for time in range(curr_time, self.custom_time_start - 1, -step_time):
                        self.extrapol_direct = "past"

                        next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                              Position0,
                                                                                              Velocity0,
                                                                                              Acceleration0)

                    end_time_4 = self.custom_time_start + 23 * 3600 + 45 * 60

                    for time in range(self.custom_time_start, end_time_4 + 1, step_time):

                        self.extrapol_direct = "future"

                        res2, self.time_row = self.middle_func(self.time_row, time, sv_date[2])

                        if res2 == 0:
                            next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                                  Position0,
                                                                                                  Velocity0,
                                                                                                  Acceleration0)

                            self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                              Acceleration0, sv_others, infos, self.new_rinex)

                else:  # self.custom_time_start > curr_time
                    #               2h45      >       0h15
                    end_time_3 = self.custom_time_start + 23 * 3600 + 45 * 60

                    for time in range(curr_time, self.custom_time_start, step_time):
                        self.extrapol_direct = "future"

                        next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                              Position0,
                                                                                              Velocity0,
                                                                                              Acceleration0)

                    for time in range(self.custom_time_start, end_time_3 - 1, step_time):

                        res2, self.time_row = self.middle_func(self.time_row, time, sv_date[2])

                        if res2 == 0:
                            next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                                  Position0,
                                                                                                  Velocity0,
                                                                                                  Acceleration0)
                            self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                              Acceleration0, sv_others, infos, self.new_rinex)

            else:

                diff_date = int(date_1) - int(date_2)

                sv_date = [str(self.custom_year), str(self.custom_month), str(self.custom_date)]

                if diff_date > 0:

                    extrapol_total_time = (int(diff_date)) * 24 * 60 * 60 - ((int(self.custom_hour) * 60 * 60 + int(
                        self.custom_minute) * 60 + int(
                        self.custom_second)) - curr_time)
                    cnt1 = 0

                    for time in range(extrapol_total_time + 1800, 0, -step_time):
                        self.extrapol_direct = "past"
                        cnt1 = cnt1 + 1
                        next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                              Position0,
                                                                                              Velocity0,
                                                                                              Acceleration0)

                    last_time_extrapol = self.custom_time_start + 23 * 3600 + 45 * 60

                    for time in range(self.custom_time_start, last_time_extrapol, step_time):
                        self.extrapol_direct = "future"

                        next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                              Position0,
                                                                                              Velocity0,
                                                                                              Acceleration0)

                        self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                          Acceleration0, sv_others, infos, self.new_rinex)


                else:
                    extrapol_total_time = (abs(int(diff_date))) * 24 * 60 * 60 + (
                            (int(self.custom_hour) * 60 * 60 + int(
                                self.custom_minute) * 60 + int(
                                self.custom_second)) - curr_time)

                    cnt2 = 0

                    for time in range(0, extrapol_total_time - 1800, step_time):
                        cnt2 = cnt2 + 1
                        self.extrapol_direct = "future"

                        next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                              Position0,
                                                                                              Velocity0,
                                                                                              Acceleration0)

                    last_time_extrapol = self.custom_time_start + 23 * 3600 + 45 * 60

                    for time in range(self.custom_time_start, last_time_extrapol, step_time):

                        self.extrapol_direct = "future"

                        res2, self.time_row = self.middle_func(self.time_row, time, sv_date[2])

                        if res2 == 0:
                            next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.extrapol_direct,
                                                                                                  Position0,
                                                                                                  Velocity0,
                                                                                                  Acceleration0)

                            self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                              Acceleration0, sv_others, infos, self.new_rinex)

    def rinex_parser(self, time, sv_name, sv_date, position, velocity, acceleration, sv_others, info,
                     rinex_f):

        try:
            f = open(rinex_f, "a")
            self.header_info_1 = self.header_info[0]
            self.header_info_1 = self.header_info_1.split()
            self.rinex_version = self.header_info_1[0]

            sv_name = sv_name
            sv_year = sv_date[0]

            sv_real_year = sv_year

            if len(str(sv_year)) == 4:
                sv_year = sv_year.split("0")
                sv_year = sv_year[1]

            sv_month = sv_date[1]
            sv_day = sv_date[2]

            List_month_30 = [1, 4, 6, 9, 11]
            List_month_31 = [3, 5, 7, 8, 10, 12]

            sv_hour: str

            if time < 0:
                time = 24 * 60 * 60 + time
                sv_day = str(int(sv_day) - 1)

            sv_hour, sv_minutes, sv_secondes = sec_to_hours(time)

            if int(sv_hour) >= 24:
                sv_hour = str(int(sv_hour) - 24)
                sv_day = str(int(sv_day) + 1)

            if int(sv_day) == 30:
                if int(sv_month) in List_month_30:
                    sv_day = str(1)
                    sv_month = str(int(sv_month) + 1)

                    if int(sv_month) >= 12:
                        sv_month = str(1)
                        sv_year = str(int(sv_year) + 1)

            if int(sv_day) > 31:
                if int(sv_month) in List_month_31:
                    sv_day = str(1)
                    sv_month = str(int(sv_month) + 1)

                    if int(sv_month) >= 12:
                        sv_month = str(1)
                        sv_year = str(int(sv_year) + 1)

            if int(sv_day) == 28:
                if int(sv_month) == 2:
                    sv_month = str(int(sv_month) + 1)

            sv_other_1 = sv_others[0]
            sv_other_1 = '%.12e' % Decimal(sv_other_1)

            sv_other_2 = sv_others[1]
            sv_other_2 = '%.12e' % Decimal(sv_other_2)

            sv_other_3 = sv_others[2]
            sv_other_3 = '%.12e' % Decimal(sv_other_3)

            sv_x_position = position[0]
            sv_x_position = '%.12e' % Decimal(sv_x_position)

            sv_x_velocity = position[1]
            sv_x_velocity = '%.12e' % Decimal(sv_x_velocity)

            sv_x_acceleration = position[2]
            sv_x_acceleration = '%.12e' % Decimal(sv_x_acceleration)

            sv_y_position = velocity[0]
            sv_y_position = '%.12e' % Decimal(sv_y_position)

            sv_y_velocity = velocity[1]
            sv_y_velocity = '%.12e' % Decimal(sv_y_velocity)

            sv_y_acceleration = velocity[2]
            sv_y_acceleration = '%.12e' % Decimal(sv_y_acceleration)

            sv_z_position = acceleration[0]
            sv_z_position = '%.12e' % Decimal(sv_z_position)

            sv_z_velocity = acceleration[1]
            sv_z_velocity = '%.12e' % Decimal(sv_z_velocity)

            sv_z_acceleration = acceleration[2]
            sv_z_acceleration = '%.12e' % Decimal(sv_z_acceleration)

            sv_info_1 = info[0]
            sv_info_1 = '%.12e' % Decimal(sv_info_1)

            sv_info_2 = info[1]
            sv_info_2 = '%.12e' % Decimal(sv_info_2)

            sv_info_3 = info[2]
            sv_info_3 = '%.12e' % Decimal(sv_info_3)

            exp1 = ' -'
            exp2 = '-'

            if "R" in str(sv_name) or self.rinex_version == "3.04":

                if len(sv_name) == 1:
                    sv_name = "0" + str(sv_name)

                if "R" not in sv_name:
                    sv_name = "R" + str(sv_name)

                sv_hour = "{:02d}".format(int(sv_hour))
                sv_minutes = "{:02d}".format(int(sv_minutes))
                sv_secondes = "{:02d}".format(int(sv_secondes))
                sv_day = "{:02d}".format(int(sv_day))

                str_date = str(sv_name) + " " + str(sv_real_year) + " " + str(sv_month) + " " + str(
                    sv_day) + " " + sv_hour + " " + str(sv_minutes) + " " + str(sv_secondes) + " " + str(
                    sv_other_1) + " " + str(sv_other_2) + " " + str(sv_other_3) + "\n"

                str_date = str(str_date)
                str_date = str_date.replace(exp1, exp2)
                str_x = "     " + str(sv_x_position) + " " + str(sv_y_position) + " " + str(sv_z_position) + " " + str(
                    sv_info_1) + "\n"
                str_x = str_x.replace(exp1, exp2)

                str_y = "     " + str(sv_x_velocity) + " " + str(sv_y_velocity) + " " + str(sv_z_velocity) + " " + str(
                    sv_info_2) + "\n"
                str_y = str_y.replace(exp1, exp2)

                str_z = "     " + str(sv_x_acceleration) + " " + str(sv_y_acceleration) + " " + str(
                    sv_z_acceleration) + " " + str(sv_info_3) + "\n"
                str_z = str_z.replace(exp1, exp2)

            else:
                sv_hour = int(sv_hour)
                sv_day = int(sv_day)
                sv_month = int(sv_month)
                sv_secondes = "{:0.1f}".format(int(sv_secondes))

                string_name = " " + str(sv_name)

                string_year = " " + str(sv_year)

                string_month = "  " + str(sv_month)
                string_day = "  " + str(sv_day)
                string_hour = "  " + str(sv_hour)
                string_minutes = " " + str(sv_minutes)
                string_secondes = "  " + str(sv_secondes)
                string_str1 = " " + str(sv_other_1)
                string_str2 = " " + str(sv_other_2)
                string_str3 = " " + str(sv_other_3)

                if self.rinex_version == "2.01":
                    string_name_0 = len(sv_name)

                    if int(sv_name) >= 10:
                        string_name = str(sv_name)

                    if string_name_0 == 2:
                        string_name = str(sv_name)

                    if int(sv_month) >= 10:
                        string_month = " " + str(sv_month)

                    if int(sv_day) >= 10:
                        string_day = " " + str(sv_day)

                    if int(sv_hour) >= 10:
                        string_hour = " " + str(sv_hour)

                if self.rinex_version == "2.11" or self.rinex_version == "2.10":
                    string_name = str(sv_name)
                    string_name_1 = len(sv_name)
                    if int(sv_name) < 10 and string_name_1 == 1:
                        string_name = " " + str(sv_name)
                    elif string_name_1 == 2:
                        string_name = str(sv_name)

                    if int(sv_month) >= 10:
                        string_month = " " + str(sv_month)

                    if int(sv_day) >= 10:
                        string_day = " " + str(sv_day)

                    if int(sv_hour) >= 10:
                        string_hour = " " + str(sv_hour)

                str_date = string_name + string_year + string_month + string_day + string_hour + string_minutes + \
                           string_secondes + string_str1 + string_str2 + string_str3 + "\n"

                str_date = str(str_date)
                str_date = str_date.replace(exp1, exp2)

                str_x = "    " + str(sv_x_position) + " " + str(sv_y_position) + " " + str(sv_z_position) + " " + str(
                    sv_info_1) + "\n"
                str_x = str_x.replace(exp1, exp2)

                str_y = "    " + str(sv_x_velocity) + " " + str(sv_y_velocity) + " " + str(sv_z_velocity) + " " + str(
                    sv_info_2) + "\n"
                str_y = str_y.replace(exp1, exp2)

                str_z = "    " + str(sv_x_acceleration) + " " + str(sv_y_acceleration) + " " + str(
                    sv_z_acceleration) + " " + str(sv_info_3) + "\n"
                str_z = str_z.replace(exp1, exp2)

            if self.extrapol_direct == "future":
                f.write(str_date)
                f.write(str_x)
                f.write(str_y)
                f.write(str_z)
                return 0

            else:
                return str_date, str_x, str_y, str_z

        except PermissionError as perm_err_1:
            print(perm_err_1)

    def middle_func(self, time_row, time, sv_date_extrapolate):
        res = 0

        for time_step in time_row:
            if int(time_step) == int(time):

                ind = time_row.index(time_step)
                next_data = self.rows[ind]

                true_time, sv_name, sv_date, sv_time, Position0, velocity0, acceleration0, sv_others, info = find_pos(
                    next_data)

                if sv_date[2] == sv_date_extrapolate:

                    self.rinex_parser(true_time, sv_name, sv_date, Position0, velocity0, acceleration0,
                                      sv_others, info, self.new_rinex)
                    self.count = self.count + 1
                else:
                    res = 0
                    break

                res = 1
                break
            else:
                res = 0

        return res, time_row

    def past_time(self, mat):
        len_mat = len(mat)
        for c in range(len_mat, 0, -4):
            mat_mat = mat[c - 4:c]
            f = open(self.new_rinex, "a")
            f.write(str(mat_mat[0]))
            f.write(str(mat_mat[1]))
            f.write(str(mat_mat[2]))
            f.write(str(mat_mat[3]))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    qtmodern.styles.light(app)
    mw = qtmodern.windows.ModernWindow(w)
    mw.show()
    app.exec_()
