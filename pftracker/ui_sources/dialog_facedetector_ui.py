# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_facedetector.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_detector(object):
    def setupUi(self, Dialog_detector):
        Dialog_detector.setObjectName("Dialog_detector")
        Dialog_detector.resize(363, 315)
        Dialog_detector.setStyleSheet("")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog_detector)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Dialog_detector)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_viola = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_viola.setChecked(True)
        self.radioButton_viola.setObjectName("radioButton_viola")
        self.verticalLayout.addWidget(self.radioButton_viola)
        self.radioButton_SSD = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_SSD.setObjectName("radioButton_SSD")
        self.verticalLayout.addWidget(self.radioButton_SSD)
        self.radioButton_HOG = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_HOG.setObjectName("radioButton_HOG")
        self.verticalLayout.addWidget(self.radioButton_HOG)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.checkBox_save = QtWidgets.QCheckBox(Dialog_detector)
        self.checkBox_save.setObjectName("checkBox_save")
        self.verticalLayout_3.addWidget(self.checkBox_save)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.PB_acept = QtWidgets.QPushButton(Dialog_detector)
        self.PB_acept.setObjectName("PB_acept")
        self.horizontalLayout.addWidget(self.PB_acept)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_detector)
        QtCore.QMetaObject.connectSlotsByName(Dialog_detector)

    def retranslateUi(self, Dialog_detector):
        _translate = QtCore.QCoreApplication.translate
        Dialog_detector.setWindowTitle(_translate("Dialog_detector", "Face Detector"))
        self.groupBox.setTitle(_translate("Dialog_detector", "Select face detector to apply:"))
        self.radioButton_viola.setText(_translate("Dialog_detector", "Viola and Jones (V&J)"))
        self.radioButton_SSD.setText(_translate("Dialog_detector", "Single Shot Detector (SSD)"))
        self.radioButton_HOG.setText(_translate("Dialog_detector", "Histogram of Oriented Gradient (HOG)"))
        self.checkBox_save.setText(_translate("Dialog_detector", "Save output video"))
        self.PB_acept.setText(_translate("Dialog_detector", "Acept"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_detector = QtWidgets.QDialog()
    ui = Ui_Dialog_detector()
    ui.setupUi(Dialog_detector)
    Dialog_detector.show()
    sys.exit(app.exec_())

