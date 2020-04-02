# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transaction.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(313, 162)
        self.horizontalLayout = QtWidgets.QHBoxLayout(dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.sender_nums = QtWidgets.QComboBox(self.frame)
        self.sender_nums.setObjectName("sender_nums")
        self.horizontalLayout_2.addWidget(self.sender_nums)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.receivers_nums = QtWidgets.QComboBox(self.frame)
        self.receivers_nums.setObjectName("receivers_nums")
        self.horizontalLayout_3.addWidget(self.receivers_nums)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.add_exception = QtWidgets.QRadioButton(self.frame)
        self.add_exception.setObjectName("add_exception")
        self.verticalLayout.addWidget(self.add_exception)
        self.begin_transfer = QtWidgets.QPushButton(self.frame)
        self.begin_transfer.setObjectName("begin_transfer")
        self.verticalLayout.addWidget(self.begin_transfer)
        self.horizontalLayout.addWidget(self.frame)
        self.stu_table = QtWidgets.QTableView(dialog)
        self.stu_table.setObjectName("stu_table")
        self.horizontalLayout.addWidget(self.stu_table)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "事务管理"))
        self.label.setText(_translate("dialog", "转账学号："))
        self.label_2.setText(_translate("dialog", "收账学号："))
        self.add_exception.setText(_translate("dialog", "模拟异常：关"))
        self.begin_transfer.setText(_translate("dialog", "开始转帐"))
