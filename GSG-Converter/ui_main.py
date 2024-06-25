# -*- coding: utf-8 -*-
################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
## This project can be used freely for all uses, as long as they maintain the
## respective credits only in the Python scripts, any information in the visual
## interface (GUI) can be modified without any implication.
##
## There are limitations on Qt licenses if you want to use your products
## commercially, I recommend reading them on the official website:
## https://doc.qt.io/qtforpython/licenses.html
##
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                            QRect, QSize, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
                           QRadialGradient)
from PySide6.QtWidgets import *
import os
import sys
import platform
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide6.QtWidgets import *
import files_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 720)
        MainWindow.setMinimumSize(QSize(1000, 720))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 0))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(66, 73, 90, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(55, 61, 75, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        brush4 = QBrush(QColor(22, 24, 30, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush4)
        brush5 = QBrush(QColor(29, 32, 40, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush5)
        brush6 = QBrush(QColor(210, 210, 210, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        brush7 = QBrush(QColor(0, 0, 0, 255))
        brush7.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush7)
        brush8 = QBrush(QColor(85, 170, 255, 255))
        brush8.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Active, QPalette.Link, brush8)
        brush9 = QBrush(QColor(255, 0, 127, 255))
        brush9.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush4)
        brush10 = QBrush(QColor(44, 49, 60, 255))
        brush10.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush6)
        brush11 = QBrush(QColor(210, 210, 210, 128))
        brush11.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush11)
        # endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush7)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.Link, brush8)
        palette.setBrush(QPalette.Inactive, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush6)
        brush12 = QBrush(QColor(210, 210, 210, 128))
        brush12.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush12)
        # endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush7)
        brush13 = QBrush(QColor(51, 153, 255, 255))
        brush13.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush13)
        palette.setBrush(QPalette.Disabled, QPalette.Link, brush8)
        palette.setBrush(QPalette.Disabled, QPalette.LinkVisited, brush9)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush10)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush6)
        brush14 = QBrush(QColor(210, 210, 210, 128))
        brush14.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush14)
        # endif
        MainWindow.setPalette(palette)
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QMainWindow {background: transparent; }\n"
                                 "QToolTip {\n"
                                 "	color: #ffffff;\n"
                                 "	background-color: rgba(27, 29, 35, 160);\n"
                                 "	border: 1px solid rgb(40, 40, 40);\n"
                                 "	border-radius: 2px;\n"
                                 "}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background: transparent;\n"
                                         "color: rgb(210, 210, 210);")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setStyleSheet(u"/* LINE EDIT */\n"
                                      "QLineEdit {\n"
                                      "	background-color: rgb(27, 29, 35);\n"
                                      "	border-radius: 5px;\n"
                                      "	border: 2px solid rgb(27, 29, 35);\n"
                                      "	padding-left: 10px;\n"
                                      "}\n"
                                      "QLineEdit:hover {\n"
                                      "	border: 2px solid rgb(64, 71, 88);\n"
                                      "}\n"
                                      "QLineEdit:focus {\n"
                                      "	border: 2px solid rgb(91, 101, 124);\n"
                                      "}\n"
                                      "\n"
                                      "/* SCROLL BARS */\n"
                                      "QScrollBar:horizontal {\n"
                                      "    border: none;\n"
                                      "    background: rgb(52, 59, 72);\n"
                                      "    height: 14px;\n"
                                      "    margin: 0px 21px 0 21px;\n"
                                      "	border-radius: 0px;\n"
                                      "}\n"
                                      "QScrollBar::handle:horizontal {\n"
                                      "    background: rgb(85, 170, 255);\n"
                                      "    min-width: 25px;\n"
                                      "	border-radius: 7px\n"
                                      "}\n"
                                      "QScrollBar::add-line:horizontal {\n"
                                      "    border: none;\n"
                                      "    background: rgb(55, 63, 77);\n"
                                      "    width: 20px;\n"
                                      "	border-top-right-radius: 7px;\n"
                                      "    border-bottom-right-radius: 7px;\n"
                                      "    subcontrol-position: right;\n"
                                      "    subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::sub-line:horizontal {\n"
                                      "    border: none;\n"
                                      "    background: rgb(55, 63, 77);\n"
                                      "    width: 20px;\n"
                                      ""
                                      "	border-top-left-radius: 7px;\n"
                                      "    border-bottom-left-radius: 7px;\n"
                                      "    subcontrol-position: left;\n"
                                      "    subcontrol-origin: margin;\n"
                                      "}\n"
                                      "QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
                                      "{\n"
                                      "     background: none;\n"
                                      "}\n"
                                      "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
                                      "{\n"
                                      "     background: none;\n"
                                      "}\n"
                                      " QScrollBar:vertical {\n"
                                      "	border: none;\n"
                                      "    background: rgb(52, 59, 72);\n"
                                      "    width: 14px;\n"
                                      "    margin: 21px 0 21px 0;\n"
                                      "	border-radius: 0px;\n"
                                      " }\n"
                                      " QScrollBar::handle:vertical {	\n"
                                      "	background: rgb(85, 170, 255);\n"
                                      "    min-height: 25px;\n"
                                      "	border-radius: 7px\n"
                                      " }\n"
                                      " QScrollBar::add-line:vertical {\n"
                                      "     border: none;\n"
                                      "    background: rgb(55, 63, 77);\n"
                                      "     height: 20px;\n"
                                      "	border-bottom-left-radius: 7px;\n"
                                      "    border-bottom-right-radius: 7px;\n"
                                      "     subcontrol-position: bottom;\n"
                                      "     subcontrol-origin: margin;\n"
                                      " }\n"
                                      " QScrollBar::sub-line:vertical {\n"
                                      "	border: none;\n"
                                      "    background: rgb(55, 63"
                                      ", 77);\n"
                                      "     height: 20px;\n"
                                      "	border-top-left-radius: 7px;\n"
                                      "    border-top-right-radius: 7px;\n"
                                      "     subcontrol-position: top;\n"
                                      "     subcontrol-origin: margin;\n"
                                      " }\n"
                                      " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                      "     background: none;\n"
                                      " }\n"
                                      "\n"
                                      " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                      "     background: none;\n"
                                      " }\n"
                                      "\n"
                                      "/* CHECKBOX */\n"
                                      "QCheckBox::indicator {\n"
                                      "    border: 3px solid rgb(52, 59, 72);\n"
                                      "	width: 15px;\n"
                                      "	height: 15px;\n"
                                      "	border-radius: 10px;\n"
                                      "    background: rgb(44, 49, 60);\n"
                                      "}\n"
                                      "QCheckBox::indicator:hover {\n"
                                      "    border: 3px solid rgb(58, 66, 81);\n"
                                      "}\n"
                                      "QCheckBox::indicator:checked {\n"
                                      "    background: 3px solid rgb(52, 59, 72);\n"
                                      "	border: 3px solid rgb(52, 59, 72);	\n"
                                      "	background-image: url(:/16x16/icons/16x16/cil-check-alt.png);\n"
                                      "}\n"
                                      "\n"
                                      "/* RADIO BUTTON */\n"
                                      "QRadioButton::indicator {\n"
                                      "    border: 3px solid rgb(52, 59, 72);\n"
                                      "	width: 15px;\n"
                                      "	height: 15px;\n"
                                      "	border-radius"
                                      ": 10px;\n"
                                      "    background: rgb(44, 49, 60);\n"
                                      "}\n"
                                      "QRadioButton::indicator:hover {\n"
                                      "    border: 3px solid rgb(58, 66, 81);\n"
                                      "}\n"
                                      "QRadioButton::indicator:checked {\n"
                                      "    background: 3px solid rgb(94, 106, 130);\n"
                                      "	border: 3px solid rgb(52, 59, 72);	\n"
                                      "}\n"
                                      "\n"
                                      "/* COMBOBOX */\n"
                                      "QComboBox{\n"
                                      "	background-color: rgb(27, 29, 35);\n"
                                      "	border-radius: 5px;\n"
                                      "	border: 2px solid rgb(27, 29, 35);\n"
                                      "	padding: 5px;\n"
                                      "	padding-left: 10px;\n"
                                      "}\n"
                                      "QComboBox:hover{\n"
                                      "	border: 2px solid rgb(64, 71, 88);\n"
                                      "}\n"
                                      "QComboBox::drop-down {\n"
                                      "	subcontrol-origin: padding;\n"
                                      "	subcontrol-position: top right;\n"
                                      "	width: 25px; \n"
                                      "	border-left-width: 3px;\n"
                                      "	border-left-color: rgba(39, 44, 54, 150);\n"
                                      "	border-left-style: solid;\n"
                                      "	border-top-right-radius: 3px;\n"
                                      "	border-bottom-right-radius: 3px;	\n"
                                      "	background-image: url(:/16x16/icons/16x16/cil-arrow-bottom.png);\n"
                                      "	background-position: center;\n"
                                      "	background-repeat: no-reperat;\n"
                                      " }\n"
                                      "QComboBox QAbstractItemView {\n"
                                      "	color: rgb("
                                      "85, 170, 255);	\n"
                                      "	background-color: rgb(27, 29, 35);\n"
                                      "	padding: 10px;\n"
                                      "	selection-background-color: rgb(39, 44, 54);\n"
                                      "}\n"
                                      "\n"
                                      "/* SLIDERS */\n"
                                      "QSlider::groove:horizontal {\n"
                                      "    border-radius: 9px;\n"
                                      "    height: 18px;\n"
                                      "	margin: 0px;\n"
                                      "	background-color: rgb(52, 59, 72);\n"
                                      "}\n"
                                      "QSlider::groove:horizontal:hover {\n"
                                      "	background-color: rgb(55, 62, 76);\n"
                                      "}\n"
                                      "QSlider::handle:horizontal {\n"
                                      "    background-color: rgb(85, 170, 255);\n"
                                      "    border: none;\n"
                                      "    height: 18px;\n"
                                      "    width: 18px;\n"
                                      "    margin: 0px;\n"
                                      "	border-radius: 9px;\n"
                                      "}\n"
                                      "QSlider::handle:horizontal:hover {\n"
                                      "    background-color: rgb(105, 180, 255);\n"
                                      "}\n"
                                      "QSlider::handle:horizontal:pressed {\n"
                                      "    background-color: rgb(65, 130, 195);\n"
                                      "}\n"
                                      "\n"
                                      "QSlider::groove:vertical {\n"
                                      "    border-radius: 9px;\n"
                                      "    width: 18px;\n"
                                      "    margin: 0px;\n"
                                      "	background-color: rgb(52, 59, 72);\n"
                                      "}\n"
                                      "QSlider::groove:vertical:hover {\n"
                                      "	background-color: rgb(55, 62, 76);\n"
                                      "}\n"
                                      "QSlider::handle:verti"
                                      "cal {\n"
                                      "    background-color: rgb(85, 170, 255);\n"
                                      "	border: none;\n"
                                      "    height: 18px;\n"
                                      "    width: 18px;\n"
                                      "    margin: 0px;\n"
                                      "	border-radius: 9px;\n"
                                      "}\n"
                                      "QSlider::handle:vertical:hover {\n"
                                      "    background-color: rgb(105, 180, 255);\n"
                                      "}\n"
                                      "QSlider::handle:vertical:pressed {\n"
                                      "    background-color: rgb(65, 130, 195);\n"
                                      "}\n"
                                      "\n"
                                      "")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_main)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_top = QFrame(self.frame_main)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setMinimumSize(QSize(0, 65))
        self.frame_top.setMaximumSize(QSize(16777215, 65))
        self.frame_top.setStyleSheet(u"background-color: transparent;")
        self.frame_top.setFrameShape(QFrame.NoFrame)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_toggle = QFrame(self.frame_top)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMaximumSize(QSize(70, 16777215))
        self.frame_toggle.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_toggle.setFrameShape(QFrame.NoFrame)
        self.frame_toggle.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_toggle)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_toggle_menu = QPushButton(self.frame_toggle)
        self.btn_toggle_menu.setObjectName(u"btn_toggle_menu")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_toggle_menu.sizePolicy().hasHeightForWidth())
        self.btn_toggle_menu.setSizePolicy(sizePolicy)
        self.btn_toggle_menu.setStyleSheet(u"QPushButton {\n"
                                           "	background-image: url(:/24x24/icons/24x24/cil-menu.png);\n"
                                           "	background-position: center;\n"
                                           "	background-repeat: no-reperat;\n"
                                           "	border: none;\n"
                                           "	background-color: rgb(27, 29, 35);\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "	background-color: rgb(33, 37, 43);\n"
                                           "}\n"
                                           "QPushButton:pressed {	\n"
                                           "	background-color: rgb(85, 170, 255);\n"
                                           "}")

        self.verticalLayout_3.addWidget(self.btn_toggle_menu)

        self.horizontalLayout_3.addWidget(self.frame_toggle)

        self.frame_top_right = QFrame(self.frame_top)
        self.frame_top_right.setObjectName(u"frame_top_right")
        self.frame_top_right.setStyleSheet(u"background: transparent;")
        self.frame_top_right.setFrameShape(QFrame.NoFrame)
        self.frame_top_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_top_right)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_top_btns = QFrame(self.frame_top_right)
        self.frame_top_btns.setObjectName(u"frame_top_btns")
        self.frame_top_btns.setMaximumSize(QSize(16777215, 42))
        self.frame_top_btns.setStyleSheet(u"background-color: rgba(27, 29, 35, 200)")
        self.frame_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_top_btns)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_label_top_btns = QFrame(self.frame_top_btns)
        self.frame_label_top_btns.setObjectName(u"frame_label_top_btns")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_label_top_btns.sizePolicy().hasHeightForWidth())
        self.frame_label_top_btns.setSizePolicy(sizePolicy1)
        self.frame_label_top_btns.setFrameShape(QFrame.NoFrame)
        self.frame_label_top_btns.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_label_top_btns)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(5, 0, 10, 0)
        self.frame_icon_top_bar = QFrame(self.frame_label_top_btns)
        self.frame_icon_top_bar.setObjectName(u"frame_icon_top_bar")
        self.frame_icon_top_bar.setMaximumSize(QSize(30, 30))
        self.frame_icon_top_bar.setStyleSheet(u"background: transparent;\n"
                                              "background-image: url(:/16x16/icons/16x16/cil-terminal.png);\n"
                                              "background-position: center;\n"
                                              "background-repeat: no-repeat;\n"
                                              "")
        self.frame_icon_top_bar.setFrameShape(QFrame.StyledPanel)
        self.frame_icon_top_bar.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_10.addWidget(self.frame_icon_top_bar)

        self.label_title_bar_top = QLabel(self.frame_label_top_btns)
        self.label_title_bar_top.setObjectName(u"label_title_bar_top")
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(10)
        font1.setBold(True)
        font1.Weight(75)
        self.label_title_bar_top.setFont(font1)
        self.label_title_bar_top.setStyleSheet(u"background: transparent;\n"
                                               "")

        self.horizontalLayout_10.addWidget(self.label_title_bar_top)

        self.horizontalLayout_4.addWidget(self.frame_label_top_btns)

        self.frame_btns_right = QFrame(self.frame_top_btns)
        self.frame_btns_right.setObjectName(u"frame_btns_right")
        sizePolicy1.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy1)
        self.frame_btns_right.setMaximumSize(QSize(120, 16777215))
        self.frame_btns_right.setFrameShape(QFrame.NoFrame)
        self.frame_btns_right.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_minimize = QPushButton(self.frame_btns_right)
        self.btn_minimize.setObjectName(u"btn_minimize")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_minimize.sizePolicy().hasHeightForWidth())
        self.btn_minimize.setSizePolicy(sizePolicy2)
        self.btn_minimize.setMinimumSize(QSize(40, 0))
        self.btn_minimize.setMaximumSize(QSize(40, 16777215))
        self.btn_minimize.setStyleSheet(u"QPushButton {	\n"
                                        "	border: none;\n"
                                        "	background-color: transparent;\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "	background-color: rgb(52, 59, 72);\n"
                                        "}\n"
                                        "QPushButton:pressed {	\n"
                                        "	background-color: rgb(85, 170, 255);\n"
                                        "}")
        icon = QIcon()
        icon.addFile(u":/16x16/icons/16x16/cil-window-minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_minimize.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.btn_minimize)

        self.btn_maximize_restore = QPushButton(self.frame_btns_right)
        self.btn_maximize_restore.setObjectName(u"btn_maximize_restore")
        sizePolicy2.setHeightForWidth(self.btn_maximize_restore.sizePolicy().hasHeightForWidth())
        self.btn_maximize_restore.setSizePolicy(sizePolicy2)
        self.btn_maximize_restore.setMinimumSize(QSize(40, 0))
        self.btn_maximize_restore.setMaximumSize(QSize(40, 16777215))
        self.btn_maximize_restore.setStyleSheet(u"QPushButton {	\n"
                                                "	border: none;\n"
                                                "	background-color: transparent;\n"
                                                "}\n"
                                                "QPushButton:hover {\n"
                                                "	background-color: rgb(52, 59, 72);\n"
                                                "}\n"
                                                "QPushButton:pressed {	\n"
                                                "	background-color: rgb(85, 170, 255);\n"
                                                "}")
        icon1 = QIcon()
        icon1.addFile(u":/16x16/icons/16x16/cil-window-maximize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_maximize_restore.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.btn_maximize_restore)

        self.btn_close = QPushButton(self.frame_btns_right)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy2.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy2)
        self.btn_close.setMinimumSize(QSize(40, 0))
        self.btn_close.setMaximumSize(QSize(40, 16777215))
        self.btn_close.setStyleSheet(u"QPushButton {	\n"
                                     "	border: none;\n"
                                     "	background-color: transparent;\n"
                                     "}\n"
                                     "QPushButton:hover {\n"
                                     "	background-color: rgb(52, 59, 72);\n"
                                     "}\n"
                                     "QPushButton:pressed {	\n"
                                     "	background-color: rgb(85, 170, 255);\n"
                                     "}")
        icon2 = QIcon()
        icon2.addFile(u":/16x16/icons/16x16/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_close.setIcon(icon2)

        self.horizontalLayout_5.addWidget(self.btn_close)

        self.horizontalLayout_4.addWidget(self.frame_btns_right, 0, Qt.AlignRight)

        self.verticalLayout_2.addWidget(self.frame_top_btns)

        self.frame_top_info = QFrame(self.frame_top_right)
        self.frame_top_info.setObjectName(u"frame_top_info")
        self.frame_top_info.setMaximumSize(QSize(16777215, 65))
        self.frame_top_info.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        self.frame_top_info.setFrameShape(QFrame.NoFrame)
        self.frame_top_info.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_top_info)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, 0, 10, 0)
        self.label_top_info_1 = QLabel(self.frame_top_info)
        self.label_top_info_1.setObjectName(u"label_top_info_1")
        self.label_top_info_1.setMaximumSize(QSize(16777215, 15))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        self.label_top_info_1.setFont(font2)
        self.label_top_info_1.setStyleSheet(u"color: rgb(98, 103, 111); ")

        self.horizontalLayout_8.addWidget(self.label_top_info_1)

        self.label_top_info_2 = QLabel(self.frame_top_info)
        self.label_top_info_2.setObjectName(u"label_top_info_2")
        self.label_top_info_2.setMinimumSize(QSize(0, 0))
        self.label_top_info_2.setMaximumSize(QSize(250, 20))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setBold(True)
        font3.Weight(75)
        self.label_top_info_2.setFont(font3)
        self.label_top_info_2.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_top_info_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_top_info_2)
        self.verticalLayout_2.addWidget(self.frame_top_info)
        self.horizontalLayout_3.addWidget(self.frame_top_right)
        self.verticalLayout.addWidget(self.frame_top)

        self.frame_center = QFrame(self.frame_main)
        self.frame_center.setObjectName(u"frame_center")
        sizePolicy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy)
        self.frame_center.setStyleSheet(u"background-color: rgb(40, 44, 52);")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_left_menu = QFrame(self.frame_center)
        self.frame_left_menu.setObjectName(u"frame_left_menu")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(sizePolicy3)
        self.frame_left_menu.setMinimumSize(QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QSize(70, 16777215))
        self.frame_left_menu.setLayoutDirection(Qt.LeftToRight)
        self.frame_left_menu.setStyleSheet(u"background-color: rgb(27, 29, 35);")
        self.frame_left_menu.setFrameShape(QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_5.setSpacing(1)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_menus = QFrame(self.frame_left_menu)
        self.frame_menus.setObjectName(u"frame_menus")
        self.frame_menus.setFrameShape(QFrame.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Raised)
        self.layout_menus = QVBoxLayout(self.frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setObjectName(u"layout_menus")
        self.layout_menus.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_5.addWidget(self.frame_menus, 0, Qt.AlignTop)

        self.frame_extra_menus = QFrame(self.frame_left_menu)
        self.frame_extra_menus.setObjectName(u"frame_extra_menus")
        sizePolicy3.setHeightForWidth(self.frame_extra_menus.sizePolicy().hasHeightForWidth())
        self.frame_extra_menus.setSizePolicy(sizePolicy3)
        self.frame_extra_menus.setFrameShape(QFrame.NoFrame)
        self.frame_extra_menus.setFrameShadow(QFrame.Raised)
        self.layout_menu_bottom = QVBoxLayout(self.frame_extra_menus)
        self.layout_menu_bottom.setSpacing(10)
        self.layout_menu_bottom.setObjectName(u"layout_menu_bottom")
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 25)
        self.label_user_icon = QLabel(self.frame_extra_menus)
        self.label_user_icon.setObjectName(u"label_user_icon")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_user_icon.sizePolicy().hasHeightForWidth())
        self.label_user_icon.setSizePolicy(sizePolicy4)
        self.label_user_icon.setMinimumSize(QSize(60, 60))
        self.label_user_icon.setMaximumSize(QSize(60, 60))
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(12)
        self.label_user_icon.setFont(font4)
        self.label_user_icon.setStyleSheet(u"QLabel {\n"
                                           "	border-radius: 30px;\n"
                                           "	background-color: rgb(44, 49, 60);\n"
                                           "	border: 5px solid rgb(39, 44, 54);\n"
                                           "	background-position: center;\n"
                                           "	background-repeat: no-repeat;\n"
                                           "}")
        self.label_user_icon.setAlignment(Qt.AlignCenter)
        self.layout_menu_bottom.addWidget(self.label_user_icon, 0, Qt.AlignHCenter)
        self.verticalLayout_5.addWidget(self.frame_extra_menus, 0, Qt.AlignBottom)
        self.horizontalLayout_2.addWidget(self.frame_left_menu)

        self.frame_content_right = QFrame(self.frame_center)
        self.frame_content_right.setObjectName(u"frame_content_right")
        self.frame_content_right.setStyleSheet(u"background-color: rgb(44, 49, 60);")
        self.frame_content_right.setFrameShape(QFrame.NoFrame)
        self.frame_content_right.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_content_right)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_content = QFrame(self.frame_content_right)
        self.frame_content.setObjectName(u"frame_content")
        self.frame_content.setFrameShape(QFrame.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_content)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.stackedWidget = QStackedWidget(self.frame_content)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")

        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.verticalLayout_10 = QVBoxLayout(self.page_home)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")

        spacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                 QSizePolicy.Policy.Expanding)
        # self.verticalLayout_10.addItem(spacerItem)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem1)
        self.gsg56_icon = QLabel(parent=self.page_home)
        self.gsg56_icon.setMinimumSize(QSize(600, 300))
        self.gsg56_icon.setMaximumSize(QSize(600, 300))
        self.gsg56_icon.setFrameShape(QFrame.Shape.NoFrame)
        self.gsg56_icon.setFrameShadow(QFrame.Shadow.Sunken)
        self.gsg56_icon.setText("")
        self.gsg56_icon.setTextFormat(Qt.TextFormat.AutoText)
        self.gsg56_icon.setPixmap(
            QPixmap(
                "Orolia_GSG5.png").scaled(
                600, 300, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.gsg56_icon.setStyleSheet("border-radius:50px")

        self.gsg56_icon.setScaledContents(True)
        self.gsg56_icon.setObjectName("gsg56_icon")
        self.horizontalLayout_15.addWidget(self.gsg56_icon)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem2)
        self.verticalLayout_12.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem3)
        self.GSG56_scenarios_label = QLabel(parent=self.page_home)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush)
        brush = QBrush(QColor(59, 66, 81))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush)
        brush = QBrush(QColor(49, 55, 67))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush)
        brush = QBrush(QColor(26, 29, 36))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush)
        brush = QBrush(QColor(19, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 220))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush)
        brush = QBrush(QColor(255, 255, 255, 127))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        brush = QBrush(QColor(240, 240, 240))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush)
        brush = QBrush(QColor(227, 227, 227))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush)
        brush = QBrush(QColor(160, 160, 160))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush)
        brush = QBrush(QColor(160, 160, 160))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        brush = QBrush(QColor(240, 240, 240))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        brush = QBrush(QColor(105, 105, 105))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush)
        brush = QBrush(QColor(245, 245, 245))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 220))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush)
        brush = QBrush(QColor(0, 0, 0, 128))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush)
        brush = QBrush(QColor(59, 66, 81))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush)
        brush = QBrush(QColor(49, 55, 67))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush)
        brush = QBrush(QColor(26, 29, 36))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush)
        brush = QBrush(QColor(245, 245, 245))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 220))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush)
        brush = QBrush(QColor(0, 0, 0, 128))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush)
        self.GSG56_scenarios_label.setPalette(palette)
        font = QFont()
        font.setPointSize(35)
        self.GSG56_scenarios_label.setFont(font)
        self.GSG56_scenarios_label.setObjectName("GSG56_scenarios_label")
        self.horizontalLayout_16.addWidget(self.GSG56_scenarios_label)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem4)
        self.verticalLayout_12.addLayout(self.horizontalLayout_16)
        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Expanding)
        self.verticalLayout_12.addItem(spacerItem5)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pushButton_gsg56_select_folder = QPushButton(parent=self.page_home)
        self.pushButton_gsg56_select_folder.setMinimumSize(QSize(150, 30))

        font8 = QFont()
        font8.setFamily(u"Segoe UI")
        font8.setPointSize(9)
        self.pushButton_gsg56_select_folder.setFont(font8)
        self.pushButton_gsg56_select_folder.setStyleSheet(u"QPushButton {\n"
                                                          "	border: 2px solid rgb(52, 59, 72);\n"
                                                          "	border-radius: 5px;	\n"
                                                          "	background-color: rgb(52, 59, 72);\n"
                                                          "}\n"
                                                          "QPushButton:hover {\n"
                                                          "	background-color: rgb(57, 65, 80);\n"
                                                          "	border: 2px solid rgb(61, 70, 86);\n"
                                                          "}\n"
                                                          "QPushButton:pressed {	\n"
                                                          "	background-color: rgb(35, 40, 49);\n"
                                                          "	border: 2px solid rgb(43, 50, 61);\n"
                                                          "}")
        icon3 = QIcon()
        icon3.addFile(u":/16x16/icons/16x16/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_gsg56_select_folder.setIcon(icon3)
        self.pushButton_gsg56_select_folder.setObjectName("pushButton_gsg56_select_folder")
        self.horizontalLayout_14.addWidget(self.pushButton_gsg56_select_folder)
        self.lineEdit_gsg56_folder_name = QLineEdit(parent=self.page_home)
        self.lineEdit_gsg56_folder_name.setMinimumSize(QSize(5000, 30))
        self.lineEdit_gsg56_folder_name.setStyleSheet("QLineEdit {\n"
                                                      "    background-color: rgb(27, 29, 35);\n"
                                                      "    border-radius: 5px;\n"
                                                      "    border: 2px solid rgb(27, 29, 35);\n"
                                                      "    padding-left: 10px;\n"
                                                      "}\n"
                                                      "QLineEdit:hover {\n"
                                                      "    border: 2px solid rgb(64, 71, 88);\n"
                                                      "}\n"
                                                      "QLineEdit:focus {\n"
                                                      "    border: 2px solid rgb(91, 101, 124);\n"
                                                      "}")
        self.lineEdit_gsg56_folder_name.setObjectName("lineEdit_gsg56_folder_name")
        self.horizontalLayout_14.addWidget(self.lineEdit_gsg56_folder_name)
        self.verticalLayout_12.addLayout(self.horizontalLayout_14)
        self.gridLayout_3.addLayout(self.verticalLayout_12, 0, 0, 1, 1)
        self.verticalLayout_10.addLayout(self.gridLayout_3)
        self.label_2 = QLabel(parent=self.page_home)
        self.label_2.setStyleSheet("color: rgb(98, 103, 111);")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_10.addWidget(self.label_2)
        spacerItem6 = QSpacerItem(30, 40, QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Expanding)
        self.verticalLayout_10.addItem(spacerItem6)
        # self.label_6 = QLabel(self.page_home)
        # self.label_6.setObjectName(u"label_6")
        # font5 = QFont()
        # font5.setFamily(u"Segoe UI")
        # font5.setPointSize(40)
        # self.label_6.setFont(font5)
        # self.label_6.setStyleSheet(u"")
        # self.label_6.setAlignment(Qt.AlignCenter)
        #
        # self.verticalLayout_10.addWidget(self.label_6)
        #
        # self.label = QLabel(self.page_home)
        # self.label.setObjectName(u"label")
        # font6 = QFont()
        # font6.setFamily(u"Segoe UI")
        # font6.setPointSize(14)
        # self.label.setFont(font6)
        # self.label.setAlignment(Qt.AlignCenter)
        #
        # self.verticalLayout_10.addWidget(self.label)
        #
        # self.label_7 = QLabel(self.page_home)
        # self.label_7.setObjectName(u"label_7")
        # font7 = QFont()
        # font7.setFamily(u"Segoe UI")
        # font7.setPointSize(15)
        # self.label_7.setFont(font7)
        # self.label_7.setAlignment(Qt.AlignCenter)
        #
        # self.verticalLayout_10.addWidget(self.label_7)

        self.tableWidget_home = QTableWidget(self.page_home)
        if (self.tableWidget_home.columnCount() < 2):
            self.tableWidget_home.setColumnCount(2)

        __QTableWidgetitem_home = QTableWidgetItem()
        self.tableWidget_home.setHorizontalHeaderItem(0, __QTableWidgetitem_home)
        __QTableWidgetitem_home1 = QTableWidgetItem()
        self.tableWidget_home.setHorizontalHeaderItem(1, __QTableWidgetitem_home1)

        if (self.tableWidget_home.rowCount() < 5):
            self.tableWidget_home.setRowCount(5)
        __QTableWidgetitem_home4 = QTableWidgetItem()
        __QTableWidgetitem_home4.setFont(font2)
        self.tableWidget_home.setVerticalHeaderItem(0, __QTableWidgetitem_home4)
        __QTableWidgetitem_home5 = QTableWidgetItem()
        self.tableWidget_home.setVerticalHeaderItem(1, __QTableWidgetitem_home5)
        __QTableWidgetitem_home6 = QTableWidgetItem()
        self.tableWidget_home.setVerticalHeaderItem(2, __QTableWidgetitem_home6)
        __QTableWidgetitem_home7 = QTableWidgetItem()
        self.tableWidget_home.setVerticalHeaderItem(3, __QTableWidgetitem_home7)
        __QTableWidgetitem_home8 = QTableWidgetItem()
        self.tableWidget_home.setVerticalHeaderItem(4, __QTableWidgetitem_home8)
        __QTableWidgetitem_home9 = QTableWidgetItem()
        self.tableWidget_home.setVerticalHeaderItem(5, __QTableWidgetitem_home9)

        __QTableWidgetitem_home21 = QTableWidgetItem()
        self.tableWidget_home.setItem(0, 1, __QTableWidgetitem_home21)
        __QTableWidgetitem_home22 = QTableWidgetItem()
        self.tableWidget_home.setItem(0, 2, __QTableWidgetitem_home22)
        __QTableWidgetitem_home23 = QTableWidgetItem()
        self.tableWidget_home.setItem(0, 3, __QTableWidgetitem_home23)

        self.tableWidget_home.setObjectName(u"tableWidget_home")
        sizePolicy.setHeightForWidth(self.tableWidget_home.sizePolicy().hasHeightForWidth())
        self.tableWidget_home.setSizePolicy(sizePolicy)
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        brush15 = QBrush(QColor(39, 44, 54, 255))
        brush15.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush15)
        brush16 = QBrush(QColor(210, 210, 210, 128))
        brush16.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush16)
        # endif
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        brush17 = QBrush(QColor(210, 210, 210, 128))
        brush17.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush17)
        # endif
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        brush18 = QBrush(QColor(210, 210, 210, 128))
        brush18.setStyle(Qt.NoBrush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush18)
        # endif
        self.tableWidget_home.setPalette(palette1)
        self.tableWidget_home.setStyleSheet(u"QTableWidget {	\n"
                                            "	background-color: rgb(39, 44, 54);\n"
                                            "	padding: 10px;\n"
                                            "	border-radius: 5px;\n"
                                            "	gridline-color: rgb(44, 49, 60);\n"
                                            "	border-bottom: 1px solid rgb(44, 49, 60);\n"
                                            "}\n"
                                            "QTableWidget::item{\n"
                                            "	border-color: rgb(44, 49, 60);\n"
                                            "	padding-left: 5px;\n"
                                            "	padding-right: 5px;\n"
                                            "	gridline-color: rgb(44, 49, 60);\n"
                                            "}\n"
                                            "QTableWidget::item:selected{\n"
                                            "	background-color: rgb(85, 170, 255);\n"
                                            "}\n"
                                            "QScrollBar:horizontal {\n"
                                            "    border: none;\n"
                                            "    background: rgb(52, 59, 72);\n"
                                            "    height: 14px;\n"
                                            "    margin: 0px 21px 0 21px;\n"
                                            "	border-radius: 0px;\n"
                                            "}\n"
                                            " QScrollBar:vertical {\n"
                                            "	border: none;\n"
                                            "    background: rgb(52, 59, 72);\n"
                                            "    width: 14px;\n"
                                            "    margin: 21px 0 21px 0;\n"
                                            "	border-radius: 0px;\n"
                                            " }\n"
                                            "QHeaderView::section{\n"
                                            "	Background-color: rgb(39, 44, 54);\n"
                                            "	max-width: 30px;\n"
                                            "	border: 1px solid rgb(44, 49, 60);\n"
                                            "	border-style: none;\n"
                                            "    border-bottom: 1px solid rgb(44, 49, 60);\n"
                                            "    border-right: 1px solid rgb(44, 49, 60);\n"
                                            "}\n"
                                            ""
                                            "QTableWidget::horizontalHeader {	\n"
                                            "	background-color: rgb(81, 255, 0);\n"
                                            "}\n"
                                            "QHeaderView::section:horizontal\n"
                                            "{\n"
                                            "    border: 1px solid rgb(32, 34, 42);\n"
                                            "	background-color: rgb(27, 29, 35);\n"
                                            "	padding: 3px;\n"
                                            "	border-top-left-radius: 7px;\n"
                                            "    border-top-right-radius: 7px;\n"
                                            "}\n"
                                            "QHeaderView::section:vertical\n"
                                            "{\n"
                                            "    border: 1px solid rgb(44, 49, 60);\n"
                                            "}\n"
                                            "")
        self.tableWidget_home.setFrameShape(QFrame.NoFrame)
        self.tableWidget_home.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableWidget_home.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget_home.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_home.setAlternatingRowColors(False)
        self.tableWidget_home.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget_home.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_home.setShowGrid(True)
        self.tableWidget_home.setGridStyle(Qt.SolidLine)
        self.tableWidget_home.setSortingEnabled(False)
        self.tableWidget_home.horizontalHeader().setVisible(True)
        self.tableWidget_home.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget_home.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget_home.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_home.verticalHeader().setVisible(False)
        self.tableWidget_home.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_home.verticalHeader().setHighlightSections(False)
        self.tableWidget_home.verticalHeader().setStretchLastSection(True)

        self.verticalLayout_10.addWidget(self.tableWidget_home)

        self.verticalLayout_10.addItem(spacerItem6)

        self.stackedWidget.addWidget(self.page_home)

        self.page_convert_to_skydel = QWidget()
        self.page_convert_to_skydel.setObjectName(u"page_convert_to_skydel")

        self.verticalLayout_100 = QVBoxLayout(self.page_convert_to_skydel)
        self.verticalLayout_100.setObjectName(u"verticalLayout_100")

        spacerItem0 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                  QSizePolicy.Policy.Expanding)
        # self.verticalLayout_100.addItem(spacerItem0)
        self.gridLayout_30 = QGridLayout()
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.verticalLayout_120 = QVBoxLayout()
        self.verticalLayout_120.setObjectName("verticalLayout_120")
        self.horizontalLayout_150 = QHBoxLayout()
        self.horizontalLayout_150.setObjectName("horizontalLayout_150")
        spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Minimum)
        self.horizontalLayout_150.addItem(spacerItem10)

        self.skydel_icon = QLabel(parent=self.page_convert_to_skydel)
        self.skydel_icon.setMinimumSize(QSize(200, 250))
        self.skydel_icon.setMaximumSize(QSize(200, 250))
        self.skydel_icon.setFrameShape(QFrame.Shape.NoFrame)
        self.skydel_icon.setFrameShadow(QFrame.Shadow.Sunken)
        self.skydel_icon.setText("")
        self.skydel_icon.setTextFormat(Qt.TextFormat.AutoText)
        self.skydel_icon.setPixmap(
            QPixmap(
                "skydel_white.png").scaled(
                200, 250, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        # self.skydel_icon.setStyleSheet("border-radius:50px")

        self.skydel_icon.setScaledContents(True)
        self.skydel_icon.setObjectName("skydel_icon")

        self.horizontalLayout_150.addWidget(self.skydel_icon)
        spacerItem20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Minimum)
        self.horizontalLayout_150.addItem(spacerItem20)
        self.verticalLayout_120.addLayout(self.horizontalLayout_150)
        self.horizontalLayout_160 = QHBoxLayout()
        self.horizontalLayout_160.setObjectName("horizontalLayout_160")
        spacerItem30 = QSpacerItem(60, 40, QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Minimum)
        self.horizontalLayout_160.addItem(spacerItem30)
        self.skydel_conversion_label = QLabel(parent=self.page_convert_to_skydel)
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush)
        brush = QBrush(QColor(59, 66, 81))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush)
        brush = QBrush(QColor(49, 55, 67))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush)
        brush = QBrush(QColor(26, 29, 36))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush)
        brush = QBrush(QColor(19, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 220))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush)
        brush = QBrush(QColor(255, 255, 255, 127))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        brush = QBrush(QColor(240, 240, 240))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush)
        brush = QBrush(QColor(227, 227, 227))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush)
        brush = QBrush(QColor(160, 160, 160))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush)
        brush = QBrush(QColor(160, 160, 160))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        brush = QBrush(QColor(240, 240, 240))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush)
        brush = QBrush(QColor(105, 105, 105))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush)
        brush = QBrush(QColor(245, 245, 245))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 220))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush)
        brush = QBrush(QColor(0, 0, 0, 128))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush)
        brush = QBrush(QColor(59, 66, 81))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush)
        brush = QBrush(QColor(49, 55, 67))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush)
        brush = QBrush(QColor(26, 29, 36))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush)
        brush = QBrush(QColor(20, 22, 27))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush)
        brush = QBrush(QColor(39, 44, 54))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush)
        brush = QBrush(QColor(245, 245, 245))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush)
        brush = QBrush(QColor(255, 255, 220))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush)
        brush = QBrush(QColor(0, 0, 0, 128))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush)
        self.skydel_conversion_label.setPalette(palette)
        font = QFont()
        font.setPointSize(35)
        self.skydel_conversion_label.setFont(font)
        self.skydel_conversion_label.setObjectName("skydel_conversion_label")
        self.horizontalLayout_160.addWidget(self.skydel_conversion_label)
        spacerItem40 = QSpacerItem(60, 110, QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Minimum)
        self.horizontalLayout_160.addItem(spacerItem40)
        self.verticalLayout_120.addLayout(self.horizontalLayout_160)
        spacerItem50 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                   QSizePolicy.Policy.Expanding)
        self.verticalLayout_120.addItem(spacerItem50)

        self.horizontalLayout_140 = QHBoxLayout()
        self.horizontalLayout_140.setObjectName("horizontalLayout_14")
        self.pushButton_convert_skydel = QPushButton(parent=self.page_convert_to_skydel)
        self.pushButton_convert_skydel.setMinimumSize(QSize(150, 30))

        font8 = QFont()
        font8.setFamily(u"Segoe UI")
        font8.setPointSize(9)
        self.pushButton_convert_skydel.setFont(font8)
        self.pushButton_convert_skydel.setStyleSheet(u"QPushButton {\n"
                                                     "	border: 2px solid rgb(52, 59, 72);\n"
                                                     "	border-radius: 5px;	\n"
                                                     "	background-color: rgb(52, 59, 72);\n"
                                                     "}\n"
                                                     "QPushButton:hover {\n"
                                                     "	background-color: rgb(57, 65, 80);\n"
                                                     "	border: 2px solid rgb(61, 70, 86);\n"
                                                     "}\n"
                                                     "QPushButton:pressed {	\n"
                                                     "	background-color: rgb(35, 40, 49);\n"
                                                     "	border: 2px solid rgb(43, 50, 61);\n"
                                                     "}")
        icon30 = QIcon()
        icon30.addFile(u":/16x16/icons/16x16/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_convert_skydel.setIcon(icon30)
        self.pushButton_convert_skydel.setObjectName("pushButton_skydel_convert")

        self.script_convert_status = QLabel(parent=self.page_convert_to_skydel)
        self.script_convert_status.setObjectName(u"script_convert_status")
        self.script_convert_status.setAutoFillBackground(False)
        self.script_convert_status.setStyleSheet(u"")
        self.script_convert_status.setEnabled(False)

        self.lineEdit_skydel_folder_name = QLineEdit(parent=self.page_convert_to_skydel)
        self.lineEdit_skydel_folder_name.setMinimumSize(QSize(5000, 30))
        self.lineEdit_skydel_folder_name.setStyleSheet("QLineEdit {\n"
                                                       "    background-color: rgb(27, 29, 35);\n"
                                                       "    border-radius: 5px;\n"
                                                       "    border: 2px solid rgb(27, 29, 35);\n"
                                                       "    padding-left: 10px;\n"
                                                       "}\n"
                                                       "QLineEdit:hover {\n"
                                                       "    border: 2px solid rgb(64, 71, 88);\n"
                                                       "}\n"
                                                       "QLineEdit:focus {\n"
                                                       "    border: 2px solid rgb(91, 101, 124);\n"
                                                       "}")
        self.lineEdit_skydel_folder_name.setObjectName("lineedit_skydel_folder_name")

        self.comboBox_skydel_conv = QComboBox(parent=self.page_convert_to_skydel)
        self.comboBox_skydel_conv.addItem("")
        self.comboBox_skydel_conv.addItem("")
        self.comboBox_skydel_conv.addItem("")
        self.comboBox_skydel_conv.addItem("")
        self.comboBox_skydel_conv.setObjectName(u"comboBox")
        self.comboBox_skydel_conv.setFont(font8)
        self.comboBox_skydel_conv.setAutoFillBackground(False)
        self.comboBox_skydel_conv.setStyleSheet(u"QComboBox{\n"
                                                "	background-color: rgb(27, 29, 35);\n"
                                                "	border-radius: 5px;\n"
                                                "	border: 2px solid rgb(27, 29, 35);\n"
                                                "	padding: 5px;\n"
                                                "	padding-left: 10px;\n"
                                                "}\n"
                                                "QComboBox:hover{\n"
                                                "	border: 2px solid rgb(64, 71, 88);\n"
                                                "}\n"
                                                "QComboBox QAbstractItemView {\n"
                                                "	color: rgb(85, 170, 255);	\n"
                                                "	background-color: rgb(27, 29, 35);\n"
                                                "	padding: 10px;\n"
                                                "	selection-background-color: rgb(39, 44, 54);\n"
                                                "}")
        self.comboBox_skydel_conv.setIconSize(QSize(16, 16))
        self.comboBox_skydel_conv.setFrame(True)

        self.horizontalLayout_170 = QHBoxLayout()
        self.horizontalLayout_170.setObjectName("horizontalLayout_17")

        #
        self.skydel_rad_gain_labl = QLabel(parent=self.page_convert_to_skydel)
        self.skydel_rad_gain_labl.setObjectName(u"skydel_output_label")
        self.skydel_rad_gain_labl.setAutoFillBackground(False)
        self.skydel_rad_gain_labl.setStyleSheet(u"")

        self.skydel_rad_edit = QLineEdit(parent=self.page_convert_to_skydel)
        self.skydel_rad_edit.setObjectName(u"lineEdit")
        self.skydel_rad_edit.setMinimumSize(QSize(0, 30))
        self.skydel_rad_edit.setStyleSheet(u"QLineEdit {\n"
                                           "	background-color: rgb(27, 29, 35);\n"
                                           "	border-radius: 5px;\n"
                                           "	border: 2px solid rgb(27, 29, 35);\n"
                                           "	padding-left: 10px;\n"
                                           "}\n"
                                           "QLineEdit:hover {\n"
                                           "	border: 2px solid rgb(64, 71, 88);\n"
                                           "}\n"
                                           "QLineEdit:focus {\n"
                                           "	border: 2px solid rgb(91, 101, 124);\n"
                                           "}")

        # self.skydel_rad_GN_labl = QLabel(parent=self.page_convert_to_skydel)
        # self.skydel_rad_GN_labl.setObjectName(u"skydel_output_label")
        # self.skydel_rad_GN_labl.setAutoFillBackground(False)
        # self.skydel_rad_GN_labl.setStyleSheet(u"")

        self.skydel_GN_checkBox = QCheckBox(parent=self.page_convert_to_skydel)
        self.skydel_GN_checkBox.setStyleSheet("")
        self.skydel_GN_checkBox.setObjectName("checkBox")


        self.horizontalLayout_170.addItem(spacerItem40)
        self.horizontalLayout_170.addWidget(self.skydel_rad_gain_labl)
        self.horizontalLayout_170.addWidget(self.skydel_rad_edit)
        self.horizontalLayout_170.addItem(spacerItem40)
        self.horizontalLayout_170.addWidget(self.pushButton_convert_skydel)
        self.horizontalLayout_170.addItem(spacerItem40)

        self.skydel_output_label_0 = QLabel(parent=self.page_convert_to_skydel)
        self.skydel_output_label_0.setObjectName(u"skydel_output_label")
        self.skydel_output_label_0.setAutoFillBackground(False)
        self.skydel_output_label_0.setStyleSheet(u"")

        self.horizontalLayout_140.addItem(spacerItem40)
        self.horizontalLayout_140.addWidget(self.skydel_output_label_0)
        self.horizontalLayout_140.addWidget(self.comboBox_skydel_conv)
        self.horizontalLayout_140.addItem(spacerItem40)
        self.horizontalLayout_140.addWidget(self.skydel_GN_checkBox)
        self.horizontalLayout_140.addItem(spacerItem40)

        self.verticalLayout_120.addLayout(self.horizontalLayout_140)
        self.verticalLayout_120.addItem(spacerItem50)
        self.verticalLayout_120.addLayout(self.horizontalLayout_170)
        self.verticalLayout_120.addWidget(self.script_convert_status)
        self.verticalLayout_120.addItem(spacerItem50)

        self.gridLayout_30.addLayout(self.verticalLayout_120, 0, 0, 1, 1)
        self.verticalLayout_100.addLayout(self.gridLayout_30)
        self.label_20 = QLabel(parent=self.page_convert_to_skydel)
        self.label_20.setStyleSheet("color: rgb(98, 103, 111);")
        self.label_20.setObjectName("label_2")
        self.verticalLayout_100.addWidget(self.label_20)
        spacerItem60 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                   QSizePolicy.Policy.Expanding)
        self.verticalLayout_100.addWidget(self.lineEdit_skydel_folder_name)

        self.verticalLayout_100.addItem(spacerItem60)
        self.stackedWidget.addWidget(self.page_convert_to_skydel)

        #
        #
        #
        #
        #
        #
        #
        #
        #
        # self.verticalLayout_20 = QVBoxLayout(self.page_convert_to_skydel)
        # self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        #
        #
        #
        # self.gridLayoutWidget = QWidget(parent=self.page_convert_to_skydel)
        # self.gridLayoutWidget.setGeometry(QRect(9, 0, 1071, 251))
        # self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        # self.gridLayout_5__conversion_page = QGridLayout(self.gridLayoutWidget)
        # self.gridLayout_5__conversion_page.setContentsMargins(0, 0, 0, 0)
        # self.gridLayout_5__conversion_page.setObjectName("gridLayout_5__conversion_page")
        #
        # self.Skydel_label_conversion_page = QLabel(parent=self.gridLayoutWidget)
        # self.Skydel_label_conversion_page.setObjectName("Skydel_label_conversion_page")
        #
        # self.Skydel_label_conversion_page.setMinimumSize(QSize(300, 200))
        # self.Skydel_label_conversion_page.setMaximumSize(QSize(300, 200))
        # self.Skydel_label_conversion_page.setFrameShape(QFrame.Shape.NoFrame)
        # self.Skydel_label_conversion_page.setFrameShadow(QFrame.Shadow.Sunken)
        # self.Skydel_label_conversion_page.setText("")
        # self.Skydel_label_conversion_page.setTextFormat(Qt.TextFormat.AutoText)
        # self.Skydel_label_conversion_page.setPixmap(
        #     QPixmap(
        #         "/SKYDEL_LOGO_Safran version_blue.png").scaled(
        #         300, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        # #self.Skydel_label_conversion_page.setStyleSheet("border-radius:50px")
        #
        # self.Skydel_label_conversion_page.setScaledContents(True)
        # self.Skydel_label_conversion_page.setObjectName("skydel_icon")
        # self.gridLayout_5__conversion_page.addWidget(self.Skydel_label_conversion_page, 1, 1, 1, 1)
        #
        # spacerItem7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
        #                                     QSizePolicy.Policy.Expanding)
        # self.gridLayout_5__conversion_page.addItem(spacerItem7, 2, 1, 1, 1)
        # spacerItem8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
        #                                     QSizePolicy.Policy.Expanding)
        # self.gridLayout_5__conversion_page.addItem(spacerItem8, 0, 1, 1, 1)
        # spacerItem9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
        #                                     QSizePolicy.Policy.Minimum)
        # self.gridLayout_5__conversion_page.addItem(spacerItem9, 1, 0, 1, 1)
        # spacerItem10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
        #                                      QSizePolicy.Policy.Minimum)
        # self.gridLayout_5__conversion_page.addItem(spacerItem10, 1, 2, 1, 1)
        # self.verticalLayoutWidget = QWidget(parent=self.page_convert_to_skydel)
        # self.verticalLayoutWidget.setGeometry(QRect(9, 249, 1071, 241))
        # self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        # self.verticalLayout_14_conversion_page = QVBoxLayout(self.verticalLayoutWidget)
        # self.verticalLayout_14_conversion_page.setContentsMargins(0, 0, 0, 0)
        # self.verticalLayout_14_conversion_page.setObjectName("verticalLayout_14_conversion_page")
        # spacerItem11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
        #                                      QSizePolicy.Policy.Expanding)
        # self.verticalLayout_14_conversion_page.addItem(spacerItem11)
        #
        # self.generate_script_conversion_page = QPushButton(parent=self.verticalLayoutWidget)
        # self.generate_script_conversion_page.setObjectName("generate_script_conversion_page")
        # self.generate_script_conversion_page.setMinimumSize(QSize(150, 30))
        #
        # font8 = QFont()
        # font8.setFamily(u"Segoe UI")
        # font8.setPointSize(9)
        # self.generate_script_conversion_page.setFont(font8)
        # self.generate_script_conversion_page.setStyleSheet(u"QPushButton {\n"
        #                                                   "	border: 2px solid rgb(52, 59, 72);\n"
        #                                                   "	border-radius: 5px;	\n"
        #                                                   "	background-color: rgb(52, 59, 72);\n"
        #                                                   "}\n"
        #                                                   "QPushButton:hover {\n"
        #                                                   "	background-color: rgb(57, 65, 80);\n"
        #                                                   "	border: 2px solid rgb(61, 70, 86);\n"
        #                                                   "}\n"
        #                                                   "QPushButton:pressed {	\n"
        #                                                   "	background-color: rgb(35, 40, 49);\n"
        #                                                   "	border: 2px solid rgb(43, 50, 61);\n"
        #                                                   "}")
        # icon3 = QIcon()
        # icon3.addFile(u":/16x16/icons/16x16/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        # self.generate_script_conversion_page.setIcon(icon3)
        # self.generate_script_conversion_page.setObjectName("pushButton_gsg56_select_folder")
        #
        #
        #
        # self.verticalLayout_14_conversion_page.addWidget(self.generate_script_conversion_page)
        # spacerItem12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
        #                                      QSizePolicy.Policy.Expanding)
        # self.verticalLayout_14_conversion_page.addItem(spacerItem12)
        # self.script_path_lineEdit_conversion_page = QLineEdit(parent=self.verticalLayoutWidget)
        # self.script_path_lineEdit_conversion_page.setObjectName("script_path_lineEdit_conversion_page")
        # self.verticalLayout_14_conversion_page.addWidget(self.script_path_lineEdit_conversion_page)
        # spacerItem13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
        #                                      QSizePolicy.Policy.Expanding)
        # self.verticalLayout_14_conversion_page.addItem(spacerItem13)

        self.page_widgets = QWidget()
        self.page_widgets.setObjectName(u"page_widgets")
        self.verticalLayout_6 = QVBoxLayout(self.page_widgets)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame = QFrame(self.page_widgets)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"border-radius: 5px;")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        # self.verticalLayout_15 = QVBoxLayout(self.frame)
        # self.verticalLayout_15.setSpacing(0)
        # self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        # self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        # self.frame_div_content_1 = QFrame(self.frame)
        # self.frame_div_content_1.setObjectName(u"frame_div_content_1")
        # self.frame_div_content_1.setMinimumSize(QSize(0, 110))
        # self.frame_div_content_1.setMaximumSize(QSize(16777215, 110))
        # self.frame_div_content_1.setStyleSheet(u"background-color: rgb(41, 45, 56);\n"
        #                                        "border-radius: 5px;\n"
        #                                        "")
        # self.frame_div_content_1.setFrameShape(QFrame.NoFrame)
        # self.frame_div_content_1.setFrameShadow(QFrame.Raised)
        # # self.verticalLayout_7 = QVBoxLayout(self.frame_div_content_1)
        # # self.verticalLayout_7.setSpacing(0)
        # # self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        # # self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        # self.frame_title_wid_1 = QFrame(self.frame_div_content_1)
        # self.frame_title_wid_1.setObjectName(u"frame_title_wid_1")
        # self.frame_title_wid_1.setMaximumSize(QSize(16777215, 35))
        # self.frame_title_wid_1.setStyleSheet(u"background-color: rgb(39, 44, 54);")
        # self.frame_title_wid_1.setFrameShape(QFrame.StyledPanel)
        # self.frame_title_wid_1.setFrameShadow(QFrame.Raised)
        #self.verticalLayout_8 = QVBoxLayout(self.frame_title_wid_1)
        #self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        # self.labelBoxBlenderInstalation = QLabel(self.frame_title_wid_1)
        # self.labelBoxBlenderInstalation.setObjectName(u"labelBoxBlenderInstalation")
        # self.labelBoxBlenderInstalation.setFont(font1)
        # self.labelBoxBlenderInstalation.setStyleSheet(u"")
        #self.verticalLayout_8.addWidget(self.labelBoxBlenderInstalation)
        #self.verticalLayout_7.addWidget(self.frame_title_wid_1)

        # self.frame_content_wid_1 = QFrame(self.frame_div_content_1)
        # self.frame_content_wid_1.setObjectName(u"frame_content_wid_1")
        # self.frame_content_wid_1.setFrameShape(QFrame.NoFrame)
        # self.frame_content_wid_1.setFrameShadow(QFrame.Raised)
        #self.horizontalLayout_9 = QHBoxLayout(self.frame_content_wid_1)
        #self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        # self.gridLayout = QGridLayout()
        # self.gridLayout.setObjectName(u"gridLayout")
        # self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        #self.lineEdit = QLineEdit(self.frame_content_wid_1)
       # self.lineEdit.setObjectName(u"lineEdit")
        #self.lineEdit.setMinimumSize(QSize(0, 30))
        # self.lineEdit.setStyleSheet(u"QLineEdit {\n"
        #                             "	background-color: rgb(27, 29, 35);\n"
        #                             "	border-radius: 5px;\n"
        #                             "	border: 2px solid rgb(27, 29, 35);\n"
        #                             "	padding-left: 10px;\n"
        #                             "}\n"
        #                             "QLineEdit:hover {\n"
        #                             "	border: 2px solid rgb(64, 71, 88);\n"
        #                             "}\n"
        #                             "QLineEdit:focus {\n"
        #                             "	border: 2px solid rgb(91, 101, 124);\n"
        #                             "}")
        #
        # # self.lineEdit.setPlaceholderText("Test Test")
        # # self.lineEdit.setText("Test Test")
        #
        #
        # self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)


        #self.gridLayout.addWidget(self.pushButton_load_skydel, 0, 1, 1, 1)

        # self.labelVersion_3 = QLabel(self.frame_content_wid_1)
        # self.labelVersion_3.setObjectName(u"labelVersion_3")
        # self.labelVersion_3.setStyleSheet(u"color: rgb(98, 103, 111);")
        # self.labelVersion_3.setLineWidth(1)
        # self.labelVersion_3.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        #self.gridLayout.addWidget(self.labelVersion_3, 1, 0, 1, 2)

        #self.horizontalLayout_9.addLayout(self.gridLayout)

        #self.verticalLayout_7.addWidget(self.frame_content_wid_1)

        #self.verticalLayout_15.addWidget(self.frame_div_content_1)

        self.verticalLayout_6.addWidget(self.frame)

        self.frame_2 = QFrame(self.page_widgets)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 150))
        self.frame_2.setStyleSheet(u"background-color: rgb(39, 44, 54);\n"
                                   "border-radius: 5px;")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        # self.checkBox = QCheckBox(self.frame_2)
        # self.checkBox.setObjectName(u"checkBox")
        # self.checkBox.setAutoFillBackground(False)
        # self.checkBox.setStyleSheet(u"")
        #
        # self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)

        self.skydel_output_label = QLabel(self.frame_2)
        self.skydel_output_label.setObjectName(u"skydel_output_label")
        self.skydel_output_label.setAutoFillBackground(False)
        self.skydel_output_label.setStyleSheet(u"")
        self.gridLayout_2.addWidget(self.skydel_output_label, 0, 0, 1, 1)

        self.comboBox_play_sdel = QComboBox(self.frame_2)
        self.comboBox_play_sdel.addItem("")
        self.comboBox_play_sdel.addItem("")
        self.comboBox_play_sdel.addItem("")
        self.comboBox_play_sdel.addItem("")
        self.comboBox_play_sdel.setObjectName(u"comboBox")
        self.comboBox_play_sdel.setFont(font8)
        self.comboBox_play_sdel.setAutoFillBackground(False)
        self.comboBox_play_sdel.setStyleSheet(u"QComboBox{\n"
                                    "	background-color: rgb(27, 29, 35);\n"
                                    "	border-radius: 5px;\n"
                                    "	border: 2px solid rgb(27, 29, 35);\n"
                                    "	padding: 5px;\n"
                                    "	padding-left: 10px;\n"
                                    "}\n"
                                    "QComboBox:hover{\n"
                                    "	border: 2px solid rgb(64, 71, 88);\n"
                                    "}\n"
                                    "QComboBox QAbstractItemView {\n"
                                    "	color: rgb(85, 170, 255);	\n"
                                    "	background-color: rgb(27, 29, 35);\n"
                                    "	padding: 10px;\n"
                                    "	selection-background-color: rgb(39, 44, 54);\n"
                                    "}")
        self.comboBox_play_sdel.setIconSize(QSize(16, 16))
        self.comboBox_play_sdel.setFrame(True)
        self.gridLayout_2.addWidget(self.comboBox_play_sdel, 1, 0, 1, 1)

        self.skydel_rad_gain_labl_2 = QLabel(self.frame_2)
        self.skydel_rad_gain_labl_2.setObjectName(u"skydel_output_label")
        self.skydel_rad_gain_labl_2.setAutoFillBackground(False)
        self.skydel_rad_gain_labl_2.setStyleSheet(u"")
        self.gridLayout_2.addWidget(self.skydel_rad_gain_labl_2, 2, 0, 1, 1)

        self.skydel_rad_edit_2 = QLineEdit(self.frame_2)
        self.skydel_rad_edit_2.setObjectName(u"lineEdit")
        self.skydel_rad_edit_2.setMinimumSize(QSize(0, 30))
        self.skydel_rad_edit_2.setStyleSheet(u"QLineEdit {\n"
                                           "	background-color: rgb(27, 29, 35);\n"
                                           "	border-radius: 5px;\n"
                                           "	border: 2px solid rgb(27, 29, 35);\n"
                                           "	padding-left: 10px;\n"
                                           "}\n"
                                           "QLineEdit:hover {\n"
                                           "	border: 2px solid rgb(64, 71, 88);\n"
                                           "}\n"
                                           "QLineEdit:focus {\n"
                                           "	border: 2px solid rgb(91, 101, 124);\n"
                                           "}")

        self.gridLayout_2.addWidget(self.skydel_rad_edit_2, 3, 0, 1, 1)

        self.pushButton_load_skydel = QPushButton(self.frame_2)
        self.pushButton_load_skydel.setObjectName(u"pushButton")
        self.pushButton_load_skydel.setMinimumSize(QSize(150, 30))
        font8 = QFont()
        font8.setFamily(u"Segoe UI")
        font8.setPointSize(9)
        self.pushButton_load_skydel.setFont(font8)
        self.pushButton_load_skydel.setStyleSheet(u"QPushButton {\n"
                                                  "	border: 2px solid rgb(52, 59, 72);\n"
                                                  "	border-radius: 5px;	\n"
                                                  "	background-color: rgb(52, 59, 72);\n"
                                                  "}\n"
                                                  "QPushButton:hover {\n"
                                                  "	background-color: rgb(57, 65, 80);\n"
                                                  "	border: 2px solid rgb(61, 70, 86);\n"
                                                  "}\n"
                                                  "QPushButton:pressed {	\n"
                                                  "	background-color: rgb(35, 40, 49);\n"
                                                  "	border: 2px solid rgb(43, 50, 61);\n"
                                                  "}")
        icon3 = QIcon()
        icon3.addFile(u":/16x16/icons/16x16/cil-folder-open.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_load_skydel.setIcon(icon3)

        self.gridLayout_2.addWidget(self.pushButton_load_skydel, 5, 1, 1, 1)


        # self.radioButton = QRadioButton(self.frame_2)
        # self.radioButton.setObjectName(u"radioButton")
        # self.radioButton.setStyleSheet(u"")
        #
        # self.gridLayout_2.addWidget(self.radioButton, 0, 1, 1, 1)

        # self.verticalSlider = QSlider(self.frame_2)
        # self.verticalSlider.setObjectName(u"verticalSlider")
        # self.verticalSlider.setStyleSheet(u"")
        # self.verticalSlider.setOrientation(Qt.Vertical)
        # self.gridLayout_2.addWidget(self.verticalSlider, 0, 2, 3, 1)

        # self.verticalScrollBar = QScrollBar(self.frame_2)
        # self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        # self.verticalScrollBar.setStyleSheet(u" QScrollBar:vertical {\n"
        #                                      "	border: none;\n"
        #                                      "    background: rgb(52, 59, 72);\n"
        #                                      "    width: 14px;\n"
        #                                      "    margin: 21px 0 21px 0;\n"
        #                                      "	border-radius: 0px;\n"
        #                                      " }")
        # self.verticalScrollBar.setOrientation(Qt.Vertical)
        #
        # self.gridLayout_2.addWidget(self.verticalScrollBar, 0, 4, 3, 1)

        self.scrollArea = QScrollArea(self.frame_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"QScrollArea {\n"
                                      "	border: none;\n"
                                      "	border-radius: 0px;\n"
                                      "}\n"
                                      "QScrollBar:horizontal {\n"
                                      "    border: none;\n"
                                      "    background: rgb(52, 59, 72);\n"
                                      "    height: 14px;\n"
                                      "    margin: 0px 21px 0 21px;\n"
                                      "	border-radius: 0px;\n"
                                      "}\n"
                                      " QScrollBar:vertical {\n"
                                      "	border: none;\n"
                                      "    background: rgb(52, 59, 72);\n"
                                      "    width: 14px;\n"
                                      "    margin: 21px 0 21px 0;\n"
                                      "	border-radius: 0px;\n"
                                      " }\n"
                                      "")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 274, 218))
        self.horizontalLayout_11 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.plainTextEdit = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMinimumSize(QSize(200, 200))
        self.plainTextEdit.setStyleSheet(u"QPlainTextEdit {\n"
                                         "	background-color: rgb(27, 29, 35);\n"
                                         "	border-radius: 5px;\n"
                                         "	padding: 10px;\n"
                                         "}\n"
                                         "QPlainTextEdit:hover {\n"
                                         "	border: 2px solid rgb(64, 71, 88);\n"
                                         "}\n"
                                         "QPlainTextEdit:focus {\n"
                                         "	border: 2px solid rgb(91, 101, 124);\n"
                                         "}")
        #self.plainTextEdit.insertPlainText(" Test Test")

        self.horizontalLayout_11.addWidget(self.plainTextEdit)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 5, 3, 1)

        # self.horizontalScrollBar = QScrollBar(self.frame_2)
        # self.horizontalScrollBar.setObjectName(u"horizontalScrollBar")
        # sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # sizePolicy5.setHorizontalStretch(0)
        # sizePolicy5.setVerticalStretch(0)
        # sizePolicy5.setHeightForWidth(self.horizontalScrollBar.sizePolicy().hasHeightForWidth())
        # self.horizontalScrollBar.setSizePolicy(sizePolicy5)
        # self.horizontalScrollBar.setStyleSheet(u"QScrollBar:horizontal {\n"
        #                                        "    border: none;\n"
        #                                        "    background: rgb(52, 59, 72);\n"
        #                                        "    height: 14px;\n"
        #                                        "    margin: 0px 21px 0 21px;\n"
        #                                        "	border-radius: 0px;\n"
        #                                        "}\n"
        #                                        "")
        # self.horizontalScrollBar.setOrientation(Qt.Horizontal)
        #
        # self.gridLayout_2.addWidget(self.horizontalScrollBar, 1, 3, 1, 1)

        # self.commandLinkButton = QCommandLinkButton(self.frame_2)
        # self.commandLinkButton.setObjectName(u"commandLinkButton")
        # self.commandLinkButton.setStyleSheet(u"QCommandLinkButton {	\n"
        #                                      "	color: rgb(85, 170, 255);\n"
        #                                      "	border-radius: 5px;\n"
        #                                      "	padding: 5px;\n"
        #                                      "}\n"
        #                                      "QCommandLinkButton:hover {	\n"
        #                                      "	color: rgb(210, 210, 210);\n"
        #                                      "	background-color: rgb(44, 49, 60);\n"
        #                                      "}\n"
        #                                      "QCommandLinkButton:pressed {	\n"
        #                                      "	color: rgb(210, 210, 210);\n"
        #                                      "	background-color: rgb(52, 58, 71);\n"
        #                                      "}")
        # icon4 = QIcon()
        # icon4.addFile(u":/16x16/icons/16x16/cil-link.png", QSize(), QIcon.Normal, QIcon.Off)
        # self.commandLinkButton.setIcon(icon4)
        #
        # self.gridLayout_2.addWidget(self.commandLinkButton, 1, 6, 1, 1)

        # self.horizontalSlider = QSlider(self.frame_2)
        # self.horizontalSlider.setObjectName(u"horizontalSlider")
        # self.horizontalSlider.setStyleSheet(u"")
        # self.horizontalSlider.setOrientation(Qt.Horizontal)
        #
        # self.gridLayout_2.addWidget(self.horizontalSlider, 2, 0, 1, 2)

        self.verticalLayout_11.addLayout(self.gridLayout_2)

        self.verticalLayout_6.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.page_widgets)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 150))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        # self.tableWidget = QTableWidget(self.frame_3)
        # if (self.tableWidget.columnCount() < 4):
        #     self.tableWidget.setColumnCount(4)
        # __qtablewidgetitem = QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        # __qtablewidgetitem1 = QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        # __qtablewidgetitem2 = QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        # __qtablewidgetitem3 = QTableWidgetItem()
        # self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        # if (self.tableWidget.rowCount() < 16):
        #     self.tableWidget.setRowCount(16)
        # __qtablewidgetitem4 = QTableWidgetItem()
        # __qtablewidgetitem4.setFont(font2);
        # self.tableWidget.setVerticalHeaderItem(0, __qtablewidgetitem4)
        # __qtablewidgetitem5 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(1, __qtablewidgetitem5)
        # __qtablewidgetitem6 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(2, __qtablewidgetitem6)
        # __qtablewidgetitem7 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(3, __qtablewidgetitem7)
        # __qtablewidgetitem8 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(4, __qtablewidgetitem8)
        # __qtablewidgetitem9 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(5, __qtablewidgetitem9)
        # __qtablewidgetitem10 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(6, __qtablewidgetitem10)
        # __qtablewidgetitem11 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(7, __qtablewidgetitem11)
        # __qtablewidgetitem12 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(8, __qtablewidgetitem12)
        # __qtablewidgetitem13 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(9, __qtablewidgetitem13)
        # __qtablewidgetitem14 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(10, __qtablewidgetitem14)
        # __qtablewidgetitem15 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(11, __qtablewidgetitem15)
        # __qtablewidgetitem16 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(12, __qtablewidgetitem16)
        # __qtablewidgetitem17 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(13, __qtablewidgetitem17)
        # __qtablewidgetitem18 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(14, __qtablewidgetitem18)
        # __qtablewidgetitem19 = QTableWidgetItem()
        # self.tableWidget.setVerticalHeaderItem(15, __qtablewidgetitem19)
        # __qtablewidgetitem20 = QTableWidgetItem()
        # self.tableWidget.setItem(0, 0, __qtablewidgetitem20)
        # __qtablewidgetitem21 = QTableWidgetItem()
        # self.tableWidget.setItem(0, 1, __qtablewidgetitem21)
        # __qtablewidgetitem22 = QTableWidgetItem()
        # self.tableWidget.setItem(0, 2, __qtablewidgetitem22)
        # __qtablewidgetitem23 = QTableWidgetItem()
        # self.tableWidget.setItem(0, 3, __qtablewidgetitem23)
        # self.tableWidget.setObjectName(u"tableWidget")
        # sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        # self.tableWidget.setSizePolicy(sizePolicy)
        # palette1 = QPalette()
        # palette1.setBrush(QPalette.Active, QPalette.WindowText, brush6)
        # brush15 = QBrush(QColor(39, 44, 54, 255))
        # brush15.setStyle(Qt.SolidPattern)
        # palette1.setBrush(QPalette.Active, QPalette.Button, brush15)
        # palette1.setBrush(QPalette.Active, QPalette.Text, brush6)
        # palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush6)
        # palette1.setBrush(QPalette.Active, QPalette.Base, brush15)
        # palette1.setBrush(QPalette.Active, QPalette.Window, brush15)
        # brush16 = QBrush(QColor(210, 210, 210, 128))
        # brush16.setStyle(Qt.NoBrush)
        # # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        # palette1.setBrush(QPalette.Active, QPalette.PlaceholderText, brush16)
        # # endif
        # palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush6)
        # palette1.setBrush(QPalette.Inactive, QPalette.Button, brush15)
        # palette1.setBrush(QPalette.Inactive, QPalette.Text, brush6)
        # palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush6)
        # palette1.setBrush(QPalette.Inactive, QPalette.Base, brush15)
        # palette1.setBrush(QPalette.Inactive, QPalette.Window, brush15)
        # brush17 = QBrush(QColor(210, 210, 210, 128))
        # brush17.setStyle(Qt.NoBrush)
        # # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        # palette1.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush17)
        # # endif
        # palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush6)
        # palette1.setBrush(QPalette.Disabled, QPalette.Button, brush15)
        # palette1.setBrush(QPalette.Disabled, QPalette.Text, brush6)
        # palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush6)
        # palette1.setBrush(QPalette.Disabled, QPalette.Base, brush15)
        # palette1.setBrush(QPalette.Disabled, QPalette.Window, brush15)
        # brush18 = QBrush(QColor(210, 210, 210, 128))
        # brush18.setStyle(Qt.NoBrush)
        # # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        # palette1.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush18)
        # # endif
        # self.tableWidget.setPalette(palette1)
        # self.tableWidget.setStyleSheet(u"QTableWidget {	\n"
        #                                "	background-color: rgb(39, 44, 54);\n"
        #                                "	padding: 10px;\n"
        #                                "	border-radius: 5px;\n"
        #                                "	gridline-color: rgb(44, 49, 60);\n"
        #                                "	border-bottom: 1px solid rgb(44, 49, 60);\n"
        #                                "}\n"
        #                                "QTableWidget::item{\n"
        #                                "	border-color: rgb(44, 49, 60);\n"
        #                                "	padding-left: 5px;\n"
        #                                "	padding-right: 5px;\n"
        #                                "	gridline-color: rgb(44, 49, 60);\n"
        #                                "}\n"
        #                                "QTableWidget::item:selected{\n"
        #                                "	background-color: rgb(85, 170, 255);\n"
        #                                "}\n"
        #                                "QScrollBar:horizontal {\n"
        #                                "    border: none;\n"
        #                                "    background: rgb(52, 59, 72);\n"
        #                                "    height: 14px;\n"
        #                                "    margin: 0px 21px 0 21px;\n"
        #                                "	border-radius: 0px;\n"
        #                                "}\n"
        #                                " QScrollBar:vertical {\n"
        #                                "	border: none;\n"
        #                                "    background: rgb(52, 59, 72);\n"
        #                                "    width: 14px;\n"
        #                                "    margin: 21px 0 21px 0;\n"
        #                                "	border-radius: 0px;\n"
        #                                " }\n"
        #                                "QHeaderView::section{\n"
        #                                "	Background-color: rgb(39, 44, 54);\n"
        #                                "	max-width: 30px;\n"
        #                                "	border: 1px solid rgb(44, 49, 60);\n"
        #                                "	border-style: none;\n"
        #                                "    border-bottom: 1px solid rgb(44, 49, 60);\n"
        #                                "    border-right: 1px solid rgb(44, 49, 60);\n"
        #                                "}\n"
        #                                ""
        #                                "QTableWidget::horizontalHeader {	\n"
        #                                "	background-color: rgb(81, 255, 0);\n"
        #                                "}\n"
        #                                "QHeaderView::section:horizontal\n"
        #                                "{\n"
        #                                "    border: 1px solid rgb(32, 34, 42);\n"
        #                                "	background-color: rgb(27, 29, 35);\n"
        #                                "	padding: 3px;\n"
        #                                "	border-top-left-radius: 7px;\n"
        #                                "    border-top-right-radius: 7px;\n"
        #                                "}\n"
        #                                "QHeaderView::section:vertical\n"
        #                                "{\n"
        #                                "    border: 1px solid rgb(44, 49, 60);\n"
        #                                "}\n"
        #                                "")
        # self.tableWidget.setFrameShape(QFrame.NoFrame)
        # self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setAlternatingRowColors(False)
        # self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.tableWidget.setShowGrid(True)
        # self.tableWidget.setGridStyle(Qt.SolidLine)
        # self.tableWidget.setSortingEnabled(False)
        # self.tableWidget.horizontalHeader().setVisible(True)
        # self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        # self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # self.tableWidget.verticalHeader().setVisible(False)
        # self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        # self.tableWidget.verticalHeader().setHighlightSections(False)
        # self.tableWidget.verticalHeader().setStretchLastSection(True)

        #self.horizontalLayout_12.addWidget(self.tableWidget)

        self.verticalLayout_6.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.page_widgets)

        self.verticalLayout_9.addWidget(self.stackedWidget)

        self.verticalLayout_4.addWidget(self.frame_content)

        self.frame_grip = QFrame(self.frame_content_right)
        self.frame_grip.setObjectName(u"frame_grip")
        self.frame_grip.setMinimumSize(QSize(0, 25))
        self.frame_grip.setMaximumSize(QSize(16777215, 25))
        self.frame_grip.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.frame_grip.setFrameShape(QFrame.NoFrame)
        self.frame_grip.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_grip)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 2, 0)
        self.frame_label_bottom = QFrame(self.frame_grip)
        self.frame_label_bottom.setObjectName(u"frame_label_bottom")
        self.frame_label_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_label_bottom.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_label_bottom)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(10, 0, 10, 0)
        self.label_credits = QLabel(self.frame_label_bottom)
        self.label_credits.setObjectName(u"label_credits")
        self.label_credits.setFont(font2)
        self.label_credits.setStyleSheet(u"color: rgb(98, 103, 111);")

        self.horizontalLayout_7.addWidget(self.label_credits)

        self.label_version = QLabel(self.frame_label_bottom)
        self.label_version.setObjectName(u"label_version")
        self.label_version.setMaximumSize(QSize(100, 16777215))
        self.label_version.setFont(font2)
        self.label_version.setStyleSheet(u"color: rgb(98, 103, 111);")
        self.label_version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_version)

        self.horizontalLayout_6.addWidget(self.frame_label_bottom)

        self.frame_size_grip = QFrame(self.frame_grip)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMaximumSize(QSize(20, 20))
        self.frame_size_grip.setStyleSheet(u"QSizeGrip {\n"
                                           "	background-image: url(:/16x16/icons/16x16/cil-size-grip.png);\n"
                                           "	background-position: center;\n"
                                           "	background-repeat: no-reperat;\n"
                                           "}")
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_6.addWidget(self.frame_size_grip)

        self.verticalLayout_4.addWidget(self.frame_grip)

        self.horizontalLayout_2.addWidget(self.frame_content_right)

        self.verticalLayout.addWidget(self.frame_center)

        self.horizontalLayout.addWidget(self.frame_main)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.btn_minimize, self.btn_maximize_restore)
        QWidget.setTabOrder(self.btn_maximize_restore, self.btn_close)
        QWidget.setTabOrder(self.btn_close, self.btn_toggle_menu)
        QWidget.setTabOrder(self.btn_toggle_menu, self.skydel_output_label)
        # QWidget.setTabOrder(self.checkBox, self.comboBox)
        # QWidget.setTabOrder(self.comboBox, self.radioButton)
        # QWidget.setTabOrder(self.radioButton, self.horizontalSlider)
        # QWidget.setTabOrder(self.horizontalSlider, self.verticalSlider)
        # QWidget.setTabOrder(self.verticalSlider, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.plainTextEdit)
        #QWidget.setTabOrder(self.plainTextEdit, self.tableWidget)
        # QWidget.setTabOrder(self.tableWidget, self.commandLinkButton)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.btn_toggle_menu.setText("")
        self.label_title_bar_top.setText(QCoreApplication.translate("MainWindow", u"Main Window - Base", None))
        # if QT_CONFIG(tooltip)
        self.btn_minimize.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_minimize.setText("")
        # if QT_CONFIG(tooltip)
        self.btn_maximize_restore.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_maximize_restore.setText("")
        # if QT_CONFIG(tooltip)
        self.btn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
        # endif // QT_CONFIG(tooltip)
        self.btn_close.setText("")
        # self.label_top_info_1.setText(
        #     QCoreApplication.translate("MainWindow", u"C:\\Program Files\\Blender Foundation\\Blender 2.82", None))
        self.label_top_info_2.setText(QCoreApplication.translate("MainWindow", u"| HOME", None))
        self.label_user_icon.setText(QCoreApplication.translate("MainWindow", u"Skydel", None))

        # self.gsg56_icon.setText(QCoreApplication.translate())
        self.GSG56_scenarios_label.setText(QCoreApplication.translate("MainWindow", "GSG5/6 Scenario", None))
        self.pushButton_gsg56_select_folder.setText(QCoreApplication.translate("MainWindow", "Open folder", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", "ex: C:/GSG_5_6_scenario_path/", None))

        self.skydel_conversion_label.setText(QCoreApplication.translate("MainWindow", "Conversion to Skydel", None))
        self.script_convert_status.setText(QCoreApplication.translate("MainWindow", "Script status ", None))
        self.pushButton_convert_skydel.setText(QCoreApplication.translate("MainWindow", "Convert", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", "ex: C:/skydel_script_path/", None))

        # self.Skydel_label_conversion_page.setText(QCoreApplication.translate("MainWindow", "Skydel Logo", None))
        # self.generate_script_conversion_page.setText(QCoreApplication.translate("MainWindow", "PushButton", None))
        # self.label_6.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        # self.label.setText(QCoreApplication.translate("MainWindow", u"Empyt Page - By: Wanderson M. Pimenta", None))
        # self.label_7.setText(QCoreApplication.translate("MainWindow", u"Page Index 0", None))
        #self.labelBoxBlenderInstalation.setText(QCoreApplication.translate("MainWindow", u"Playback in Skydel", None))
        #self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"", None))
        self.pushButton_load_skydel.setText(QCoreApplication.translate("MainWindow", u"Playback", None))
        # self.labelVersion_3.setText(
        #     QCoreApplication.translate("MainWindow", u"Ex: C:Program FilesBlender FoundationBlender 2.82 blender.exe",
        #                                None))
        self.skydel_output_label.setText(QCoreApplication.translate("MainWindow", u"Skydel Output Type", None))
        self.skydel_output_label_0.setText(QCoreApplication.translate("MainWindow", u"Skydel Output Type", None))
        self.skydel_rad_gain_labl.setText(QCoreApplication.translate("MainWindow", u"Gain", None))
        self.skydel_rad_gain_labl_2.setText(QCoreApplication.translate("MainWindow", u"Gain", None))

        #self.skydel_rad_GN_labl.setText(QCoreApplication.translate("MainWindow", u"Gaussian Noise", None))
        self.skydel_GN_checkBox.setText(QCoreApplication.translate("MainWindow", "Gaussian Noise", None))
        self.skydel_rad_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"", None))
        self.skydel_rad_edit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"", None))


        # self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        # self.radioButton.setText(QCoreApplication.translate("MainWindow", u"RadioButton", None))
        self.comboBox_play_sdel.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.comboBox_play_sdel.setItemText(1, QCoreApplication.translate("MainWindow", u"NoneRT", None))
        self.comboBox_play_sdel.setItemText(2, QCoreApplication.translate("MainWindow", u"DTA-2115B", None))
        self.comboBox_play_sdel.setItemText(3, QCoreApplication.translate("MainWindow", u"DTA-2116", None))

        self.comboBox_skydel_conv.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.comboBox_skydel_conv.setItemText(1, QCoreApplication.translate("MainWindow", u"NoneRT", None))
        self.comboBox_skydel_conv.setItemText(2, QCoreApplication.translate("MainWindow", u"DTA-2115B", None))
        self.comboBox_skydel_conv.setItemText(3, QCoreApplication.translate("MainWindow", u"DTA-2116", None))

        # self.commandLinkButton.setText(QCoreApplication.translate("MainWindow", u"CommandLinkButton", None))
        # self.commandLinkButton.setDescription(QCoreApplication.translate("MainWindow", u"Open External Link", None))
        # ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        # ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"0", None));
        # ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        # ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"1", None));
        # ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        # ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"2", None));
        # ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        # ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"3", None));
        # ___qtablewidgetitem4 = self.tableWidget.verticalHeaderItem(0)
        # ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem5 = self.tableWidget.verticalHeaderItem(1)
        # ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem6 = self.tableWidget.verticalHeaderItem(2)
        # ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem7 = self.tableWidget.verticalHeaderItem(3)
        # ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem8 = self.tableWidget.verticalHeaderItem(4)
        # ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem9 = self.tableWidget.verticalHeaderItem(5)
        # ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem10 = self.tableWidget.verticalHeaderItem(6)
        # ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem11 = self.tableWidget.verticalHeaderItem(7)
        # ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem12 = self.tableWidget.verticalHeaderItem(8)
        # ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem13 = self.tableWidget.verticalHeaderItem(9)
        # ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem14 = self.tableWidget.verticalHeaderItem(10)
        # ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem15 = self.tableWidget.verticalHeaderItem(11)
        # ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem16 = self.tableWidget.verticalHeaderItem(12)
        # ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem17 = self.tableWidget.verticalHeaderItem(13)
        # ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem18 = self.tableWidget.verticalHeaderItem(14)
        # ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        # ___qtablewidgetitem19 = self.tableWidget.verticalHeaderItem(15)
        # ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"New Row", None));
        #
        # __sortingEnabled = self.tableWidget.isSortingEnabled()
        # self.tableWidget.setSortingEnabled(False)
        # ___qtablewidgetitem20 = self.tableWidget.item(0, 0)
        # ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        # ___qtablewidgetitem21 = self.tableWidget.item(0, 1)
        # ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Text", None))
        #
        # self.tableWidget.setSortingEnabled(__sortingEnabled)

        ___qtablewidgetitem_home = self.tableWidget_home.horizontalHeaderItem(0)
        ___qtablewidgetitem_home.setText(QCoreApplication.translate("MainWindow", u"GSG5/6 file", None))
        ___qtablewidgetitem_home1 = self.tableWidget_home.horizontalHeaderItem(1)
        ___qtablewidgetitem_home1.setText(QCoreApplication.translate("MainWindow", u"Path", None))

        ___qtablewidgetitem_home4 = self.tableWidget_home.verticalHeaderItem(0)
        ___qtablewidgetitem_home4.setText(QCoreApplication.translate("MainWindow", u"New Row", None))
        ___qtablewidgetitem_home5 = self.tableWidget_home.verticalHeaderItem(1)
        ___qtablewidgetitem_home5.setText(QCoreApplication.translate("MainWindow", u"New Row", None))

        __sortingEnabled = self.tableWidget_home.isSortingEnabled()
        self.tableWidget_home.setSortingEnabled(False)
        # ___qtablewidgetitem_home20 = self.tableWidget_home.item(0, 0)
        # ___qtablewidgetitem_home20.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        # ___qtablewidgetitem_home21 = self.tableWidget_home.item(0, 1)
        # ___qtablewidgetitem_home21.setText(QCoreApplication.translate("MainWindow", u"Text", None))
        # ___qtablewidgetitem_home22 = self.tableWidget_home.item(0, 2)
        # ___qtablewidgetitem_home22.setText(QCoreApplication.translate("MainWindow", u"Cell", None))
        # ___qtablewidgetitem_home23 = self.tableWidget_home.item(0, 3)
        # ___qtablewidgetitem_home23.setText(QCoreApplication.translate("MainWindow", u"Line", None))
        self.tableWidget_home.setSortingEnabled(__sortingEnabled)

        self.label_credits.setText(
            QCoreApplication.translate("MainWindow", u"GSG5/6 to Skydel converter", None))
        self.label_version.setText(QCoreApplication.translate("MainWindow", u"v24.6.1", None))
    # retranslateUi

