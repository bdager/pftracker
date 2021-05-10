# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_error.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_error(object):
    def setupUi(self, Dialog_error):
        Dialog_error.setObjectName("Dialog_error")
        Dialog_error.setWindowModality(QtCore.Qt.WindowModal)
        Dialog_error.resize(863, 466)
        Dialog_error.setFocusPolicy(QtCore.Qt.NoFocus)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_error)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_chart = QtWidgets.QVBoxLayout()
        self.verticalLayout_chart.setObjectName("verticalLayout_chart")
        self.widget = QtWidgets.QWidget(Dialog_error)
        self.widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.widget.setObjectName("widget")
        self.verticalLayout_chart.addWidget(self.widget)
        self.verticalLayout.addLayout(self.verticalLayout_chart)

        self.retranslateUi(Dialog_error)
        QtCore.QMetaObject.connectSlotsByName(Dialog_error)

    def retranslateUi(self, Dialog_error):
        _translate = QtCore.QCoreApplication.translate
        Dialog_error.setWindowTitle(_translate("Dialog_error", "Precision and Recall"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_error = QtWidgets.QDialog()
    ui = Ui_Dialog_error()
    ui.setupUi(Dialog_error)
    Dialog_error.show()
    sys.exit(app.exec_())

