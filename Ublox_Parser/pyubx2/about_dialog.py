# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'about_dialog.ui'
# Created by: PyQt5 UI code generator 5.13.0
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDialog
from PyQt5.QtCore import Qt


class Ui_AboutDialog(QDialog):

    def __init__(self):

        super(Ui_AboutDialog, self).__init__()
        self.setWindowIcon(QtGui.QIcon('Skydel-NewLogo-Square-Orange.png'))

        self.setWindowTitle('About')
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        gridLayout = QtWidgets.QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 40)
        gridLayout.setSpacing(0)

        topFrame = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(topFrame.sizePolicy().hasHeightForWidth())
        topFrame.setSizePolicy(sizePolicy)
        topFrame.setMinimumSize(QtCore.QSize(0, 40))
        topFrame.setMaximumSize(QtCore.QSize(16777215, 40))
        topFrame.setStyleSheet("color: rgb(0, 165, 165);")
        topFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        topFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        gridLayout_2 = QtWidgets.QGridLayout(topFrame)
        gridLayout_2.setContentsMargins(-1, 5, -1, -1)
        gridLayout_2.setVerticalSpacing(20)
        spacerItem = QtWidgets.QSpacerItem(102, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)

        title = QtWidgets.QLabel(topFrame)
        title.setStyleSheet("color: rgb(0, 0, 0);font: 16px;")
        title.setText("3D Antenna pattern")

        gridLayout_2.addWidget(title, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(102, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)

        self.tbClose = QtWidgets.QToolButton(topFrame)
        self.tbClose.setMinimumSize(QtCore.QSize(40, 40))
        # self.tbClose.setStyleSheet("QToolButton {\n"
        #                            "    border: 0px\n"
        #                            "}\n"
        #                            "QToolButton:pressed {\n"
        #                            "    border: 1px solid #374b5a;\n"
        #                            "}")
        self.tbClose.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("orolia_rgb.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbClose.setIcon(icon)
        self.tbClose.setIconSize(QtCore.QSize(25, 25))

        gridLayout_2.addWidget(self.tbClose, 0, 4, 1, 1)

        gridLayout.addWidget(topFrame, 0, 0, 1, 3)

        verticalLayout = QtWidgets.QVBoxLayout()
        verticalLayout.setContentsMargins(26, 20, 26, 25)
        self.lblTitle = QtWidgets.QLabel()
        self.lblTitle.setText("3D ANTENNA PATTERN CONVERTOR")
        self.lblTitle.setStyleSheet('color: black')
        verticalLayout.addWidget(self.lblTitle)
        self.lblBuild = QtWidgets.QLabel()
        self.lblBuild.setText("20.9.5  (Beta)")
        self.lblBuild1 = QtWidgets.QLabel()
        self.lblBuild1.setText("Release Date  2021-03-08")
        self.lblBuild.setStyleSheet('color: black')
        self.lblBuild1.setStyleSheet('color: black')

        verticalLayout.addWidget(self.lblBuild)
        verticalLayout.addWidget(self.lblBuild1)

        self.label_2 = QtWidgets.QLabel()
        self.label_2.setText("")
        verticalLayout.addWidget(self.label_2)
        self.lblCopyright = QtWidgets.QLabel()
        self.lblCopyright.setText("Copyright")
        self.lblCopyright.setStyleSheet('color: black')
        verticalLayout.addWidget(self.lblCopyright)
        self.lblCopyrightText = QtWidgets.QLabel()
        self.lblCopyrightText1 = QtWidgets.QLabel()
        self.lblCopyrightText2 = QtWidgets.QLabel()

        font = QtGui.QFont()
        font.setPointSize(9)
        self.lblCopyrightText.setFont(font)
        self.lblCopyrightText.setWordWrap(True)
        self.lblCopyrightText.setText("2021 Orolia Canada Inc. All Rights Reserved.")
        self.lblCopyrightText1.setFont(font)
        self.lblCopyrightText1.setWordWrap(True)
        self.lblCopyrightText1.setText("All Rights Reserved.")
        self.lblCopyrightText2.setFont(font)
        self.lblCopyrightText2.setWordWrap(True)
        self.lblCopyrightText2.setText("skydel-support@orolia.com")
        self.lblCopyrightText.setStyleSheet('color: black')
        verticalLayout.addWidget(self.lblCopyrightText)
        verticalLayout.addWidget(self.lblCopyrightText1)
        verticalLayout.addWidget(self.lblCopyrightText2)

        gridLayout.addLayout(verticalLayout, 1, 1, 2, 2)

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setContentsMargins(25, 10, 40, 1)
        horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem2)
        self.label = QtWidgets.QLabel()
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignJustify | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label.setText("The information, software and documentation are protected by copyright laws\n"
                           "as well as international copyright treaties as well as other laws and conven-\n"
                           "tions related to intellectual property. The User shall observe such laws and in\n"
                           "particular shall not modify, conceal or remove any alphanumeric code, marks\n"
                           "or copyright notices neither from the information nor from the software or\n"
                           "documentation, or any copies thereof.")
        self.label.setStyleSheet('color: black')
        horizontalLayout.addWidget(self.label)

        gridLayout.addLayout(horizontalLayout, 3, 1, 3, 2)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        # self.pbClose = QtWidgets.QPushButton()
        # self.pbClose.setMinimumSize(QtCore.QSize(100, 35))
        # self.pbClose.setText("Close")
        # self.horizontalLayout_3.addWidget(self.pbClose)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)

        gridLayout.addLayout(self.horizontalLayout_3, 7, 1, 1, 1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Ui_AboutDialog()
    w.show()
    app.exec_()
