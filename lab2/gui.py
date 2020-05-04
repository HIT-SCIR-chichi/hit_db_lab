# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(660, 464)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../lab1/src/system.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.query_table = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.query_table.sizePolicy().hasHeightForWidth())
        self.query_table.setSizePolicy(sizePolicy)
        self.query_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.query_table.setColumnCount(2)
        self.query_table.setObjectName("query_table")
        self.query_table.setRowCount(0)
        self.query_table.horizontalHeader().setVisible(False)
        self.query_table.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.query_table)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.optimize_on = QtWidgets.QRadioButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optimize_on.sizePolicy().hasHeightForWidth())
        self.optimize_on.setSizePolicy(sizePolicy)
        self.optimize_on.setObjectName("optimize_on")
        self.horizontalLayout.addWidget(self.optimize_on)
        self.query_box = QtWidgets.QComboBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.query_box.sizePolicy().hasHeightForWidth())
        self.query_box.setSizePolicy(sizePolicy)
        self.query_box.setObjectName("query_box")
        self.horizontalLayout.addWidget(self.query_box)
        self.parse_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parse_button.sizePolicy().hasHeightForWidth())
        self.parse_button.setSizePolicy(sizePolicy)
        self.parse_button.setObjectName("parse_button")
        self.horizontalLayout.addWidget(self.parse_button)
        self.verticalLayout.addWidget(self.frame)
        self.parse_tree = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.parse_tree.sizePolicy().hasHeightForWidth())
        self.parse_tree.setSizePolicy(sizePolicy)
        self.parse_tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.parse_tree.setObjectName("parse_tree")
        self.verticalLayout.addWidget(self.parse_tree)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.parse_button.clicked.connect(MainWindow.query)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "语法树"))
        self.optimize_on.setText(_translate("MainWindow", "优化开启"))
        self.parse_button.setText(_translate("MainWindow", "查询"))
