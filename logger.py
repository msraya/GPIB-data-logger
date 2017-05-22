# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\logger.ui'
#
# Created: Wed Apr 12 18:51:41 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(620, 300)
        self.graphicsView = PlotWidget(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 591, 231))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.pb_start = QtGui.QPushButton(Dialog)
        self.pb_start.setGeometry(QtCore.QRect(10, 260, 91, 23))
        self.pb_start.setObjectName(_fromUtf8("pb_start"))
        self.pb_stop = QtGui.QPushButton(Dialog)
        self.pb_stop.setGeometry(QtCore.QRect(120, 260, 91, 23))
        self.pb_stop.setObjectName(_fromUtf8("pb_stop"))
        self.pb_exit = QtGui.QPushButton(Dialog)
        self.pb_exit.setGeometry(QtCore.QRect(510, 260, 91, 23))
        self.pb_exit.setObjectName(_fromUtf8("pb_exit"))
        self.pb_save = QtGui.QPushButton(Dialog)
        self.pb_save.setGeometry(QtCore.QRect(410, 260, 91, 23))
        self.pb_save.setObjectName(_fromUtf8("pb_save"))
        self.select_box = QtGui.QComboBox(Dialog)
        self.select_box.setGeometry(QtCore.QRect(270, 260, 69, 22))
        self.select_box.setObjectName(_fromUtf8("select_box"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pb_start.setText(_translate("Dialog", "Start", None))
        self.pb_stop.setText(_translate("Dialog", "Stop", None))
        self.pb_exit.setText(_translate("Dialog", "Exit", None))
        self.pb_save.setText(_translate("Dialog", "Save", None))

from pyqtgraph import PlotWidget
