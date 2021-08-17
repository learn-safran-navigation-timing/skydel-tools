import csv
import os
import re
import sys
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLineEdit, QLabel, QMenuBar, QDesktopWidget, QMessageBox, QComboBox, QFormLayout, QGroupBox, \
    QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from plotly.offline import plot
from about import Ui_AboutDialog
from new_extractor import NewAntReader

matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from numpy import inf
import pandas as pd

start = time.time()

"ADD warning when file is not csv format"


def update_plot_1_2(X, Y, Z, G):
    layout = go.Layout(title="3D Radiation Antenna Pattern")
    fig = go.Figure(data=[
        go.Surface(x=X, y=Y, z=-Z, surfacecolor=G, colorscale='Reds',
                   colorbar=dict(title="Gain", thickness=60, xpad=500))],
        layout=layout)
    fig.update_layout(autosize=True, margin=dict(l=50, r=50, t=200, b=200))
    plot(fig)


def find_gain(finder_el_az, length_skipline, ang_elevation, ang_azimuth, gain):
    search_gain = float()
    for i in range(length_skipline):
        search_el = ang_elevation[i]
        search_az = ang_azimuth[i]
        search_el_az = [search_el, search_az]
        if finder_el_az == search_el_az:
            search_gain = gain[i]
    return search_gain


class MainWindow(QtWidgets.QMainWindow):
    selected_freq_sig = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        ''' This part is the implementation of the Ui view'''
        # *************************************************************************************************************
        # ******************************* Menubar
        hlay = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap('Skydel-NewLogo.png')
        label.resize(85, 85)
        label.setPixmap(pixmap.scaled(label.size(), QtCore.Qt.KeepAspectRatio))
        hlay.addWidget(label, 0)
        menubar = QMenuBar()
        actionFile1 = menubar.addMenu("View")
        self.ui_view = actionFile1.addAction("UI view")
        self.ui_view.setCheckable(True)
        self.ui_view.setChecked(True)
        self.ui_view.triggered.connect(self.on_view_changed)
        actionFile1.addSeparator()
        self.html_view = actionFile1.addAction("HTML view")
        self.html_view.setCheckable(True)
        self.html_view.setChecked(False)
        self.html_view.triggered.connect(self.on_view_changed)
        self.view_type = 1
        actionFile2 = menubar.addMenu("Help")
        self.about_ui = actionFile2.addAction("About")
        self.about_ui.triggered.connect(self.show_about)
        actionFile2.addSeparator()
        self.user_manuel = actionFile2.addAction("User manuel")
        # self.user_manuel.triggered.connect(self.on_user_manuel_open)
        actionFile2 = menubar.addMenu("Exit")
        actionFile2.addAction("Quit")
        actionFile2.triggered.connect(self.quit_app)

        # *************************************************************************************************************
        # Studio view to Skydel layout
        layout_std_details = QFormLayout()
        self.theta_sample_num_1 = QLineEdit()
        self.theta_sample_num_1.setFont(QFont('Arial', 9))
        self.phi_sample_num_1 = QLineEdit()
        self.phi_sample_num_1.setFont(QFont('Arial', 9))
        self.frequency_1 = QLineEdit()
        self.frequency_1.setFont(QFont('Arial', 9))
        self.pas_theta_1 = QLineEdit()
        self.pas_theta_1.setFont(QFont('Arial', 9))
        self.pas_phi_1 = QLineEdit()
        self.pas_phi_1.setFont(QFont('Arial', 9))
        self.elevation_range_1 = QLineEdit()
        self.elevation_range_1.setFont(QFont('Arial', 9))
        self.azimuth_range_1 = QLineEdit()
        self.azimuth_range_1.setFont(QFont('Arial', 9))

        layout_std_details.addRow("El sample", self.theta_sample_num_1)
        layout_std_details.addRow("Az sample", self.phi_sample_num_1)
        emailLabel = QLabel("Frequency")
        layout_std_details.addRow(emailLabel, self.frequency_1)
        layout_std_details.addRow("El step (°C)", self.pas_theta_1)
        layout_std_details.addRow("Az step (°C)", self.pas_phi_1)
        layout_std_details.addRow("El range (°C)", self.elevation_range_1)
        layout_std_details.addRow("Az range (°C)", self.azimuth_range_1)

        self.title_std_details = QLabel("Studio-View to Skydel")
        self.title_std_details.setFont(QFont('Arial', 9))
        self.title_std_details.setStyleSheet("background-color:#3f829d; border-radius:3.5px")
        self.title_std_details.setAlignment(Qt.AlignCenter)

        std_details_group = QGroupBox()
        std_details_group.setLayout(layout_std_details)
        std_details_group.setStyleSheet("QGroupBox{border-radius:3.5px; padding-top:1px; margin-top:-1px}")

        # *************************************************************************************************************
        # *************************** Skydel to Studio View layout

        layout_sky_details = QFormLayout()
        self.theta_sample_num_2 = QLineEdit()
        self.theta_sample_num_2.setFont(QFont('Arial', 9))
        self.phi_sample_num_2 = QLineEdit()
        self.phi_sample_num_2.setFont(QFont('Arial', 9))
        self.frequency_edit_2 = QLineEdit()
        self.frequency_edit_2.setFont(QFont('Arial', 9))
        self.pas_theta_2 = QLineEdit()
        self.pas_theta_2.setFont(QFont('Arial', 9))
        self.pas_phi_2 = QLineEdit()
        self.pas_phi_2.setFont(QFont('Arial', 9))
        self.elevation_range_2 = QLineEdit()
        self.elevation_range_2.setFont(QFont('Arial', 9))
        self.azimuth_range_2 = QLineEdit()
        self.azimuth_range_2.setFont(QFont('Arial', 9))

        layout_sky_details.addRow("El sample", self.theta_sample_num_2)
        layout_sky_details.addRow("Az sample", self.phi_sample_num_2)
        emailLabel = QLabel("Frequency")
        layout_sky_details.addRow(emailLabel, self.frequency_edit_2)
        layout_sky_details.addRow("El step (°C)", self.pas_theta_2)
        layout_sky_details.addRow("Az step (°C)", self.pas_phi_2)
        layout_sky_details.addRow("El range (°C)", self.elevation_range_2)
        layout_sky_details.addRow("Az range (°C)", self.azimuth_range_2)

        self.title_sky_details = QLabel("Skydel to Studio view")
        self.title_sky_details.setFont(QFont('Arial', 9))
        self.title_sky_details.setStyleSheet("background-color:#de7e5d; border-radius:3.5px")
        self.title_sky_details.setAlignment(Qt.AlignCenter)

        sky_details_group = QGroupBox()
        sky_details_group.setLayout(layout_sky_details)
        sky_details_group.setStyleSheet("QGroupBox{border-radius:3.5px; padding-top:1px; margin-top:-1px}")

        spacerItem0 = QtWidgets.QSpacerItem(102, 61, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.spacerItem01 = QtWidgets.QSpacerItem(102, 91, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Minimum)

        self.frame1 = QtWidgets.QFrame(self)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Plain)

        layout_multi_freq = QFormLayout()
        self.combo3 = QComboBox(self)
        self.combo3.setFont(QFont('Arial', 9))
        self.combo3.activated[str].connect(self.onActivated3)
        layout_multi_freq.addWidget(self.combo3)

        self.multi_freq_details = QLabel("Select frequency ( Hz)")
        self.multi_freq_details.setFont(QFont('Arial', 9))
        self.multi_freq_details.setStyleSheet("background-color:slategray; border-radius:3.5px")
        self.multi_freq_details.setAlignment(Qt.AlignCenter)
        self.multi_freq_group = QGroupBox()
        self.multi_freq_group.setLayout(layout_multi_freq)
        self.multi_freq_group.setStyleSheet("QGroupBox{border-radius:3.5px; padding-top:1px; margin-top:-1px}")

        self.multi_freq_details.setVisible(False)
        self.multi_freq_group.setVisible(False)

        self.menubar_layout = QtWidgets.QVBoxLayout()
        self.menubar_layout.addWidget(menubar, 0)
        self.menubar_layout.addWidget(self.frame1, 2)
        self.menubar_layout.addItem(spacerItem0)
        self.menubar_layout.addWidget(self.multi_freq_details, 1)
        self.menubar_layout.addWidget(self.multi_freq_group, 1)

        self.menubar_layout.addWidget(self.frame1, 3)
        self.menubar_layout.addItem(self.spacerItem01)
        self.menubar_layout.addWidget(self.title_std_details, 2)
        self.menubar_layout.addWidget(std_details_group, 2)
        self.menubar_layout.addWidget(self.frame1, 1)
        self.menubar_layout.addItem(self.spacerItem01)
        self.menubar_layout.addWidget(self.title_sky_details, 3)
        self.menubar_layout.addWidget(sky_details_group, 3)
        self.menubar_layout.addWidget(self.frame1, 4)
        self.menubar_layout.addItem(spacerItem0)

        # *************************************************************************************************************
        # Studio view to Skydel View

        self.title1 = QLabel("Studio view to Skydel - 3D antenna radiation view")
        self.title1.setAlignment(Qt.AlignCenter)
        self.title1.setFont(QFont('Arial', 12))
        self.title1.setStyleSheet("background-color:#3f829d; border-radius:5px")

        self.file_path_1 = QLineEdit()
        self.file_path_1.setFont(QFont('Arial', 10))

        self.load_button_1_layout = QtWidgets.QHBoxLayout()
        self.load_button1 = QtWidgets.QPushButton('Load ant')
        self.load_button1.setFont(QFont('Arial', 10))
        self.load_button1.clicked.connect(self.load_ant)
        self.load_button_1_layout.addWidget(self.load_button1)
        self.load_button_1_layout.addWidget(self.file_path_1)

        self.fig1 = Figure(figsize=(7, 7), dpi=100)
        self.canvas1 = FigureCanvas(self.fig1)
        self.axes1 = self.fig1.add_subplot(111, projection='3d')
        toolbar1 = NavigationToolbar(self.canvas1, self)
        self.mappable1 = plt.cm.ScalarMappable()
        self.cb1 = self.fig1.colorbar(self.mappable1, shrink=0.7)

        self.axes1.grid(True)
        self.axes1.axis('off')
        self.axes1.set_xticks([])
        self.axes1.set_yticks([])
        self.axes1.set_zticks([])

        phi1, theta1 = np.linspace(0, 2 * np.pi, 40), np.linspace(0, np.pi, 40)
        PHI1, THETA1 = np.meshgrid(phi1, theta1)
        R1 = 2
        self.X1 = R1 * np.sin(THETA1) * np.cos(PHI1)
        self.Y1 = R1 * np.sin(THETA1) * np.sin(PHI1)
        self.Z1 = R1 * np.cos(THETA1)
        self.axes1.plot_wireframe(self.X1, self.Y1, self.Z1, linewidth=0.5, rstride=3, cstride=3)

        combo1 = QLineEdit(self)
        combo1.setFont(QFont('Arial', 10))
        combo1.setEnabled(False)
        combo1.setStyleSheet("background-color:white")

        self.file_save_path_1 = QLineEdit()
        self.file_save_path_1.setText("File save here:")
        self.file_save_path_1.setEnabled(False)
        self.file_save_path_1.setFont(QFont('Arial', 10))

        self.save_button_1_layout = QtWidgets.QHBoxLayout()
        self.save_button1 = QtWidgets.QPushButton('Save csv')
        self.save_button1.setFont(QFont('Arial', 10))
        self.save_button1.clicked.connect(self.save_file_1)
        self.save_button1.setEnabled(False)
        self.save_button_1_layout.setAlignment(Qt.AlignCenter)
        self.save_button_1_layout.addWidget(self.save_button1)
        # self.save_button_1_layout.addWidget(self.file_save_path_1)

        spacerItem1 = QtWidgets.QSpacerItem(50, 15, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        layout1 = QtWidgets.QVBoxLayout()
        layout1.addWidget(self.title1, 0)
        # layout1.addWidget(self.file_path_1)
        layout1.addItem(spacerItem1)
        layout1.addLayout(self.load_button_1_layout)
        layout1.addWidget(self.canvas1, 3)
        layout1.addWidget(toolbar1, 4)
        layout1.addWidget(combo1, 5)
        layout1.addLayout(self.save_button_1_layout)

        # **************************************************************************************************************
        self.title2 = QLabel("Skydel to Studio view - 3D antenna radiation view")
        self.title2.setAlignment(Qt.AlignCenter)
        self.title2.setFont(QFont('Arial', 12))
        self.title2.setStyleSheet("background-color:#de7e5d; border-radius:5px")

        self.file_path_2 = QLineEdit()
        self.file_path_2.setFont(QFont('Arial', 10))

        self.load_button_2_layout = QtWidgets.QHBoxLayout()
        self.load_button2 = QtWidgets.QPushButton('Load csv')
        self.load_button2.setFont(QFont('Arial', 10))
        self.load_button2.clicked.connect(self.load_csv)

        self.load_button_2_layout.setAlignment(Qt.AlignCenter)
        self.load_button_2_layout.addWidget(self.load_button2)
        self.load_button_2_layout.addWidget(self.file_path_2)

        self.fig2 = Figure(figsize=(7, 7), dpi=100)
        self.canvas2 = FigureCanvas(self.fig2)
        self.axes2 = self.fig2.add_subplot(111, projection='3d')
        toolbar2 = NavigationToolbar(self.canvas2, self)
        self.mappable2 = plt.cm.ScalarMappable()
        self.cb2 = self.fig2.colorbar(self.mappable2, shrink=0.7)

        self.axes2.grid(True)
        self.axes2.axis('off')
        self.axes2.set_xticks([])
        self.axes2.set_yticks([])
        self.axes2.set_zticks([])

        phi2, theta2 = np.linspace(0, 2 * np.pi, 40), np.linspace(0, np.pi, 40)
        PHI2, THETA2 = np.meshgrid(phi2, theta2)
        R2 = 2
        X2 = R2 * np.sin(THETA2) * np.cos(PHI2)
        Y2 = R2 * np.sin(THETA2) * np.sin(PHI2)
        Z2 = R2 * np.cos(THETA2)

        self.axes2.plot_wireframe(X2, Y2, Z2, linewidth=0.5, rstride=3, cstride=3)

        combo2 = QComboBox(self)
        combo2.setFont(QFont('Arial', 10))
        combo2.addItem('GPS L1')
        combo2.addItem('GPS L2')
        combo2.addItem('GPS L5')
        combo2.addItem('GlONASS L1')
        combo2.addItem('GLONASS L2')
        combo2.activated[str].connect(self.onActivated2)
        self.frequency_2 = 'GPS_L1'
        self.frequency_2_val = "1.57542e+09"

        self.file_save_path_2 = QLineEdit()
        self.file_save_path_2.setText("File save here:")
        self.file_save_path_2.setEnabled(False)
        self.file_save_path_2.setFont(QFont('Arial', 10))

        self.save_button_2_layout = QtWidgets.QHBoxLayout()
        self.save_button2 = QtWidgets.QPushButton('Save ant')
        self.save_button2.setFont(QFont('Arial', 10))
        self.save_button2.clicked.connect(self.save_file_2)
        self.save_button2.setEnabled(False)
        self.save_button_2_layout.setAlignment(Qt.AlignCenter)
        self.save_button_2_layout.addWidget(self.save_button2)

        spacerItem2 = QtWidgets.QSpacerItem(50, 15, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addWidget(self.title2, 0)
        layout2.addItem(spacerItem2)
        layout2.addLayout(self.load_button_2_layout)
        layout2.addWidget(self.canvas2, 3)
        layout2.addWidget(toolbar2, 4)
        layout2.addWidget(combo2, 5)
        layout2.addLayout(self.save_button_2_layout)

        spacerItem = QtWidgets.QSpacerItem(15, 15, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        layout = QtWidgets.QHBoxLayout()
        # layout.addWidget(panel, 0)
        layout.addLayout(self.menubar_layout, 0)
        layout.addItem(spacerItem)
        layout.addLayout(layout1, 1)
        layout.addItem(spacerItem)
        layout.addLayout(layout2, 1)
        layout_final = QtWidgets.QVBoxLayout()
        layout_final.addLayout(hlay, 0)
        layout_final.addLayout(layout, 1)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout_final)

        self.resize(1324, 934)
        self.setCentralWidget(widget)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def load_ant(self):

        self.model_filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + " DATA Files", ".",
                                                                             "(*.ant)")
        if self.model_filename:
            self.file_path_1.setText(self.model_filename)
            self.ant_filename = self.model_filename
            self.convert_1()
        elif self.model_filename == "":
            QMessageBox.about(self, "Load file error", "File path is empty.")
        else:
            QMessageBox.about(self, "Load file error", "File path is empty.")

    def load_csv(self):
        self.model_filename, _filter = QtWidgets.QFileDialog.getOpenFileName(None, "Open " + " DATA Files", ".",
                                                                             "(*.csv)")
        if self.model_filename:
            self.file_path_2.setText(self.model_filename)
            self.csv_filename = self.model_filename
            self.convert_2()
        elif self.model_filename == "":
            QMessageBox.about(self, "Load file error", "File path is empty.")
        else:
            QMessageBox.about(self, "Load file error", "File path is empty.")

    def on_view_changed(self):
        if self.ui_view.isChecked():
            self.view_type = 1
            if self.html_view.isChecked():
                self.view_type = 3
        elif self.html_view.isChecked():
            self.view_type = 2
        else:
            self.view_type = 1

    def convert_1(self):

        base = os.path.basename(self.ant_filename)
        file_extension_1 = os.path.splitext(base)[1]
        self.combo3.clear()
        try:
            if file_extension_1 == ".ant":
                self.new_reader = NewAntReader()
                occur, data, self.freq1, self.theta_sample_convert_1, self.phi_sample_convert_1 = self.new_reader.check_multi(
                    self.ant_filename, 7)

                self.true_list_freq = []
                self.index_freq = int()
                self.selected_freq = ""

                if occur < 1:
                    self.multi_freq_details.setVisible(False)
                    self.multi_freq_group.setVisible(False)
                    freq, elev_list, azim_list, gain = self.new_reader.read_info(data, 7)
                    line_skip = len(data)
                    self.convert_1_suite(freq, self.theta_sample_convert_1, self.phi_sample_convert_1, elev_list,
                                         azim_list,
                                         gain, line_skip)
                else:
                    # print(" Theta and phi sample:", self.theta_sample_convert_1, self.phi_sample_convert_1)
                    self.list_frequency, self.new_data = self.new_reader.slice_data(data, 7)
                    self.true_list_freq.append(str(self.freq1))
                    for freq in self.list_frequency:
                        true_freq = freq[1]
                        self.true_list_freq.append(str(true_freq))
                    self.axes1.plot_wireframe(self.X1, self.Y1, self.Z1, linewidth=0.5, rstride=3, cstride=3)
                    self.combo3.addItems(self.true_list_freq)
                    self.multi_freq_details.setVisible(True)
                    self.multi_freq_group.setVisible(True)
                    self.combo3.setCurrentText(self.freq1)
                    QMessageBox.about(self, "Frequency selection", "Multiple frequency detected.")

                    QMessageBox.about(self, "Frequency selection",
                                      "Please, select a frequency in the select frequency box to continue.")
            else:
                QMessageBox.about(self, ".ant File conversion error", "The selected file is not an ant file")

        except ValueError:
            QMessageBox.about(self, "Format error",
                              "Please check the format of the csv file for antenna pattern")

    def convert_1_multi(self):

        if self.selected_freq:
            index = self.true_list_freq.index(self.selected_freq)
            data_part = self.new_data[index]
            freq, elev_list, azim_list, gain = self.new_reader.read_info(data_part, 7)
            line_skip = len(data_part)
            self.convert_1_suite(freq, self.theta_sample_convert_1, self.phi_sample_convert_1, elev_list, azim_list,
                                 gain, line_skip)

    def convert_1_suite(self, freq, theta_sample, phi_sample, elev_list, azim_list, gain, line_skip):
        ang_elevation = np.array(elev_list)
        matrix_elevation = []
        matrix_azimuth = []
        self.matrix_gain_1 = []
        self.matrix_gain_save = []
        try:
            pas_elevation = 180 / (int(theta_sample) - 1)
        except ZeroDivisionError:
            pas_elevation = 180
        ang_azimuth = azim_list

        try:
            pas_azimuth = 360 / (int(phi_sample) - 1)
        except ZeroDivisionError:
            pas_azimuth = 360

        self.theta_sample_num_1.setText(str(theta_sample))
        self.phi_sample_num_1.setText(str(phi_sample))
        if self.selected_freq:
            self.frequency_1.setText(str(self.selected_freq))
        else:
            self.frequency_1.setText(str(self.freq1))
        self.pas_theta_1.setText(str(pas_elevation))
        self.pas_phi_1.setText(str(pas_azimuth))
        self.elevation_range_1.setText("0 - 180")
        self.azimuth_range_1.setText("0 - 360")

        ang_elevation = np.add(ang_elevation, -90.0)
        if phi_sample == "1":
            pas_azimuth = 10
            phi_sample = int(360 / pas_azimuth + 1)
            self.matrix_gain_save = np.transpose([gain] * 1)
            self.matrix_gain_1 = np.transpose([gain] * phi_sample)
            for el in np.arange(-90, 90 + 0.01, pas_elevation):
                list_elevation = []
                list_azimuth = []
                for az in np.arange(0, 360 + 0.01, pas_azimuth):
                    list_elevation.append(el)
                    list_azimuth.append(az)
                matrix_azimuth.append(list_azimuth)
                matrix_elevation.append(list_elevation)
        else:
            for el in np.arange(-90, 90 + 0.01, pas_elevation):
                list_gain = []
                list_elevation = []
                list_azimuth = []
                for az in np.arange(0, 360 + 0.01, pas_azimuth):
                    list_elevation.append(el)
                    list_azimuth.append(az)
                    find_el_az = [float(el), float(az)]
                    finded_gain = find_gain(find_el_az, line_skip, ang_elevation, ang_azimuth, gain)
                    chech_inf = round(finded_gain, 5)
                    if chech_inf == -inf:
                        list_gain.append(-100.0)
                    elif chech_inf == inf:
                        list_gain.append(100.0)
                    else:
                        list_gain.append(finded_gain)

                self.matrix_gain_1.append(list_gain)
                matrix_azimuth.append(list_azimuth)
                matrix_elevation.append(list_elevation)
            self.matrix_gain_save = self.matrix_gain_1

        self.plot_antenna_1(matrix_elevation, matrix_azimuth, self.matrix_gain_1)
        self.save_button1.setEnabled(True)

    def plot_antenna_1(self, matrix_elevation, matrix_azimuth, matrix_gain):
        # #print(" ***** start Plot antenna")

        matrix_elevation = np.add(matrix_elevation, -90.0)
        THETA = np.deg2rad(matrix_elevation)
        PHI = np.deg2rad(np.array(matrix_azimuth))
        R = np.array(matrix_gain)
        G = R

        Rmax = (np.max(R))
        Rmin = (np.min(R))
        RmaxMap = (np.max(R))
        RminMap = (np.min(R))

        # #print(Rmin)
        check_same_gain = np.all(R == R[0])
        count_zero = np.count_nonzero(R)
        count_total = len(R)
        # print("count:", count_zero, count_total)

        if check_same_gain == False:
            if Rmin < 0.0:
                R = np.add(R, +abs(Rmin))
            else:
                R = np.add(R, -abs(Rmin))
        else:
            R = np.add(R, +abs(Rmin))

        Rmap = R
        if Rmax < abs(Rmin):
            Rmax = Rmin

        is_all_zero = np.all((R == 0))
        if is_all_zero:
            R = np.add(R, 1)
            Rmax = 1
            RminMap = 0
            RmaxMap = 0

        X = R * np.sin(THETA) * np.cos(PHI)
        Y = R * np.sin(THETA) * np.sin(PHI)
        Z = R * np.cos(THETA)

        if self.view_type == 1:
            self.update_plot_1_1(X, Y, Z, G, Rmax)
        elif self.view_type == 2:
            update_plot_1_2(X, Y, -Z, G)
        else:
            self.update_plot_1_1(X, Y, Z, G, Rmax)
            update_plot_1_2(X, Y, -Z, G)

    def update_plot_1_1(self, X, Y, Z, G, Rmax):
        # #print("***** Update Plot start")
        self.mappable1.set_array(G)
        self.mappable2.set_array(G)
        Gmax = (np.max(G))
        Gmin = (np.min(G))

        self.mappable1.set_clim(Gmin, Gmax)

        if Gmax < abs(Gmin):
            Gmax = Gmin

        self.axes1.cla()  # Clear the canvas.
        self.axes1.grid(True)
        self.axes1.axis('off')
        self.axes1.set_xticks([])
        self.axes1.set_yticks([])
        self.axes1.set_zticks([])
        axes_length = 1.5
        self.axes1.plot([0, -axes_length * Gmax], [0, 0], [0, 0], linewidth=1, color='red')
        self.axes1.plot([0, 0], [0, -axes_length * Gmax], [0, 0], linewidth=1, color='green')
        self.axes1.plot([0, 0], [0, 0], [0, -axes_length * Gmax], linewidth=1, color='blue')
        # self.axes1.annotate("", xy=(0.5, 0.5), xytext=(0, 0), arrowprops = dict(arrowstyle="->"))
        self.axes1.plot_surface(
            X, Y, Z, rstride=1, cstride=1, cmap=self.mappable1.cmap,
            linewidth=0, antialiased=False, alpha=0.5, zorder=0.5)
        self.axes1.view_init(azim=-60, elev=0)
        self.canvas1.draw()

    def on_file_saved_1(self):
        base1 = os.path.basename(self.ant_filename)
        ant_name = os.path.splitext(base1)[0]
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", ant_name,
                                                  "All Files (*);;Text Files (*.csv)", options=options)
        return fileName

    def save_file_1(self):
        skydel_file_name = str(self.on_file_saved_1())
        if skydel_file_name:
            base1 = os.path.basename(self.ant_filename)
            studio_view_name = os.path.splitext(base1)[0]
            # #print(studio_view_name)
            text1 = "Studio View to Skydel: " + studio_view_name
            self.title1.setText(text1)
            # print(skydel_file_name)
            with open(skydel_file_name, mode='w') as ant_pattern:
                ant_pattern = csv.writer(ant_pattern, delimiter=',', quotechar='"', lineterminator='\n',
                                         quoting=csv.QUOTE_MINIMAL)
                for list in self.matrix_gain_save:
                    ant_pattern.writerow(list)
            save_file_path_1 = os.path.splitext(self.ant_filename)[0] + skydel_file_name
        else:
            QMessageBox.about(self, ".ant File conversion error", "No path found")

    def convert_2(self):
        try:
            base = os.path.basename(self.csv_filename)
            file_extension_2 = os.path.splitext(base)[1]

            if file_extension_2 == ".csv":
                data = pd.read_csv(self.csv_filename, error_bad_lines=False, header=None)
                # #print(data.iloc[0:, 0:])
                power = np.asarray(data.iloc[0:, 0:])
                self.power_2 = power
                # power = np.power(10, power * 0.1)  # converting from db to watt
                self.ligne, self.colonne = np.shape(power)
                # print(self.ligne, self.colonne)

                theta = []
                phi = []
                new_power = []
                power_1 = []
                new_phi = []
                len_new_phi = int()
                pas_azimuth = int()
                pas_elevation = int()
                try:
                    pas_elevation = 180 / (int(self.ligne) - 1)
                    # print("pas_elevation:", pas_elevation)

                    pas_azimuth = 360 / (int(self.colonne) - 1)
                    # print("pas_azimuth:", pas_azimuth)
                    theta = np.arange(-90, 90 + 0.01, pas_elevation)
                    phi = np.arange(0, 360 + 0.01, pas_azimuth)
                    self.phi_2 = phi
                    # print("Phi 2:", self.phi_2)
                    self.pas_azimuth_studio = pas_azimuth
                    self.colonne_studio = self.colonne

                except ZeroDivisionError:
                    if self.colonne == 1:
                        self.colonne_studio = 1
                        pas_elevation = 180 / (int(self.ligne) - 1)
                        theta = np.arange(-90, 90 + 0.01, pas_elevation)
                        pas_azimuth = 10
                        # if azimuth is only one column, azimuth is then 0 in all line.
                        phi = np.arange(0, 360, 360)
                        self.phi_studio = phi
                        self.pas_azimuth_studio = 360 + 1
                        new_phi = np.arange(0, 360 + 0.01, pas_azimuth)
                        phi = new_phi
                        len_new_phi = len(new_phi)
                        # print(len_new_phi)
                        # print("A completer")
                        for j in range(len(power)):
                            power_1.append(float(power[j]))
                        for i in range(len_new_phi):
                            new_power.append(power_1)
                            power = np.array(new_power)
                            power = power.transpose()
                            self.power_2 = power
                            self.ligne, self.colonne = np.shape(power)

                    if self.ligne == 1:
                        QMessageBox.about(self, ".csv File conversion error",
                                          "This file type is not support, there is only"
                                          " one elevation line")

                self.theta_2 = theta
                theta = np.add(theta, 90.0)

                THETA = []
                PHI = []
                R = []
                self.pas_azimuth_2 = pas_azimuth
                self.pas_elevation_2 = pas_elevation

                # print(self.ligne, self.colonne)
                for p in range(0, self.colonne, 1):
                    # for t in np.arange(0, self.ligne, self.saut_elevation):
                    for t in range(0, self.ligne, 1):
                        THETA.append(float(theta[t]))
                        PHI.append(float(phi[p]))
                        R.append(float(power[t, p]))

                R_2 = R

                THETA = np.deg2rad(np.asarray(THETA))
                PHI = np.deg2rad(np.asarray(PHI))
                R = np.array(R)
                # print(power.shape[1], )
                THETA = THETA.reshape(power.shape[1], power.shape[0])
                THETA = np.transpose(THETA)
                PHI = PHI.reshape(power.shape[1], power.shape[0])
                PHI = np.transpose(PHI)
                R = R.reshape(power.shape[1], power.shape[0])
                R = np.transpose(R)
                G = R
                Gmax = (np.max(G))
                Gmin = (np.min(G))
                Rmax = (np.max(R))
                Rmin = (np.min(R))
                RmaxMap = (np.max(R))
                RminMap = (np.min(R))
                if Rmin < 0:
                    R = np.add(R, abs(Rmin))
                else:
                    R = np.add(R, -abs(Rmin))

                if Rmax < abs(Rmin):
                    Rmax = Rmin

                Rmap = R

                is_all_zero = np.all((R == 0))
                if is_all_zero:
                    # print('Array contains only 0')
                    R = np.add(R, 1)
                    Rmax = 1
                    RminMap = 0
                    RmaxMap = 0

                X = R * np.sin(THETA) * np.cos(PHI)
                Y = R * np.sin(THETA) * np.sin(PHI)
                Z = R * np.cos(THETA)

                if self.view_type == 1:
                    self.update_plot_2_1(X, Y, Z, G)
                elif self.view_type == 2:
                    self.update_plot_1_2(X, Y, Z, G)
                else:
                    self.update_plot_2_1(X, Y, Z, G)
                    update_plot_1_2(X, Y, Z, G)
                self.save_button2.setEnabled(True)

                self.theta_sample_num_2.setText(str(self.ligne))
                self.phi_sample_num_2.setText(str(self.colonne))
                self.frequency_edit_2.setText("Default")
                self.pas_theta_2.setText(str(self.pas_elevation_2))
                self.pas_phi_2.setText(str(self.pas_azimuth_2))
                self.elevation_range_2.setText("0 - 180")
                self.azimuth_range_2.setText("0 - 360")

            else:
                QMessageBox.about(self, ".csv File conversion error", "The selected file is not an .csv file")
        except ValueError:
            QMessageBox.about(self, "Format error",
                              "Please check the format of the csv file for antenna pattern")

    def save_file_2(self):

        theta_studio = []
        for i in range(0, self.colonne_studio, 1):
            theta_studio = np.append(self.theta_2, theta_studio)

        theta_studio = np.asarray(theta_studio)

        phi_studio = []
        # print(self.pas_azimuth_2)
        for j in np.arange(0, 360 + 0.01, self.pas_azimuth_studio):
            for k in range(0, self.ligne, 1):
                phi_studio.append(j)

        phi_studio = np.asarray(phi_studio)

        gain_studio = []

        for m in range(0, self.colonne_studio, 1):
            for n in range(0, self.ligne, 1):
                gain_studio.append(self.power_2[n, m])

        base2 = os.path.basename(self.csv_filename)
        studio_view_name = os.path.splitext(base2)[0]
        text2 = "Skydel to Studio view: " + studio_view_name
        self.title2.setText(text2)

        studio_view_name = str(self.on_file_saved_2())
        print('File save here:', studio_view_name)
        if studio_view_name:
            f = open(studio_view_name, "w+")
            f.write("##File Type: Far field\n")
            f.write("#Frequency: " + self.frequency_2_val + "\n")
            f.write("#No. of Theta Samples: ")
            f.write(str(self.ligne) + "\n")
            f.write("#No. of Phi Samples: ")
            f.write(str(self.colonne_studio) + "\n")
            f.write("#Far Field Type: Gain\n")
            f.write("#No. of Header Lines: 1\n")
            f.write(
                """#    "Theta"    "Phi"    "Re(Etheta)"    "Im(Etheta)"    "Re(Ephi)"    "Im(Ephi)"    "Gain(Theta)"    "Gain(Phi)"    "Gain(Total)"\n""")

            for i in range(0, len(gain_studio), 1):
                line_to_write = theta_studio[i] + 90.0, phi_studio[i], 0, 0, 0, 0, 0, 0, gain_studio[i]
                document = str(line_to_write)
                document = re.sub('[()]', '', document)
                document = re.sub('[,]', '', document)
                f.write(document)
                f.write("\n")
            f.close()
            save_file_path_2 = os.path.splitext(self.csv_filename)[0] + studio_view_name
            print("Path save here:", save_file_path_2)
            self.file_save_path_2.setText(save_file_path_2)
            self.file_save_path_2.setEnabled(True)
        else:
            QMessageBox.about(self, ".csv File conversion error", "No path found")

    def update_plot_2_1(self, X, Y, Z, G):
        # #print("***** Update Plot start")
        self.mappable2.set_array(G)
        Gmax = (np.max(G))
        Gmin = (np.min(G))

        self.mappable2.set_clim(Gmin, Gmax)

        if Gmax < abs(Gmin):
            Gmax = Gmin

        axes_length = 1.5
        self.axes2.cla()  # Clear the canvas.
        self.axes2.grid(True)
        self.axes2.axis('off')
        self.axes2.set_xticks([])
        self.axes2.set_yticks([])
        self.axes2.set_zticks([])
        self.axes2.plot([0, -axes_length * Gmax], [0, 0], [0, 0], linewidth=1, color='red')
        self.axes2.plot([0, 0], [0, -axes_length * Gmax], [0, 0], linewidth=1, color='green')
        self.axes2.plot([0, 0], [0, 0], [0, -axes_length * Gmax], linewidth=1, color='blue')

        self.axes2.plot_surface(
            X, Y, -Z, rstride=1, cstride=1, cmap=self.mappable2.cmap,
            linewidth=0, antialiased=False, alpha=0.5, zorder=0.5)
        self.axes2.view_init(azim=-60, elev=0)
        self.canvas2.draw()

    def on_file_saved_2(self):
        print("on_file_saved_2")
        base2 = os.path.basename(self.csv_filename)
        csv_name = os.path.splitext(base2)[0]
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", csv_name,
                                                  "All Files (*);;Text Files (*.ant)", options=options)
        print(self.csv_filename)
        print(fileName)
        return fileName

    def show_about(self):
        self.ui_about = Ui_AboutDialog()
        self.ui_about.show()

    def onActivated3(self, text):
        if text:
            self.selected_freq = text
            self.convert_1_multi()
        else:
            QMessageBox.about(self, "Multi-Frequency detected", "No selected frequency")

    def onActivated2(self, text):
        if text == 'GPS L1':
            self.frequency_2 = 'GPS_L1'
            self.frequency_2_val = "1.57542e+09"

        elif text == 'GPS L2':
            self.frequency_2 = 'GPS_L2'
            self.frequency_2_val = "1.2276e+09"

        elif text == 'GPS L5':
            self.frequency_2 = 'GPS_L5'
            self.frequency_2_val = "1.17645e+09"

        elif text == 'GLONASS L1':
            self.frequency_2 = 'GLONASS_L1'
            self.frequency_2_val = "1.602e+09"

        else:
            self.frequency_2 = 'GLONASS_L2'
            self.frequency_2_val = "1.246e+09"

    def quit_app(self):
        sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    qtmodern.styles.light(app)
    mw = qtmodern.windows.ModernWindow(w)
    mw.show()
    app.exec_()
