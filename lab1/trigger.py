# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trigger.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_trigger_dialog(object):
    def setupUi(self, trigger_dialog):
        trigger_dialog.setObjectName("trigger_dialog")
        trigger_dialog.resize(400, 300)

        self.retranslateUi(trigger_dialog)
        QtCore.QMetaObject.connectSlotsByName(trigger_dialog)

    def retranslateUi(self, trigger_dialog):
        _translate = QtCore.QCoreApplication.translate
        trigger_dialog.setWindowTitle(_translate("trigger_dialog", "Dialog"))
