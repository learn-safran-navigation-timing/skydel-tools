"""
Skydel Extrapolator for Rinex GLONASS Navigation File - Main QT application class.

Created on 14 06 2021

:author: Grace Oulai
:copyright: Skydel © 2021
:Version: 21.6.1
"""

# Import
import glob
import csv
import os
import sys
import subprocess
import shutil
import qtmodern.styles
import qtmodern.windows
from PyQt5 import QtGui, QtCore
from get_sat_navigation import RinexReader
from Runge_Kutta_4 import RungeKutta4
from decimal import Decimal
from PyQt5.QtWidgets import QLineEdit, QLabel, QDesktopWidget, QFileDialog, QMenuBar, QMessageBox
from PyQt5 import QtWidgets
from about import UiAboutDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

ephemeris_reader = RinexReader()
range_kutta = RungeKutta4()


def find_pos(line):
    """'Sat_ID': sv_name, 'year': sv_year, 'month': sv_month, 'day': sv_day, 'hour': sv_hour,
     'min': sv_minutes, 'sec': sv_secondes, 'totalsec': totalsec,
     'bias': float(sv_clock_bias), 'freq': float(sv_freq_draft), 'frame': float(sv_frame_time),
     'x': float(sv_x_position), 'y': float(sv_y_position), 'z': float(sv_z_position),
     'vx': float(sv_x_velocity), 'vy': float(sv_y_velocity), 'vz': float(sv_z_velocity),
     'ax': float(sv_x_acceleration), 'ay': float(sv_y_acceleration), 'az': float(sv_z_acceleration),
     'health': float(sv_x_health), 'freq_num': float(sv_y_health), 'age': float(sv_z_health)})"""
    sv_name = str(line[0])
    sv_date = [str(line[1]), str(line[2]), str(line[3])]
    sv_time = [str(line[4]), str(line[5]), str(line[6])]
    time = int(line[7])
    sv_others = [float(line[8]), float(line[9]), float(line[10])]
    Position0 = [float(line[11]), float(line[12]), float(line[13])]
    Velocity0 = [float(line[14]), float(line[15]), float(line[16])]
    Acceleration0 = [float(line[17]), float(line[18]), float(line[19])]
    infos = [float(line[20]), float(line[21]), float(line[22])]
    return time, sv_name, sv_date, sv_time, Position0, Velocity0, Acceleration0, sv_others, infos


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
        self.direc = "future"
        self.file = str()
        self.path = str()
        self.new_rinex = str()
        self.count = int()
        self.time_row = list()
        self.rows = list()
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

        # Studio view to Skydel View

        self.title1 = QLabel("Skydel Extrapolator for Rinex GLONASS Navigation")
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setFont(QFont('Arial', 14))
        self.title1.setStyleSheet("background-color:#545759; border-radius:5px")

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
        # self.save_button1.setStyleSheet("background-color:white; border-radius:3.5px")
        self.save_button_1_layout.setAlignment(Qt.AlignCenter)
        self.save_button_1_layout.addWidget(self.save_button1)

        self.end_process = QLabel()
        self.end_process.setFont(QFont('Arial', 10))

        # self.save_button_1_layout.addWidget(self.file_save_path_1)
        spacerItem0 = QtWidgets.QSpacerItem(50, 30, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        spacerItem1 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        layout1 = QtWidgets.QVBoxLayout()
        layout1.addWidget(menubar, 0)
        layout1.addItem(spacerItem1)
        layout1.addWidget(self.title1, 0)
        layout1.addItem(spacerItem0)
        layout1.addLayout(self.load_button_1_layout, 1)
        layout1.addItem(spacerItem1)
        layout1.addLayout(self.save_button_1_layout)
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

    def show_about(self):
        self.ui_about.show()

    def load_rinex(self):
        self.end_process.setText("")

        self.file, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + " DATA Files", ".",
                                                                   "(*.rnx *.csv *.txt *.**g)")
        self.path = "tmp"

        try:
            os.rmdir(self.path)
        except OSError:
            print("Deletion of the temporary directory %s failed" % self.path)
        else:
            print("Successfully deleted the temporary directory %s" % self.path)

        if self.file:
            skip_header, rin_detec, self.header_infos  = ephemeris_reader.find_header(self.file)
            if rin_detec == 3:
                new_lines, length_skipline = ephemeris_reader.readRinex(self.file, skip_header)
                ephemeris_reader.readline(new_lines, length_skipline)
                self.file_path_1.setText(self.file)
                self.save_button1.setEnabled(True)
            else:
                QMessageBox.about(self, "Rinex Format Error", "The loaded file is not a Rinex Navigation GLONASS.")

    def on_file_saved_2(self):

        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "New_Rinex",
                                                  "All Files (*);;Text Files (*.rnx)", options=options)
        return fileName

    def main_func(self):
        self.end_process.setText("Processing...")

        self.new_rinex = self.on_file_saved_2()

        f = open(self.new_rinex, "a+")

        with open(self.file) as handler:
            for i, line in enumerate(handler):
                f.write(line)
                if 'END OF HEADER' in line:
                    break

        for filename in glob.glob((os.path.join(self.path, '*.csv'))):

            self.count = 0

            self.time_row = []
            with open(os.path.join(os.getcwd(), filename), 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Reads header row as a list
                self.rows = list(reader)

                for row in self.rows:
                    self.time_row.append(row[7])

            with open(os.path.join(os.getcwd(), filename), 'r') as f:  # open in readonly mode
                reader = csv.reader(f)
                next(reader)
                true_data = next(reader)
                true_time, sv_name, sv_date, sv_time, Position0, Velocity0, Acceleration0, sv_others, infos = find_pos(
                    true_data)
                curr_time = int(true_time)
                step_time = 900 + 900
                end_time = 23 * 3600 + 45 * 60

                self.suite_1(true_time, sv_name, sv_date, Position0, Velocity0, Acceleration0,
                             sv_others, infos, curr_time, step_time, end_time)

                if true_time == 900:

                    for time in range(900, curr_time + 1, step_time):
                        self.direc = "future"

                        res1, self.time_row = self.midle_func(self.time_row, time)

                        if res1 == 0:
                            next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.direc, Position0,
                                                                                                  Velocity0,
                                                                                                  Acceleration0)

                            self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                              Acceleration0,
                                              sv_others,
                                              infos, self.new_rinex)

                    for time in range(curr_time + 1800, end_time + 1, step_time):

                        self.direc = "future"

                        res2, self.time_row = self.midle_func(self.time_row, time)

                        if res2 == 1:
                            next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.direc, Position0,
                                                                                                  Velocity0,
                                                                                                  Acceleration0)
                        else:
                            next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.direc, Position0,
                                                                                                  Velocity0,
                                                                                                  Acceleration0)
                            self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                              Acceleration0,
                                              sv_others, infos, self.new_rinex)

        shutil.rmtree(self.path)
        self.end_process.setText("The new rinex has been successfully generated.")

    def suite_1(self, true_time, sv_name, sv_date, Position0, Velocity0, Acceleration0, sv_others,
                infos, curr_time, step_time, end_time):
        mat = []

        if true_time > 900:

            for time in range(curr_time, 1, -step_time):
                self.direc = "past"
                if time == true_time:
                    string_date, string_x, string_y, string_z = self.midle_func_2(time)
                else:

                    next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.direc, Position0,
                                                                                          Velocity0,
                                                                                          Acceleration0)

                    string_date, string_x, string_y, string_z = self.rinex_parser(time, sv_name, sv_date,
                                                                                  next_Position,
                                                                                  next_Velocity, Acceleration0,
                                                                                  sv_others,
                                                                                  infos, self.new_rinex)

                mat.append(string_date)
                mat.append(string_x)
                mat.append(string_y)
                mat.append(string_z)
            self.past_time(mat)
            mat_x = mat[1]
            mat_v = mat[2]
            mat_a = mat[3]

            mat_x = mat_x.replace('e', 'E').replace('E-', 'Eneg').replace('-', ' -').split()
            mat_x = [item.replace('Eneg', 'E-') for item in mat_x]

            mat_v = mat_v.replace('e', 'E').replace('E-', 'Eneg').replace('-', ' -').split()
            mat_v = [item.replace('Eneg', 'E-') for item in mat_v]

            mat_a = mat_a.replace('e', 'E').replace('E-', 'Eneg').replace('-', ' -').split()
            mat_a = [item.replace('Eneg', 'E-') for item in mat_a]

            Position0 = [mat_x[0], mat_v[0], mat_a[0]]
            Position0 = [float(i) for i in Position0]

            Velocity0 = [mat_x[1], mat_v[1], mat_a[1]]
            Velocity0 = [float(i) for i in Velocity0]

            Acceleration0 = [mat_x[2], mat_v[2], mat_a[2]]
            Acceleration0 = [float(i) for i in Acceleration0]

            for time in range(curr_time + 1800, end_time + 1, step_time):

                self.direc = "future"

                res2, self.time_row = self.midle_func(self.time_row, time)

                if res2 == 1:
                    next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.direc,
                                                                                          Position0,
                                                                                          Velocity0,
                                                                                          Acceleration0)
                else:

                    next_Position, next_Velocity, Acceleration0 = range_kutta.check_multi(self.direc, Position0,
                                                                                          Velocity0,
                                                                                          Acceleration0)

                    self.rinex_parser(time, sv_name, sv_date, next_Position, next_Velocity,
                                      Acceleration0, sv_others, infos, self.new_rinex)

    def rinex_parser(self, time, sv_name, sv_date, position, velocity, acceleration, sv_others, infos,
                     rinex_f):

        f = open(rinex_f, "a+")

        self.header_info_1 = self.header_infos[0]
        self.header_info_1 = self.header_info_1.split()
        self.rinex_version = self.header_info_1[0]
        print(self.rinex_version)

        sv_name = sv_name
        sv_year = sv_date[0]
        sv_month = sv_date[1]
        sv_day = sv_date[2]

        sv_hour, sv_minutes, sv_secondes = sec_to_hours(time)

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

        sv_info_1 = infos[0]
        sv_info_1 = '%.12e' % Decimal(sv_info_1)

        sv_info_2 = infos[1]
        sv_info_2 = '%.12e' % Decimal(sv_info_2)

        sv_info_3 = infos[2]
        sv_info_3 = '%.12e' % Decimal(sv_info_3)

        exp1 = ' -'
        exp2 = '-'

        if "R" in str(sv_name):
            sv_hour = "{:02d}".format(int(sv_hour))
            sv_minutes = "{:02d}".format(int(sv_minutes))
            sv_secondes = "{:02d}".format(int(sv_secondes))
            string_date = str(sv_name) + " " + str(sv_year) + " " + str(sv_month) + " " + str(
                sv_day) + " " + sv_hour + " " + str(sv_minutes) + " " + str(sv_secondes) + " " + str(
                sv_other_1) + " " + str(
                sv_other_2) + " " + str(sv_other_3) + "\n"

            string_date = str(string_date)
            string_date = string_date.replace(exp1, exp2)
            string_x = "     " + str(sv_x_position) + " " + str(sv_y_position) + " " + str(sv_z_position) + " " + str(
                sv_info_1) + "\n"
            string_x = string_x.replace(exp1, exp2)

            string_y = "     " + str(sv_x_velocity) + " " + str(sv_y_velocity) + " " + str(sv_z_velocity) + " " + str(
                sv_info_2) + "\n"
            string_y = string_y.replace(exp1, exp2)

            string_z = "     " + str(sv_x_acceleration) + " " + str(sv_y_acceleration) + " " + str(
                sv_z_acceleration) + " " + str(sv_info_3) + "\n"
            string_z = string_z.replace(exp1, exp2)

        else:
            sv_hour = int(sv_hour)
            sv_day = int(sv_day)
            sv_month = int(sv_month)

            sv_secondes = "{:0.1f}".format(int(sv_secondes))

            if int(sv_hour) < 10:
                if int(sv_name) < 10:

                    if self.rinex_version == "2.01":
                        string_date = " " + str(sv_name) + " " + str(sv_year) + " " + str(sv_month) + " " + str(
                            sv_day) + "  " + str(sv_hour) + " " + str(sv_minutes) + "  " + str(sv_secondes) + " " + str(
                            sv_other_1) + " " + str(
                            sv_other_2) + " " + str(sv_other_3) + "\n"
                    else:
                        string_date = " " + str(sv_name) + " " + str(sv_year) + "  " + str(sv_month) + "  " + str(
                            sv_day) + "  " + str(sv_hour) + " " + str(sv_minutes) + "  " + str(sv_secondes) + " " + str(
                            sv_other_1) + " " + str(
                            sv_other_2) + " " + str(sv_other_3) + "\n"
                else:

                    if self.rinex_version == "2.01":
                        string_date = str(sv_name) + " " + str(sv_year) + " " + str(sv_month) + " " + str(
                            sv_day) + "  " + str(sv_hour) + " " + str(sv_minutes) + "  " + str(sv_secondes) + " " + str(
                            sv_other_1) + " " + str(
                            sv_other_2) + " " + str(sv_other_3) + "\n"
                    else:
                        string_date = str(sv_name) + " " + str(sv_year) + "  " + str(sv_month) + "  " + str(
                            sv_day) + "  " + str(sv_hour) + " " + str(sv_minutes) + "  " + str(sv_secondes) + " " + str(
                            sv_other_1) + " " + str(
                            sv_other_2) + " " + str(sv_other_3) + "\n"

            else:
                if int(sv_name) < 10:

                    if self.rinex_version == "2.01":
                        string_date = " " + str(sv_name) + " " + str(sv_year) + " " + str(sv_month) + " " + str(
                            sv_day) + " " + str(sv_hour) + " " + str(sv_minutes) + "  " + str(sv_secondes) + " " + str(
                            sv_other_1) + " " + str(
                            sv_other_2) + " " + str(sv_other_3) + "\n"
                    else:
                        string_date = " " + str(sv_name) + " " + str(sv_year) + "  " + str(sv_month) + "  " + str(
                            sv_day) + " " + str(sv_hour) + " " + str(sv_minutes) + "  " + str(sv_secondes) + " " + str(
                            sv_other_1) + " " + str(
                            sv_other_2) + " " + str(sv_other_3) + "\n"
                else:

                    if self.rinex_version == "2.01":
                        string_date = str(sv_name) + " " + str(sv_year) + " " + str(sv_month) + " " + str(
                            sv_day) + " " + str(sv_hour) + " " + str(sv_minutes) + "  " + str(sv_secondes) + " " + str(
                            sv_other_1) + " " + str(
                            sv_other_2) + " " + str(sv_other_3) + "\n"
                    else:
                        string_date = str(sv_name) + " " + str(sv_year) + "  " + str(sv_month) + "  " + str(
                            sv_day) + " " + str(sv_hour) + " " + str(sv_minutes) + "  " + str(sv_secondes) + " " + str(
                            sv_other_1) + " " + str(
                            sv_other_2) + " " + str(sv_other_3) + "\n"

            string_date = str(string_date)
            string_date = string_date.replace(exp1, exp2)

            string_x = "    " + str(sv_x_position) + " " + str(sv_y_position) + " " + str(sv_z_position) + " " + str(
                sv_info_1) + "\n"
            string_x = string_x.replace(exp1, exp2)

            string_y = "    " + str(sv_x_velocity) + " " + str(sv_y_velocity) + " " + str(sv_z_velocity) + " " + str(
                sv_info_2) + "\n"
            string_y = string_y.replace(exp1, exp2)
            string_z = "    " + str(sv_x_acceleration) + " " + str(sv_y_acceleration) + " " + str(
                sv_z_acceleration) + " " + str(sv_info_3) + "\n"
            string_z = string_z.replace(exp1, exp2)

        if self.direc == "future":
            f.write(string_date)
            f.write(string_x)
            f.write(string_y)
            f.write(string_z)

            return 0

        else:
            return string_date, string_x, string_y, string_z

    def midle_func_2(self, time):
        self.direc = "past"

        next_data = self.rows[self.count]

        true_time, sv_name, sv_date, sv_time, Position0, Velocity0, Acceleration0, sv_others, infos = find_pos(
            next_data)
        string_date, string_x, string_y, string_z = self.rinex_parser(time, sv_name, sv_date,
                                                                      Position0, Velocity0, Acceleration0,
                                                                      sv_others, infos, self.new_rinex)
        return string_date, string_x, string_y, string_z

    def midle_func(self, time_row, time):
        res = 0

        for time_step in time_row:
            if int(time_step) == int(time):

                ind = time_row.index(time_step)
                next_data = self.rows[ind]

                true_time, sv_name, sv_date, sv_time, Position0, Velocity0, Acceleration0, sv_others, infos = find_pos(
                    next_data)
                self.rinex_parser(true_time, sv_name, sv_date, Position0, Velocity0, Acceleration0,
                                  sv_others, infos, self.new_rinex)
                self.count = self.count + 1

                res = 1
                break
            else:
                res = 0

        return res, time_row

    def past_time(self, mat):

        len_mat = len(mat)
        for c in range(len_mat, 0, -4):
            mat_mat = mat[c - 4:c]
            f = open(self.new_rinex, "a+")
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
