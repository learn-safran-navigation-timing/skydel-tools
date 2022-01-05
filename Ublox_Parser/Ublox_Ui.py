import csv
import glob
import os
import sys
import time
# import qtmodern
from PyQt5.QtWidgets import QFileDialog
# import qtmodern.styles
# import qtmodern.windows
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import (QLabel, QRadioButton, QApplication)
from PyQt5.QtWidgets import QLineEdit, QMenuBar, QDesktopWidget, QMessageBox, QComboBox, QGroupBox, QCheckBox
import serial
from serial import Serial
from pyubx2 import UBXMessage, SET

import pyubx2.ubxtypes_core as ubt
from mySwitch import MySwitch
from pyubx2 import UBXReader
from pyubx2.ubxtypes_core import GNSSLIST, GALILEOSIGLIST, GPSSIGLIST, BEIDOUSIGLIST, GLONASSSIGLIST, QZSSSIGLIST
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication)
from pyubx2.about_dialog import Ui_AboutDialog
from pyubx2.serial_handler import SerialHandler
from pyubx2.ubxhelpers import itow2utc


# ajouter un bouton connect
# ajouter un bouton save csv qu'on peut activer et desactiver au cours du sauvetage ( Saving CSV - Not saving CSV.)

# https://xkcd.com/color/rgb/

# class PushButtonStop(QWidget):
#
#     stop_streaming = pyqtSignal(bool)
#
#     def __init__(self):
#         super().__init__()
#         self.okButton = QPushButton("Stop")
#         self.okButton.clicked.connect(self.stop_stream)
#
#         hbox = QVBoxLayout()
#         #hbox.addStretch(1)
#         hbox.addWidget(self.okButton)
#
#         self.setLayout(hbox)
#
#         self.setGeometry(300, 300, 300, 150)
#         self.setWindowTitle('Stop Streaming')
#
#     def stop_stream(self):
#         print("Stop the streaming")
#         self.stop_streaming.emit(True)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set the necessary variables
        self.counter = 0
        self.minute = '00'
        self.second = '00'
        self.count = '00'
        self.startWatch = False

        # Create label to display the watch
        # Set geometry for the label
        # self.label.setGeometry(100, 40, 150, 70)

        # Create timer object
        self.timer_count = QTimer(self)
        # Add a method with the timer
        self.timer_count.timeout.connect(self.showCounter)
        # Call start() method to modify the timer value
        self.timer_count.start(100)

        self.running_mode = str()
        self.serial_running = False
        self.csv_list = []
        self.csv_list_1 = []
        self.csv_list_2 = []
        self.csv_list_3 = []
        self.csv_list_4 = []
        self.csv_list_5 = []
        self.csv_list_6 = []
        self.csv_list_7 = []

        self.testfname = ""
        self.save_folder = ""
        self.running_stop = False

        hlay = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('Skydel-NewLogo.png')
        label.resize(85, 85)
        label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio))
        hlay.addWidget(label, 0)

        # MenuBar
        menubar = QMenuBar()
        actionFile00 = menubar.addMenu("File")
        actionFile00.addAction("Quit")
        actionFile00.triggered.connect(self.quit_app)

        # self.save_file = actionFile00.addAction("Load")
        # self.save_file.triggered.connect(self.on_button_clicked)
        actionFile01 = menubar.addMenu("View")
        self.ui_view = actionFile01.addAction("Settings")
        self.ui_view.setCheckable(True)
        self.ui_view.setChecked(True)
        self.ui_view.triggered.connect(self.on_view_changed)
        actionFile01.addSeparator()
        self.html_view = actionFile01.addAction("Status bar")
        self.html_view.setCheckable(True)
        self.html_view.setChecked(False)
        self.html_view.triggered.connect(self.on_view_changed)
        actionFile01.addSeparator()
        self.html_view = actionFile01.addAction("Console")
        self.html_view.setCheckable(True)
        self.html_view.setChecked(False)
        self.html_view.triggered.connect(self.on_view_changed)
        actionFile01.addSeparator()
        self.html_view = actionFile01.addAction("Map")
        self.html_view.setCheckable(True)
        self.html_view.setChecked(False)
        self.html_view.triggered.connect(self.on_view_changed)
        actionFile01.addSeparator()
        self.html_view = actionFile01.addAction("Satellites")
        self.html_view.setCheckable(True)
        self.html_view.setChecked(False)
        self.html_view.triggered.connect(self.on_view_changed)
        actionFile02 = menubar.addMenu("Help")
        self.about_ui = actionFile02.addAction("About")
        self.about_ui.triggered.connect(self.show_about)
        actionFile02.addSeparator()
        self.ubx_config = actionFile02.addAction("Ubx configuration")
        # self.ubx_config.triggered.connect(self.show_about)
        actionFile02.addSeparator()
        # actionFile02 = menubar.addMenu("Exit")
        # actionFile02.addAction("Quit")
        # actionFile02.triggered.connect(self.quit_app)

        # Switch button
        self.streamin_type_label = QLabel('Streaming Type')
        self.streamin_type_label.setFont(QFont('Arial', 9))
        self.ch_bx = MySwitch()
        self.ch_bx.setChecked(True)
        self.running_mode = "FILE"
        self.ch_bx.toggled.connect(self.on_mode_running_changed)
        self.streamin_type_layout = QtWidgets.QHBoxLayout()
        self.serial_port_lab = QLabel('Serial Port')
        self.file_load = QLabel('File')
        # self.streamin_type_layout.addWidget(self.serial_port_lab, 0)
        self.streamin_type_layout.addWidget(self.ch_bx)
        # self.streamin_type_layout.addWidget(self.file_load, 2)

        ch_box_layout = QtWidgets.QHBoxLayout()
        ch_box_layout.addWidget(self.streamin_type_label, 0)
        ch_box_layout.addWidget(self.ch_bx, 1)

        frame1 = QtWidgets.QFrame(self)
        frame1.setFrameShadow(QtWidgets.QFrame.Plain)

        # SWITCH GROUP BOX

        self.port_label = QLabel('Port')
        self.port_combo = QComboBox(self)
        self.port_combo.setFont(QFont('Arial', 10))
        # self.port_combo.addItem('COM 1')
        # self.port_combo.addItem('COM 2')
        # self.port_combo.addItem('COM 5')
        # self.port_combo.addItem('COM 6')
        self.port_combo.activated[str].connect(self.onActivated10)
        port_layout = QtWidgets.QHBoxLayout()
        port_layout.addWidget(self.port_label, 0)
        port_layout.addWidget(self.port_combo, 1)

        self.baud_rate_label = QLabel('Baud rate')
        self.baud_rate_edit = QLineEdit()
        self.baud_rate_edit.setText(str(9600))
        baud_rate_layout = QtWidgets.QHBoxLayout()
        baud_rate_layout.addWidget(self.baud_rate_label, 1)
        baud_rate_layout.addWidget(self.baud_rate_edit, 1)

        self.cold_start_button = QtWidgets.QPushButton('Cold start')
        self.cold_start_button.setFont(QFont('Arial', 10))
        self.cold_start_button.clicked.connect(self.cold_start)

        # self.connect_port_button = QtWidgets.QPushButton('Connect')
        # self.connect_port_button.setFont(QFont('Arial', 10))
        # self.connect_port_button.clicked.connect(self.connect_port)

        self.hot_start_button = QtWidgets.QPushButton('Hot start')
        self.hot_start_button.setFont(QFont('Arial', 10))
        self.hot_start_button.clicked.connect(self.hot_start)

        self.warm_start_button = QtWidgets.QPushButton('Warm start')
        self.warm_start_button.setFont(QFont('Arial', 10))
        self.warm_start_button.clicked.connect(self.warm_start)

        self.serial_group = QGroupBox("Serial Port Settings")
        self.serial_group.setFont(QFont('Arial', 9))
        serial_setting_layout = QtWidgets.QVBoxLayout()
        self.serial_group.setLayout(serial_setting_layout)
        serial_setting_layout.addLayout(port_layout, 0)
        serial_setting_layout.addLayout(baud_rate_layout, 1)
        serial_setting_layout.addWidget(self.hot_start_button, 2)
        serial_setting_layout.addWidget(self.warm_start_button, 2)
        serial_setting_layout.addWidget(self.cold_start_button, 2)

        self.load_file_button_layout = QtWidgets.QHBoxLayout()
        self.load_file_button = QtWidgets.QPushButton('Load file')
        self.load_file_button.setFont(QFont('Arial', 10))
        self.load_file_button.clicked.connect(self.load_file)
        self.load_file_button_layout.setAlignment(Qt.AlignCenter)
        self.load_file_button_layout.addWidget(self.load_file_button)
        self.serial_group.setEnabled(False)

        self.file_group = QGroupBox("File settings")
        self.file_group.setFont(QFont('Arial', 9))
        self.file_group_layout = QtWidgets.QHBoxLayout()
        self.file_group.setLayout(self.file_group_layout)
        self.file_group_layout.addLayout(self.load_file_button_layout)

        self.rbtn1 = QRadioButton('UBX')
        self.rbtn2 = QRadioButton('UBX + NMEA')
        # self.rbtn3 = QRadioButton('ALL')
        self.rbtn1.toggled.connect(self.onClickedProtocol_UBX)
        self.rbtn2.toggled.connect(self.onClickedProtocol_UBX_NMEA)
        self.rbtn1.setChecked(True)
        self.protocol_mode = "UBX"

        # self.rbtn3.toggled.connect(self.onClickedProtocol_ALL)

        groupbox12 = QGroupBox("Protocols Displayed")
        groupbox12.setFont(QFont('Arial', 9))
        layout12 = QtWidgets.QHBoxLayout()
        groupbox12.setLayout(layout12)
        layout12.addWidget(self.rbtn1, 1)
        layout12.addWidget(self.rbtn2, 1)
        # layout12.addWidget(self.rbtn3, 1)

        self.save_checkbox = QCheckBox("Save CSV.")
        self.labelA = QLabel("Not save.")
        self.save_checkbox.stateChanged.connect(self.checkBoxChangedAction)

        save_goup = QGroupBox("Save Options")
        save_goup.setFont(QFont('Arial', 9))
        save_layout = QtWidgets.QHBoxLayout()
        save_goup.setLayout(save_layout)
        save_layout.addWidget(self.save_checkbox, 1)
        save_layout.addWidget(self.labelA, 1)

        # self.ubx_label = QLabel('UBX')
        # ubx_message_combo = QComboBox(self)
        # ubx_message_combo.setFont(QFont('Arial', 10))
        # ubx_message_combo.activated[str].connect(self.onActivated10)
        # ubx_layout = QtWidgets.QHBoxLayout()
        # ubx_layout.addWidget(self.ubx_label, 0)
        # ubx_layout.addWidget(ubx_message_combo, 1)

        self.ubx_msg_class = []
        self.ubx_1 = QCheckBox('RXM-RAWX')
        self.ubx_2 = QCheckBox('NAV-PVT')
        self.ubx_3 = QCheckBox('NAV-POSECEF')
        self.ubx_4 = QCheckBox('ALL')
        self.ubx_4.setChecked(True)

        self.ubx_1.stateChanged.connect(self.msg_type_handler)
        self.ubx_2.stateChanged.connect(self.msg_type_handler)
        self.ubx_3.stateChanged.connect(self.msg_type_handler)
        self.ubx_4.stateChanged.connect(self.msg_type_handler)

        ubx_msg_group = QGroupBox("UBX/NMEA Message")
        ubx_msg_group.setFont(QFont('Arial', 9))
        ubx_msg_layout = QtWidgets.QVBoxLayout()
        ubx_msg_group.setLayout(ubx_msg_layout)
        # ubx_msg_layout.addLayout(ubx_layout, 0)
        ubx_msg_layout.addWidget(self.ubx_1, 1)
        ubx_msg_layout.addWidget(self.ubx_2, 1)
        ubx_msg_layout.addWidget(self.ubx_3, 1)
        ubx_msg_layout.addWidget(self.ubx_4, 1)

        spacerItem = QtWidgets.QSpacerItem(102, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        layout4 = QtWidgets.QVBoxLayout()
        layout4.addWidget(menubar, 0)
        layout4.addItem(spacerItem)
        layout4.addLayout(ch_box_layout, 1)
        layout4.addItem(spacerItem)
        layout4.addWidget(self.serial_group, 2)
        layout4.addItem(spacerItem)
        layout4.addWidget(self.file_group, 3)
        layout4.addItem(spacerItem)
        layout4.addWidget(groupbox12, 4)
        layout4.addItem(spacerItem)
        layout4.addWidget(save_goup, 5)
        layout4.addItem(spacerItem)
        layout4.addWidget(ubx_msg_group, 6)
        # layout4.addWidget(frame1, 6)

        self.layout3 = QtWidgets.QHBoxLayout()
        self.title1 = QLabel("UBX MESSAGE DISPLAY")
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setFont(QFont('Arial', 10))
        self.title1.setStyleSheet("background-color:#3f829d; border-radius:5px")

        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.setFont(QFont('Arial', 10))
        self.start_button.pressed.connect(self.pre_start)

        # self.connect_button = QtWidgets.QPushButton('Connect')
        # self.connect_button.setFont(QFont('Arial', 10))
        # self.connect_button.clicked.connect(self.connect_serial)

        # self.pause_button = QtWidgets.QPushButton('Pause')
        # self.pause_button.setFont(QFont('Arial', 10))
        # self.pause_button.clicked.connect(self.pause_streaming_func)

        self.stop_button = QtWidgets.QPushButton('Stop')
        self.stop_button.setFont(QFont('Arial', 10))
        self.stop_button.clicked.connect(self.stop_streaming_func)

        # self.iTow = QtWidgets.QLineEdit('2021:02:05')
        # self.iTow.setAlignment(QtCore.Qt.AlignCenter)  # <-----
        # self.iTow.setFont(QFont('Arial', 10))

        self.iTow = QtWidgets.QLineEdit('00:00:00')
        # self.iTow = QLabel(self)
        self.iTow.setAlignment(QtCore.Qt.AlignCenter)  # <-----
        self.iTow.setFont(QFont('Arial', 10))

        self.real_itow = QtWidgets.QLineEdit('00:00:00')
        # self.iTow = QLabel(self)
        self.real_itow.setAlignment(QtCore.Qt.AlignCenter)  # <-----
        self.real_itow.setFont(QFont('Arial', 10))

        # self.button1.setStyleSheet("background-color:darkgray; border-radius:5px")
        # self.button1.setEnabled(False)

        self.layout3.addWidget(self.start_button, 1)
        self.layout3.addWidget(self.iTow, 2)
        self.layout3.addWidget(self.real_itow, 3)
        self.layout3.addWidget(self.title1, 4)

        # 107ab0  3f829d 047495 39758d

        layout2 = QtWidgets.QHBoxLayout()
        self.show_message = QtWidgets.QTextEdit()
        self.show_message.setFont(QFont('Arial', 9))
        # self.show_message.setPlainText("UBX self.streaming")
        self.cursor = self.show_message.textCursor()
        self.cursor.insertText("UBX STREAMING BOARD")

        # neither of the following commands have any effect
        # self.cursor.setPosition(self.cursor.position() - 5)
        # self.cursor.movePosition(self.cursor.Left, self.cursor.KeepAnchor, 3)
        # self.show_message.setTextCursor(self.cursor)

        self.show_other_message = QtWidgets.QTextEdit()
        self.show_other_message.setFont(QFont('Arial', 9))
        layout2.addWidget(self.show_other_message, 0)
        layout2.addWidget(self.show_message, 1)

        # combo1 = QLineEdit(self)
        # combo1.setFont(QFont('Arial', 10))
        # combo1.setEnabled(False)
        # combo1.setStyleSheet("background-color:white")
        # combo1.setFont(QFont('Arial', 10))
        # combo1.addItem('GPS L1')
        # combo1.addItem('GPS L2')
        # combo1.addItem('GPS L5')
        # combo1.addItem('GlONASS L1')
        # combo1.addItem('GLONASS L2')
        # combo1.activated[str].connect(self.onActivated1)
        # self.frequency_1 = 'GPS_L1'

        layout1 = QtWidgets.QVBoxLayout()
        layout1.addLayout(self.layout3, 0)
        layout1.addLayout(layout2, 1)
        # layout1.addWidget(combo1, 2)
        # layout1.addLayout(self.button_1_layout)

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

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def show_about(self):
        print("About")
        self.about = Ui_AboutDialog()
        self.about.show()

    def showCounter(self):
        # Check the value of startWatch  variable to start or stop the Stop Watch
        if self.startWatch:
            # Increment counter by 1
            self.counter += 1

            # Count and set the time counter value
            cnt = int((self.counter / 10 - int(self.counter / 10)) * 10)
            self.count = '0' + str(cnt)

            # Set the second value
            if int(self.counter / 10) < 10:
                self.second = '0' + str(int(self.counter / 10))
            else:
                self.second = str(int(self.counter / 10))
                # Set the minute value
                if self.counter / 10 == 60.0:
                    self.second == '00'
                    self.counter = 0
                    min = int(self.minute) + 1
                    if min < 10:
                        self.minute = '0' + str(min)
                    else:
                        self.minute = str(min)

        # Merge the mintue, second and count values
        text = self.minute + ':' + self.second + ':' + self.count
        # Display the stop watch values in the label
        self.iTow.setText(text)

    def checkBoxChangedAction(self, state):
        if QtCore.Qt.Checked == state:
            self.labelA.setText("Saving CSV.")

            if self.running_stop == False or self.serial_running == False:

                if self.save_folder == "":

                    self.save_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
                    print("Saving:", self.running_stop, self.serial_running)
                    print(self.save_folder)
                    self.refresh_text_box_2("\n")
                    self.refresh_text_box_2("CSV FILE SAVED HERE:")
                    self.refresh_text_box_2(self.save_folder)
                    self.delete_folder(self.save_folder)
                    return self.save_folder

                elif self.save_folder:
                    self.refresh_text_box_2("\n")
                    self.refresh_text_box_2("CSV FILE SAVED HERE:")
                    self.refresh_text_box_2(self.save_folder)
                    # self.delete_folder(self.save_folder)
                    return self.save_folder

                else:
                    QMessageBox.about(self, "CSV FOLDER PATH", "THE FOLDER PATH IS EMPTY")

            elif self.running_stop == True or self.serial_running == True:
                print("Saving:", self.running_stop, self.serial_running)

                if self.save_folder == "":

                    self.save_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
                    print("Saving:", self.running_stop, self.serial_running)
                    print(self.save_folder)

                    self.refresh_text_box_2("\n")
                    self.refresh_text_box_2("CSV FILE SAVED HERE:")
                    self.refresh_text_box_2(self.save_folder)
                    self.delete_folder(self.save_folder)
                    return self.save_folder

                elif self.save_folder:

                    self.refresh_text_box_2("\n")
                    self.refresh_text_box_2("CSV FILE SAVED HERE:")
                    self.refresh_text_box_2(self.save_folder)
                    # self.delete_folder(self.save_folder)
                    return self.save_folder

                else:
                    QMessageBox.about(self, "CSV FOLDER PATH", "THE FOLDER PATH IS EMPTY")
        else:
            self.labelA.setText("Not saving.")

        # base1 = os.path.basename(self.ant_filename)
        # ant_name = os.path.splitext(base1)[0]
        # options = QFileDialog.Options()
        # fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", ant_name,
        #                                           "All Files (*);", options=options)

    def delete_folder(self, folder):
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

    def on_view_changed(self):
        if self.ui_view.isChecked():
            self.view_type = 1
            if self.html_view.isChecked():
                self.view_type = 3
        elif self.html_view.isChecked():
            self.view_type = 2
        else:
            self.view_type = 1
        # print(self.view_type)

    def load_file(self):

        self.testfname, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + " DATA Files", ".",
                                                                        "(*.ubx *.bin)")
        if self.testfname:
            self.refresh_text_box_2("\n")  # MY_FUNCTION_CALL

            self.refresh_text_box_2("FILE MODE:")  # MY_FUNCTION_CALL

            self.refresh_text_box_2(self.testfname)  # MY_FUNCTION_CALL

            # base = os.path.basename(self.model_filename)
            # file_extension = os.path.splitext(base)[1]
            # if file_extension == ".ant":
            #     self.file_path_1.setText(self.model_filename)
            #     self.ant_filename = self.model_filename
            #     self.convert_1()
            # else:
            #     self.ant_filename = ""
            #
            # if file_extension == ".csv":
            #     self.file_path_2.setText(self.model_filename)
            #     self.csv_filename = self.model_filename
            #     self.convert_2()
            # else:
            #     self.csv_filename = ""
        else:
            QMessageBox.about(self, "Load file error", "File not found.")

    def _scan_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
            ports.append("Dell DA20 Adapter")
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            patterns = ('/dev/tty[A-Za-z]*', '/dev/ttyUSB*')
            ports = [glob.glob(pattern) for pattern in patterns]
            ports = [item for sublist in ports for item in sublist]  # flatten
        elif sys.platform.startswith('darwin'):
            patterns = ('/dev/*serial*', '/dev/ttyUSB*', '/dev/ttyS*')
            ports = [glob.glob(pattern) for pattern in patterns]
            ports = [item for sublist in ports for item in sublist]  # flatten
        else:
            raise EnvironmentError('Unsupported platform')
        print(ports)
        result = []

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                if port in result:
                    print("Already in")
                else:
                    result.append(port)
            except (OSError, serial.SerialException):
                pass

        self.port_combo.clear()
        self.port_combo.addItems(result)

        try:
            item = result[0]
            self.port_combo.setCurrentIndex(ports.index(item))
            self.selected_port = item
            return result
        except IndexError as err:
            print(err)
            QMessageBox.about(self, "PORT COM ERROR", "No connected PORT COM")

    def on_mode_running_changed(self):

        # Nomad is not available in this version.
        # See the script RRAP_Performance_GUI.py to see this section with Nomad option.

        if self.ch_bx.isChecked():
            self.running_mode = "FILE"
            self.file_group.setEnabled(True)
            self.serial_group.setEnabled(False)

        else:
            self.running_mode = "SERIAL"
            # self.layout3.addWidget(self.connect_button, 0)
            self.serial_group.setEnabled(True)
            self.file_group.setEnabled(False)
            self._scan_ports()

    def onClickedProtocol_UBX(self):
        self.protocol_mode = "UBX"
        print("UBX")

    def onClickedProtocol_UBX_NMEA(self):
        self.protocol_mode = "UBX + NMEA"
        print("UBX + NMEA")

    def msg_type_handler(self):

        if self.ubx_4.isChecked():
            self.ubx_1.setChecked(False)
            self.ubx_2.setChecked(False)
            self.ubx_3.setChecked(False)
            self.ubx_1.setEnabled(False)
            self.ubx_2.setEnabled(False)
            self.ubx_3.setEnabled(False)
        else:
            self.ubx_1.setEnabled(True)
            self.ubx_2.setEnabled(True)
            self.ubx_3.setEnabled(True)

    # def rxm_rawx(self, state):
    #     if QtCore.Qt.Checked == state:
    #         self.ubx_msg_class.append("RXM-RAWX")
    #
    # def nav_pvt(self, state):
    #     if QtCore.Qt.Checked == state:
    #         self.ubx_msg_class.append("NAV-PVT")
    #
    # def nav_posecef(self, state):
    #     if QtCore.Qt.Checked == state:
    #         self.ubx_msg_class.append("NAV-POSECEF")
    #
    # def ubx_all(self, state):
    #     if QtCore.Qt.Checked == state:
    #         self.ubx_1.setChecked(False)
    #         self.ubx_2.setChecked(False)
    #         self.ubx_3.setChecked(False)
    #         self.ubx_4.setChecked(False)
    #         self.ubx_msg_class.append("ALL")
    #     # import serial
    #     # ser = serial.Serial('/dev/ttyACM0')
    #     # ser_bytes = ser.readline()
    #     # radioBtn = self.sender()
    #     # if radioBtn.isChecked():
    #     #     self.label2.setText("You live in " + radioBtn.text())
    #
    # # def onActivated1(self, text):
    # #     if text == 'GPS L1':
    # #         self.frequency_1 = 'GPS_L1'
    # #     elif text == 'GPS L2':
    # #         self.frequency_1 = 'GPS_L2'
    # #     elif text == 'GPS L5':
    # #         self.frequency_1 = 'GPS_L5'
    # #     elif text == 'GLONASS L1':
    # #         self.frequency_1 = 'GLONASS_L1'
    # #     else:
    # #         self.frequency_1 = 'GLONASS_L2'

    def pre_start(self):
        print(" PRESART")
        if self.running_mode == "":
            print("NO SELECTED MODE: FILE OR SERIAL")
            QMessageBox.about(self, "Start Error", "NO SELECTED MODE: FILE OR SERIAL")

        elif self.protocol_mode == "":
            QMessageBox.about(self, "Start Error", "NO SELECTED PROTOCOLE: UBX OR NMEA")
            print("NO SELECTED PROTOCOLE: UBX OR NMEA")

        elif self.save_checkbox == "":
            QMessageBox.about(self, "Start Error", "NO SELECTED PROTOCOLE: UBX OR NMEA")
            print("NO SELECTED PROTOCOLE: UBX OR NMEA")

        elif self.ubx_msg_class == "":
            QMessageBox.about(self, "Start Error", "NO SELECTED UBX MSG CLASS: RXM-RAWX , NAV_PVT ETC")
            print("NO SELECTED UBX MSG CLASS: RXM-RAWX , NAV_PVT Etc.")

        # elif self.running_mode == "FILE":
        #     print(self.running_mode)
        #     print(self.testfname)
        #     if self.testfname =="":
        #         QMessageBox.about(self, "Start Error", "NO SELECTED FILE")
        #         print("NO SELECTED FILE")
        else:
            self.running_stop = True
            print("--- self.Streaming START")
            self.refresh_text_box_2("\n")  # MY_FUNCTION_CALL
            self.refresh_text_box_2("--- Streaming START")  # MY_FUNCTION_CALL
            # self.Stop_widget = PushButtonStop()
            # self.Stop_widget.show()
            self.layout3.addWidget(self.start_button, 0)
            self.layout3.addWidget(self.stop_button, 1)
            self.layout3.addWidget(self.iTow, 2)
            self.layout3.addWidget(self.real_itow, 3)
            self.layout3.addWidget(self.title1, 4)
            self.start()
            self.refresh_text_box_2("\n")  # MY_FUNCTION_CALL
            self.refresh_text_box_2("--- Streaming END.")  # MY_FUNCTION_CALL
            self.running_stop = False
            self.startWatch = False
            self.stop_streaming_func()

    def start(self):
        # self.Stop_widget.stop_streaming.connect(self.stop_streaming_func)
        # if self.start_button.text() == 'Stop':
        #     self.start_button.setText('Resume')
        #     self.startWatch = False
        # else:
        #     # making startWatch to true
        #     self.startWatch = True
        #     self.start_button.setText('Stop')
        print(self.running_stop)
        print("START")
        self.csv_list = []
        self.csv_list_1 = []
        self.csv_list_2 = []
        self.csv_list_3 = []
        self.csv_list_4 = []
        self.csv_list_5 = []
        self.csv_list_6 = []
        self.delete_folder(self.save_folder)

        if self.running_mode == "FILE":
            if self.running_stop:
                # #testfname = Path(__file__).parent.joinpath("relposned_test.bin")
                # self.testfname = Path(__file__).parent.joinpath("ublox_test_parser.ubx")
                # # testfname = Path(__file__).parent.joinpath("test2.bin")
                # testfile = self.testfname.open("rb")
                # # file = os.path.join(os.path.dirname(__file__), 'ubxdata.bin')
                # with open(self.stream = open(self.testfname, 'rb')
                with open(self.testfname, 'rb') as self.stream:
                    self.startWatch = True

                    if self.protocol_mode == "UBX":
                        ubr = UBXReader(self.stream, False)
                        self.refresh_text_box_2("\n")  # MY_FUNCTION_CALL
                        self.refresh_text_box_2("--- Streaming ...")  # MY_FUNCTION_CALL

                    elif self.protocol_mode == "UBX + NMEA":
                        ubr = UBXReader(self.stream, False)
                        self.refresh_text_box_2("\n")  # MY_FUNCTION_CALL
                        self.refresh_text_box_2("--- Streaming ...")  # MY_FUNCTION_CALL

                    else:
                        print("SURELY A MESSAGE FROM THE MOON")
                    print('UBR:', ubr)

                    for (raw_data, self.parsed_data) in ubr:

                        if self.running_stop == False:
                            break

                        if self.parsed_data:

                            if self.ubx_1.isChecked() and self.ubx_2.isChecked():
                                if self.parsed_data.identity == 'RXM-RAWX' or self.parsed_data.identity == 'NAV-PVT':
                                    self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                                    self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                                    print(self.parsed_data)

                            elif self.ubx_1.isChecked() and self.ubx_3.isChecked():
                                if self.parsed_data.identity == 'RXM-RAWX' or self.parsed_data.identity == 'NAV-POSECEF':
                                    self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                                    self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                                    print(self.parsed_data)

                            elif self.ubx_2.isChecked() and self.ubx_3.isChecked():
                                if self.parsed_data.identity == 'NAV-PVT' or self.parsed_data.identity == 'NAV-POSECEF':
                                    self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                                    self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                                    print(self.parsed_data)

                            # elif self.ubx_2.isChecked():
                            #     if self.parsed_data.identity == 'NAV-PVT':
                            #         self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                            #         self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                            #         print(self.parsed_data)
                            #
                            # elif self.ubx_3.isChecked():
                            #     if self.parsed_data.identity == 'NAV-POSECEF':
                            #         self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                            #         self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                            #         print(self.parsed_data)

                            elif self.ubx_4.isChecked():

                                self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                                self.refresh_text_box("\n")  # MY_FUNCTION_CALL

                                print(self.parsed_data)

                            if self.save_checkbox.isChecked():
                                print("Saving CSV")
                                self.save_parsed_data(self.parsed_data)

                            else:
                                print("Not Saving CSV")

                            try:
                                self.real_itow.setText("iTOW: " + str(itow2utc(self.parsed_data.iTOW)))
                            except AttributeError:
                                continue

        elif self.running_mode == "SERIAL":
            try:
                selected_baud = 9600
                self.stream = Serial(self.selected_port, selected_baud, timeout=5)
                print(" Port is open:", self.stream.is_open)
                # self.selected_port = str(self.port_combo)
                # selected_baud = self.baud_rate_edit
                print("selected_port:", self.selected_port)
                self.refresh_text_box_2("\n")  # MY_FUNCTION_CALL
                self.refresh_text_box_2("--- Streaming ...")  # MY_FUNCTION_CALL

                if self.stream.is_open == True:
                    self.startWatch = True
                    self.serial_running = True

                    while self.stream.is_open == True:

                        if self.serial_running == False:
                            break
                        ubr = UBXReader(self.stream, False)
                        (raw_data, self.parsed_data) = ubr.read()

                        if self.ubx_1.isChecked() and self.ubx_2.isChecked():
                            if self.parsed_data.identity == 'RXM-RAWX' or self.parsed_data.identity == 'NAV-PVT':
                                self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                                self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                                print(self.parsed_data)

                        elif self.ubx_1.isChecked() and self.ubx_3.isChecked():
                            if self.parsed_data.identity == 'RXM-RAWX' or self.parsed_data.identity == 'NAV-POSECEF':
                                self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                                self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                                print(self.parsed_data)

                        elif self.ubx_2.isChecked() and self.ubx_3.isChecked():
                            if self.parsed_data.identity == 'NAV-PVT' or self.parsed_data.identity == 'NAV-POSECEF':
                                self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                                self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                                print(self.parsed_data)
                        # elif self.ubx_2.isChecked():
                        #     if self.parsed_data.identity == 'NAV-PVT':
                        #         self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                        #         self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                        #         print(self.parsed_data)
                        #
                        # elif self.ubx_3.isChecked():
                        #     if self.parsed_data.identity == 'NAV-POSECEF':
                        #         self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                        #         self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                        #         print(self.parsed_data)

                        elif self.ubx_4.isChecked():
                            self.refresh_text_box(self.parsed_data)  # MY_FUNCTION_CALL
                            self.refresh_text_box("\n")  # MY_FUNCTION_CALL
                            print(self.parsed_data)

                        if self.save_checkbox.isChecked():
                            print("Saving CSV")
                            self.save_parsed_data(self.parsed_data)
                        else:
                            print("Not Saving CSV")

            except serial.serialutil.SerialException as err:
                QMessageBox.about(self, "Start Error", str(err))

            # ser = serial.Serial('/dev/ttyUSB0')  # open serial port
            # print(ser.name)  # check which port was really used
            # ser.write(b'hello')  # write a string
            # ser.close()  # close port
        else:
            print("MUST BE A MESSAGE FROM ANOTHER PLANET")

    def save_parsed_data(self, parsed_data):

        print(parsed_data)

        if self.ubx_1.isChecked():
            if parsed_data.identity == 'RXM-RAWX':

                try:
                    num_message = parsed_data.numMeas

                    for gnss_id in range(1, 10, 1):
                        gnss_message_id = 'gnssId_0' + str(gnss_id)
                        gnss_message_id_number = getattr(parsed_data, gnss_message_id)
                        gnss_name = GNSSLIST[gnss_message_id_number]
                        if gnss_name == "GPS":
                            print(gnss_name)
                            gnss_sv_id = 'svId_0' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_0' + str(gnss_id)
                            gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_1 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"
                            print(csv_name_1)
                            # rcvTow_id = 'prMes_0' + str(gnss_id)
                            # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                            #
                            # week_id = 'prMes_0' + str(gnss_id)
                            # week_id_name = getattr(parsed_data, week_id)
                            #
                            # leapS_id = 'prMes_0' + str(gnss_id)
                            # leapS_id_name = getattr(parsed_data, leapS_id)
                            prMes_id = 'prMes_0' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_0' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_0' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_0' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_0' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_0' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_0' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_0' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_0' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_0' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_0' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_1 in self.csv_list_1:
                                self.csv_list_1.append(csv_name_1)
                                with open(csv_name_1, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_1, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                        if gnss_name == "Galileo":
                            print(gnss_name)
                            gnss_sv_id = 'svId_0' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_0' + str(gnss_id)
                            gnss_sig_id_name = GALILEOSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_2 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"

                            prMes_id = 'prMes_0' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_0' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_0' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_0' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_0' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_0' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_0' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_0' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_0' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_0' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_0' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_2 in self.csv_list_2:
                                self.csv_list_2.append(csv_name_2)
                                with open(csv_name_2, 'a+', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_2, 'a+', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                        # if gnss_name == "Galileo":
                        #     print(gnss_name)
                        #     gnss_sv_id = 'svId_0' + str(gnss_id)
                        #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                        #     gnss_sig_id = 'sigId_0' + str(gnss_id)
                        #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                        #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                        #     if not csv_name in csv_list:
                        #         with open(csv_name, mode='w') as gal_info:
                        #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                        #                                   quoting=csv.QUOTE_MINIMAL)
                        #             gal_info.writerow(gnss_name)
                        #         csv_list.append(csv_name)
                        #     else:
                        #         pass

                        if gnss_name == "GLONASS":
                            print(gnss_name)
                            gnss_sv_id = 'svId_0' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_0' + str(gnss_id)
                            gnss_sig_id_name = GLONASSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_3 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"
                            # rcvTow_id = 'prMes_0' + str(gnss_id)
                            # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                            #
                            # week_id = 'prMes_0' + str(gnss_id)
                            # week_id_name = getattr(parsed_data, week_id)
                            #
                            # leapS_id = 'prMes_0' + str(gnss_id)
                            # leapS_id_name = getattr(parsed_data, leapS_id)
                            prMes_id = 'prMes_0' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_0' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_0' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_0' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_0' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_0' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_0' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_0' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_0' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_0' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_0' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_3 in self.csv_list_3:
                                self.csv_list_3.append(csv_name_3)
                                with open(csv_name_3, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_3, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                        if gnss_name == "BeiDou":
                            print(gnss_name)
                            gnss_sv_id = 'svId_0' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_0' + str(gnss_id)
                            gnss_sig_id_name = BEIDOUSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_4 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"

                        if gnss_name == "QZSS":
                            print(gnss_name)
                            gnss_sv_id = 'svId_0' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_0' + str(gnss_id)
                            gnss_sig_id_name = QZSSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_5 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"
                            # rcvTow_id = 'prMes_0' + str(gnss_id)
                            # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                            #
                            # week_id = 'prMes_0' + str(gnss_id)
                            # week_id_name = getattr(parsed_data, week_id)
                            #
                            # leapS_id = 'prMes_0' + str(gnss_id)
                            # leapS_id_name = getattr(parsed_data, leapS_id)
                            prMes_id = 'prMes_0' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_0' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_0' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_0' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_0' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_0' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_0' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_0' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_0' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_0' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_0' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_5 in self.csv_list_5:
                                self.csv_list_5.append(csv_name_5)
                                with open(csv_name_5, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_5, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                    for gnss_id in range(10, num_message + 1, 1):
                        gnss_message_id = 'gnssId_' + str(gnss_id)
                        gnss_message_id_number = getattr(parsed_data, gnss_message_id)
                        gnss_name = GNSSLIST[gnss_message_id_number]

                        if gnss_name == "GPS":
                            print(gnss_name)
                            gnss_sv_id = 'svId_' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_' + str(gnss_id)
                            gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_1 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"
                            # rcvTow_id = 'prMes_0' + str(gnss_id)
                            # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                            #
                            # week_id = 'prMes_0' + str(gnss_id)
                            # week_id_name = getattr(parsed_data, week_id)
                            #
                            # leapS_id = 'prMes_0' + str(gnss_id)
                            # leapS_id_name = getattr(parsed_data, leapS_id)
                            prMes_id = 'prMes_' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_1 in self.csv_list_1:
                                self.csv_list_1.append(csv_name_1)
                                with open(csv_name_1, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_1, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                        if gnss_name == "Galileo":
                            print(gnss_name)
                            gnss_sv_id = 'svId_' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_' + str(gnss_id)
                            gnss_sig_id_name = GALILEOSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_2 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"
                            # rcvTow_id = 'prMes_0' + str(gnss_id)
                            # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                            #
                            # week_id = 'prMes_0' + str(gnss_id)
                            # week_id_name = getattr(parsed_data, week_id)
                            #
                            # leapS_id = 'prMes_0' + str(gnss_id)
                            # leapS_id_name = getattr(parsed_data, leapS_id)
                            prMes_id = 'prMes_' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_2 in self.csv_list_2:
                                self.csv_list_2.append(csv_name_2)
                                with open(csv_name_2, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_2, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                        if gnss_name == "GLONASS":
                            print(gnss_name)
                            gnss_sv_id = 'svId_' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_' + str(gnss_id)
                            gnss_sig_id_name = GLONASSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_3 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"
                            # rcvTow_id = 'prMes_0' + str(gnss_id)
                            # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                            #
                            # week_id = 'prMes_0' + str(gnss_id)
                            # week_id_name = getattr(parsed_data, week_id)
                            #
                            # leapS_id = 'prMes_0' + str(gnss_id)
                            # leapS_id_name = getattr(parsed_data, leapS_id)
                            prMes_id = 'prMes_' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_3 in self.csv_list_3:
                                self.csv_list_3.append(csv_name_3)
                                with open(csv_name_3, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_3, 'a+', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                        # if gnss_name == "Galileo":
                        #     print(gnss_name)
                        #     gnss_sv_id = 'svId_0' + str(gnss_id)
                        #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                        #     gnss_sig_id = 'sigId_0' + str(gnss_id)
                        #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                        #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                        #     if not csv_name in csv_list:
                        #         with open(csv_name, mode='w') as gal_info:
                        #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                        #                                   quoting=csv.QUOTE_MINIMAL)
                        #             gal_info.writerow(gnss_name)
                        #         csv_list.append(csv_name)
                        #     else:
                        #         pass

                        if gnss_name == "BeiDou":
                            print(gnss_name)
                            gnss_sv_id = 'svId_' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_' + str(gnss_id)
                            gnss_sig_id_name = BEIDOUSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_4 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"
                            # rcvTow_id = 'prMes_0' + str(gnss_id)
                            # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                            #
                            # week_id = 'prMes_0' + str(gnss_id)
                            # week_id_name = getattr(parsed_data, week_id)
                            #
                            # leapS_id = 'prMes_0' + str(gnss_id)
                            # leapS_id_name = getattr(parsed_data, leapS_id)
                            prMes_id = 'prMes_' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_4 in self.csv_list_4:
                                self.csv_list_4.append(csv_name_4)
                                with open(csv_name_4, 'a', newline='') as file:
                                    writer.writeheader()
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_4, 'a', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                        if gnss_name == "QZSS":
                            print(gnss_name)
                            gnss_sv_id = 'svId_' + str(gnss_id)
                            gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            gnss_sig_id = 'sigId_' + str(gnss_id)
                            gnss_sig_id_name = QZSSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                            csv_name_5 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                gnss_sv_id_name) + ".csv"
                            # rcvTow_id = 'prMes_0' + str(gnss_id)
                            # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                            #
                            # week_id = 'prMes_0' + str(gnss_id)
                            # week_id_name = getattr(parsed_data, week_id)
                            #
                            # leapS_id = 'prMes_0' + str(gnss_id)
                            # leapS_id_name = getattr(parsed_data, leapS_id)
                            prMes_id = 'prMes_' + str(gnss_id)
                            prMes_id_name = getattr(parsed_data, prMes_id)

                            cpMes_id = 'cpMes_' + str(gnss_id)
                            cpMes_id_name = getattr(parsed_data, cpMes_id)

                            doMes_id = 'doMes_' + str(gnss_id)
                            doMes_id_name = getattr(parsed_data, doMes_id)

                            freq_id = 'freqId_' + str(gnss_id)
                            freq_id_name = getattr(parsed_data, freq_id)

                            locktime_id = 'locktime_' + str(gnss_id)
                            locktime_id_name = getattr(parsed_data, locktime_id)

                            cno_id = 'cno_' + str(gnss_id)
                            cno_id_name = getattr(parsed_data, cno_id)

                            prStdev_id = 'prStdev_' + str(gnss_id)
                            prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                            cpStdev_id = 'cpStdev_' + str(gnss_id)
                            cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                            doStdev_id = 'doStdev_' + str(gnss_id)
                            doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                            trkStat_id = 'trkStat_' + str(gnss_id)
                            trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                            print(trkStat_id_name)

                            reserved2_id = 'reserved2_' + str(gnss_id)
                            reserved2_id_name = getattr(parsed_data, reserved2_id)

                            fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                          'freqId', 'locktime', 'cno']
                            if not csv_name_5 in self.csv_list_5:
                                self.csv_list_5.append(csv_name_5)
                                with open(csv_name_5, 'a+', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writeheader()
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            else:
                                with open(csv_name_5, 'a+', newline='') as file:
                                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                                    writer.writerow({
                                        'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                        'leapS': parsed_data.leapS,
                                        'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                        'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                except AttributeError:
                    print("WRONG MESSAGE FORMAT.")

        if self.ubx_2.isChecked():
            if parsed_data.identity == 'NAV-PVT':

                fieldnames = ['iTOW', 'year', 'month', 'day', 'hour', 'min', 'second', 'tAcc', 'nano', 'fixType',
                              'numSV', 'lon', 'lat', 'height', 'hMSL', 'hAcc', 'vAcc', 'velN', 'velE', 'velD',
                              'gSpeed', 'headMot', 'sAcc', 'headAcc', 'pDOP', 'reserved1', 'headVeh', 'magDec',
                              'magAcc']

                csv_name_6 = self.save_folder + "/" + str(parsed_data.identity) + ".csv"

                # file exists
                if not csv_name_6 in self.csv_list_6:
                    self.csv_list_6.append(csv_name_6)
                    self.csv_name_6_open = open(csv_name_6, 'a', newline='')
                    csv_name_6_writer = csv.DictWriter(self.csv_name_6_open, fieldnames=fieldnames)
                    csv_name_6_writer.writeheader()
                    csv_name_6_writer.writerow(
                        {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
                         'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
                         'second': parsed_data.second, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
                         'fixType': parsed_data.fixType, 'numSV': parsed_data.numSV, 'lon': parsed_data.lon,
                         'lat': parsed_data.lat,
                         'height': parsed_data.height,
                         'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
                         'velN': parsed_data.velN,
                         'velE': parsed_data.velE, 'velD': parsed_data.velD,
                         'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
                         'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
                         'reserved1': parsed_data.reserved1,
                         'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
                         })
                else:
                    self.csv_name_6_open = open(csv_name_6, 'a', newline='')
                    csv_name_6_writer = csv.DictWriter(self.csv_name_6_open, fieldnames=fieldnames)
                    csv_name_6_writer.writerow(
                        {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
                         'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
                         'second': parsed_data.second, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
                         'fixType': parsed_data.fixType,
                         'numSV': parsed_data.numSV, 'lon': parsed_data.lon, 'lat': parsed_data.lat,
                         'height': parsed_data.height,
                         'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
                         'velN': parsed_data.velN,
                         'velE': parsed_data.velE, 'velD': parsed_data.velD,
                         'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
                         'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
                         'reserved1': parsed_data.reserved1,
                         'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
                         })
                self.csv_name_6_open.truncate()
                self.csv_name_6_open.close()

                # if not csv_name_6 in self.csv_list_6:
                #     print(self.csv_list_6)
                #     self.csv_list_6.append(csv_name_6)
                #     with open(csv_name_6, 'a', newline='') as file:
                #         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #         writer.writeheader()
                #         writer.writerow(
                #             {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
                #              'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
                #              'second': parsed_data.second,
                #              'valid': parsed_data.valid, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
                #              'fixType': parsed_data.fixType, 'flags': parsed_data.flags, 'flags2': parsed_data.flags2,
                #              'numSV': parsed_data.numSV, 'lon': parsed_data.lon, 'lat': parsed_data.lat,
                #              'height': parsed_data.height,
                #              'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
                #              'velN': parsed_data.velN,
                #              'velE': parsed_data.velE, 'velD': parsed_data.velD,
                #              'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
                #              'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
                #              'reserved1': parsed_data.reserved1,
                #              'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
                #              })
                # else:
                #     self.csv_list_6.append(csv_name_6)
                #     with open(csv_name_6, 'a', newline='') as file:
                #         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #         writer.writerow(
                #             {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
                #              'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
                #              'second': parsed_data.second,
                #              'valid': parsed_data.valid, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
                #              'fixType': parsed_data.fixType, 'flags': parsed_data.flags, 'flags2': parsed_data.flags2,
                #              'numSV': parsed_data.numSV, 'lon': parsed_data.lon, 'lat': parsed_data.lat,
                #              'height': parsed_data.height,
                #              'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
                #              'velN': parsed_data.velN,
                #              'velE': parsed_data.velE, 'velD': parsed_data.velD,
                #              'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
                #              'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
                #              'reserved1': parsed_data.reserved1,
                #              'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
                #              })

        if self.ubx_3.isChecked():
            if parsed_data.identity == "NAV-POSECEF":
                fieldnames = ['iTOW (utc)', 'iTOW', 'ecefX', 'ecefY', 'ecefZ', 'pAcc']

                csv_name_7 = self.save_folder + "/" + str(parsed_data.identity) + ".csv"
                if not csv_name_7 in self.csv_list_7:
                    self.csv_list_7.append(csv_name_7)
                    self.csv_name_7_open = open(csv_name_7, 'a', newline='')
                    csv_name_7_writer = csv.DictWriter(self.csv_name_7_open, fieldnames=fieldnames)
                    csv_name_7_writer.writeheader()
                    csv_name_7_writer.writerow(
                        {'iTOW (utc)': itow2utc(parsed_data.iTOW), 'iTOW': parsed_data.iTOW, 'ecefX': parsed_data.ecefX,
                         'ecefY': parsed_data.ecefY,
                         'ecefZ': parsed_data.ecefZ, 'pAcc': parsed_data.pAcc
                         })
                else:
                    self.csv_name_7_open = open(csv_name_7, 'a', newline='')
                    csv_name_7_writer = csv.DictWriter(self.csv_name_7_open, fieldnames=fieldnames)
                    csv_name_7_writer.writerow(
                        {'iTOW (utc)': itow2utc(parsed_data.iTOW), 'iTOW': parsed_data.iTOW, 'ecefX': parsed_data.ecefX,
                         'ecefY': parsed_data.ecefY,
                         'ecefZ': parsed_data.ecefZ, 'pAcc': parsed_data.pAcc
                         })
        # for msg_type in self.ubx_msg_class:
        #     if msg_type == 'RXM-RAWX':
        #         print('RXM-RAWX')
        #         if parsed_data.identity == 'RXM-RAWX':
        #
        #             try:
        #                 num_message = parsed_data.numMeas
        #
        #                 for gnss_id in range(1, 10, 1):
        #                     gnss_message_id = 'gnssId_0' + str(gnss_id)
        #                     gnss_message_id_number = getattr(parsed_data, gnss_message_id)
        #                     gnss_name = GNSSLIST[gnss_message_id_number]
        #                     if gnss_name == "GPS":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_0' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_0' + str(gnss_id)
        #                         gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_1 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #                         print(csv_name_1)
        #                         # rcvTow_id = 'prMes_0' + str(gnss_id)
        #                         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #                         #
        #                         # week_id = 'prMes_0' + str(gnss_id)
        #                         # week_id_name = getattr(parsed_data, week_id)
        #                         #
        #                         # leapS_id = 'prMes_0' + str(gnss_id)
        #                         # leapS_id_name = getattr(parsed_data, leapS_id)
        #                         prMes_id = 'prMes_0' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_0' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_0' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_0' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_0' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_0' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_0' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_0' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_0' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_0' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_0' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_1 in self.csv_list_1:
        #                             self.csv_list_1.append(csv_name_1)
        #                             with open(csv_name_1, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_1, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #
        #                     if gnss_name == "Galileo":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_0' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_0' + str(gnss_id)
        #                         gnss_sig_id_name = GALILEOSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_2 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #
        #                         prMes_id = 'prMes_0' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_0' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_0' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_0' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_0' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_0' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_0' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_0' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_0' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_0' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_0' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_2 in self.csv_list_2:
        #                             self.csv_list_2.append(csv_name_2)
        #                             with open(csv_name_2, 'a+', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_2, 'a+', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                     # if gnss_name == "Galileo":
        #                     #     print(gnss_name)
        #                     #     gnss_sv_id = 'svId_0' + str(gnss_id)
        #                     #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                     #     gnss_sig_id = 'sigId_0' + str(gnss_id)
        #                     #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
        #                     #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
        #                     #     if not csv_name in csv_list:
        #                     #         with open(csv_name, mode='w') as gal_info:
        #                     #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
        #                     #                                   quoting=csv.QUOTE_MINIMAL)
        #                     #             gal_info.writerow(gnss_name)
        #                     #         csv_list.append(csv_name)
        #                     #     else:
        #                     #         pass
        #
        #                     if gnss_name == "Glonass":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_0' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_0' + str(gnss_id)
        #                         gnss_sig_id_name = GLONASSSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_3 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #                         # rcvTow_id = 'prMes_0' + str(gnss_id)
        #                         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #                         #
        #                         # week_id = 'prMes_0' + str(gnss_id)
        #                         # week_id_name = getattr(parsed_data, week_id)
        #                         #
        #                         # leapS_id = 'prMes_0' + str(gnss_id)
        #                         # leapS_id_name = getattr(parsed_data, leapS_id)
        #                         prMes_id = 'prMes_0' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_0' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_0' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_0' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_0' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_0' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_0' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_0' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_0' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_0' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_0' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_3 in self.csv_list_3:
        #                             self.csv_list_3.append(csv_name_3)
        #                             with open(csv_name_3, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_3, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #
        #                     if gnss_name == "BeiDou":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_0' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_0' + str(gnss_id)
        #                         gnss_sig_id_name = BEIDOUSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_4 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #
        #                         prMes_id = 'prMes_0' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_0' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_0' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_0' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_0' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_0' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_0' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_0' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_0' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_0' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_0' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_4 in self.csv_list_4:
        #                             self.csv_list_4.append(csv_name_4)
        #                             with open(csv_name_4, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_4, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #
        #                     if gnss_name == "Qszz":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_0' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_0' + str(gnss_id)
        #                         gnss_sig_id_name = QZSSSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_5 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #                         # rcvTow_id = 'prMes_0' + str(gnss_id)
        #                         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #                         #
        #                         # week_id = 'prMes_0' + str(gnss_id)
        #                         # week_id_name = getattr(parsed_data, week_id)
        #                         #
        #                         # leapS_id = 'prMes_0' + str(gnss_id)
        #                         # leapS_id_name = getattr(parsed_data, leapS_id)
        #                         prMes_id = 'prMes_0' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_0' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_0' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_0' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_0' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_0' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_0' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_0' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_0' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_0' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_0' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_5 in self.csv_list_5:
        #                             self.csv_list_5.append(csv_name_5)
        #                             with open(csv_name_5, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_5, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #
        #                 for gnss_id in range(10, num_message + 1, 1):
        #                     gnss_message_id = 'gnssId_' + str(gnss_id)
        #                     gnss_message_id_number = getattr(parsed_data, gnss_message_id)
        #                     gnss_name = GNSSLIST[gnss_message_id_number]
        #
        #                     if gnss_name == "GPS":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_' + str(gnss_id)
        #                         gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_1 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #                         # rcvTow_id = 'prMes_0' + str(gnss_id)
        #                         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #                         #
        #                         # week_id = 'prMes_0' + str(gnss_id)
        #                         # week_id_name = getattr(parsed_data, week_id)
        #                         #
        #                         # leapS_id = 'prMes_0' + str(gnss_id)
        #                         # leapS_id_name = getattr(parsed_data, leapS_id)
        #                         prMes_id = 'prMes_' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_1 in self.csv_list_1:
        #                             self.csv_list_1.append(csv_name_1)
        #                             with open(csv_name_1, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_1, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #
        #                     if gnss_name == "Galileo":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_' + str(gnss_id)
        #                         gnss_sig_id_name = GALILEOSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_2 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #                         # rcvTow_id = 'prMes_0' + str(gnss_id)
        #                         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #                         #
        #                         # week_id = 'prMes_0' + str(gnss_id)
        #                         # week_id_name = getattr(parsed_data, week_id)
        #                         #
        #                         # leapS_id = 'prMes_0' + str(gnss_id)
        #                         # leapS_id_name = getattr(parsed_data, leapS_id)
        #                         prMes_id = 'prMes_' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_2 in self.csv_list_2:
        #                             self.csv_list_2.append(csv_name_2)
        #                             with open(csv_name_2, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_2, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #
        #                     if gnss_name == "Glonass":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_' + str(gnss_id)
        #                         gnss_sig_id_name = GLONASSSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_3 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #                         # rcvTow_id = 'prMes_0' + str(gnss_id)
        #                         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #                         #
        #                         # week_id = 'prMes_0' + str(gnss_id)
        #                         # week_id_name = getattr(parsed_data, week_id)
        #                         #
        #                         # leapS_id = 'prMes_0' + str(gnss_id)
        #                         # leapS_id_name = getattr(parsed_data, leapS_id)
        #                         prMes_id = 'prMes_' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_3 in self.csv_list_3:
        #                             self.csv_list_3.append(csv_name_3)
        #                             with open(csv_name_3, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_3, 'a+', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                     # if gnss_name == "Galileo":
        #                     #     print(gnss_name)
        #                     #     gnss_sv_id = 'svId_0' + str(gnss_id)
        #                     #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                     #     gnss_sig_id = 'sigId_0' + str(gnss_id)
        #                     #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
        #                     #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
        #                     #     if not csv_name in csv_list:
        #                     #         with open(csv_name, mode='w') as gal_info:
        #                     #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
        #                     #                                   quoting=csv.QUOTE_MINIMAL)
        #                     #             gal_info.writerow(gnss_name)
        #                     #         csv_list.append(csv_name)
        #                     #     else:
        #                     #         pass
        #
        #                     if gnss_name == "BeiDou":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_' + str(gnss_id)
        #                         gnss_sig_id_name = BEIDOUSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_4 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #                         # rcvTow_id = 'prMes_0' + str(gnss_id)
        #                         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #                         #
        #                         # week_id = 'prMes_0' + str(gnss_id)
        #                         # week_id_name = getattr(parsed_data, week_id)
        #                         #
        #                         # leapS_id = 'prMes_0' + str(gnss_id)
        #                         # leapS_id_name = getattr(parsed_data, leapS_id)
        #                         prMes_id = 'prMes_' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_4 in self.csv_list_4:
        #                             self.csv_list_4.append(csv_name_4)
        #                             with open(csv_name_4, 'a', newline='') as file:
        #                                 writer.writeheader()
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_4, 'a', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #
        #                     if gnss_name == "Qszz":
        #                         print(gnss_name)
        #                         gnss_sv_id = 'svId_' + str(gnss_id)
        #                         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #                         gnss_sig_id = 'sigId_' + str(gnss_id)
        #                         gnss_sig_id_name = QZSSSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #                         csv_name_5 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
        #                             gnss_sv_id_name) + ".csv"
        #                         # rcvTow_id = 'prMes_0' + str(gnss_id)
        #                         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #                         #
        #                         # week_id = 'prMes_0' + str(gnss_id)
        #                         # week_id_name = getattr(parsed_data, week_id)
        #                         #
        #                         # leapS_id = 'prMes_0' + str(gnss_id)
        #                         # leapS_id_name = getattr(parsed_data, leapS_id)
        #                         prMes_id = 'prMes_' + str(gnss_id)
        #                         prMes_id_name = getattr(parsed_data, prMes_id)
        #
        #                         cpMes_id = 'cpMes_' + str(gnss_id)
        #                         cpMes_id_name = getattr(parsed_data, cpMes_id)
        #
        #                         doMes_id = 'doMes_' + str(gnss_id)
        #                         doMes_id_name = getattr(parsed_data, doMes_id)
        #
        #                         freq_id = 'freqId_' + str(gnss_id)
        #                         freq_id_name = getattr(parsed_data, freq_id)
        #
        #                         locktime_id = 'locktime_' + str(gnss_id)
        #                         locktime_id_name = getattr(parsed_data, locktime_id)
        #
        #                         cno_id = 'cno_' + str(gnss_id)
        #                         cno_id_name = getattr(parsed_data, cno_id)
        #
        #                         prStdev_id = 'prStdev_' + str(gnss_id)
        #                         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #
        #                         cpStdev_id = 'cpStdev_' + str(gnss_id)
        #                         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #
        #                         doStdev_id = 'doStdev_' + str(gnss_id)
        #                         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #
        #                         trkStat_id = 'trkStat_' + str(gnss_id)
        #                         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #                         print(trkStat_id_name)
        #
        #                         reserved2_id = 'reserved2_' + str(gnss_id)
        #                         reserved2_id_name = getattr(parsed_data, reserved2_id)
        #
        #                         fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #                                       'freqId', 'locktime', 'cno']
        #                         if not csv_name_5 in self.csv_list_5:
        #                             self.csv_list_5.append(csv_name_5)
        #                             with open(csv_name_5, 'a+', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writeheader()
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #                         else:
        #                             with open(csv_name_5, 'a+', newline='') as file:
        #                                 writer = csv.DictWriter(file, fieldnames=fieldnames)
        #                                 writer.writerow({
        #                                     'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #                                     'leapS': parsed_data.leapS,
        #                                     'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #                                     'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
        #
        #             except AttributeError:
        #                 print("WRONG MESSAGE FORMAT.")
        #     elif msg_type == 'NAV-PVT':
        #         if parsed_data.identity == 'NAV-PVT':
        #
        #             fieldnames = ['iTOW', 'year', 'month', 'day', 'hour', 'min', 'second', 'tAcc', 'nano', 'fixType',
        #                           'numSV', 'lon', 'lat', 'height', 'hMSL', 'hAcc', 'vAcc', 'velN', 'velE', 'velD',
        #                           'gSpeed', 'headMot', 'sAcc', 'headAcc', 'pDOP', 'reserved1', 'headVeh', 'magDec',
        #                           'magAcc']
        #
        #             csv_name_6 = self.save_folder + "/" + str(parsed_data.identity) + ".csv"
        #
        #             # file exists
        #             if not csv_name_6 in self.csv_list_6:
        #                 self.csv_list_6.append(csv_name_6)
        #                 self.csv_name_6_open = open(csv_name_6, 'a', newline='')
        #                 csv_name_6_writer = csv.DictWriter(self.csv_name_6_open, fieldnames=fieldnames)
        #                 csv_name_6_writer.writeheader()
        #                 csv_name_6_writer.writerow(
        #                     {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
        #                      'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
        #                      'second': parsed_data.second, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
        #                      'fixType': parsed_data.fixType, 'numSV': parsed_data.numSV, 'lon': parsed_data.lon,
        #                      'lat': parsed_data.lat,
        #                      'height': parsed_data.height,
        #                      'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
        #                      'velN': parsed_data.velN,
        #                      'velE': parsed_data.velE, 'velD': parsed_data.velD,
        #                      'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
        #                      'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
        #                      'reserved1': parsed_data.reserved1,
        #                      'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
        #                      })
        #             else:
        #                 self.csv_name_6_open = open(csv_name_6, 'a', newline='')
        #                 csv_name_6_writer = csv.DictWriter(self.csv_name_6_open, fieldnames=fieldnames)
        #                 csv_name_6_writer.writerow(
        #                     {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
        #                      'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
        #                      'second': parsed_data.second, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
        #                      'fixType': parsed_data.fixType,
        #                      'numSV': parsed_data.numSV, 'lon': parsed_data.lon, 'lat': parsed_data.lat,
        #                      'height': parsed_data.height,
        #                      'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
        #                      'velN': parsed_data.velN,
        #                      'velE': parsed_data.velE, 'velD': parsed_data.velD,
        #                      'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
        #                      'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
        #                      'reserved1': parsed_data.reserved1,
        #                      'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
        #                      })
        #             self.csv_name_6_open.truncate()
        #             self.csv_name_6_open.close()
        #
        #             # if not csv_name_6 in self.csv_list_6:
        #             #     print(self.csv_list_6)
        #             #     self.csv_list_6.append(csv_name_6)
        #             #     with open(csv_name_6, 'a', newline='') as file:
        #             #         writer = csv.DictWriter(file, fieldnames=fieldnames)
        #             #         writer.writeheader()
        #             #         writer.writerow(
        #             #             {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
        #             #              'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
        #             #              'second': parsed_data.second,
        #             #              'valid': parsed_data.valid, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
        #             #              'fixType': parsed_data.fixType, 'flags': parsed_data.flags, 'flags2': parsed_data.flags2,
        #             #              'numSV': parsed_data.numSV, 'lon': parsed_data.lon, 'lat': parsed_data.lat,
        #             #              'height': parsed_data.height,
        #             #              'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
        #             #              'velN': parsed_data.velN,
        #             #              'velE': parsed_data.velE, 'velD': parsed_data.velD,
        #             #              'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
        #             #              'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
        #             #              'reserved1': parsed_data.reserved1,
        #             #              'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
        #             #              })
        #             # else:
        #             #     self.csv_list_6.append(csv_name_6)
        #             #     with open(csv_name_6, 'a', newline='') as file:
        #             #         writer = csv.DictWriter(file, fieldnames=fieldnames)
        #             #         writer.writerow(
        #             #             {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
        #             #              'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
        #             #              'second': parsed_data.second,
        #             #              'valid': parsed_data.valid, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
        #             #              'fixType': parsed_data.fixType, 'flags': parsed_data.flags, 'flags2': parsed_data.flags2,
        #             #              'numSV': parsed_data.numSV, 'lon': parsed_data.lon, 'lat': parsed_data.lat,
        #             #              'height': parsed_data.height,
        #             #              'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
        #             #              'velN': parsed_data.velN,
        #             #              'velE': parsed_data.velE, 'velD': parsed_data.velD,
        #             #              'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
        #             #              'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
        #             #              'reserved1': parsed_data.reserved1,
        #             #              'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
        #             #              })
        #     elif msg_type == 'RXM-MEASX':
        #         print(" Not ready yet")
        #         # if parsed_data.identity == 'RXM-MEASX':
        #         #     num_sv = parsed_data.numSV
        #         #
        #         #     for gnss_id in range(1, 10, 1):
        #         #         gnss_message_id = 'gnssId_0' + str(gnss_id)
        #         #         gnss_message_id_number = getattr(parsed_data, gnss_message_id)
        #         #         gnss_name = GNSSLIST[gnss_message_id_number]
        #         #         id_msg = '0' + str(gnss_id)
        #         #         if gnss_name == "GPS":
        #         #             print(gnss_name)
        #         #             gnss_sv_id = 'svId_0' + str(gnss_id)
        #         #             gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #         #             # gnss_sig_id = 'sigId_0' + str(gnss_id)
        #         #             # gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
        #         #             csv_name_2 = self.save_folder + "/" + gnss_name + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
        #         #             # rcvTow_id = 'prMes_0' + str(gnss_id)
        #         #             # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #         #             #
        #         #             # week_id = 'prMes_0' + str(gnss_id)
        #         #             # week_id_name = getattr(parsed_data, week_id)
        #         #             #
        #         #             # leapS_id = 'prMes_0' + str(gnss_id)
        #         #             # leapS_id_name = getattr(parsed_data, leapS_id)
        #         #             prMes_id = 'prMes_0' + str(gnss_id)
        #         #             prMes_id_name = getattr(parsed_data, prMes_id)
        #         #
        #         #             cpMes_id = 'cpMes_0' + str(gnss_id)
        #         #             cpMes_id_name = getattr(parsed_data, cpMes_id)
        #         #
        #         #             doMes_id = 'doMes_0' + str(gnss_id)
        #         #             doMes_id_name = getattr(parsed_data, doMes_id)
        #         #
        #         #             freq_id = 'freqId_0' + str(gnss_id)
        #         #             freq_id_name = getattr(parsed_data, freq_id)
        #         #
        #         #             locktime_id = 'locktime_0' + str(gnss_id)
        #         #             locktime_id_name = getattr(parsed_data, locktime_id)
        #         #
        #         #             cno_id = 'cno_0' + str(gnss_id)
        #         #             cno_id_name = getattr(parsed_data, cno_id)
        #         #
        #         #             prStdev_id = 'prStdev_0' + str(gnss_id)
        #         #             prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #         #
        #         #             cpStdev_id = 'cpStdev_0' + str(gnss_id)
        #         #             cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #         #
        #         #             doStdev_id = 'doStdev_0' + str(gnss_id)
        #         #             doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #         #
        #         #             trkStat_id = 'trkStat_0' + str(gnss_id)
        #         #             trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #         #             print(trkStat_id_name)
        #         #
        #         #             reserved2_id = 'reserved2_0' + str(gnss_id)
        #         #             reserved2_id_name = getattr(parsed_data, reserved2_id)
        #         #
        #         #             fieldnames = ['gnssId', 'svId', 'sigId', 'rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #         #                           'freqId',
        #         #                           'locktime', 'cno',
        #         #                           'prStdev', 'cpStdev', 'doStdev', 'trkStat', 'reserved2']
        #         #             if not csv_name_2 in self.csv_list_2:
        #         #                 self.csv_list_2.append(csv_name_2)
        #         #                 with open(csv_name_2, 'a+', newline='') as file:
        #         #                     writer = csv.DictWriter(file, fieldnames=fieldnames)
        #         #                     writer.writeheader()
        #         #                     writer.writerow({
        #         #                         'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
        #         #                         'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week, 'leapS': parsed_data.leapS,
        #         #                         'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #         #                         'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
        #         #                         'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
        #         #                         'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
        #         #                         'reserved2': reserved2_id_name})
        #         #             else:
        #         #                 with open(csv_name_2, 'a+', newline='') as file:
        #         #                     writer = csv.DictWriter(file, fieldnames=fieldnames)
        #         #                     writer.writerow(
        #         #                         {
        #         #                             'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
        #         #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #         #                             'leapS': parsed_data.leapS,
        #         #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #         #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
        #         #                             'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
        #         #                             'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
        #         #                             'reserved2': reserved2_id_name})
        #         #
        #         #         if gnss_name == "Galileo":
        #         #             print(gnss_name)
        #         #             gnss_sv_id = 'svId_0' + str(gnss_id)
        #         #             gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #         #             gnss_sig_id = 'sigId_0' + str(gnss_id)
        #         #             gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
        #         #             csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
        #         #             if not csv_name in csv_list:
        #         #                 with open(csv_name, mode='w') as gal_info:
        #         #                     gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
        #         #                                           quoting=csv.QUOTE_MINIMAL)
        #         #                     gal_info.writerow(gnss_name)
        #         #                 csv_list.append(csv_name)
        #         #             else:
        #         #                 pass
        #         #
        #         #         if gnss_name == "BeiDou":
        #         #             pass
        #         #         else:
        #         #             pass
        #         #
        #         #     for gnss_id in range(10, num_sv + 1, 1):
        #         #         gnss_message_id = 'gnssId_' + str(gnss_id)
        #         #         gnss_message_id_number = getattr(parsed_data, gnss_message_id)
        #         #         gnss_name = GNSSLIST[gnss_message_id_number]
        #         #         id_msg = '0' + str(gnss_id)
        #         #         if gnss_name == "GPS":
        #         #             print(gnss_name)
        #         #             gnss_sv_id = 'svId_' + str(gnss_id)
        #         #             gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #         #             gnss_sig_id = 'sigId_' + str(gnss_id)
        #         #             gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
        #         #             csv_name_2 = self.save_folder + "/" + str(GPSSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(
        #         #                 gnss_sv_id_name) + ".csv"
        #         #
        #         #             # rcvTow_id = 'prMes_' + str(gnss_id)
        #         #             # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
        #         #             #
        #         #             # week_id = 'prMes_' + str(gnss_id)
        #         #             # week_id_name = getattr(parsed_data, week_id)
        #         #             #
        #         #             # leapS_id = 'prMes_' + str(gnss_id)
        #         #             # leapS_id_name = getattr(parsed_data, leapS_id)
        #         #
        #         #             prMes_id = 'prMes_' + str(gnss_id)
        #         #             prMes_id_name = getattr(parsed_data, prMes_id)
        #         #
        #         #             cpMes_id = 'cpMes_' + str(gnss_id)
        #         #             cpMes_id_name = getattr(parsed_data, cpMes_id)
        #         #
        #         #             doMes_id = 'doMes_' + str(gnss_id)
        #         #             doMes_id_name = getattr(parsed_data, doMes_id)
        #         #
        #         #             freq_id = 'freqId_' + str(gnss_id)
        #         #             freq_id_name = getattr(parsed_data, freq_id)
        #         #
        #         #             locktime_id = 'locktime_' + str(gnss_id)
        #         #             locktime_id_name = getattr(parsed_data, locktime_id)
        #         #
        #         #             cno_id = 'cno_' + str(gnss_id)
        #         #             cno_id_name = getattr(parsed_data, cno_id)
        #         #
        #         #             prStdev_id = 'prStdev_' + str(gnss_id)
        #         #             prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
        #         #
        #         #             cpStdev_id = 'cpStdev_' + str(gnss_id)
        #         #             cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
        #         #
        #         #             doStdev_id = 'doStdev_' + str(gnss_id)
        #         #             doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
        #         #
        #         #             trkStat_id = 'trkStat_' + str(gnss_id)
        #         #             trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
        #         #
        #         #             reserved2_id = 'reserved2_' + str(gnss_id)
        #         #             reserved2_id_name = getattr(parsed_data, reserved2_id)
        #         #
        #         #             fieldnames = ['gnssId', 'svId', 'sigId', 'rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
        #         #                           'freqId',
        #         #                           'locktime', 'cno',
        #         #                           'prStdev', 'cpStdev', 'doStdev', 'trkStat', 'reserved2']
        #         #
        #         #             if not csv_name_2 in self.csv_list_2:
        #         #                 self.csv_list_2.append(csv_name_2)
        #         #                 with open(csv_name_2, 'a+', newline='') as file:
        #         #                     writer = csv.DictWriter(file, fieldnames=fieldnames)
        #         #                     writer.writeheader()
        #         #                     writer.writerow(
        #         #                         {
        #         #                             'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
        #         #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #         #                             'leapS': parsed_data.leapS,
        #         #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #         #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
        #         #                             'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
        #         #                             'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
        #         #                             'reserved2': reserved2_id_name})
        #         #             else:
        #         #                 with open(csv_name_2, 'a+', newline='') as file:
        #         #                     writer = csv.DictWriter(file, fieldnames=fieldnames)
        #         #                     writer.writerow(
        #         #                         {
        #         #                             'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
        #         #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
        #         #                             'leapS': parsed_data.leapS,
        #         #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
        #         #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
        #         #                             'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
        #         #                             'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
        #         #                             'reserved2': reserved2_id_name})
        #         #         if gnss_name == "Galileo":
        #         #             print(gnss_name)
        #         #             gnss_sv_id = 'svId_' + str(gnss_id)
        #         #             gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
        #         #             gnss_sig_id = 'sigId_' + str(gnss_id)
        #         #             gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
        #         #             csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
        #         #             if not csv_name in csv_list:
        #         #                 with open(csv_name, mode='w') as gal_info:
        #         #                     gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
        #         #                                           quoting=csv.QUOTE_MINIMAL)
        #         #                     gal_info.writerow(gnss_name)
        #         #                 csv_list.append(csv_name)
        #         #             else:
        #         #                 pass
        #         #
        #         #         if gnss_name == "BeiDou":
        #         #             pass
        #         #         else:
        #         #             pass
        #     elif msg_type == "NAV-POSECEF":
        #         if parsed_data.identity == "NAV-POSECEF":
        #             fieldnames = ['iTOW', 'ecefX', 'ecefY', 'ecefZ', 'pAcc']
        #
        #             csv_name_7 = self.save_folder + "/" + str(parsed_data.identity) + ".csv"
        #             if not csv_name_7 in self.csv_list_7:
        #                 self.csv_list_7.append(csv_name_7)
        #                 self.csv_name_7_open = open(csv_name_7, 'a', newline='')
        #                 csv_name_7_writer = csv.DictWriter(self.csv_name_7_open, fieldnames=fieldnames)
        #                 csv_name_7_writer.writeheader()
        #                 csv_name_7_writer.writerow(
        #                     {'iTOW': parsed_data.iTOW, 'ecefX': parsed_data.ecefX, 'ecefY': parsed_data.ecefY,
        #                      'ecefZ': parsed_data.ecefZ, 'pAcc': parsed_data.pAcc
        #                      })
        #             else:
        #                 self.csv_name_7_open = open(csv_name_7, 'a', newline='')
        #                 csv_name_7_writer = csv.DictWriter(self.csv_name_7_open, fieldnames=fieldnames)
        #                 csv_name_7_writer.writerow(
        #                     {'iTOW': parsed_data.iTOW, 'ecefX': parsed_data.ecefX, 'ecefY': parsed_data.ecefY,
        #                      'ecefZ': parsed_data.ecefZ, 'pAcc': parsed_data.pAcc
        #                      })
        if self.ubx_4.isChecked():
            try:
                if parsed_data.identity == 'RXM-RAWX':
                    print(parsed_data.identity)
                    print(parsed_data.msg_cls)
                    try:
                        num_message = parsed_data.numMeas
                        # if num_message == 0:
                        #     print(parsed_data.identity)
                        #     print(parsed_data.msg_cls)
                        # else:
                        for gnss_id in range(1, 10, 1):
                            gnss_message_id = 'gnssId_0' + str(gnss_id)
                            gnss_message_id_number = getattr(parsed_data, gnss_message_id)
                            gnss_name = GNSSLIST[gnss_message_id_number]
                            id_msg = '0' + str(gnss_id)
                            if gnss_name == "GPS":
                                print(gnss_name)
                                gnss_sv_id = 'svId_0' + str(gnss_id)
                                gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                gnss_sig_id = 'sigId_0' + str(gnss_id)
                                gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                csv_name_1 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                    gnss_sv_id_name) + ".csv"
                                print(csv_name_1)
                                # rcvTow_id = 'prMes_0' + str(gnss_id)
                                # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                #
                                # week_id = 'prMes_0' + str(gnss_id)
                                # week_id_name = getattr(parsed_data, week_id)
                                #
                                # leapS_id = 'prMes_0' + str(gnss_id)
                                # leapS_id_name = getattr(parsed_data, leapS_id)
                                prMes_id = 'prMes_0' + str(gnss_id)
                                prMes_id_name = getattr(parsed_data, prMes_id)

                                cpMes_id = 'cpMes_0' + str(gnss_id)
                                cpMes_id_name = getattr(parsed_data, cpMes_id)

                                doMes_id = 'doMes_0' + str(gnss_id)
                                doMes_id_name = getattr(parsed_data, doMes_id)

                                freq_id = 'freqId_0' + str(gnss_id)
                                freq_id_name = getattr(parsed_data, freq_id)

                                locktime_id = 'locktime_0' + str(gnss_id)
                                locktime_id_name = getattr(parsed_data, locktime_id)

                                cno_id = 'cno_0' + str(gnss_id)
                                cno_id_name = getattr(parsed_data, cno_id)

                                prStdev_id = 'prStdev_0' + str(gnss_id)
                                prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                                cpStdev_id = 'cpStdev_0' + str(gnss_id)
                                cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                                doStdev_id = 'doStdev_0' + str(gnss_id)
                                doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                                trkStat_id = 'trkStat_0' + str(gnss_id)
                                trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                                print(trkStat_id_name)

                                reserved2_id = 'reserved2_0' + str(gnss_id)
                                reserved2_id_name = getattr(parsed_data, reserved2_id)

                                fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                              'freqId', 'locktime', 'cno']
                                if not csv_name_1 in self.csv_list_1:
                                    self.csv_list_1.append(csv_name_1)
                                    with open(csv_name_1, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writeheader()
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                                else:
                                    with open(csv_name_1, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                            if gnss_name == "Galileo":
                                print(gnss_name)
                                gnss_sv_id = 'svId_0' + str(gnss_id)
                                gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                gnss_sig_id = 'sigId_0' + str(gnss_id)
                                gnss_sig_id_name = GALILEOSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                csv_name_2 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                    gnss_sv_id_name) + ".csv"

                                # rcvTow_id = 'prMes_0' + str(gnss_id)
                                # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                #
                                # week_id = 'prMes_0' + str(gnss_id)
                                # week_id_name = getattr(parsed_data, week_id)
                                #
                                # leapS_id = 'prMes_0' + str(gnss_id)
                                # leapS_id_name = getattr(parsed_data, leapS_id)
                                prMes_id = 'prMes_0' + str(gnss_id)
                                prMes_id_name = getattr(parsed_data, prMes_id)

                                cpMes_id = 'cpMes_0' + str(gnss_id)
                                cpMes_id_name = getattr(parsed_data, cpMes_id)

                                doMes_id = 'doMes_0' + str(gnss_id)
                                doMes_id_name = getattr(parsed_data, doMes_id)

                                freq_id = 'freqId_0' + str(gnss_id)
                                freq_id_name = getattr(parsed_data, freq_id)

                                locktime_id = 'locktime_0' + str(gnss_id)
                                locktime_id_name = getattr(parsed_data, locktime_id)

                                cno_id = 'cno_0' + str(gnss_id)
                                cno_id_name = getattr(parsed_data, cno_id)

                                prStdev_id = 'prStdev_0' + str(gnss_id)
                                prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                                cpStdev_id = 'cpStdev_0' + str(gnss_id)
                                cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                                doStdev_id = 'doStdev_0' + str(gnss_id)
                                doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                                trkStat_id = 'trkStat_0' + str(gnss_id)
                                trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                                print(trkStat_id_name)

                                reserved2_id = 'reserved2_0' + str(gnss_id)
                                reserved2_id_name = getattr(parsed_data, reserved2_id)

                                fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                              'freqId', 'locktime', 'cno']
                                if not csv_name_2 in self.csv_list_2:
                                    self.csv_list_2.append(csv_name_2)
                                    with open(csv_name_2, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writeheader()
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                                else:
                                    with open(csv_name_2, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                            # if gnss_name == "Galileo":
                            #     print(gnss_name)
                            #     gnss_sv_id = 'svId_0' + str(gnss_id)
                            #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                            #     gnss_sig_id = 'sigId_0' + str(gnss_id)
                            #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                            #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                            #     if not csv_name in csv_list:
                            #         with open(csv_name, mode='w') as gal_info:
                            #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                            #                                   quoting=csv.QUOTE_MINIMAL)
                            #             gal_info.writerow(gnss_name)
                            #         csv_list.append(csv_name)
                            #     else:
                            #         pass
                            if gnss_name == "GLONASS":
                                print(gnss_name)
                                gnss_sv_id = 'svId_0' + str(gnss_id)
                                gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                gnss_sig_id = 'sigId_0' + str(gnss_id)
                                gnss_sig_id_name = GLONASSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                csv_name_3 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                    gnss_sv_id_name) + ".csv"
                                # rcvTow_id = 'prMes_0' + str(gnss_id)
                                # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                #
                                # week_id = 'prMes_0' + str(gnss_id)
                                # week_id_name = getattr(parsed_data, week_id)
                                #
                                # leapS_id = 'prMes_0' + str(gnss_id)
                                # leapS_id_name = getattr(parsed_data, leapS_id)
                                prMes_id = 'prMes_0' + str(gnss_id)
                                prMes_id_name = getattr(parsed_data, prMes_id)

                                cpMes_id = 'cpMes_0' + str(gnss_id)
                                cpMes_id_name = getattr(parsed_data, cpMes_id)

                                doMes_id = 'doMes_0' + str(gnss_id)
                                doMes_id_name = getattr(parsed_data, doMes_id)

                                freq_id = 'freqId_0' + str(gnss_id)
                                freq_id_name = getattr(parsed_data, freq_id)

                                locktime_id = 'locktime_0' + str(gnss_id)
                                locktime_id_name = getattr(parsed_data, locktime_id)

                                cno_id = 'cno_0' + str(gnss_id)
                                cno_id_name = getattr(parsed_data, cno_id)

                                prStdev_id = 'prStdev_0' + str(gnss_id)
                                prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                                cpStdev_id = 'cpStdev_0' + str(gnss_id)
                                cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                                doStdev_id = 'doStdev_0' + str(gnss_id)
                                doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                                trkStat_id = 'trkStat_0' + str(gnss_id)
                                trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                                print(trkStat_id_name)

                                reserved2_id = 'reserved2_0' + str(gnss_id)
                                reserved2_id_name = getattr(parsed_data, reserved2_id)

                                fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                              'freqId', 'locktime', 'cno']
                                if not csv_name_3 in self.csv_list_3:
                                    self.csv_list_3.append(csv_name_3)
                                    with open(csv_name_3, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writeheader()
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                                else:
                                    with open(csv_name_3, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                            if gnss_name == "BeiDou":
                                print(gnss_name)
                                gnss_sv_id = 'svId_0' + str(gnss_id)
                                gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                gnss_sig_id = 'sigId_0' + str(gnss_id)
                                gnss_sig_id_name = BEIDOUSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                csv_name_4 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                    gnss_sv_id_name) + ".csv"
                                # rcvTow_id = 'prMes_0' + str(gnss_id)
                                # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                #
                                # week_id = 'prMes_0' + str(gnss_id)
                                # week_id_name = getattr(parsed_data, week_id)
                                #
                                # leapS_id = 'prMes_0' + str(gnss_id)
                                # leapS_id_name = getattr(parsed_data, leapS_id)
                                prMes_id = 'prMes_0' + str(gnss_id)
                                prMes_id_name = getattr(parsed_data, prMes_id)

                                cpMes_id = 'cpMes_0' + str(gnss_id)
                                cpMes_id_name = getattr(parsed_data, cpMes_id)

                                doMes_id = 'doMes_0' + str(gnss_id)
                                doMes_id_name = getattr(parsed_data, doMes_id)

                                freq_id = 'freqId_0' + str(gnss_id)
                                freq_id_name = getattr(parsed_data, freq_id)

                                locktime_id = 'locktime_0' + str(gnss_id)
                                locktime_id_name = getattr(parsed_data, locktime_id)

                                cno_id = 'cno_0' + str(gnss_id)
                                cno_id_name = getattr(parsed_data, cno_id)

                                prStdev_id = 'prStdev_0' + str(gnss_id)
                                prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                                cpStdev_id = 'cpStdev_0' + str(gnss_id)
                                cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                                doStdev_id = 'doStdev_0' + str(gnss_id)
                                doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                                trkStat_id = 'trkStat_0' + str(gnss_id)
                                trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                                print(trkStat_id_name)

                                reserved2_id = 'reserved2_0' + str(gnss_id)
                                reserved2_id_name = getattr(parsed_data, reserved2_id)

                                fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                              'freqId', 'locktime', 'cno']
                                if not csv_name_4 in self.csv_list_4:
                                    self.csv_list_4.append(csv_name_4)
                                    with open(csv_name_4, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writeheader()
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                                else:
                                    with open(csv_name_4, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                            if gnss_name == "QZSS":
                                print(gnss_name)
                                gnss_sv_id = 'svId_0' + str(gnss_id)
                                gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                gnss_sig_id = 'sigId_0' + str(gnss_id)
                                gnss_sig_id_name = QZSSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                csv_name_5 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                    gnss_sv_id_name) + ".csv"
                                # rcvTow_id = 'prMes_0' + str(gnss_id)
                                # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                #
                                # week_id = 'prMes_0' + str(gnss_id)
                                # week_id_name = getattr(parsed_data, week_id)
                                #
                                # leapS_id = 'prMes_0' + str(gnss_id)
                                # leapS_id_name = getattr(parsed_data, leapS_id)
                                prMes_id = 'prMes_0' + str(gnss_id)
                                prMes_id_name = getattr(parsed_data, prMes_id)

                                cpMes_id = 'cpMes_0' + str(gnss_id)
                                cpMes_id_name = getattr(parsed_data, cpMes_id)

                                doMes_id = 'doMes_0' + str(gnss_id)
                                doMes_id_name = getattr(parsed_data, doMes_id)

                                freq_id = 'freqId_0' + str(gnss_id)
                                freq_id_name = getattr(parsed_data, freq_id)

                                locktime_id = 'locktime_0' + str(gnss_id)
                                locktime_id_name = getattr(parsed_data, locktime_id)

                                cno_id = 'cno_0' + str(gnss_id)
                                cno_id_name = getattr(parsed_data, cno_id)

                                prStdev_id = 'prStdev_0' + str(gnss_id)
                                prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)

                                cpStdev_id = 'cpStdev_0' + str(gnss_id)
                                cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)

                                doStdev_id = 'doStdev_0' + str(gnss_id)
                                doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)

                                trkStat_id = 'trkStat_0' + str(gnss_id)
                                trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                                print(trkStat_id_name)

                                reserved2_id = 'reserved2_0' + str(gnss_id)
                                reserved2_id_name = getattr(parsed_data, reserved2_id)

                                fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                              'freqId', 'locktime', 'cno']
                                if not csv_name_5 in self.csv_list_5:
                                    self.csv_list_5.append(csv_name_5)
                                    print(csv_name_5)
                                    print(self.csv_list_5)
                                    with open(csv_name_5, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writeheader()
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                                else:
                                    with open(csv_name_5, 'a+', newline='') as file:
                                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                                        writer.writerow({
                                            'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                            'leapS': parsed_data.leapS,
                                            'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                            'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})

                        for gnss_id in range(10, num_message + 1, 1):
                            gnss_message_id = 'gnssId_' + str(gnss_id)
                            gnss_message_id_number = getattr(parsed_data, gnss_message_id)
                            try:
                                gnss_name = GNSSLIST[gnss_message_id_number]

                                id_msg = '0' + str(gnss_id)
                                #     if gnss_name == "GPS":
                                #         print(gnss_name)
                                #         gnss_sv_id = 'svId_' + str(gnss_id)
                                #         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                #         gnss_sig_id = 'sigId_' + str(gnss_id)
                                #         gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                                #         csv_name_1 = str(GPSSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                                #
                                #         # rcvTow_id = 'prMes_' + str(gnss_id)
                                #         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                #         #
                                #         # week_id = 'prMes_' + str(gnss_id)
                                #         # week_id_name = getattr(parsed_data, week_id)
                                #         #
                                #         # leapS_id = 'prMes_' + str(gnss_id)
                                #         # leapS_id_name = getattr(parsed_data, leapS_id)
                                #
                                #         prMes_id = 'prMes_' + str(gnss_id)
                                #         prMes_id_name = getattr(parsed_data, prMes_id)
                                #
                                #         cpMes_id = 'cpMes_' + str(gnss_id)
                                #         cpMes_id_name = getattr(parsed_data, cpMes_id)
                                #
                                #         doMes_id = 'doMes_' + str(gnss_id)
                                #         doMes_id_name = getattr(parsed_data, doMes_id)
                                #
                                #         freq_id = 'freqId_' + str(gnss_id)
                                #         freq_id_name = getattr(parsed_data, freq_id)
                                #
                                #         locktime_id = 'locktime_' + str(gnss_id)
                                #         locktime_id_name = getattr(parsed_data, locktime_id)
                                #
                                #         cno_id = 'cno_' + str(gnss_id)
                                #         cno_id_name = getattr(parsed_data, cno_id)
                                #
                                #         prStdev_id = 'prStdev_' + str(gnss_id)
                                #         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                                #
                                #         cpStdev_id = 'cpStdev_' + str(gnss_id)
                                #         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                                #
                                #         doStdev_id = 'doStdev_' + str(gnss_id)
                                #         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                                #
                                #         trkStat_id = 'trkStat_' + str(gnss_id)
                                #         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                                #
                                #         reserved2_id = 'reserved2_' + str(gnss_id)
                                #         reserved2_id_name = getattr(parsed_data, reserved2_id)
                                #
                                #         fieldnames = ['gnssId', 'svId', 'sigId', 'rcvTow', 'week', 'leapS', 'prMes', 'cpMes',
                                #                       'doMes',
                                #                       'freqId',
                                #                       'locktime', 'cno',
                                #                       'prStdev', 'cpStdev', 'doStdev', 'trkStat', 'reserved2']
                                #
                                #         if not csv_name_1 in self.csv_list_1:
                                #             self.csv_list_1.append(csv_name_1)
                                #             with open(csv_name_1, 'a+', newline='') as file:
                                #                 writer = csv.DictWriter(file, fieldnames=fieldnames)
                                #                 writer.writeheader()
                                #                 writer.writerow(
                                #                     {
                                #                         'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
                                #                         'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                #                         'leapS': parsed_data.leapS,
                                #                         'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                #                         'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
                                #                         'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
                                #                         'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
                                #                         'reserved2': reserved2_id_name})
                                #         else:
                                #             with open(csv_name_1, 'a+', newline='') as file:
                                #                 writer = csv.DictWriter(file, fieldnames=fieldnames)
                                #                 writer.writerow(
                                #                     {
                                #                         'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
                                #                         'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                #                         'leapS': parsed_data.leapS,
                                #                         'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                                #                         'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
                                #                         'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
                                #                         'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
                                #                         'reserved2': reserved2_id_name})
                                #     if gnss_name == "Galileo":
                                #         print(gnss_name)
                                #         gnss_sv_id = 'svId_' + str(gnss_id)
                                #         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                #         gnss_sig_id = 'sigId_' + str(gnss_id)
                                #         gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                                #         csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                                #         if not csv_name in csv_list:
                                #             with open(csv_name, mode='w') as gal_info:
                                #                 gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                                #                                       quoting=csv.QUOTE_MINIMAL)
                                #                 gal_info.writerow(gnss_name)
                                #             csv_list.append(csv_name)
                                #         else:
                                #             pass
                                #
                                #     if gnss_name == "BeiDou":
                                #         pass
                                #     else:
                                #         pass
                                # # for gnssId in range(1, num_message + 1, 1):
                                # #     gnss_message_id = 'gnssId_' + str(gnssId)
                                # #     try:
                                # #         gnss_message_id_number = getattr(parsed_data, gnss_message_id)
                                # #
                                # #         gnss_name = GNSSLIST[gnss_message_id_number]
                                # #         id_msg = '0' + str(gnssId)
                                # #
                                # #         if gnss_name == "Galileo":
                                # #             print(gnss_name)
                                # #             # for sv_id_gal in range(1, 35 + 1, 1):
                                # #             #     gnss_sv_id = 'svId_0' + str(sv_id_gal)
                                # #             #     print(gnss_sv_id)
                                # #             #     list_gnss_sv_id.append(gnss_sv_id)
                                # #             #     if getattr(parsed_data, gnss_sv_id):
                                # #             #         print(getattr(parsed_data, gnss_sv_id))
                                # #
                                # #         elif gnss_name == "GPS":
                                # #             print(gnss_name)
                                # #             # for sv_id in range(1, 10, 1):
                                # #             #     gnss_sv_id = 'svId_0' + str(sv_id)
                                # #             #     print(gnss_sv_id)
                                # #             #     list_gnss_sv_id.append(gnss_sv_id)
                                # #             #     if getattr(parsed_data, gnss_sv_id):
                                # #             #         print(getattr(parsed_data, gnss_sv_id))
                                # #
                                # #             for sv_id in range(10, 24, 1):
                                # #                 gnss_sv_id = 'svId_' + str(sv_id)
                                # #                 print(gnss_sv_id)
                                # #                 # list_gnss_sv_id.append(gnss_sv_id)
                                # #                 # if getattr(parsed_data, gnss_sv_id):
                                # #                 #     print(getattr(parsed_data, gnss_sv_id))
                                # #
                                # #
                                # #         elif gnss_name == "BeiDou":
                                # #             pass
                                # #         else:
                                # #             pass
                                # #     except:
                                # #         pass

                                if gnss_name == "GPS":
                                    print(gnss_name)
                                    gnss_sv_id = 'svId_' + str(gnss_id)
                                    gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                    gnss_sig_id = 'sigId_' + str(gnss_id)
                                    try:
                                        gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                        csv_name_1 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                            gnss_sv_id_name) + ".csv"
                                        # rcvTow_id = 'prMes_0' + str(gnss_id)
                                        # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                        #
                                        # week_id = 'prMes_0' + str(gnss_id)
                                        # week_id_name = getattr(parsed_data, week_id)
                                        #
                                        # leapS_id = 'prMes_0' + str(gnss_id)
                                        # leapS_id_name = getattr(parsed_data, leapS_id)
                                        prMes_id = 'prMes_' + str(gnss_id)
                                        prMes_id_name = getattr(parsed_data, prMes_id)

                                        cpMes_id = 'cpMes_' + str(gnss_id)
                                        cpMes_id_name = getattr(parsed_data, cpMes_id)

                                        doMes_id = 'doMes_' + str(gnss_id)
                                        doMes_id_name = getattr(parsed_data, doMes_id)

                                        freq_id = 'freqId_' + str(gnss_id)
                                        freq_id_name = getattr(parsed_data, freq_id)

                                        locktime_id = 'locktime_' + str(gnss_id)
                                        locktime_id_name = getattr(parsed_data, locktime_id)

                                        cno_id = 'cno_' + str(gnss_id)
                                        cno_id_name = getattr(parsed_data, cno_id)

                                        prStdev_id = 'prStdev_' + str(gnss_id)
                                        prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id),
                                                                                ubt.U1)

                                        cpStdev_id = 'cpStdev_' + str(gnss_id)
                                        cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id),
                                                                                ubt.U1)

                                        doStdev_id = 'doStdev_' + str(gnss_id)
                                        doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id),
                                                                                ubt.U1)

                                        trkStat_id = 'trkStat_' + str(gnss_id)
                                        trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id),
                                                                                ubt.U1)
                                        print(trkStat_id_name)

                                        reserved2_id = 'reserved2_' + str(gnss_id)
                                        reserved2_id_name = getattr(parsed_data, reserved2_id)

                                        fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                                      'freqId', 'locktime', 'cno']
                                        if not csv_name_1 in self.csv_list_1:
                                            self.csv_list_1.append(csv_name_1)
                                            with open(csv_name_1, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writeheader()
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                        else:
                                            with open(csv_name_1, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                    except KeyError as err:
                                        print(err, getattr(parsed_data, gnss_sig_id))

                                if gnss_name == "Galileo":
                                    print(gnss_name)
                                    gnss_sv_id = 'svId_' + str(gnss_id)
                                    gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                    gnss_sig_id = 'sigId_' + str(gnss_id)
                                    try:
                                        gnss_sig_id_name = GALILEOSIGLIST[getattr(parsed_data, gnss_sig_id)]

                                        csv_name_2 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                            gnss_sv_id_name) + ".csv"
                                        # rcvTow_id = 'prMes_0' + str(gnss_id)
                                        # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                        #
                                        # week_id = 'prMes_0' + str(gnss_id)
                                        # week_id_name = getattr(parsed_data, week_id)
                                        #
                                        # leapS_id = 'prMes_0' + str(gnss_id)
                                        # leapS_id_name = getattr(parsed_data, leapS_id)
                                        prMes_id = 'prMes_' + str(gnss_id)
                                        prMes_id_name = getattr(parsed_data, prMes_id)

                                        cpMes_id = 'cpMes_' + str(gnss_id)
                                        cpMes_id_name = getattr(parsed_data, cpMes_id)

                                        doMes_id = 'doMes_' + str(gnss_id)
                                        doMes_id_name = getattr(parsed_data, doMes_id)

                                        freq_id = 'freqId_' + str(gnss_id)
                                        freq_id_name = getattr(parsed_data, freq_id)

                                        locktime_id = 'locktime_' + str(gnss_id)
                                        locktime_id_name = getattr(parsed_data, locktime_id)

                                        cno_id = 'cno_' + str(gnss_id)
                                        cno_id_name = getattr(parsed_data, cno_id)

                                        prStdev_id = 'prStdev_' + str(gnss_id)
                                        prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id),
                                                                                ubt.U1)

                                        cpStdev_id = 'cpStdev_' + str(gnss_id)
                                        cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id),
                                                                                ubt.U1)

                                        doStdev_id = 'doStdev_' + str(gnss_id)
                                        doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id),
                                                                                ubt.U1)

                                        trkStat_id = 'trkStat_' + str(gnss_id)
                                        trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id),
                                                                                ubt.U1)
                                        print(trkStat_id_name)

                                        reserved2_id = 'reserved2_' + str(gnss_id)
                                        reserved2_id_name = getattr(parsed_data, reserved2_id)

                                        fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                                      'freqId', 'locktime', 'cno']
                                        if not csv_name_2 in self.csv_list_2:
                                            self.csv_list_2.append(csv_name_2)
                                            with open(csv_name_2, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writeheader()
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                        else:
                                            with open(csv_name_2, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                    except KeyError as err:
                                        print(err, getattr(parsed_data, gnss_sig_id))
                                    # if gnss_name == "Galileo":
                                    #     print(gnss_name)
                                    #     gnss_sv_id = 'svId_0' + str(gnss_id)
                                    #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                    #     gnss_sig_id = 'sigId_0' + str(gnss_id)
                                    #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                                    #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                                    #     if not csv_name in csv_list:
                                    #         with open(csv_name, mode='w') as gal_info:
                                    #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                                    #                                   quoting=csv.QUOTE_MINIMAL)
                                    #             gal_info.writerow(gnss_name)
                                    #         csv_list.append(csv_name)
                                    #     else:
                                    #         pass

                                if gnss_name == "GLONASS":
                                    print(gnss_name)
                                    gnss_sv_id = 'svId_' + str(gnss_id)
                                    gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                    gnss_sig_id = 'sigId_' + str(gnss_id)
                                    try:
                                        gnss_sig_id_name = GLONASSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                        csv_name_3 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                            gnss_sv_id_name) + ".csv"
                                        # rcvTow_id = 'prMes_0' + str(gnss_id)
                                        # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                        #
                                        # week_id = 'prMes_0' + str(gnss_id)
                                        # week_id_name = getattr(parsed_data, week_id)
                                        #
                                        # leapS_id = 'prMes_0' + str(gnss_id)
                                        # leapS_id_name = getattr(parsed_data, leapS_id)
                                        prMes_id = 'prMes_' + str(gnss_id)
                                        prMes_id_name = getattr(parsed_data, prMes_id)

                                        cpMes_id = 'cpMes_' + str(gnss_id)
                                        cpMes_id_name = getattr(parsed_data, cpMes_id)

                                        doMes_id = 'doMes_' + str(gnss_id)
                                        doMes_id_name = getattr(parsed_data, doMes_id)

                                        freq_id = 'freqId_' + str(gnss_id)
                                        freq_id_name = getattr(parsed_data, freq_id)

                                        locktime_id = 'locktime_' + str(gnss_id)
                                        locktime_id_name = getattr(parsed_data, locktime_id)

                                        cno_id = 'cno_' + str(gnss_id)
                                        cno_id_name = getattr(parsed_data, cno_id)

                                        prStdev_id = 'prStdev_' + str(gnss_id)
                                        prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id),
                                                                                ubt.U1)

                                        cpStdev_id = 'cpStdev_' + str(gnss_id)
                                        cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id),
                                                                                ubt.U1)

                                        doStdev_id = 'doStdev_' + str(gnss_id)
                                        doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id),
                                                                                ubt.U1)

                                        trkStat_id = 'trkStat_' + str(gnss_id)
                                        trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id),
                                                                                ubt.U1)
                                        print(trkStat_id_name)

                                        reserved2_id = 'reserved2_' + str(gnss_id)
                                        reserved2_id_name = getattr(parsed_data, reserved2_id)

                                        fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                                      'freqId', 'locktime', 'cno']
                                        if not csv_name_3 in self.csv_list_3:
                                            self.csv_list_3.append(csv_name_3)
                                            with open(csv_name_3, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writeheader()
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                        else:
                                            with open(csv_name_3, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                    except KeyError as err:
                                        print(err, getattr(parsed_data, gnss_sig_id))
                                # if gnss_name == "Galileo":
                                #     print(gnss_name)
                                #     gnss_sv_id = 'svId_0' + str(gnss_id)
                                #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                #     gnss_sig_id = 'sigId_0' + str(gnss_id)
                                #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                                #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                                #     if not csv_name in csv_list:
                                #         with open(csv_name, mode='w') as gal_info:
                                #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                                #                                   quoting=csv.QUOTE_MINIMAL)
                                #             gal_info.writerow(gnss_name)
                                #         csv_list.append(csv_name)
                                #     else:
                                #         pass

                                if gnss_name == "BeiDou":
                                    print(gnss_name)
                                    gnss_sv_id = 'svId_' + str(gnss_id)
                                    gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                    gnss_sig_id = 'sigId_' + str(gnss_id)
                                    try:
                                        gnss_sig_id_name = BEIDOUSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                        csv_name_4 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                            gnss_sv_id_name) + ".csv"
                                        # rcvTow_id = 'prMes_0' + str(gnss_id)
                                        # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                        #
                                        # week_id = 'prMes_0' + str(gnss_id)
                                        # week_id_name = getattr(parsed_data, week_id)
                                        #
                                        # leapS_id = 'prMes_0' + str(gnss_id)
                                        # leapS_id_name = getattr(parsed_data, leapS_id)
                                        prMes_id = 'prMes_' + str(gnss_id)
                                        prMes_id_name = getattr(parsed_data, prMes_id)

                                        cpMes_id = 'cpMes_' + str(gnss_id)
                                        cpMes_id_name = getattr(parsed_data, cpMes_id)

                                        doMes_id = 'doMes_' + str(gnss_id)
                                        doMes_id_name = getattr(parsed_data, doMes_id)

                                        freq_id = 'freqId_' + str(gnss_id)
                                        freq_id_name = getattr(parsed_data, freq_id)

                                        locktime_id = 'locktime_' + str(gnss_id)
                                        locktime_id_name = getattr(parsed_data, locktime_id)

                                        cno_id = 'cno_' + str(gnss_id)
                                        cno_id_name = getattr(parsed_data, cno_id)

                                        prStdev_id = 'prStdev_' + str(gnss_id)
                                        prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id),
                                                                                ubt.U1)

                                        cpStdev_id = 'cpStdev_' + str(gnss_id)
                                        cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id),
                                                                                ubt.U1)

                                        doStdev_id = 'doStdev_' + str(gnss_id)
                                        doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id),
                                                                                ubt.U1)

                                        trkStat_id = 'trkStat_' + str(gnss_id)
                                        trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id),
                                                                                ubt.U1)
                                        print(trkStat_id_name)

                                        reserved2_id = 'reserved2_' + str(gnss_id)
                                        reserved2_id_name = getattr(parsed_data, reserved2_id)

                                        fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                                      'freqId', 'locktime', 'cno']
                                        if not csv_name_4 in self.csv_list_4:
                                            self.csv_list_4.append(csv_name_4)
                                            with open(csv_name_4, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writeheader()
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                        else:
                                            with open(csv_name_4, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                    except KeyError as err:
                                        print(err, getattr(parsed_data, gnss_sig_id))

                                if gnss_name == "QZSS":
                                    print(gnss_name)
                                    gnss_sv_id = 'svId_' + str(gnss_id)
                                    gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                                    gnss_sig_id = 'sigId_' + str(gnss_id)
                                    try:
                                        gnss_sig_id_name = QZSSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                                        csv_name_5 = self.save_folder + "/" + str(gnss_sig_id_name) + " Sv_Id " + str(
                                            gnss_sv_id_name) + ".csv"
                                        # rcvTow_id = 'prMes_0' + str(gnss_id)
                                        # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                                        #
                                        # week_id = 'prMes_0' + str(gnss_id)
                                        # week_id_name = getattr(parsed_data, week_id)
                                        #
                                        # leapS_id = 'prMes_0' + str(gnss_id)
                                        # leapS_id_name = getattr(parsed_data, leapS_id)
                                        prMes_id = 'prMes_' + str(gnss_id)
                                        prMes_id_name = getattr(parsed_data, prMes_id)

                                        cpMes_id = 'cpMes_' + str(gnss_id)
                                        cpMes_id_name = getattr(parsed_data, cpMes_id)

                                        doMes_id = 'doMes_' + str(gnss_id)
                                        doMes_id_name = getattr(parsed_data, doMes_id)

                                        freq_id = 'freqId_' + str(gnss_id)
                                        freq_id_name = getattr(parsed_data, freq_id)

                                        locktime_id = 'locktime_' + str(gnss_id)
                                        locktime_id_name = getattr(parsed_data, locktime_id)

                                        cno_id = 'cno_' + str(gnss_id)
                                        cno_id_name = getattr(parsed_data, cno_id)

                                        prStdev_id = 'prStdev_' + str(gnss_id)
                                        prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id),
                                                                                ubt.U1)

                                        cpStdev_id = 'cpStdev_' + str(gnss_id)
                                        cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id),
                                                                                ubt.U1)

                                        doStdev_id = 'doStdev_' + str(gnss_id)
                                        doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id),
                                                                                ubt.U1)

                                        trkStat_id = 'trkStat_' + str(gnss_id)
                                        trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id),
                                                                                ubt.U1)
                                        print(trkStat_id_name)

                                        reserved2_id = 'reserved2_' + str(gnss_id)
                                        reserved2_id_name = getattr(parsed_data, reserved2_id)

                                        fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                                                      'freqId', 'locktime', 'cno']
                                        if not csv_name_5 in self.csv_list_5:
                                            self.csv_list_5.append(csv_name_5)
                                            with open(csv_name_5, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writeheader()
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                        else:
                                            with open(csv_name_5, 'a+', newline='') as file:
                                                writer = csv.DictWriter(file, fieldnames=fieldnames)
                                                writer.writerow({
                                                    'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                                                    'leapS': parsed_data.leapS,
                                                    'prMes': prMes_id_name, 'cpMes': cpMes_id_name,
                                                    'doMes': doMes_id_name,
                                                    'freqId': freq_id_name, 'locktime': locktime_id_name,
                                                    'cno': cno_id_name})
                                    except KeyError as err:
                                        print(err, getattr(parsed_data, gnss_sig_id))

                            except KeyError as err:
                                print(err, gnss_message_id_number)

                    except AttributeError:
                        print("WRONG MESSAGE FORMAT.")

                if parsed_data.identity == 'NAV-PVT':

                    fieldnames = ['iTOW', 'year', 'month', 'day', 'hour', 'min', 'second', 'tAcc', 'nano', 'fixType',
                                  'numSV', 'lon', 'lat', 'height', 'hMSL', 'hAcc', 'vAcc', 'velN', 'velE', 'velD',
                                  'gSpeed', 'headMot', 'sAcc', 'headAcc', 'pDOP', 'reserved1', 'headVeh', 'magDec',
                                  'magAcc']

                    csv_name_6 = self.save_folder + "/" + str(parsed_data.identity) + ".csv"
                    if not csv_name_6 in self.csv_list_6:
                        self.csv_list_6.append(csv_name_6)
                        self.csv_name_6_open = open(csv_name_6, 'a', newline='')
                        csv_name_6_writer = csv.DictWriter(self.csv_name_6_open, fieldnames=fieldnames)
                        csv_name_6_writer.writeheader()
                        csv_name_6_writer.writerow(
                            {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
                             'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
                             'second': parsed_data.second, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
                             'fixType': parsed_data.fixType, 'numSV': parsed_data.numSV, 'lon': parsed_data.lon,
                             'lat': parsed_data.lat,
                             'height': parsed_data.height,
                             'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
                             'velN': parsed_data.velN,
                             'velE': parsed_data.velE, 'velD': parsed_data.velD,
                             'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
                             'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
                             'reserved1': parsed_data.reserved1,
                             'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
                             })
                    else:
                        self.csv_name_6_open = open(csv_name_6, 'a', newline='')
                        csv_name_6_writer = csv.DictWriter(self.csv_name_6_open, fieldnames=fieldnames)
                        csv_name_6_writer.writerow(
                            {'iTOW': parsed_data.iTOW, 'year': parsed_data.year, 'month': parsed_data.month,
                             'day': parsed_data.day, 'hour': parsed_data.hour, 'min': parsed_data.min,
                             'second': parsed_data.second, 'tAcc': parsed_data.tAcc, 'nano': parsed_data.nano,
                             'fixType': parsed_data.fixType,
                             'numSV': parsed_data.numSV, 'lon': parsed_data.lon, 'lat': parsed_data.lat,
                             'height': parsed_data.height,
                             'hMSL': parsed_data.hMSL, 'hAcc': parsed_data.hAcc, 'vAcc': parsed_data.vAcc,
                             'velN': parsed_data.velN,
                             'velE': parsed_data.velE, 'velD': parsed_data.velD,
                             'gSpeed': parsed_data.gSpeed, 'headMot': parsed_data.headMot, 'sAcc': parsed_data.sAcc,
                             'headAcc': parsed_data.headAcc, 'pDOP': parsed_data.pDOP,
                             'reserved1': parsed_data.reserved1,
                             'headVeh': parsed_data.headVeh, 'magDec': parsed_data.magDec, 'magAcc': parsed_data.magAcc
                             })

                if parsed_data.identity == "NAV-POSECEF":
                    fieldnames = ['iTOW (utc)', 'iTOW', 'ecefX', 'ecefY', 'ecefZ', 'pAcc']

                    csv_name_7 = self.save_folder + "/" + str(parsed_data.identity) + ".csv"
                    if not csv_name_7 in self.csv_list_7:
                        self.csv_list_7.append(csv_name_7)
                        self.csv_name_7_open = open(csv_name_7, 'a', newline='')
                        csv_name_7_writer = csv.DictWriter(self.csv_name_7_open, fieldnames=fieldnames)
                        csv_name_7_writer.writeheader()
                        csv_name_7_writer.writerow(
                            {'iTOW (utc)': itow2utc(parsed_data.iTOW), 'iTOW': parsed_data.iTOW,
                             'ecefX': parsed_data.ecefX, 'ecefY': parsed_data.ecefY,
                             'ecefZ': parsed_data.ecefZ, 'pAcc': parsed_data.pAcc
                             })
                    else:
                        self.csv_name_7_open = open(csv_name_7, 'a', newline='')
                        csv_name_7_writer = csv.DictWriter(self.csv_name_7_open, fieldnames=fieldnames)
                        csv_name_7_writer.writerow(
                            {'iTOW (utc)': itow2utc(parsed_data.iTOW), 'iTOW': parsed_data.iTOW,
                             'ecefX': parsed_data.ecefX, 'ecefY': parsed_data.ecefY,
                             'ecefZ': parsed_data.ecefZ, 'pAcc': parsed_data.pAcc
                             })

                # if parsed_data.identity == 'NAV-SIG':
                #     print(parsed_data.identity)
                #     print(parsed_data.msg_cls)
                #     try:
                #         num_message = parsed_data.numMeas
                #         # if num_message == 0:
                #         #     print(parsed_data.identity)
                #         #     print(parsed_data.msg_cls)
                #         # else:
                #         for gnss_id in range(1, 10, 1):
                #             gnss_message_id = 'gnssId_0' + str(gnss_id)
                #             gnss_message_id_number = getattr(parsed_data, gnss_message_id)
                #             gnss_name = GNSSLIST[gnss_message_id_number]
                #             id_msg = '0' + str(gnss_id)
                #             if gnss_name == "GPS":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_0' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_0' + str(gnss_id)
                #                 gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_1 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 print(csv_name_1)
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 itow_id = 'iTOW'
                #                 itow_id_name = getattr(parsed_data, itow_id)
                #
                #                 freq_id = 'freqId_0' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 prRes_id = 'prRes_0' + str(gnss_id)
                #                 prRes_id_name = parsed_data.bytes2val(getattr(parsed_data, prRes_id), ubt.I2)
                #
                #                 cno_id = 'cno_0' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 qualityInd_id = 'qualityInd_0' + str(gnss_id)
                #                 qualityInd_id_name = parsed_data.bytes2val(getattr(parsed_data, qualityInd_id), ubt.U1)
                #
                #                 corrSource_id = 'corrSource_0' + str(gnss_id)
                #                 corrSource_id_name = parsed_data.bytes2val(getattr(parsed_data, corrSource_id), ubt.U1)
                #
                #                 ionoModel_id = 'ionoModel_0' + str(gnss_id)
                #                 ionoModel_id_name = parsed_data.bytes2val(getattr(parsed_data, ionoModel_id), ubt.U1)
                #
                #                 sigFlags_id = 'sigFlags_0' + str(gnss_id)
                #                 sigFlags_id_name = parsed_data.bytes2val(getattr(parsed_data, sigFlags_id), ubt.U1)
                #
                #                 reserved2_id = 'reserved2_0' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['iTOW', 'freqId', 'prRes',
                #                               'cno', 'qualityInd', 'corrSource', 'ionoModel', 'sigFlags', 'reserved2']
                #                 if not csv_name_1 in self.csv_list_1:
                #                     self.csv_list_1.append(csv_name_1)
                #                     with open(csv_name_1, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'iTOW': parsed_data.iTOW, 'freqId': freq_id_name,
                #                             'prRes': prRes_id_name,'cno': cno_id_name, 'qualityInd': qualityInd_id_name,
                #                             'corrSource': corrSource_id_name, 'ionoModel': ionoModel_id_name,
                #                             'sigFlags': sigFlags_id_name, 'reserved2': reserved2_id_name})
                #                 else:
                #                     with open(csv_name_1, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'iTOW': parsed_data.iTOW, 'freqId': freq_id_name,
                #                             'prRes': prRes_id_name,'cno': cno_id_name, 'qualityInd': qualityInd_id_name,
                #                             'corrSource': corrSource_id_name, 'ionoModel': ionoModel_id_name,
                #                             'sigFlags': sigFlags_id_name, 'reserved2': reserved2_id_name})
                #
                #             if gnss_name == "Galileo":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_0' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_0' + str(gnss_id)
                #                 gnss_sig_id_name = GALILEOSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_2 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_0' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_0' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_0' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_0' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_0' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_0' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_0' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_0' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_0' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_0' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_0' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_2 in self.csv_list_2:
                #                     self.csv_list_2.append(csv_name_2)
                #                     with open(csv_name_2, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_2, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #             # if gnss_name == "Galileo":
                #             #     print(gnss_name)
                #             #     gnss_sv_id = 'svId_0' + str(gnss_id)
                #             #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #             #     gnss_sig_id = 'sigId_0' + str(gnss_id)
                #             #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                #             #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                #             #     if not csv_name in csv_list:
                #             #         with open(csv_name, mode='w') as gal_info:
                #             #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                #             #                                   quoting=csv.QUOTE_MINIMAL)
                #             #             gal_info.writerow(gnss_name)
                #             #         csv_list.append(csv_name)
                #             #     else:
                #             #         pass
                #
                #             if gnss_name == "GLONASS":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_0' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_0' + str(gnss_id)
                #                 gnss_sig_id_name = GLONASSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_3 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_0' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_0' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_0' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_0' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_0' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_0' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_0' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_0' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_0' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_0' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_0' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_3 in self.csv_list_3:
                #                     self.csv_list_3.append(csv_name_3)
                #                     with open(csv_name_3, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_3, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #
                #             if gnss_name == "BeiDou":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_0' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_0' + str(gnss_id)
                #                 gnss_sig_id_name = BEIDOUSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_4 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_0' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_0' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_0' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_0' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_0' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_0' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_0' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_0' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_0' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_0' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_0' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_4 in self.csv_list_4:
                #                     self.csv_list_4.append(csv_name_4)
                #                     with open(csv_name_4, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_4, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #
                #             if gnss_name == "Qszz":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_0' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_0' + str(gnss_id)
                #                 gnss_sig_id_name = QZSSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_5 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_0' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_0' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_0' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_0' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_0' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_0' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_0' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_0' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_0' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_0' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_0' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_5 in self.csv_list_5:
                #                     self.csv_list_5.append(csv_name_5)
                #                     with open(csv_name_5, 'a', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_5, 'a', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #
                #         for gnss_id in range(10, num_message + 1, 1):
                #             gnss_message_id = 'gnssId_' + str(gnss_id)
                #             gnss_message_id_number = getattr(parsed_data, gnss_message_id)
                #             gnss_name = GNSSLIST[gnss_message_id_number]
                #             id_msg = '0' + str(gnss_id)
                #             #     if gnss_name == "GPS":
                #             #         print(gnss_name)
                #             #         gnss_sv_id = 'svId_' + str(gnss_id)
                #             #         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #             #         gnss_sig_id = 'sigId_' + str(gnss_id)
                #             #         gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                #             #         csv_name_1 = str(GPSSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                #             #
                #             #         # rcvTow_id = 'prMes_' + str(gnss_id)
                #             #         # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #             #         #
                #             #         # week_id = 'prMes_' + str(gnss_id)
                #             #         # week_id_name = getattr(parsed_data, week_id)
                #             #         #
                #             #         # leapS_id = 'prMes_' + str(gnss_id)
                #             #         # leapS_id_name = getattr(parsed_data, leapS_id)
                #             #
                #             #         prMes_id = 'prMes_' + str(gnss_id)
                #             #         prMes_id_name = getattr(parsed_data, prMes_id)
                #             #
                #             #         cpMes_id = 'cpMes_' + str(gnss_id)
                #             #         cpMes_id_name = getattr(parsed_data, cpMes_id)
                #             #
                #             #         doMes_id = 'doMes_' + str(gnss_id)
                #             #         doMes_id_name = getattr(parsed_data, doMes_id)
                #             #
                #             #         freq_id = 'freqId_' + str(gnss_id)
                #             #         freq_id_name = getattr(parsed_data, freq_id)
                #             #
                #             #         locktime_id = 'locktime_' + str(gnss_id)
                #             #         locktime_id_name = getattr(parsed_data, locktime_id)
                #             #
                #             #         cno_id = 'cno_' + str(gnss_id)
                #             #         cno_id_name = getattr(parsed_data, cno_id)
                #             #
                #             #         prStdev_id = 'prStdev_' + str(gnss_id)
                #             #         prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #             #
                #             #         cpStdev_id = 'cpStdev_' + str(gnss_id)
                #             #         cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #             #
                #             #         doStdev_id = 'doStdev_' + str(gnss_id)
                #             #         doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #             #
                #             #         trkStat_id = 'trkStat_' + str(gnss_id)
                #             #         trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #             #
                #             #         reserved2_id = 'reserved2_' + str(gnss_id)
                #             #         reserved2_id_name = getattr(parsed_data, reserved2_id)
                #             #
                #             #         fieldnames = ['gnssId', 'svId', 'sigId', 'rcvTow', 'week', 'leapS', 'prMes', 'cpMes',
                #             #                       'doMes',
                #             #                       'freqId',
                #             #                       'locktime', 'cno',
                #             #                       'prStdev', 'cpStdev', 'doStdev', 'trkStat', 'reserved2']
                #             #
                #             #         if not csv_name_1 in self.csv_list_1:
                #             #             self.csv_list_1.append(csv_name_1)
                #             #             with open(csv_name_1, 'a+', newline='') as file:
                #             #                 writer = csv.DictWriter(file, fieldnames=fieldnames)
                #             #                 writer.writeheader()
                #             #                 writer.writerow(
                #             #                     {
                #             #                         'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
                #             #                         'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #             #                         'leapS': parsed_data.leapS,
                #             #                         'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #             #                         'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
                #             #                         'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
                #             #                         'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
                #             #                         'reserved2': reserved2_id_name})
                #             #         else:
                #             #             with open(csv_name_1, 'a+', newline='') as file:
                #             #                 writer = csv.DictWriter(file, fieldnames=fieldnames)
                #             #                 writer.writerow(
                #             #                     {
                #             #                         'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
                #             #                         'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #             #                         'leapS': parsed_data.leapS,
                #             #                         'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #             #                         'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
                #             #                         'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
                #             #                         'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
                #             #                         'reserved2': reserved2_id_name})
                #             #     if gnss_name == "Galileo":
                #             #         print(gnss_name)
                #             #         gnss_sv_id = 'svId_' + str(gnss_id)
                #             #         gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #             #         gnss_sig_id = 'sigId_' + str(gnss_id)
                #             #         gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                #             #         csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                #             #         if not csv_name in csv_list:
                #             #             with open(csv_name, mode='w') as gal_info:
                #             #                 gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                #             #                                       quoting=csv.QUOTE_MINIMAL)
                #             #                 gal_info.writerow(gnss_name)
                #             #             csv_list.append(csv_name)
                #             #         else:
                #             #             pass
                #             #
                #             #     if gnss_name == "BeiDou":
                #             #         pass
                #             #     else:
                #             #         pass
                #             # # for gnssId in range(1, num_message + 1, 1):
                #             # #     gnss_message_id = 'gnssId_' + str(gnssId)
                #             # #     try:
                #             # #         gnss_message_id_number = getattr(parsed_data, gnss_message_id)
                #             # #
                #             # #         gnss_name = GNSSLIST[gnss_message_id_number]
                #             # #         id_msg = '0' + str(gnssId)
                #             # #
                #             # #         if gnss_name == "Galileo":
                #             # #             print(gnss_name)
                #             # #             # for sv_id_gal in range(1, 35 + 1, 1):
                #             # #             #     gnss_sv_id = 'svId_0' + str(sv_id_gal)
                #             # #             #     print(gnss_sv_id)
                #             # #             #     list_gnss_sv_id.append(gnss_sv_id)
                #             # #             #     if getattr(parsed_data, gnss_sv_id):
                #             # #             #         print(getattr(parsed_data, gnss_sv_id))
                #             # #
                #             # #         elif gnss_name == "GPS":
                #             # #             print(gnss_name)
                #             # #             # for sv_id in range(1, 10, 1):
                #             # #             #     gnss_sv_id = 'svId_0' + str(sv_id)
                #             # #             #     print(gnss_sv_id)
                #             # #             #     list_gnss_sv_id.append(gnss_sv_id)
                #             # #             #     if getattr(parsed_data, gnss_sv_id):
                #             # #             #         print(getattr(parsed_data, gnss_sv_id))
                #             # #
                #             # #             for sv_id in range(10, 24, 1):
                #             # #                 gnss_sv_id = 'svId_' + str(sv_id)
                #             # #                 print(gnss_sv_id)
                #             # #                 # list_gnss_sv_id.append(gnss_sv_id)
                #             # #                 # if getattr(parsed_data, gnss_sv_id):
                #             # #                 #     print(getattr(parsed_data, gnss_sv_id))
                #             # #
                #             # #
                #             # #         elif gnss_name == "BeiDou":
                #             # #             pass
                #             # #         else:
                #             # #             pass
                #             # #     except:
                #             # #         pass
                #
                #             if gnss_name == "GPS":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_' + str(gnss_id)
                #                 gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_1 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_1 in self.csv_list_1:
                #                     self.csv_list_1.append(csv_name_1)
                #                     with open(csv_name_1, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_1, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #
                #             if gnss_name == "Galileo":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_' + str(gnss_id)
                #                 gnss_sig_id_name = GALILEOSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_2 = self.save_folder + "/" + "NAV-SIG-"+ str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_2 in self.csv_list_2:
                #                     self.csv_list_2.append(csv_name_2)
                #                     with open(csv_name_2, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_2, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #             # if gnss_name == "Galileo":
                #             #     print(gnss_name)
                #             #     gnss_sv_id = 'svId_0' + str(gnss_id)
                #             #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #             #     gnss_sig_id = 'sigId_0' + str(gnss_id)
                #             #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                #             #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                #             #     if not csv_name in csv_list:
                #             #         with open(csv_name, mode='w') as gal_info:
                #             #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                #             #                                   quoting=csv.QUOTE_MINIMAL)
                #             #             gal_info.writerow(gnss_name)
                #             #         csv_list.append(csv_name)
                #             #     else:
                #             #         pass
                #
                #             if gnss_name == "GLONASS":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_' + str(gnss_id)
                #                 gnss_sig_id_name = GLONASSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_3 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_3 in self.csv_list_3:
                #                     self.csv_list_3.append(csv_name_3)
                #                     with open(csv_name_3, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_3, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #             # if gnss_name == "Galileo":
                #             #     print(gnss_name)
                #             #     gnss_sv_id = 'svId_0' + str(gnss_id)
                #             #     gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #             #     gnss_sig_id = 'sigId_0' + str(gnss_id)
                #             #     gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
                #             #     csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
                #             #     if not csv_name in csv_list:
                #             #         with open(csv_name, mode='w') as gal_info:
                #             #             gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
                #             #                                   quoting=csv.QUOTE_MINIMAL)
                #             #             gal_info.writerow(gnss_name)
                #             #         csv_list.append(csv_name)
                #             #     else:
                #             #         pass
                #
                #             if gnss_name == "BeiDou":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_' + str(gnss_id)
                #                 gnss_sig_id_name = BEIDOUSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_4 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_4 in self.csv_list_4:
                #                     self.csv_list_4.append(csv_name_4)
                #                     with open(csv_name_4, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_4, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #
                #             if gnss_name == "Qszz":
                #                 print(gnss_name)
                #                 gnss_sv_id = 'svId_' + str(gnss_id)
                #                 gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
                #                 gnss_sig_id = 'sigId_' + str(gnss_id)
                #                 gnss_sig_id_name = QZSSSIGLIST[getattr(parsed_data, gnss_sig_id)]
                #                 csv_name_5 = self.save_folder + "/" + "NAV-SIG-" + str(gnss_sig_id_name) + " Sv_Id " + str(
                #                     gnss_sv_id_name) + ".csv"
                #                 # rcvTow_id = 'prMes_0' + str(gnss_id)
                #                 # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
                #                 #
                #                 # week_id = 'prMes_0' + str(gnss_id)
                #                 # week_id_name = getattr(parsed_data, week_id)
                #                 #
                #                 # leapS_id = 'prMes_0' + str(gnss_id)
                #                 # leapS_id_name = getattr(parsed_data, leapS_id)
                #                 prMes_id = 'prMes_' + str(gnss_id)
                #                 prMes_id_name = getattr(parsed_data, prMes_id)
                #
                #                 cpMes_id = 'cpMes_' + str(gnss_id)
                #                 cpMes_id_name = getattr(parsed_data, cpMes_id)
                #
                #                 doMes_id = 'doMes_' + str(gnss_id)
                #                 doMes_id_name = getattr(parsed_data, doMes_id)
                #
                #                 freq_id = 'freqId_' + str(gnss_id)
                #                 freq_id_name = getattr(parsed_data, freq_id)
                #
                #                 locktime_id = 'locktime_' + str(gnss_id)
                #                 locktime_id_name = getattr(parsed_data, locktime_id)
                #
                #                 cno_id = 'cno_' + str(gnss_id)
                #                 cno_id_name = getattr(parsed_data, cno_id)
                #
                #                 prStdev_id = 'prStdev_' + str(gnss_id)
                #                 prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
                #
                #                 cpStdev_id = 'cpStdev_' + str(gnss_id)
                #                 cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
                #
                #                 doStdev_id = 'doStdev_' + str(gnss_id)
                #                 doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
                #
                #                 trkStat_id = 'trkStat_' + str(gnss_id)
                #                 trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
                #                 print(trkStat_id_name)
                #
                #                 reserved2_id = 'reserved2_' + str(gnss_id)
                #                 reserved2_id_name = getattr(parsed_data, reserved2_id)
                #
                #                 fieldnames = ['rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
                #                               'freqId', 'locktime', 'cno']
                #                 if not csv_name_5 in self.csv_list_5:
                #                     self.csv_list_5.append(csv_name_5)
                #                     with open(csv_name_5, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writeheader()
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #                 else:
                #                     with open(csv_name_5, 'a+', newline='') as file:
                #                         writer = csv.DictWriter(file, fieldnames=fieldnames)
                #                         writer.writerow({
                #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
                #                             'leapS': parsed_data.leapS,
                #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
                #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name})
                #
                #     except AttributeError:
                #         print("WRONG MESSAGE FORMAT.")

            except AttributeError as err:
                print("err")
            # if parsed_data.identity == 'RXM-MEASX':
            #     num_sv = parsed_data.numSV
            #
            #     for gnss_id in range(1, 10, 1):
            #         gnss_message_id = 'gnssId_0' + str(gnss_id)
            #         gnss_message_id_number = getattr(parsed_data, gnss_message_id)
            #         gnss_name = GNSSLIST[gnss_message_id_number]
            #         id_msg = '0' + str(gnss_id)
            #         if gnss_name == "GPS":
            #             print(gnss_name)
            #             gnss_sv_id = 'svId_0' + str(gnss_id)
            #             gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
            #             # gnss_sig_id = 'sigId_0' + str(gnss_id)
            #             # gnss_sig_id_name = GPSSIGLIST[getattr(parsed_data, gnss_sig_id)]
            #             csv_name_2 = gnss_name + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
            #             # rcvTow_id = 'prMes_0' + str(gnss_id)
            #             # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
            #             #
            #             # week_id = 'prMes_0' + str(gnss_id)
            #             # week_id_name = getattr(parsed_data, week_id)
            #             #
            #             # leapS_id = 'prMes_0' + str(gnss_id)
            #             # leapS_id_name = getattr(parsed_data, leapS_id)
            #             prMes_id = 'prMes_0' + str(gnss_id)
            #             prMes_id_name = getattr(parsed_data, prMes_id)
            #
            #             cpMes_id = 'cpMes_0' + str(gnss_id)
            #             cpMes_id_name = getattr(parsed_data, cpMes_id)
            #
            #             doMes_id = 'doMes_0' + str(gnss_id)
            #             doMes_id_name = getattr(parsed_data, doMes_id)
            #
            #             freq_id = 'freqId_0' + str(gnss_id)
            #             freq_id_name = getattr(parsed_data, freq_id)
            #
            #             locktime_id = 'locktime_0' + str(gnss_id)
            #             locktime_id_name = getattr(parsed_data, locktime_id)
            #
            #             cno_id = 'cno_0' + str(gnss_id)
            #             cno_id_name = getattr(parsed_data, cno_id)
            #
            #             prStdev_id = 'prStdev_0' + str(gnss_id)
            #             prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
            #
            #             cpStdev_id = 'cpStdev_0' + str(gnss_id)
            #             cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
            #
            #             doStdev_id = 'doStdev_0' + str(gnss_id)
            #             doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
            #
            #             trkStat_id = 'trkStat_0' + str(gnss_id)
            #             trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
            #             print(trkStat_id_name)
            #
            #             reserved2_id = 'reserved2_0' + str(gnss_id)
            #             reserved2_id_name = getattr(parsed_data, reserved2_id)
            #
            #             fieldnames = ['gnssId', 'svId', 'sigId', 'rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
            #                           'freqId',
            #                           'locktime', 'cno',
            #                           'prStdev', 'cpStdev', 'doStdev', 'trkStat', 'reserved2']
            #             if not csv_name_2 in self.csv_list_2:
            #                 self.csv_list_2.append(csv_name_2)
            #                 with open(csv_name_2, 'a+', newline='') as file:
            #                     writer = csv.DictWriter(file, fieldnames=fieldnames)
            #                     writer.writeheader()
            #                     writer.writerow({
            #                         'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
            #                         'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week, 'leapS': parsed_data.leapS,
            #                         'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
            #                         'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
            #                         'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
            #                         'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
            #                         'reserved2': reserved2_id_name})
            #             else:
            #                 with open(csv_name_2, 'a+', newline='') as file:
            #                     writer = csv.DictWriter(file, fieldnames=fieldnames)
            #                     writer.writerow(
            #                         {
            #                             'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
            #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
            #                             'leapS': parsed_data.leapS,
            #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
            #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
            #                             'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
            #                             'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
            #                             'reserved2': reserved2_id_name})
            #
            #         if gnss_name == "Galileo":
            #             print(gnss_name)
            #             gnss_sv_id = 'svId_0' + str(gnss_id)
            #             gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
            #             gnss_sig_id = 'sigId_0' + str(gnss_id)
            #             gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
            #             csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
            #             if not csv_name in csv_list:
            #                 with open(csv_name, mode='w') as gal_info:
            #                     gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
            #                                           quoting=csv.QUOTE_MINIMAL)
            #                     gal_info.writerow(gnss_name)
            #                 csv_list.append(csv_name)
            #             else:
            #                 pass
            #
            #         if gnss_name == "BeiDou":
            #             pass
            #         else:
            #             pass
            #
            #     for gnss_id in range(10, num_sv + 1, 1):
            #         gnss_message_id = 'gnssId_' + str(gnss_id)
            #         gnss_message_id_number = getattr(parsed_data, gnss_message_id)
            #         gnss_name = GNSSLIST[gnss_message_id_number]
            #         id_msg = '0' + str(gnss_id)
            #         if gnss_name == "GPS":
            #             print(gnss_name)
            #             gnss_sv_id = 'svId_' + str(gnss_id)
            #             gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
            #             gnss_sig_id = 'sigId_' + str(gnss_id)
            #             gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
            #             csv_name_2 = str(GPSSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
            #
            #             # rcvTow_id = 'prMes_' + str(gnss_id)
            #             # rcvTow_id_name = getattr(parsed_data, rcvTow_id)
            #             #
            #             # week_id = 'prMes_' + str(gnss_id)
            #             # week_id_name = getattr(parsed_data, week_id)
            #             #
            #             # leapS_id = 'prMes_' + str(gnss_id)
            #             # leapS_id_name = getattr(parsed_data, leapS_id)
            #
            #             prMes_id = 'prMes_' + str(gnss_id)
            #             prMes_id_name = getattr(parsed_data, prMes_id)
            #
            #             cpMes_id = 'cpMes_' + str(gnss_id)
            #             cpMes_id_name = getattr(parsed_data, cpMes_id)
            #
            #             doMes_id = 'doMes_' + str(gnss_id)
            #             doMes_id_name = getattr(parsed_data, doMes_id)
            #
            #             freq_id = 'freqId_' + str(gnss_id)
            #             freq_id_name = getattr(parsed_data, freq_id)
            #
            #             locktime_id = 'locktime_' + str(gnss_id)
            #             locktime_id_name = getattr(parsed_data, locktime_id)
            #
            #             cno_id = 'cno_' + str(gnss_id)
            #             cno_id_name = getattr(parsed_data, cno_id)
            #
            #             prStdev_id = 'prStdev_' + str(gnss_id)
            #             prStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, prStdev_id), ubt.U1)
            #
            #             cpStdev_id = 'cpStdev_' + str(gnss_id)
            #             cpStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, cpStdev_id), ubt.U1)
            #
            #             doStdev_id = 'doStdev_' + str(gnss_id)
            #             doStdev_id_name = parsed_data.bytes2val(getattr(parsed_data, doStdev_id), ubt.U1)
            #
            #             trkStat_id = 'trkStat_' + str(gnss_id)
            #             trkStat_id_name = parsed_data.bytes2val(getattr(parsed_data, trkStat_id), ubt.U1)
            #
            #             reserved2_id = 'reserved2_' + str(gnss_id)
            #             reserved2_id_name = getattr(parsed_data, reserved2_id)
            #
            #             fieldnames = ['gnssId', 'svId', 'sigId', 'rcvTow', 'week', 'leapS', 'prMes', 'cpMes', 'doMes',
            #                           'freqId',
            #                           'locktime', 'cno',
            #                           'prStdev', 'cpStdev', 'doStdev', 'trkStat', 'reserved2']
            #
            #             if not csv_name_2 in self.csv_list_2:
            #                 self.csv_list_2.append(csv_name_2)
            #                 with open(csv_name_2, 'a+', newline='') as file:
            #                     writer = csv.DictWriter(file, fieldnames=fieldnames)
            #                     writer.writeheader()
            #                     writer.writerow(
            #                         {
            #                             'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
            #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
            #                             'leapS': parsed_data.leapS,
            #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
            #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
            #                             'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
            #                             'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
            #                             'reserved2': reserved2_id_name})
            #             else:
            #                 with open(csv_name_2, 'a+', newline='') as file:
            #                     writer = csv.DictWriter(file, fieldnames=fieldnames)
            #                     writer.writerow(
            #                         {
            #                             'gnssId': gnss_name, 'svId': gnss_sv_id_name, 'sigId': gnss_sig_id_name,
            #                             'rcvTow': parsed_data.rcvTow, 'week': parsed_data.week,
            #                             'leapS': parsed_data.leapS,
            #                             'prMes': prMes_id_name, 'cpMes': cpMes_id_name, 'doMes': doMes_id_name,
            #                             'freqId': freq_id_name, 'locktime': locktime_id_name, 'cno': cno_id_name,
            #                             'prStdev': prStdev_id_name, 'cpStdev': cpStdev_id_name,
            #                             'doStdev': doStdev_id_name, 'trkStat': trkStat_id_name,
            #                             'reserved2': reserved2_id_name})
            #         if gnss_name == "Galileo":
            #             print(gnss_name)
            #             gnss_sv_id = 'svId_' + str(gnss_id)
            #             gnss_sv_id_name = getattr(parsed_data, gnss_sv_id)
            #             gnss_sig_id = 'sigId_' + str(gnss_id)
            #             gnss_sig_id_name = getattr(parsed_data, gnss_sig_id)
            #             csv_name = str(GALILEOSIGLIST[gnss_sig_id_name]) + " Sv_Id " + str(gnss_sv_id_name) + ".csv"
            #             if not csv_name in csv_list:
            #                 with open(csv_name, mode='w') as gal_info:
            #                     gal_info = csv.writer(gal_info, delimiter=',', quotechar='"', lineterminator='\n',
            #                                           quoting=csv.QUOTE_MINIMAL)
            #                     gal_info.writerow(gnss_name)
            #                 csv_list.append(csv_name)
            #             else:
            #                 pass
            #
            #         if gnss_name == "BeiDou":
            #             pass
            #         else:
            #             pass

    def refresh_text_box(self, MYSTRING):
        print("")
        self.cursor.insertText(str(MYSTRING))
        self.cursor.setPosition(self.cursor.position())
        self.cursor.movePosition(self.cursor.Left, self.cursor.KeepAnchor, 0)
        self.show_message.setTextCursor(self.cursor)
        # self.show_message.append(str(MYSTRING))
        # self.show_message.append('\n')
        # self.show_message.append('started appending %s' % MYSTRING)  # append string
        QApplication.processEvents()  # update gui for pyqt

    def refresh_text_box_2(self, MYSTRING):
        print("")
        self.show_other_message.append(str(MYSTRING))
        self.show_message.append('started appending %s' % MYSTRING)  # append string
        QApplication.processEvents()  # update gui for pyqt

    def quit_app(self):
        sys.exit()

    def onActivated10(self, text):
        if text:
            self.selected_port = text
            print("Selected port:", self.selected_port)
            self.refresh_text_box_2("\n")  # MY_FUNCTION_CALL
            self.refresh_text_box_2("SERIAL MODE:")  # MY_FUNCTION_CALL
            self.refresh_text_box_2("   selected port COM : " + str(self.selected_port))  # MY_FUNCTION_CALL
        else:
            QMessageBox.about(self, "Multi-Frequency detected", "No selected frequency")

    def hot_start(self):

        self.serial_running = False

        if self.stream.is_open == False:
            self.stream.open()

        # serialOut = Serial(self.selected_port, 9600, timeout=3)
        msg = UBXMessage('CFG', 'CFG-RST', SET, navBbrMask=b"\x00")

        # msg = UBXMessage('CFG', 'CFG-RST', SET, navBbrMask=0)
        print(msg)
        output = msg.serialize()
        self.stream.write(output)
        self.serial_running = True
        self.stream.close()

    def warm_start(self):

        self.serial_running = False

        if self.stream.is_open == False:
            self.stream.open()

        msg = UBXMessage('CFG', 'CFG-RST', SET, navBbrMask=b"\x01")
        # msg = UBXMessage('CFG', 'CFG-RST', SET, navBbrMask=1)
        print(msg)
        output = msg.serialize()
        print(output)
        self.stream.write(output)

        self.serial_running = True
        self.stream.close()

    def cold_start(self):

        # selected_baud = 9600
        # self.port_com = Serial(self.selected_port, selected_baud, timeout=3)
        # print(" Port is open:", self.port_com.is_open)
        # # msg = UBXMessage('CFG', 'CFG-RST', SET, navBbrMask=240)
        # while self.stream.is_open == True:

        self.serial_running = False

        if self.stream.is_open == False:
            self.stream.open()

        msg = UBXMessage('CFG', 'CFG-RST', SET, navBbrMask=b"\xff")
        print(msg)
        print('cold start:', msg)
        output = msg.serialize()
        print("serial send:", output)
        self.stream.write(output)

        self.serial_running = True
        self.stream.close()

    def stop_streaming_func(self):
        print("Stop Streaming")
        if self.running_mode == "SERIAL":
            self.stream.close()
            print(" Close PORT COM")
        else:
            self.running_stop = False

        self.startWatch = False
        # Reset all counter variables
        self.counter = 0
        self.minute = '00'
        self.second = '00'
        self.count = '00'
        # Set the initial values for the stop watch
        self.iTow.setText(str(self.counter))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    # qtmodern.styles.dark(app)
    # mw = qtmodern.windows.ModernWindow(w)
    w.show()
    app.exec_()
