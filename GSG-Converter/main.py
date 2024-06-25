####################
import os
import sys
import platform as plt
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
import pathlib as ptl
from PySide6.QtWidgets import *
from app_modules import *
from scen_conversion import ScenFunction
from nmea_conversion import NmeaFunction
import csv
import skydelsdx
import datetime
from skydelsdx.commands import *
from skydelsdx.units import Lla, toRadian


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ##################
        # INIT VARIABLES
        ##################
        self.nmea_file_item = ""
        self.gsg56_selection = 0
        # PRINT ==> SYSTEM
        print('System: ' + plt.system())
        print('Version: ' + plt.release())

        ##################
        # START - WINDOW ATTRIBUTES
        ##################

        # REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        # ==> END #

        # SET ==> WINDOW TITLE
        self.setWindowTitle('GSG5/6 to Skydel converter')
        UIFunctions.labelTitle(self, 'GSG5/6 to Skydel converter')
        # UIFunctions.labelDescription(self, 'converter page')
        # ==> END #

        # WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)
        # ==> END #

        # ==> CREATE MENUS
        ##################

        # ==> TOGGLE MENU SIZE
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        self.ui.pushButton_gsg56_select_folder.clicked.connect(self.GSG56_page_mainFunction)
        self.ui.pushButton_convert_skydel.clicked.connect(self.skydel_page_mainFunction)
        self.ui.pushButton_load_skydel.clicked.connect(self.playback_skydel_mainFunction)

        # ==> END #

        # ==> ADD CUSTOM MENUS
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "Load GSG-6 files", "btn_load_gsg5_6", "url(:/16x16/icons/16x16/cil-input.png)",
                               True)
        UIFunctions.addNewMenu(self, "Convert to Skydel Script", "btn_new_user",
                               "url(:/16x16/icons/16x16/cil-transfer.png)", True)
        UIFunctions.addNewMenu(self, "Playback in Skydel", "btn_widgets", "url(:/16x16/icons/16x16/cil-media-play.png)",
                               True)
        # ==> END #

        # START MENU => SELECTION
        UIFunctions.selectStandardMenu(self, "btn_load_gsg5_6")
        # ==> END #

        # ==> START PAGE
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        # ==> END #

        # ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ##################

        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        # ==> END #
        # ==> LOAD DEFINITIONS
        ##################
        UIFunctions.uiDefinitions(self)
        # ==> END #

        ##################
        # END - WINDOW ATTRIBUTES
        ######## ---/--/--- ########

        ##################
        #                                                                      #
        # START -------------- WIDGETS FUNCTIONS/PARAMETERS ---------------- #
        #                                                                      #
        # ==> USER CODES BELLOW                                              #
        ##################

        # ==> QTableWidget RARAMETERS
        ##################
        # self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # ==> END #

        ##################
        #                                                                      #
        # END --------------- WIDGETS FUNCTIONS/PARAMETERS ----------------- #
        #                                                                      #
        ######## ---/--/--- ########

        # SHOW ==> MAIN WINDOW
        ##################
        self.show()
        # ==> END #

    ##################
    # MENUS ==> DYNAMIC MENUS FUNCTIONS
    #########f##########

    def load_GSG56_scenarios(self):

        self.gsg56_selection = 1

        folder_selection = 0

        self.load_gsg56_scenarios_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if self.load_gsg56_scenarios_folder == "":
            QMessageBox.about(self, "CSV FOLDER PATH", "THE FOLDER PATH IS EMPTY.")

        elif not os.path.exists(self.load_gsg56_scenarios_folder):
            QMessageBox.about(self, "CSV FOLDER PATH", "THE SPECIFIED FOLDER IS NOT VALID")

        elif self.load_gsg56_scenarios_folder:
            folder_selection = 1
            self.ui.lineEdit_gsg56_folder_name.setText(str(self.load_gsg56_scenarios_folder))
            return self.load_gsg56_scenarios_folder

        if folder_selection == 0:
            return 0

    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_load_gsg5_6":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_load_gsg5_6")
            UIFunctions.labelPage(self, "Load GSG5/6 files")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE NEW USER
        if btnWidget.objectName() == "btn_new_user":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_convert_to_skydel)
            UIFunctions.resetStyle(self, "btn_new_user")
            UIFunctions.labelPage(self, "Skydel")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "PlayBack Skydel")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    # ==> END #

    ##################
    # START ==> APP EVENTS
    ##################

    # EVENT ==> MOUSE DOUBLE CLICK
    ##################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())

    # ==> END #

    # EVENT ==> MOUSE CLICK
    ##################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MiddleButton:
            print('Mouse click: MIDDLE BUTTON')

    # ==> END #

    # EVENT ==> KEY PRESSED
    ##################
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))

    # ==> END #

    # EVENT ==> RESIZE EVENT
    ##################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))

    # ==> END #

    ##################
    # END ==> APP EVENTS
    ######## ---/--/--- ########

    ##################
    # MAIN FUNCTION

    def GSG56_page_mainFunction(self):

        self.scen_dict_py = dict()
        try:
            self.GSG56_scenarios = ptl.Path(self.load_GSG56_scenarios())
            print(self.GSG56_scenarios)
        except TypeError as typ_err:
            print(typ_err)

        try:
            for file_item in self.GSG56_scenarios.iterdir():
                if file_item.is_file():
                    split_item_path = os.path.splitext(file_item)
                    item_extension = split_item_path[1]

                    if item_extension == ".scen":
                        print("file scen detected")
                        self.ui.tableWidget_home.setItem(0, 0, QTableWidgetItem(str("SCEN")))
                        self.ui.tableWidget_home.setItem(0, 1, QTableWidgetItem(str(file_item)))
                        self.scen_file_item = file_item

                    if item_extension == ".even":
                        print("file event detected")
                        self.ui.tableWidget_home.setItem(1, 0, QTableWidgetItem(str("EVEN")))
                        self.ui.tableWidget_home.setItem(1, 1, QTableWidgetItem(str(file_item)))

                    if item_extension == ".nmea":
                        print("NMEA")
                        self.ui.tableWidget_home.setItem(2, 0, QTableWidgetItem(str("NMEA")))
                        self.ui.tableWidget_home.setItem(2, 1, QTableWidgetItem(str(file_item)))
                        self.nmea_file_item = file_item

                    if item_extension == ".traj":
                        self.ui.tableWidget_home.setItem(3, 0, QTableWidgetItem(str("TRAJ")))
                        self.ui.tableWidget_home.setItem(3, 1, QTableWidgetItem(str(file_item)))
        except AttributeError as att_err_100:
            print(att_err_100)

    def skydel_page_mainFunction(self):

        if self.gsg56_selection == 1:
            try:

                self.save_folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

                if self.save_folder == "":
                    QMessageBox.about(self, "CSV FOLDER PATH", "THE FOLDER PATH IS EMPTY.")

                elif not os.path.exists(self.save_folder):
                    QMessageBox.about(self, "CSV FOLDER PATH", "THE SPECIFIED FOLDER IS NOT VALID")

                self.ui.lineEdit_skydel_folder_name.setText(self.save_folder)

                if self.nmea_file_item == "":
                    print("No NMEA file")
                else:
                    self.create_nmea_traj(self.nmea_file_item, self.save_folder)

                self.create_skydel_py(self.scen_dict_py)
                self.create_skydel_sdx(self.scen_dict_py)
                self.ui.script_convert_status.setEnabled(True)
                self.ui.script_convert_status.setText(
                    "                                                                                                                    *** Done! ***")

            except AttributeError as attr_err_100:
                print(attr_err_100)
                QMessageBox.about(self, "GSG5/6 configuration",
                                  "Please check that you selected a GSG5/6 scenario on the Load GSG5/6 files page")
        else:
            QMessageBox.about(self, "GSG5/6 configuration",
                              "Please check that you selected a GSG5/6 scenario on the Load GSG5/6 files page")

    def create_nmea_traj(self, nmea_file, save_folder_name):
        nmea_class = NmeaFunction()
        traj_file = nmea_class.start_data(nmea_file, save_folder_name)
        return traj_file

    def create_skydel_py(self):

        global tropo_model_skydel
        self.python_script_name = self.save_folder + "/" + 'Skydel_python' + '.py'

        try:
            self.python_script = open(self.python_script_name, 'w', newline='')
            self.python_script.write("#!/usr/bin/python")
            self.python_script.write("\n")
            self.python_script.write("# This Python script has been generated by the SKYDEL GNSS simulator")
            self.python_script.write("\n")
            self.python_script.write("from datetime import datetime")
            self.python_script.write("\n")
            self.python_script.write("from skydelsdx import *")
            self.python_script.write("\n")
            self.python_script.write("from skydelsdx.commands import *")
            self.python_script.write("\n")
            self.python_script.write("\n")
            self.python_script.write("sim = RemoteSimulator(True)")
            self.python_script.write("\n")
            self.python_script.write("sim.connect()")
            self.python_script.write("\n")
            self.python_script.write("sim.call(New(True, True))")
            self.python_script.write("\n")
            self.python_script.write("\n")

            RADIO_TYPE = self.ui.comboBox_skydel_conv.currentText()
            gain_dta = self.ui.skydel_rad_edit.text()

            if not gain_dta:
                if self.ui.comboBox_skydel_conv.currentText() == "DTA-2116":
                    self.ui.skydel_rad_edit.setText(str(50))
                    gain_dta = "50"
                if self.ui.comboBox_skydel_conv.currentText() == "DTA-2115B":
                    self.ui.skydel_rad_edit.setText(str(50))
                    gain_dta = "50"

            if self.ui.skydel_GN_checkBox.isChecked():
                GAUSSIAN_NOISE = True
                gaussian_noise_str = "true"
                gaussian_noise_str_py = "True"
            else:
                GAUSSIAN_NOISE = False
                gaussian_noise_str = "false"
                gaussian_noise_str_py = "False"

            scen_func = ScenFunction()

            if not self.scen_file_item:
                QMessageBox.about(self, " GSG5/6 scenario errors",
                                  " Please make sure your selected a .scen filein the page Load GSG5/6 Files.")
            else:
                self.scen_dict_py = scen_func.scen_main(self.scen_file_item, RADIO_TYPE)

            # sim.call(SetGpsStartTime(datetime.datetime(int(date[2]), int(date[0]), int(date[1]), int(hour[0]),
            # int(hour[1]), int(hour[2]))))
            new_dict_sky_py = self.scen_dict_py[0]
            date_time = new_dict_sky_py["startTime"]
            start_time_str = "sim.call(SetGpsStartTime(datetime" + "(" + str(date_time[0]) + "," + str(
                date_time[1]) + "," + str(date_time[2]) + "," + str(date_time[3]) + "," + str(date_time[4]) + "," + str(
                date_time[5]) + ")))"

            # self.python_script.write(str(sim.call(SetGpsStartTime(date_time))))
            self.python_script.write(start_time_str)
            self.python_script.write("\n")

            # sim.call(SetDuration(int(days)*86400 + int(hours)*3600 + int(minutes)*60))
            duration = new_dict_sky_py["Duration"]
            duration_str = "sim.call(SetDuration(" + str(duration) + "))"
            self.python_script.write(duration_str)
            self.python_script.write("\n")

            # sim.call(SetVehicleTrajectoryFix("Fix", positionN, positionE, positionAlt, 0, 0, 0))
            start_pos = new_dict_sky_py["Startpos"]
            start_pos_lat = start_pos[1]
            start_pos_long = start_pos[2]
            start_pos_alt = start_pos[3]
            # start_pos_yaw = start_pos[4]
            # start_pos_pitch = start_pos[5]
            # start_pos_roll = start_pos[6]
            #ecef_pos = Lla(start_pos_lat, start_pos_long, start_pos_alt).toEcef()
            # ecef_pos_x = ecef_pos.x
            # ecef_pos_y = ecef_pos.y
            # ecef_pos_z = ecef_pos.z

            start_pos_str = "sim.call(SetVehicleTrajectoryFix(" + '"' + str(start_pos[0]) + '"' + "," + str(
                start_pos[1]) + "," + str(
                start_pos[2]) + "," + str(start_pos[3]) + "," + str(start_pos[4]) + "," + str(start_pos[5]) + "," + str(
                start_pos[6]) + "))"
            self.python_script.write(start_pos_str)
            self.python_script.write("\n")

            antenna_mod = new_dict_sky_py["AntennaModel"]

            # Trajectory type
            traj_type = new_dict_sky_py['UserTrajectory']

            if traj_type == "Static" or traj_type == "3GPP":
                pass
            elif traj_type == "Circle":
                circle_param = new_dict_sky_py['CircleParam']

                circle_diam = circle_param[0]
                circle_radius = int(circle_diam / 2)
                circle_speed = circle_param[1]
                circle_motion = circle_param[2]

                circle_traj_str = "SetVehicleTrajectoryCircular(" + '"Circular"' + ", " + str(start_pos_lat) + ", "
                + str(start_pos_long) + ", " + str(start_pos_alt) + ", " + str(circle_radius) + ", " + str(circle_speed)
                + ", " + str(circle_motion) + ", " + "0" + ")"

                self.python_script.write(circle_traj_str)
                self.python_script.write("\n")
            # elif traj_type == "NmeaFile":
            #     nmea_file_name = new_dict_sky_py["NmeaFile"]
            #
            # else:
            #     traj_file_name = new_dict_sky_py["TrajFile"]
            # SetVehicleAntennaGainCSV(
            #    "C:/Users/Jean-Grace Oulai/Documents/Skydel-SDX/Templates/Antennas/Zero Antenna pattern.csv",
            #    AntennaPatternType.Custom, GNSSBand.L1, "Basic Antenna")
            current_dir = str(os.path.abspath(os.getcwd()))
            current_dir = current_dir.replace('\\', "/")

            if antenna_mod == "Zero":
                antenna_type = current_dir + "/" + "Antenna/ZeroModel.csv"
                antenna_L1_str = "sim.call(SetVehicleAntennaGainCSV(" + '"' + str(
                    antenna_type) + '"' + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L1, " + '"Basic Antenna"' + "))"
                antenna_L2_str = "sim.call(SetVehicleAntennaGainCSV(" + '"' + str(
                    antenna_type) + '"' + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L2, " + '"Basic Antenna"' + "))"
                antenna_L5_str = "sim.call(SetVehicleAntennaGainCSV(" + '"' + str(
                    antenna_type) + '"' + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L5, " + '"Basic Antenna"' + "))"
                antenna_L6_str = "sim.call(SetVehicleAntennaGainCSV(" + '"' + str(
                    antenna_type) + '"' + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.E6, " + '"Basic Antenna"' + "))"

                self.python_script.write(antenna_L1_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L2_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L5_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L6_str)
                self.python_script.write("\n")

            elif antenna_mod == "Helix":
                antenna_type = current_dir + "/" + "Antenna/Helix.csv"
                antenna_L1_str = ("sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L1, " + '"Basic Antenna"' +
                                  "))")
                antenna_L2_str = ("sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L2, " + '"Basic Antenna"' +
                                  "))")
                antenna_L5_str = ("sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L5, " + '"Basic Antenna"' +
                                  "))")
                antenna_L6_str = ("sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.E6, " + '"Basic Antenna"' +
                                  "))")

                self.python_script.write(antenna_L1_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L2_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L5_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L6_str)
                self.python_script.write("\n")

            elif antenna_mod == "Patch":
                antenna_type = current_dir + "/" + "Antenna/Patch.csv"
                antenna_L1_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L1, " + '"Basic Antenna"' + "))"
                antenna_L2_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L2, " + '"Basic Antenna"' + "))"
                antenna_L5_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L5, " + '"Basic Antenna"' + "))"
                antenna_L6_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.E6, " + '"Basic Antenna"' + "))"

                self.python_script.write(antenna_L1_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L2_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L5_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L6_str)
                self.python_script.write("\n")

            elif antenna_mod == "Cardioid":
                antenna_type = current_dir + "/" + "Antenna/Cardioid.csv"
                antenna_L1_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L1, " + "Basic Antenna" + "))"
                antenna_L2_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L2, " + "Basic Antenna" + "))"
                antenna_L5_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L5, " + "Basic Antenna" + "))"
                antenna_L6_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.E6, " + "Basic Antenna" + "))"

                self.python_script.write(antenna_L1_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L2_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L5_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L6_str)
                self.python_script.write("\n")

            elif antenna_mod == "GPS-703-GGG":
                antenna_type = current_dir + "/" + "Antenna/GSG703GGG.csv"
                antenna_L1_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L1, " + '"Basic Antenna"' + "))"
                antenna_L2_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L2, " + '"Basic Antenna"' + "))"
                antenna_L5_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.L5, " + '"Basic Antenna"' + "))"
                antenna_L6_str = "sim.call(SetVehicleAntennaGainCSV(" + str(
                    antenna_type) + ", " + "AntennaPatternType.Custom" + ", " + "GNSSBand.E6, " + '"Basic Antenna"' + "))"

                self.python_script.write(antenna_L1_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L2_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L5_str)
                self.python_script.write("\n")
                self.python_script.write(antenna_L6_str)
                self.python_script.write("\n")

            else:
                pass

            # sim.call(SetTropoModel("Saastamoinen"))
            tropo_model = new_dict_sky_py["TropoModel"]

            if tropo_model == "Saastamoinen":
                tropo_model_skydel = "Saastamoinen"

            elif tropo_model == "STANAG":
                tropo_model_skydel = "Stanag"

            elif tropo_model == "DO-229":
                tropo_model_skydel = "DO-229"

            elif tropo_model == "Off":
                tropo_model_skydel = "None"

            else:
                tropo_model_skydel = "Stanag"

            tropo_model_str = "sim.call(SetTropoModel(" + '"' + str(tropo_model_skydel) + '"' + "))"
            self.python_script.write(tropo_model_str)
            self.python_script.write("\n")

            iono_model = new_dict_sky_py["IonoModel"]

            if str(iono_model) == "1":
                iono_model_str = "sim.call(SetIonoModel(" + '"' + "Klobuchar" + '"' + "))"
                self.python_script.write(iono_model_str)
                self.python_script.write("\n")

            elif str(iono_model) == "Off":
                iono_model_str = "sim.call(SetIonoModel(" + "None" + "))"
                self.python_script.write(iono_model_str)
                self.python_script.write("\n")

            else:
                pass

            # SetVehicleAntennaOffset(10, 20, 30, 0, 0, 0, "Basic Antenna")
            lever_arm_param = new_dict_sky_py["LeverArm"]

            if not lever_arm_param:
                pass
            else:
                lever_arm_x = lever_arm_param[0]
                lever_arm_y = lever_arm_param[1]
                lever_arm_z = lever_arm_param[2]

                lever_arm_str = "SetVehicleAntennaOffset(" + str(lever_arm_x) + ", " + str(lever_arm_y) + ", " + str(
                    lever_arm_z) + ", " + "0" + ", " + "0" + ", " + "0" + ", " + '"Basic Antenna"' + ")"
                self.python_script.write(lever_arm_str)
                self.python_script.write("\n")

            # SetElevationMaskBelow(0.174532925199433336)
            elevation_mask = new_dict_sky_py["ElevationMask"]
            elevation_mask_str = "sim.call(SetElevationMaskBelow(" + str(elevation_mask) + "))"
            self.python_script.write(elevation_mask_str)
            self.python_script.write("\n")

            if RADIO_TYPE == "NoneRT" or RADIO_TYPE == "None":
                signal_upper_band = new_dict_sky_py['Signals_UpperLBand_none']
                signal_lower_band = new_dict_sky_py['Signals_LowerLBand_none']
                signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_none']
                signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_none']

                # Change configuration before starting the simulation
                if not signal_upper_band:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId"))
                    none_upper_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + "," + '""' + "," + '""' + "," + "True," + '"uniqueId"' + "))"
                    self.python_script.write(none_upper_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000, "UpperL", signal_upper_band, -1, 
                    # False, "uniqueId", None))
                    none_upper_signals_str = "sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000," + '"UpperL"' + "," + '"' + str(
                        signal_upper_band) + '"' + ", " + "0" + ", " + gaussian_noise_str_py + ", " + '"uniqueId"' + ", " + "None" + "))"
                    self.python_script.write(none_upper_signals_str)
                    self.python_script.write("\n")

                # Change configuration before starting the simulation
                if not signal_lower_band:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId2"))
                    none_lower_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + "," + '""' + "," + '""' + "," + "True," + '"uniqueId2"' + "))"
                    self.python_script.write(none_lower_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band, 0,
                    # False, "uniqueId2", None))
                    none_lower_signals_str = "sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000," + '"LowerL"' + "," + '"' + str(
                        signal_lower_band) + '"' + ", " + "0" + ", " + gaussian_noise_str_py + ", " + '"uniqueId2"' + ", " + "None" + "))"
                    self.python_script.write(none_lower_signals_str)
                    self.python_script.write("\n")

                # Change configuration before starting the simulation
                if not signal_lower_band2:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId3"))
                    none_lower2_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + "," + '""' + "," + '""' + "," + "True," + '"uniqueId3"' + "))"
                    self.python_script.write(none_lower2_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band2, 0,
                    # False, "uniqueId3", None))
                    none_lower2_signals_str = "sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000," + '"LowerL"' + "," + '"' + str(
                        signal_lower_band2) + '"' + ", " + "0" + ", " + gaussian_noise_str_py + ", " + '"uniqueId3"' + ", " + "None" + "))"
                    self.python_script.write(none_lower2_signals_str)
                    self.python_script.write("\n")

                # Change configuration before starting the simulation
                if not signal_lower_band_E6:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId4"))
                    none_lower_e6_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + ", " + '""' + ", " + '""' + "," + "True, " + '"uniqueId4"' + "))"
                    self.python_script.write(none_lower_e6_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band_E6, 0,
                    # False, "uniqueId4", None))
                    none_lower_e6_signals_str = "sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000," + '"LowerL"' + "," + '"' + str(
                        signal_lower_band_E6) + '"' + ", " + "0" + ", " + gaussian_noise_str_py + ", " + '"uniqueId4"' + ", " + "None" + "))"
                    self.python_script.write(none_lower_e6_signals_str)
                    self.python_script.write("\n")

            elif RADIO_TYPE == "DTA-2115B":

                signal_upper_band = new_dict_sky_py['Signals_UpperLBand_dta_2115']
                signal_lower_band = new_dict_sky_py['Signals_LowerLBand_dta_2115']
                signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_dta_2115']
                signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_dta_2115']

                # Change configuration before starting the simulation
                if not signal_upper_band:
                    pass
                else:

                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId"))
                    dta_2115_upper_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + ", " + '""' + "," + '""' + ", " + "True," + '"uniqueId"' + "))"
                    self.python_script.write(dta_2115_upper_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000, "UpperL", signal_upper_band, 50, 
                    # True, "uniqueId", None))
                    dta_2115_upper_signals_str = "sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000," + '"UpperL"' + ", " + '"' + str(
                        signal_upper_band) + '"' + ", " + str(
                        gain_dta) + ", " + gaussian_noise_str_py + ", " + '"uniqueId"' + ", " + "None" + "))"
                    self.python_script.write(dta_2115_upper_signals_str)
                    self.python_script.write("\n")

                if not signal_lower_band:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId2"))
                    dta_2115_lower_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + ", " + '""' + ", " + '""' + ", " + "True," + '"uniqueId2"' + "))"
                    self.python_script.write(dta_2115_lower_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000, "LowerL", signal_lower_band, 50, 
                    # True, "uniqueId2", None))
                    dta_2115_lower_signals_str = "sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000," + '"LowerL"' + ", " + '"' + str(
                        signal_lower_band) + '"' + ", " + str(
                        gain_dta) + ", " + gaussian_noise_str_py + ", " + '"uniqueId2"' + ", " + "None" + "))"
                    self.python_script.write(dta_2115_lower_signals_str)
                    self.python_script.write("\n")

                # Change configuration before starting the simulation
                if not signal_lower_band2:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId3"))
                    dta_2115_lower2_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + ", " + '""' + ", " + '""' + ", " + "True," + '"uniqueId3"' + "))"
                    self.python_script.write(dta_2115_lower2_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000, "LowerL", signal_lower_band2, 50,
                    # True, "uniqueId3", None))
                    dta_2115_lower2_signals_str = "sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000," + '"LowerL"' + "," + '"' + str(
                        signal_lower_band2) + '"' + ", " + str(
                        gain_dta) + ", " + gaussian_noise_str_py + ", " + '"uniqueId3"' + ", " + "None" + "))"
                    self.python_script.write(dta_2115_lower2_signals_str)
                    self.python_script.write("\n")

                # Change configuration before starting the simulation
                if not signal_lower_band_E6:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId4"))
                    dta_2116_lower_e6_modulation_str = "sim.callconvert(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + ", " + '""' + ", " + '""' + ", " + "True, " + '"uniqueId4"' + "))"
                    self.python_script.write(dta_2116_lower_e6_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band_E6, 0,
                    # False, "uniqueId4", None))
                    dta_2116_lower_e6_signals_str = "sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000," + '"LowerL"' + "," + '"' + str(
                        signal_lower_band_E6) + '"' + ", " + str(
                        gain_dta) + ", " + gaussian_noise_str_py + ", " + '"uniqueId4"' + ", " + "None" + "))"
                    self.python_script.write(dta_2116_lower_e6_signals_str)
                    self.python_script.write("\n")

            elif RADIO_TYPE == "DTA-2116":
                signal_upper_band = new_dict_sky_py['Signals_UpperLBand_dta_2116']
                signal_lower_band = new_dict_sky_py['Signals_LowerLBand_dta_2116']
                signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_dta_2116']
                signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_dta_2116']

                # ChangeModulationTargetSignals(0, 12500000, 125000000, "UpperL", "L1CA", 50, True, 
                # "{351cf00f-e6fe-4b27-b44a-3d6cf0a99c40}", None) Change configuration before starting the simulation

                if not signal_upper_band:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId"))
                    dta_2116_upper_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + "," + '""' + "," + '""' + "," + "True" + "," + '"uniqueId"' + "))"
                    self.python_script.write(dta_2116_upper_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000, "UpperL", signal_upper_band, 50, 
                    # True, "uniqueId", None))
                    dta_2116_upper_signals_str = "sim.call(ChangeModulationTargetSignals(0, 12500000, 125000000," + '"UpperL"' + "," + '"' + str(
                        signal_upper_band) + '"' + "," + str(
                        self.ui.skydel_rad_edit.text()) + "," + gaussian_noise_str_py + "," + '"uniqueId"' + ", None" + "))"
                    self.python_script.write(dta_2116_upper_signals_str)
                    self.python_script.write("\n")

                if not signal_lower_band:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId2"))
                    dta_2116_lower_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + "," + '""' + "," + '""' + "," + "True," + '"uniqueId1"' + "))"
                    self.python_script.write(dta_2116_lower_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000, "LowerL", signal_lower_band, 50, 
                    # True, "uniqueId2", None))
                    dta_2116_lower_signals_str = "sim.call(ChangeModulationTargetSignals(0, 12500000, 125000000," + '"LowerL"' + "," + '"' + str(
                        signal_lower_band) + '"' + "," + str(
                        gain_dta) + ", " + gaussian_noise_str_py + ", " + '"uniqueId1"' + ", " + "None" + "))"
                    self.python_script.write(dta_2116_lower_signals_str)
                    self.python_script.write("\n")

                # Change configuration before starting the simulation
                if not signal_lower_band2:
                    pass
                else:

                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId3"))
                    dta_2116_lower2_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + ", " + '""' + ", " + '""' + ", " + "True," + '"uniqueId2"' + "))"
                    self.python_script.write(dta_2116_lower2_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000, "LowerL", signal_lower_band2, 50,
                    # True, "uniqueId3", None))
                    dta_2116_lower2_signals_str = "sim.call(ChangeModulationTargetSignals(0, 12500000, 125000000," + '"LowerL"' + "," + '"' + str(
                        signal_lower_band2) + '"' + ", " + str(
                        gain_dta) + ", " + gaussian_noise_str_py + '"' + ", " + '"uniqueId2"' + ", " + "None" + "))"
                    self.python_script.write(dta_2116_lower2_signals_str)
                    self.python_script.write("\n")

                if not signal_lower_band_E6:
                    pass
                else:
                    # sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId3"))
                    dta_2116_lower_e6_modulation_str = "sim.call(SetModulationTarget(" + '"' + str(
                        RADIO_TYPE) + '"' + "," + '""' + "," + '""' + "," + "True," + '"uniqueId3"' + "))"
                    self.python_script.write(dta_2116_lower_e6_modulation_str)
                    self.python_script.write("\n")

                    # sim.call(ChangeModulationTargetSignals(0, 1250000, 85000000, "LowerL", signal_lower_band2, 50,
                    # True, "uniqueId3", None))
                    dta_2116_lower_e6_signals_str = "sim.call(ChangeModulationTargetSignals(0, 12500000, 125000000," + '"LowerL"' + "," + '"' + str(
                        signal_lower_band_E6) + '"' + ", " + str(
                        gain_dta) + ", " + '"' + gaussian_noise_str_py + '"' + ", " + '"uniqueId3"' + ", " + "None" + "))"
                    self.python_script.write(dta_2116_lower_e6_signals_str)
                    self.python_script.write("\n")

            else:
                pass

            self.python_script.close()

        except PermissionError as perm_err:
            print(perm_err)

    def playback_skydel_mainFunction(self):

        global tropo_model_skydel, antenna_type
        RADIO_TYPE = self.ui.comboBox_play_sdel.currentText()

        scen_func = ScenFunction()

        if not self.scen_file_item:
            QMessageBox.about(self, "GSG5/6 Scenarios",
                              "No .scen file was selected. Please go to the page Load GSG5/6 scenarios to load .scen "
                              "file.")
        else:
            self.scen_dict_py = scen_func.scen_main(self.scen_file_item, RADIO_TYPE)

        cnt_line = 0
        cnt_no_track = 0

        if not self.ui.skydel_rad_edit_2:
            # if self.ui.comboBox_skydel_conv.currentText() == "NoneRT":
            #     self.ui.skydel_rad_edit.setText(str(0))
            if self.ui.comboBox_play_sdel.currentText() == "DTA-2116":
                self.ui.skydel_rad_edit_2.setText(str(50))
            if self.ui.comboBox_play_sdel.currentText() == "DTA-2115B":
                self.ui.skydel_rad_edit_2.setText(str(50))

        gain_dta = self.ui.skydel_rad_edit_2.text()

        if not gain_dta:
            # if self.ui.comboBox_skydel_conv.currentText() == "NoneRT":
            #     self.ui.skydel_rad_edit.setText(str(0))
            if RADIO_TYPE == "DTA-2116":
                self.ui.skydel_rad_edit.setText(str(50))
                gain_dta = "50"
            if RADIO_TYPE == "DTA-2115B":
                self.ui.skydel_rad_edit.setText(str(50))
                gain_dta = "50"

        try:
            # Connect to Skydel
            self.sim = skydelsdx.RemoteSimulator(True)
            self.sim.connect()
            self.sim.call(New(True, True))

            # Sart Time
            new_dict_sky_py = self.scen_dict_py[0]
            date_time = new_dict_sky_py["startTime"]
            start_time_str = "sim.call(SetGpsStartTime(datetime(" + str(date_time[0]) + "," + str(
                date_time[1]) + "," + str(date_time[2]) + "," + str(date_time[3]) + "," + str(date_time[4]) + "," + str(
                date_time[5]) + ")))"
            self.ui.plainTextEdit.insertPlainText("-->" + start_time_str)
            self.ui.plainTextEdit.insertPlainText("\n")
            self.sim.call(SetGpsStartTime(
                datetime.datetime(int(date_time[0]), int(date_time[1]), int(date_time[2]), int(date_time[3]),
                                  int(date_time[4]), int(date_time[5]))))

            # Duration
            duration = new_dict_sky_py["Duration"]
            duration_str = "sim.call(SetDuration(" + str(duration) + "))"
            self.ui.plainTextEdit.insertPlainText("-->" + duration_str)
            self.ui.plainTextEdit.insertPlainText("\n")
            self.sim.call(SetDuration(int(duration)))

            duration_mode = new_dict_sky_py["DurationMode"]
            if duration_mode == 2:  # Forever
                duration_str = "sim.call(SetDuration(" + 0 + "))"
                self.ui.plainTextEdit.insertPlainText("-->" + duration_str)
                self.ui.plainTextEdit.insertPlainText("\n")
                self.sim.call(SetDuration(0))

            # Start Position
            start_pos = new_dict_sky_py["Startpos"]
            start_pos_str = "sim.call(SetVehicleTrajectoryFix(" + '"' + str(start_pos[0]) + '"' + "," + str(
                start_pos[1]) + "," + str(
                start_pos[2]) + "," + str(start_pos[3]) + "," + str(start_pos[4]) + "," + str(start_pos[5]) + "," + str(
                start_pos[6]) + "))"
            self.ui.plainTextEdit.insertPlainText("-->" + start_pos_str)
            self.ui.plainTextEdit.insertPlainText("\n")
            self.sim.call(SetVehicleTrajectoryFix("Fix", float(start_pos[1]), float(start_pos[2]), float(start_pos[3]),
                                                  float(start_pos[4]), float(start_pos[5]), float(start_pos[6])))

            # {"CmdName": "SetTropoModel", "CmdUuid": "{dbdd2ec6-9cc4-4435-8c0d-645114473137}", "Model": "Saastamoinen"}

            tropo_model = new_dict_sky_py["TropoModel"]

            if tropo_model == "Saastamoinen":
                tropo_model_skydel = "Saastamoinen"

            elif tropo_model == "STANAG":
                tropo_model_skydel = "Stanag"

            elif tropo_model == "DO-229":
                tropo_model_skydel = "DO-229"

            elif tropo_model == "Off":
                tropo_model_skydel = "None"

            else:
                pass

            tropo_model_str = "sim.call(SetTropoModel(" + '"' + str(tropo_model_skydel) + '"' + "))"
            self.ui.plainTextEdit.insertPlainText("-->" + tropo_model_str)
            self.ui.plainTextEdit.insertPlainText("\n")
            self.sim.call(SetTropoModel(str(tropo_model_skydel)))

            iono_model = new_dict_sky_py["IonoModel"]

            if str(iono_model) == "1":
                iono_model_skydel = "sim.call(SetIonoModel(" + "Klobuchar" + "))"
                self.ui.plainTextEdit.insertPlainText("-->" + iono_model_skydel)
                self.ui.plainTextEdit.insertPlainText("\n")
                self.sim.call(SetIonoModel("Klobuchar"))

            elif str(iono_model) == "Off":
                iono_model_skydel = "sim.call(SetIonoModel(" + "None" + "))"
                self.ui.plainTextEdit.insertPlainText("-->" + iono_model_skydel)
                self.ui.plainTextEdit.insertPlainText("\n")
                self.sim.call(SetIonoModel("None"))

            # {"CmdName": "SetVehicleAntennaGainCSV", "CmdUuid": "{4caa0fed-04ef-47bb-85be-78c3dea41e36}",
            # "FilePath": "C:/Users/Jean-Grace Oulai/Documents/Skydel-SDX/Templates/Antennas/Zero Antenna pattern.csv",
            # "Type": 2, "Band": 0, "Name": "Basic Antenna"}
            antenna_model = new_dict_sky_py["AntennaModel"]
            os.path.abspath(os.getcwd())
            current_dir = str(os.path.abspath(os.getcwd()))
            current_dir = current_dir.replace('\\', "/")
            os.path.abspath(os.getcwd())
            current_dir = str(os.path.abspath(os.getcwd()))
            current_dir = current_dir.replace('\\', "/")

            if antenna_model == "Cardioid":
                antenna_type = str(current_dir) + "/" + "Antenna/Cardioid.csv"

            elif antenna_model == "GPS-703-GG":
                antenna_type = str(current_dir) + "/" + "Antenna/GPS703GGG.csv"

            elif antenna_model == "Helix":
                antenna_type = str(current_dir) + "/" + "Antenna/Helix.csv"

            elif antenna_model == "Patch":
                antenna_type = str(current_dir) + "/" + "Antenna/Helix.csv"

            elif antenna_model == "Zero":
                antenna_type = str(current_dir) + "/" + "Antenna/ZeroModel.csv"

            else:
                pass

            self.sim.call(
                SetVehicleAntennaGainCSV(antenna_type, AntennaPatternType.Custom, GNSSBand.L1, "Basic Antenna"))

            self.sim.call(
                SetVehicleAntennaGainCSV(antenna_type, AntennaPatternType.Custom, GNSSBand.L2, "Basic Antenna"))

            self.sim.call(
                SetVehicleAntennaGainCSV(antenna_type, AntennaPatternType.Custom, GNSSBand.L5, "Basic Antenna"))

            self.sim.call(
                SetVehicleAntennaGainCSV(antenna_type, AntennaPatternType.Custom, GNSSBand.E6, "Basic Antenna"))

            lever_arm_param = new_dict_sky_py["LeverArm"]

            if not lever_arm_param:
                pass
            else:
                lever_arm_x = lever_arm_param[0]
                lever_arm_y = lever_arm_param[1]
                lever_arm_z = lever_arm_param[2]

                print(" Lever Arm:", lever_arm_param)

                lever_arm_str = "SetVehicleAntennaOffset(" + str(lever_arm_x) + ", " + str(lever_arm_y) + ", " + str(
                    lever_arm_z) + ", " + "0" + ", " + "0" + ", " + "0" + ", " + '"Basic Antenna"' + ")"
                self.ui.plainTextEdit.insertPlainText("-->" + lever_arm_str)
                self.ui.plainTextEdit.insertPlainText("\n")
                self.sim.call(
                    SetVehicleAntennaOffset(float(lever_arm_x), float(lever_arm_y), float(lever_arm_z), 0, 0, 0,
                                            "Basic Antenna"))

            # SetElevationMaskBelow(0.174532925199433336)
            elevation_mask = new_dict_sky_py["ElevationMask"]
            elevation_mask_str = "sim.call(SetElevationMaskBelow(" + str(elevation_mask) + "))"

            self.sim.call(SetElevationMaskBelow(elevation_mask))
            self.ui.plainTextEdit.insertPlainText("-->" + elevation_mask_str)
            self.ui.plainTextEdit.insertPlainText("\n")

            start_pos = new_dict_sky_py["Startpos"]

            start_pos_lat = start_pos[1]
            start_pos_long = start_pos[2]
            start_pos_alt = start_pos[3]
            # start_pos_yaw = start_pos[4]
            # start_pos_pitch = start_pos[5]
            # start_pos_roll = start_pos[6]
            ecef_pos = Lla(start_pos_lat, start_pos_long, start_pos_alt).toEcef()
            ecef_pos_x = ecef_pos.x
            ecef_pos_y = ecef_pos.y
            ecef_pos_z = ecef_pos.z

            self.sim.call(SetVehicleTrajectoryFixEcef("Fix", ecef_pos_x, ecef_pos_y, ecef_pos_z, 0, 0, 0))

            traj_type = new_dict_sky_py['UserTrajectory']

            if str(traj_type) == "Static" or str(traj_type) == "3GPP":
                pass
            elif str(traj_type) == "Circle":
                circle_param = new_dict_sky_py['CircleParam']
                circle_diam = circle_param[0]
                circle_radius = circle_diam / 2
                circle_speed = circle_param[1]
                circle_motion = circle_param[2]

                self.sim.call(SetVehicleTrajectoryCircular("Circular", start_pos_lat, start_pos_long, start_pos_alt,
                                                           int(circle_radius), int(circle_speed), circle_motion, 0))
                circle_traj_str = "SetVehicleTrajectoryCircular(" + '"Circular"' + ", " + str(start_pos_lat) + ", "
                + str(start_pos_long) + ", " + str(start_pos_alt) + ", " + str(circle_radius) + ", " + str(circle_speed)
                + ", " + str(circle_motion) + ", " + "0" + ")"
                self.ui.plainTextEdit.insertPlainText("-->" + circle_traj_str)
                self.ui.plainTextEdit.insertPlainText("\n")

            elif str(traj_type) == "NmeaFile":
                if self.nmea_file_item:
                    traj_file = self.create_nmea_traj(self.nmea_file_item, self.GSG56_scenarios)
                    check_traj_empty = open(traj_file, encoding='utf-8')
                    lines = check_traj_empty.readlines()

                    len_lines = len(lines)

                    if len_lines == 1:
                        pass
                    else:
                        print(
                            "NO RMC file was found, Change the time in the Skydel instance or Skydel will start at "
                            "the default time")
                        self.sim.call(SetVehicleTrajectory("Track"))

                        def pushTrackNode(sim, timestampSec, latDeg, lonDeg, altMet):
                            sim.pushTrackLla(timestampSec, Lla(toRadian(latDeg), toRadian(lonDeg), altMet))

                        with open(traj_file, "r") as f:
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
                                    try:
                                        pushTrackNode(self.sim, int(float(line[0])), float(line[2]), float(line[3]),
                                                      float(line[4]))
                                    except ValueError as val_er_10:
                                        print(val_er_10)

                            self.sim.endTrackDefinition()

                        if cnt_no_track == cnt_line and cnt_line != 0:
                            QMessageBox.about(self, "SKYDEL TRAJECTORY",
                                              "The trajectory file is empty. No trajectory was set on Skydel.")
                        else:
                            QMessageBox.about(self, "SKYDEL SIGNAL",
                                              "The trajectory is ready. Please select your signals in Skydel and press the Arm/STart button.")
                else:
                    QMessageBox.about(self, "MISSING NMEA FILE ERROR",
                                      "An NMEA file was expected, but it was not found in the selected folder. Therefore the default vehicle position will be applied. You can put the NMEA file in the same folder as your current scenario and restart the converter.")

            # else:
            #     traj_file_name = new_dict_sky_py["TrajFile"]

            if RADIO_TYPE == "NoneRT" or RADIO_TYPE == "None":
                signal_upper_band = new_dict_sky_py['Signals_UpperLBand_none']
                signal_lower_band = new_dict_sky_py['Signals_LowerLBand_none']
                signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_none']
                signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_none']

                # Change configuration before starting the simulation
                if signal_upper_band != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "UpperL", signal_upper_band, -1, False,
                                                      "uniqueId", None))

                # Change configuration before starting the simulation
                if signal_lower_band != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId2"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band, 0, False,
                                                      "uniqueId2", None))

                # Change configuration before starting the simulation
                if signal_lower_band2 != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId3"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band2, 0, False,
                                                      "uniqueId3", None))

                # Change configuration before starting the simulation
                if signal_lower_band_E6 != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId4"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band_E6, 0, False,
                                                      "uniqueId4", None))

            if RADIO_TYPE == "DTA-2115B":
                signal_upper_band = new_dict_sky_py['Signals_UpperLBand_dta_2115']
                signal_lower_band = new_dict_sky_py['Signals_LowerLBand_dta_2115']
                signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_dta_2115']
                signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_dta_2115']

                # Change configuration before starting the simulation
                if signal_upper_band != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 85000000, "UpperL", signal_upper_band, int(gain_dta),
                                                      True,
                                                      "uniqueId", None))

                if signal_lower_band != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId2"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 85000000, "LowerL", signal_lower_band, int(gain_dta),
                                                      True,
                                                      "uniqueId2", None))

                # Change configuration before starting the simulation
                if signal_lower_band2 != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId3"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 85000000, "LowerL", signal_lower_band2, int(gain_dta),
                                                      True,
                                                      "uniqueId3", None))

                # Change configuration before starting the simulation
                if signal_lower_band_E6 != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId4"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band_E6,
                                                      int(gain_dta), False,
                                                      "uniqueId4", None))

            if RADIO_TYPE == "DTA-2116":
                signal_upper_band = new_dict_sky_py['Signals_UpperLBand_dta_2116']
                signal_lower_band = new_dict_sky_py['Signals_LowerLBand_dta_2116']
                signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_dta_2116']
                signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_dta_2116']

                # ChangeModulationTargetSignals(0, 12500000, 125000000, "UpperL", "L1CA", 50, True, 
                # "{351cf00f-e6fe-4b27-b44a-3d6cf0a99c40}", None)

                # Change configuration before starting the simulation
                if signal_upper_band != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 85000000, "UpperL", signal_upper_band, int(gain_dta),
                                                      True,
                                                      "uniqueId", None))

                if signal_lower_band != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId2"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band, int(gain_dta),
                                                      True,
                                                      "uniqueId2", None))

                # Change configuration before starting the simulation
                if signal_lower_band2 != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId3"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 125000000, "LowerL", signal_lower_band2,
                                                      int(gain_dta), True,
                                                      "uniqueId3", None))

                if signal_lower_band_E6 != "":
                    self.sim.call(SetModulationTarget(RADIO_TYPE, "", "", True, "uniqueId3"))

                    self.sim.call(
                        ChangeModulationTargetSignals(0, 1250000, 85000000, "LowerL", signal_lower_band2, int(gain_dta),
                                                      True,
                                                      "uniqueId3", None))

        except ConnectionRefusedError as skydel_connect_err:
            QMessageBox.about(self, "SKYDEL ERROR",
                              str(skydel_connect_err) + ". Please make sure that a new Skydel instance is open and try again.")

    def create_skydel_sdx(self, scen_dict):

        global tropo_model_skydel, antenna_type
        antenna_type = ""
        self.sdx_script_name = self.save_folder + "/" + 'skydel_sdx' + '.sdxscript'
        self.sdx_script = open(self.sdx_script_name, 'w', newline='')
        # self.sdx_script.write("#!/usr/bin/python")
        # self.sdx_script.write("\n")
        # self.sdx_script.write("# This Python script has been generated by the SKYDEL GNSS simulator")
        # self.sdx_script.write("\n")
        # self.sdx_script.write("from datetime import datetime")
        # self.sdx_script.write("\n")
        # self.sdx_script.write("from skydelsdx import *")
        # self.sdx_script.write("\n")
        # self.sdx_script.write("from skydelsdx.commands import *")
        # self.sdx_script.write("\n")
        # self.sdx_script.write("\n")
        # self.sdx_script.write("sim = RemoteSimulator(True)")
        # self.sdx_script.write("\n")
        # self.sdx_script.write("sim.connect()")
        # self.sdx_script.write("\n")
        # self.sdx_script.write("sim.call(New(True, True))")
        # self.sdx_script.write("\n")
        # {"CmdName": "New","CmdUuid": "{c97c2537-0ae8-4586-8fc0-bc2e72f94cb1}","DiscardCurrentConfig": true,"LoadDefaultConfig": true}
        script_header_sdr = "{" + '"CmdName": ' + '"New",' + '"CmdUuid": ' + '"{id_}"' + "," + '"DiscardCurrentConfig": ' + "true" + "," + '"LoadDefaultConfig": ' + "true" + "}"
        self.sdx_script.write(script_header_sdr)
        self.sdx_script.write("\n")

        RADIO_TYPE = self.ui.comboBox_skydel_conv.currentText()

        gain_dta = self.ui.skydel_rad_edit.text()

        if not gain_dta:
            # if self.ui.comboBox_skydel_conv.currentText() == "NoneRT":
            #     self.ui.skydel_rad_edit.setText(str(0))
            if self.ui.comboBox_skydel_conv.currentText() == "DTA-2116":
                self.ui.skydel_rad_edit.setText(str(50))
                gain_dta = "50"

            if self.ui.comboBox_skydel_conv.currentText() == "DTA-2115B":
                self.ui.skydel_rad_edit.setText(str(50))
                gain_dta = "50"

        if self.ui.skydel_GN_checkBox.isChecked():
            GAUSSIAN_NOISE = True
            gaussian_noise_str = "true"
            gaussian_noise_str_py = "True"
        else:
            GAUSSIAN_NOISE = False
            gaussian_noise_str = "false"
            gaussian_noise_str_py = "False"

        scen_func = ScenFunction()
        self.scen_dict_py = scen_func.scen_main(self.scen_file_item, RADIO_TYPE)

        # {"CmdName": "SetGpsStartTime", "CmdUuid": "{53d917bd-3e67-4ea9-8f72-338bf0e5b9fa}",
        # "Start": {"Day": 24, "Hour": 12, "Minute": 0, "Month": 6, "Second": 0, "Spec": "UTC", "Year": 2020}}
        new_dict_sky_py = self.scen_dict_py[0]
        date_time = new_dict_sky_py["startTime"]

        start_time_str = "{" + '"CmdName"' + ": " + '"SetGpsStartTime"' + ", " + '"CmdUuid"' + ": " + '"{my_id_1}"' + \
                         ", " + '"Start"' + ": { " + '"Day"' + ": " + str(date_time[2]) + ", " + '"Hour": ' + \
                         str(date_time[3]) + ", " + '"Minute": ' + str(date_time[4]) + ", " + '"Month": ' + \
                         str(date_time[1]) + ", " + '"Second": ' + str(
            date_time[5]) + ", " + '"Spec": ' + '"UTC"' + ", " + '"Year": ' + str(date_time[0]) + "}}"

        # self.python_script.write(str(sim.call(SetGpsStartTime(date_time))))
        self.sdx_script.write(start_time_str)
        self.sdx_script.write("\n")

        # {"CmdName": "SetDuration","CmdUuid": "{a2f79ab3-8eea-4552-b1de-28a192fc8589}","Second": 60}
        duration = new_dict_sky_py["Duration"]
        duration_str = "{" + '"CmdName": ' + '"SetDuration"' + "," + '"CmdUuid": ' + '"{my_id_2}"' + "," + '"Second": ' + str(
            duration) + "}"
        self.sdx_script.write(duration_str)
        self.sdx_script.write("\n")

        # {"CmdName": "SetElevationMaskBelow","CmdUuid": "{304c99d1-4f75-47ff-89ae-410bc7a12ab5}","Angle": 0.0017453292519943335}
        elevation_mask = new_dict_sky_py["ElevationMask"]
        elevation_mask_str = "{" + '"CmdName": ' + '"SetElevationMaskBelow"' + "," + '"CmdUuid": ' + '"{my_id_elevation_mask}"' + "," + '"Angle": ' + str(
            elevation_mask) + "}"
        self.sdx_script.write(elevation_mask_str)
        self.sdx_script.write("\n")

        duration_mode = new_dict_sky_py["DurationMode"]
        if duration_mode == 2:  # Forever
            duration_mode_str = "{" + '"CmdName": ' + '"SetDuration", ' + '"CmdUuid": ' + '"{7my_id_60}"' + ", " + '"Second": ' + "0" + "}"
            self.sdx_script.write(duration_mode_str)
            self.sdx_script.write("\n")
        # {"CmdName": "SetTropoModel", "CmdUuid": "{dbdd2ec6-9cc4-4435-8c0d-645114473137}", "Model": "Saastamoinen"}

        tropo_model = new_dict_sky_py["TropoModel"]

        if tropo_model == "Saastamoinen":
            tropo_model_skydel = "Saastamoinen"

        elif tropo_model == "STANAG":
            tropo_model_skydel = "Stanag"

        elif tropo_model == "DO-229":
            tropo_model_skydel = "DO-229"

        elif tropo_model == "Off":
            tropo_model_skydel = "None"

        else:
            pass

        tropo_model_str = "{" + '"CmdName": ' + '"SetTropoModel"' + "," + '"CmdUuid": ' + '"{my_id_30}"' + "," + '"Model": ' + '"' + str(
            tropo_model_skydel) + '"' + "}"
        self.sdx_script.write(tropo_model_str)
        self.sdx_script.write("\n")

        iono_model = new_dict_sky_py["IonoModel"]

        if str(iono_model) == "1":
            iono_model_str = "{" + '"CmdName": ' + '"SetIonoModel"' + "," + '"CmdUuid": ' + '"{my_id_31}"' + "," + '"Model": ' + '"' + "Klobuchar" + '"' + "}"
            self.sdx_script.write(iono_model_str)
            self.sdx_script.write("\n")

        elif str(iono_model) == "Off":
            iono_model_str = "{" + '"CmdName": ' + '"SetIonoModel"' + "," + '"CmdUuid": ' + '"{my_id_31}"' + "," + '"Model": ' + "None" + "}"
            self.sdx_script.write(iono_model_str)
            self.sdx_script.write("\n")

        # {"CmdName": "SetVehicleAntennaGainCSV", "CmdUuid": "{4caa0fed-04ef-47bb-85be-78c3dea41e36}",
        # "FilePath": "C:/Users/Jean-Grace Oulai/Documents/Skydel-SDX/Templates/Antennas/Zero Antenna pattern.csv",
        # "Type": 2, "Band": 0, "Name": "Basic Antenna"}
        antenna_model = new_dict_sky_py["AntennaModel"]
        os.path.abspath(os.getcwd())
        # current_dir = pathlib.Path().resolve()
        current_dir = str(os.path.abspath(os.getcwd()))
        current_dir = current_dir.replace('\\', "/")
        os.path.abspath(os.getcwd())
        # current_dir = pathlib.Path().resolve()
        current_dir = str(os.path.abspath(os.getcwd()))
        current_dir = current_dir.replace('\\', "/")

        if antenna_model == "Cardioid":
            antenna_type = str(current_dir) + "/" + "Antenna/Cardioid.csv"

        elif antenna_model == "GPS-703-GG":
            antenna_type = str(current_dir) + "/" + "Antenna/GPS703GGG.csv"

        elif antenna_model == "Helix":
            antenna_type = str(current_dir) + "/" + "Antenna/Helix.csv"

        elif antenna_model == "Patch":
            antenna_type = str(current_dir) + "/" + "Antenna/Helix.csv"

        elif antenna_model == "Zero":
            antenna_type = str(current_dir) + "/" + "Antenna/ZeroModel.csv"

        else:
            pass

        antenna_L1_str = "{" + '"CmdName": ' + '"SetVehicleAntennaGainCSV",' + '"CmdUuid": ' + '"{my_id_20}",' + '"FilePath": ' + '"' + antenna_type + '"' + "," + '"Type": ' + '2,' + '"Band": ' + "0" + "," + '"Name": ' + '"Basic Antenna"' + "}"
        self.sdx_script.write(antenna_L1_str)
        self.sdx_script.write("\n")

        antenna_L2_str = "{" + '"CmdName": ' + '"SetVehicleAntennaGainCSV",' + '"CmdUuid": ' + '"{my_id_21}",' + '"FilePath": ' + '"' + antenna_type + '"' + "," + '"Type": ' + '2,' + '"Band": ' + "1" + "," + '"Name": ' + '"Basic Antenna"' + "}"
        self.sdx_script.write(antenna_L2_str)
        self.sdx_script.write("\n")

        antenna_L5_str = "{" + '"CmdName": ' + '"SetVehicleAntennaGainCSV",' + '"CmdUuid": ' + '"{my_id_22}",' + '"FilePath": ' + '"' + antenna_type + '"' + "," + '"Type": ' + '2,' + '"Band": ' + "2" + "," + '"Name": ' + '"Basic Antenna"' + "}"
        self.sdx_script.write(antenna_L5_str)
        self.sdx_script.write("\n")

        antenna_L6_str = "{" + '"CmdName": ' + '"SetVehicleAntennaGainCSV",' + '"CmdUuid": ' + '"{my_id_23}",' + '"FilePath": ' + '"' + antenna_type + '"' + "," + '"Type": ' + '2,' + '"Band": ' + "3" + "," + '"Name": ' + '"Basic Antenna"' + "}"
        self.sdx_script.write(antenna_L6_str)
        self.sdx_script.write("\n")

        lever_arm_param = new_dict_sky_py["LeverArm"]

        if not lever_arm_param:
            pass
        else:
            lever_arm_x = lever_arm_param[0]
            lever_arm_y = lever_arm_param[1]
            lever_arm_z = lever_arm_param[2]

            lever_arm_str = "{" + '"CmdName": ' + '"SetVehicleAntennaOffset"' + ", " + '"CmdUuid": ' + '"{my_id_60}"' + ", " + '"X": ' + str(
                lever_arm_x) + ", " + '"Y": ' + str(lever_arm_y) + ", " + '"Z": ' + str(lever_arm_z) \
                            + ", " + '"Yaw": ' + "0, " + '"Pitch": ' + "0, " + '"Roll": ' + "0, " + '"Name": ' + '"Basic Antenna"' + "}"

            self.sdx_script.write(lever_arm_str)
            self.sdx_script.write("\n")

        # {"CmdName": "SetVehicleTrajectory", "CmdUuid": "{ee865e1a-36ad-4077-89c6-d5933e370509}", "Type": "Fix"}
        # {"CmdName": "SetVehicleTrajectoryFixEcef", "CmdUuid": "{efb82982-361b-4804-bff4-f54c92e2c638}", "Type": "Fix",
        # "X": 1321269.878070516, "Y": -4066450.551903221, "Z": 4716877.816405115, "Yaw": 0, "Pitch": 0, "Roll": 0}
        pos_type_str = "{" + '"CmdName": ' + '"SetVehicleTrajectory"' + ", " + '"CmdUuid": ' + "{ee865e1a-36ad-4077-89c6-d5933e370509}" + ", " + '"Type": ' + '"Fix"}'

        start_pos = new_dict_sky_py["Startpos"]

        start_pos_lat = start_pos[1]
        start_pos_long = start_pos[2]
        start_pos_alt = start_pos[3]
        # start_pos_yaw = start_pos[4]
        # start_pos_pitch = start_pos[5]
        # start_pos_roll = start_pos[6]
        ecef_pos = Lla(start_pos_lat, start_pos_long, start_pos_alt).toEcef()
        ecef_pos_x = ecef_pos.x
        ecef_pos_y = ecef_pos.y
        ecef_pos_z = ecef_pos.z

        start_pos_str = "{" + '"CmdName": ' + '"SetVehicleTrajectoryFixEcef"' + ", " + '"CmdUuid": ' + '"{my_id_3}"' \
                        + ", " + '"Type": ' + '"Fix",' + '"X": ' + str(ecef_pos_x) + "," + '"Y": ' + str(
            ecef_pos_y) + "," + '"Z": ' + str(ecef_pos_z) + "," + '"Yaw": ' + str(
            start_pos[4]) + "," + '"Pitch": ' + str(start_pos[5]) + "," + '"Roll": ' + str(start_pos[6]) + "}"

        self.sdx_script.write(start_pos_str)
        self.sdx_script.write("\n")

        # Trajectory type
        traj_type = new_dict_sky_py['UserTrajectory']

        if str(traj_type) == "Static" or str(traj_type) == "3GPP":
            pass
        elif str(traj_type) == "Circle":
            circle_param = new_dict_sky_py['CircleParam']
            circle_diam = circle_param[0]

            circle_radius = circle_diam
            circle_speed = circle_param[1]
            circle_motion = circle_param[2]

            circle_traj_str = "{" + '"CmdName": ' + '"SetVehicleTrajectoryCircular"' + "," + '"CmdUuid": ' + \
                              '"{my_id_50}"' + "," + '"Type": ' + '"Circular"' + "," + '"Lat": ' + str(start_pos_lat) \
                              + "," + '"Lon": ' + str(start_pos_long) + "," + '"Alt": ' + str(start_pos_alt) + "," \
                              + '"Radius": ' + str(circle_radius) + \
                              "," + '"Speed": ' + str(circle_speed) + "," + '"Clockwise": ' + circle_motion + "," \
                              + '"OriginAngle": ' + "0}"

            self.sdx_script.write(circle_traj_str)
            self.sdx_script.write("\n")

        if RADIO_TYPE == "None":
            signal_upper_band = new_dict_sky_py['Signals_UpperLBand_none']
            signal_lower_band = new_dict_sky_py['Signals_LowerLBand_none']

            signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_none']

            signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_none']

            # Change configuration before starting the simulation
            if signal_upper_band != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                none_upper_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + '"{my_id_5}"' + "," + '"Type": ' + '"None"' + "," + '"Path": ' + '""' + "," + '"Address": ' + '""' + "," + \
                                            '"ClockIsExternal": ' + "true," + '"Id": ' + '"{my_id_6}"' + "}"
                self.sdx_script.write(none_upper_modulation_str)
                self.sdx_script.write("\n")

                none_upper_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                         + '"{my_id_7}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                         + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"UpperL",' + '"Signal": ' \
                                         + '"' + str(
                    signal_upper_band) + '"' + "," + '"Gain": ' + "0" + "," + '"GaussianNoise": ' \
                                         + "false" + "," + '"Id": ' + '"{my_id_6}"' + "}"
                self.sdx_script.write(none_upper_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation
            if signal_lower_band != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                none_lower_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                            '"{my_id_9}"' + "," + '"Type": ' + '"None"' + "," + '"Path": ' + '""' + "," \
                                            + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                            + '"{my_id_10}"' + "}"
                self.sdx_script.write(none_lower_modulation_str)
                self.sdx_script.write("\n")

                none_lower_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                         + '"{my_id_11}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                         + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"LowerL",' + '"Signal": ' \
                                         + '"' + str(
                    signal_lower_band) + '"' + "," + '"Gain": ' + "0" + "," + '"GaussianNoise": ' \
                                         + gaussian_noise_str + "," + '"Id": ' + '"{my_id_10}"' + "}"

                self.sdx_script.write(none_lower_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation
            if signal_lower_band2 != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                none_lower2_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                             '"{my_id_13}"' + "," + '"Type": ' + '"None"' + "," + '"Path": ' + '""' + "," \
                                             + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                             + '"{my_id_14}"' + "}"

                self.sdx_script.write(none_lower2_modulation_str)
                self.sdx_script.write("\n")

                none_lower2_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                          + '"{my_id_15}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                          + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"LowerL",' + '"Signal": ' \
                                          + '"' + str(
                    signal_lower_band2) + '"' + "," + '"Gain": ' + "0" + "," + '"GaussianNoise": ' \
                                          + gaussian_noise_str + "," + '"Id": ' + '"{my_id_14}"' + "}"

                self.sdx_script.write(none_lower2_signals_str)
                self.sdx_script.write("\n")

            # Change configuration before starting the simulation
            if signal_lower_band_E6 != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                none_lower_e6_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                               '"{my_id_13}"' + "," + '"Type": ' + '"None"' + "," + '"Path": ' + '""' + "," \
                                               + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                               + '"{my_id_14}"' + "}"

                self.sdx_script.write(none_lower_e6_modulation_str)
                self.sdx_script.write("\n")

                none_lower_e6_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                            + '"{my_id_15}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                            + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"UpperL",' + '"Signal": ' \
                                            + '"' + str(
                    signal_lower_band_E6) + '"' + "," + '"Gain": ' + "0" + "," + '"GaussianNoise": ' \
                                            + gaussian_noise_str + "," + '"Id": ' + '"{my_id_16}"' + "}"

                self.sdx_script.write(none_lower_e6_signals_str)
                self.sdx_script.write("\n")

        if RADIO_TYPE == "NoneRT":
            signal_upper_band = new_dict_sky_py['Signals_UpperLBand_none']
            signal_lower_band = new_dict_sky_py['Signals_LowerLBand_none']

            signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_none']

            signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_none']

            # Change configuration before starting the simulation
            if signal_upper_band != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                none_upper_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + '"{my_id_5}"' + "," + '"Type": ' + '"NoneRT"' + "," + '"Path": ' + '""' + "," + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' + '"{my_id_6}"' + "}"
                self.sdx_script.write(none_upper_modulation_str)
                self.sdx_script.write("\n")

                none_upper_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                         + '"{my_id_7}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                         + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"UpperL",' + '"Signal": ' \
                                         + '"' + str(
                    signal_upper_band) + '"' + "," + '"Gain": ' + "0" + "," + '"GaussianNoise": ' \
                                         + gaussian_noise_str + "," + '"Id": ' + '"{my_id_6}"' + "}"
                self.sdx_script.write(none_upper_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation
            if signal_lower_band != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                none_lower_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                            '"{my_id_9}"' + "," + '"Type": ' + '"NoneRT"' + "," + '"Path": ' + '""' + "," \
                                            + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                            + '"{my_id_10}"' + "}"
                self.sdx_script.write(none_lower_modulation_str)
                self.sdx_script.write("\n")

                none_lower_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                         + '"{my_id_11}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                         + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"LowerL",' + '"Signal": ' \
                                         + '"' + str(
                    signal_lower_band) + '"' + "," + '"Gain": ' + "0" + "," + '"GaussianNoise": ' \
                                         + gaussian_noise_str + "," + '"Id": ' + '"{my_id_10}"' + "}"

                self.sdx_script.write(none_lower_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation
            if signal_lower_band2 != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                none_lower2_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                             '"{my_id_13}"' + "," + '"Type": ' + '"NoneRT"' + "," + '"Path": ' + '""' + "," \
                                             + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                             + '"{my_id_14}"' + "}"

                self.sdx_script.write(none_lower2_modulation_str)
                self.sdx_script.write("\n")

                none_lower2_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                          + '"{my_id_15}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                          + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"LowerL",' + '"Signal": ' \
                                          + '"' + str(
                    signal_lower_band2) + '"' + "," + '"Gain": ' + "0" + "," + '"GaussianNoise": ' \
                                          + gaussian_noise_str + "," + '"Id": ' + '"{my_id_14}"' + "}"

                self.sdx_script.write(none_lower2_signals_str)
                self.sdx_script.write("\n")

            # Change configuration before starting the simulation
            if signal_lower_band_E6 != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                none_lower_e6_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                               '"{my_id_13}"' + "," + '"Type": ' + '"NoneRT"' + "," + '"Path": ' + '""' + "," \
                                               + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                               + '"{my_id_14}"' + "}"

                self.sdx_script.write(none_lower_e6_modulation_str)
                self.sdx_script.write("\n")

                none_lower_e6_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                            + '"{my_id_15}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                            + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"UpperL",' + '"Signal": ' \
                                            + '"' + str(
                    signal_lower_band_E6) + '"' + "," + '"Gain": ' + "0" + "," + '"GaussianNoise": ' \
                                            + gaussian_noise_str + "," + '"Id": ' + '"{my_id_16}"' + "}"

                self.sdx_script.write(none_lower_e6_signals_str)
                self.sdx_script.write("\n")

        if RADIO_TYPE == "DTA-2115B":  # PROBLEME CA ECRIT DES COMMANDES PYTHON ET NON DES JSON

            signal_upper_band = new_dict_sky_py['Signals_UpperLBand_dta_2115']
            signal_lower_band = new_dict_sky_py['Signals_LowerLBand_dta_2115']

            signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_dta_2115']

            signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_dta_2115']

            # Change configuration before starting the simulation
            if signal_upper_band != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                dta_2115b_upper_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + '"{my_id_5}"' + "," + '"Type": ' + '"DTA-2115B"' + "," + '"Path": ' + '""' + "," + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' + '"{my_id_6}"' + "}"
                self.sdx_script.write(dta_2115b_upper_modulation_str)
                self.sdx_script.write("\n")

                dta_2115b_upper_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                              + '"{my_id_7}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                              + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"UpperL",' + '"Signal": ' \
                                              + '"' + str(
                    signal_upper_band) + '"' + "," + '"Gain": ' + gain_dta + "," + '"GaussianNoise": ' \
                                              + gaussian_noise_str + "," + '"Id": ' + '"{my_id_6}"' + "}"
                self.sdx_script.write(dta_2115b_upper_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation

            if signal_lower_band != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                dta_2115b_lower_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                                 '"{my_id_9}"' + "," + '"Type": ' + '"DTA-2115B"' + "," + '"Path": ' + '""' + "," \
                                                 + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                                 + '"{my_id_10}"' + "}"
                self.sdx_script.write(dta_2115b_lower_modulation_str)
                self.sdx_script.write("\n")

                dta_2115b_lower_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                              + '"{my_id_11}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                              + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"LowerL",' + '"Signal": ' \
                                              + '"' + str(
                    signal_lower_band) + '"' + "," + '"Gain": ' + gain_dta + "," + '"GaussianNoise": ' \
                                              + gaussian_noise_str + "," + '"Id": ' + '"{my_id_10}"' + "}"

                self.sdx_script.write(dta_2115b_lower_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation
            if signal_lower_band2 != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                dta_2115b_lower2_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                                  '"{my_id_13}"' + "," + '"Type": ' + '"DTA-2115B"' + "," + '"Path": ' + '""' + "," \
                                                  + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                                  + '"{my_id_14}"' + "}"

                self.sdx_script.write(dta_2115b_lower2_modulation_str)
                self.sdx_script.write("\n")

                dta_2115b_lower2_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                               + '"{my_id_15}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                               + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"LowerL",' + '"Signal": ' \
                                               + '"' + str(
                    signal_lower_band2) + '"' + "," + '"Gain": ' + gain_dta + "," + '"GaussianNoise": ' \
                                               + gaussian_noise_str + "," + '"Id": ' + '"{my_id_14}"' + "}"

                self.sdx_script.write(dta_2115b_lower2_signals_str)
                self.sdx_script.write("\n")

            # Change configuration before starting the simulation
            if signal_lower_band_E6 != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                dta_2115b_lower_e6_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                                    '"{my_id_13}"' + "," + '"Type": ' + '"DTA-2115B"' + "," + '"Path": ' + '""' + "," \
                                                    + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                                    + '"{my_id_14}"' + "}"

                self.sdx_script.write(dta_2115b_lower_e6_modulation_str)
                self.sdx_script.write("\n")

                dta_2115b_lower_e6_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                                 + '"{my_id_15}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "1250000" \
                                                 + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"UpperL",' + '"Signal": ' \
                                                 + '"' + str(
                    signal_lower_band_E6) + '"' + "," + '"Gain": ' + gain_dta + "," + '"GaussianNoise": ' \
                                                 + gaussian_noise_str + "," + '"Id": ' + '"{my_id_16}"' + "}"

                self.sdx_script.write(dta_2115b_lower_e6_signals_str)
                self.sdx_script.write("\n")

        if RADIO_TYPE == "DTA-2116":
            signal_upper_band = new_dict_sky_py['Signals_UpperLBand_dta_2116']
            signal_lower_band = new_dict_sky_py['Signals_LowerLBand_dta_2116']

            signal_lower_band2 = new_dict_sky_py['Signals_LowerLBand2_dta_2116']
            signal_lower_band_E6 = new_dict_sky_py['Signals_LowerLBandE6_dta_2116']

            # Change configuration before starting the simulation
            if signal_upper_band != "":
                # {"CmdName": "SetModulationTarget", "CmdUuid": "{424cb15f-0768-482d-9194-de93c046e7f1}", 
                # "Type": "DTA-2116", "Path": "", "Address": "", "ClockIsExternal": true,
                # "Id": "{e3f29eb0-4c7c-44ec-b313-ade78248061b}"} {"CmdName": "SetModulationTarget","CmdUuid": "{
                # 8dd3937e-37df-45a3-a957-9d40b046f6a3}","Type": "NoneRT","Path": "","Address": "","ClockIsExternal":
                # true,"Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                dta_2116_upper_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + '"{my_id_5}"' + "," + '"Type": ' + '"DTA-2116"' + "," + '"Path": ' + '""' + "," + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' + '"{my_id_6}"' + "}"
                self.sdx_script.write(dta_2116_upper_modulation_str)
                self.sdx_script.write("\n")

                dta_2116_upper_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                             + '"{my_id_7}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "12500000" \
                                             + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"UpperL",' + '"Signal": ' \
                                             + '"' + str(
                    signal_upper_band) + '"' + "," + '"Gain": ' + gain_dta + "," + '"GaussianNoise": ' \
                                             + gaussian_noise_str + "," + '"Id": ' + '"{my_id_6}"' + "}"
                self.sdx_script.write(dta_2116_upper_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation
            if signal_lower_band != "":
                # {"CmdName": "SetModulationTarget", "CmdUuid": "{c811d429-6b35-4882-88ef-ae57595028e0}", 
                # "Type": "DTA-2116", "Path": "", "Address": "", "ClockIsExternal": true, 
                # "Id": "{da8ee213-1645-43c5-805c-6e163093b13e}"} {"CmdName": "SetModulationTarget","CmdUuid": "{
                # 8dd3937e-37df-45a3-a957-9d40b046f6a3}","Type": "NoneRT","Path": "","Address": "","ClockIsExternal":
                # true,"Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                dta_2116_lower_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                                '"{my_id_9}"' + "," + '"Type": ' + '"DTA-2116"' + "," + '"Path": ' + '""' + "," \
                                                + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                                + '"{my_id_10}"' + "}"
                self.sdx_script.write(dta_2116_lower_modulation_str)
                self.sdx_script.write("\n")

                dta_2116_lower_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                             + '"{my_id_11}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "12500000" \
                                             + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"LowerL",' + '"Signal": ' \
                                             + '"' + str(
                    signal_lower_band) + '"' + "," + '"Gain": ' + gain_dta + "," + '"GaussianNoise": ' \
                                             + gaussian_noise_str + "," + '"Id": ' + '"{my_id_10}"' + "}"

                self.sdx_script.write(dta_2116_lower_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation
            if signal_lower_band2 != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                dta_2116_lower2_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                                 '"{my_id_13}"' + "," + '"Type": ' + '"DTA-2116"' + "," + '"Path": ' + '""' + "," \
                                                 + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                                 + '"{my_id_14}"' + "}"

                self.sdx_script.write(dta_2116_lower2_modulation_str)
                self.sdx_script.write("\n")

                dta_2116_lower2_signals_str = "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                                              + '"{my_id_15}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "12500000" \
                                              + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"LowerL",' + '"Signal": ' \
                                              + '"' + str(
                    signal_lower_band2) + '"' + "," + '"Gain": ' + gain_dta + "," + '"GaussianNoise": ' \
                                              + gaussian_noise_str + "," + '"Id": ' + '"{my_id_14}"' + "}"

                self.sdx_script.write(dta_2116_lower2_signals_str)
                self.sdx_script.write("\n")
            # Change configuration before starting the simulation
            if signal_lower_band_E6 != "":
                # {"CmdName": "SetModulationTarget","CmdUuid": "{8dd3937e-37df-45a3-a957-9d40b046f6a3}",
                # "Type": "NoneRT","Path": "","Address": "","ClockIsExternal": true,
                # "Id": "{c6aaf761-5b49-44ad-961f-6686fe9812a5}"}
                dta_2116_lower_e6_modulation_str = "{" + '"CmdName": ' + '"SetModulationTarget",' + '"CmdUuid": ' + \
                                                   '"{my_id_13}"' + "," + '"Type": ' + '"NoneRT"' + "," + '"Path": ' + '""' + "," \
                                                   + '"Address": ' + '""' + "," + '"ClockIsExternal": ' + "true," + '"Id": ' \
                                                   + '"{my_id_14}"' + "}"

                self.sdx_script.write(dta_2116_lower_e6_modulation_str)
                self.sdx_script.write("\n")

                none_lower_e6_signals_str = (
                        "{" + '"CmdName": ' + '"ChangeModulationTargetSignals"' + "," + '"CmdUuid": ' \
                        + '"{my_id_15}"' + "," + '"Output": ' + "0" + "," + '"MinRate": ' + "12500000" \
                        + "," + '"MaxRate": ' + "125000000," + '"Band": ' + '"UpperL",' + '"Signal": ' \
                        + '"' + str(signal_lower_band_E6) + '"' + "," + '"Gain": ' + gain_dta + ","
                        + '"GaussianNoise": ' + gaussian_noise_str + "," + '"Id": ' +
                        '"{my_id_16}"' + "}")

                self.sdx_script.write(none_lower_e6_signals_str)
                self.sdx_script.write("\n")

        self.sdx_script.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    sys.exit(app.exec())
