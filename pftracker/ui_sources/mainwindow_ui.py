# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(469, 733)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/PFT.PNG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("#groupBox { \n"
"    font: 87 8pt \"Arial Black\";\n"
"     color: rgb(114, 114, 114);\n"
"}\n"
"\n"
"\n"
"#groupBox_2 {\n"
"    font: 87 8pt \"Arial Black\";\n"
"     color: rgb(114, 114, 114);\n"
" }\n"
"\n"
"#groupBox_3 {\n"
"    font: 87 8pt \"Arial Black\";\n"
"     color: rgb(114, 114, 114);\n"
" }\n"
"\n"
"#groupBox_4 { \n"
"    font: 87 8pt \"Arial Black\";\n"
"     color: rgb(114, 114, 114);\n"
"}\n"
"\n"
"#lineEdit_signal {\n"
"    background-color: rgb(227, 227, 227);\n"
"}\n"
"\n"
"#lineEdit_GT {\n"
"    background-color: rgb(227, 227, 227);\n"
"}\n"
"\n"
"#spinBox_NoParticulas{\n"
"    background-color: rgb(227, 227, 227);\n"
"}\n"
"\n"
"#spinBox_resample{\n"
"    background-color: rgb(227, 227, 227);\n"
"}\n"
"\n"
"#spinBox_salida{\n"
"    background-color: rgb(227, 227, 227);\n"
"}\n"
"\n"
"#spinBox_runs{\n"
"    background-color: rgb(227, 227, 227);\n"
"}\n"
"")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.comboBox_filtro = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_filtro.setObjectName("comboBox_filtro")
        self.comboBox_filtro.addItem("")
        self.comboBox_filtro.addItem("")
        self.comboBox_filtro.addItem("")
        self.comboBox_filtro.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_filtro)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.spinBox_NoParticulas = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_NoParticulas.setMinimum(1)
        self.spinBox_NoParticulas.setMaximum(5000)
        self.spinBox_NoParticulas.setProperty("value", 100)
        self.spinBox_NoParticulas.setObjectName("spinBox_NoParticulas")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox_NoParticulas)
        self.label_Tresample = QtWidgets.QLabel(self.groupBox_2)
        self.label_Tresample.setEnabled(False)
        self.label_Tresample.setObjectName("label_Tresample")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_Tresample)
        self.comboBox_Tresample = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_Tresample.setEnabled(False)
        self.comboBox_Tresample.setObjectName("comboBox_Tresample")
        self.comboBox_Tresample.addItem("")
        self.comboBox_Tresample.addItem("")
        self.comboBox_Tresample.addItem("")
        self.comboBox_Tresample.addItem("")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comboBox_Tresample)
        self.label_resample = QtWidgets.QLabel(self.groupBox_2)
        self.label_resample.setEnabled(False)
        self.label_resample.setObjectName("label_resample")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_resample)
        self.spinBox_resample = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_resample.setEnabled(False)
        self.spinBox_resample.setMinimum(1)
        self.spinBox_resample.setMaximum(100)
        self.spinBox_resample.setProperty("value", 50)
        self.spinBox_resample.setObjectName("spinBox_resample")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinBox_resample)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.comboBox_salida = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_salida.setObjectName("comboBox_salida")
        self.comboBox_salida.addItem("")
        self.comboBox_salida.addItem("")
        self.comboBox_salida.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.comboBox_salida)
        self.label_salida = QtWidgets.QLabel(self.groupBox_2)
        self.label_salida.setEnabled(False)
        self.label_salida.setObjectName("label_salida")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_salida)
        self.spinBox_salida = QtWidgets.QSpinBox(self.groupBox_2)
        self.spinBox_salida.setEnabled(False)
        self.spinBox_salida.setMinimum(1)
        self.spinBox_salida.setMaximum(100)
        self.spinBox_salida.setProperty("value", 25)
        self.spinBox_salida.setObjectName("spinBox_salida")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.spinBox_salida)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.comboBox_ee = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_ee.setObjectName("comboBox_ee")
        self.comboBox_ee.addItem("")
        self.comboBox_ee.addItem("")
        self.comboBox_ee.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_ee, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.comboBox_obsmodel = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_obsmodel.setObjectName("comboBox_obsmodel")
        self.comboBox_obsmodel.addItem("")
        self.comboBox_obsmodel.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_obsmodel, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.lineEdit_signal = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_signal.setEnabled(True)
        self.lineEdit_signal.setReadOnly(True)
        self.lineEdit_signal.setObjectName("lineEdit_signal")
        self.gridLayout.addWidget(self.lineEdit_signal, 0, 1, 1, 1)
        self.pushButton_signal = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_signal.setObjectName("pushButton_signal")
        self.gridLayout.addWidget(self.pushButton_signal, 0, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.lineEdit_GT = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_GT.setReadOnly(True)
        self.lineEdit_GT.setObjectName("lineEdit_GT")
        self.gridLayout.addWidget(self.lineEdit_GT, 1, 1, 1, 1)
        self.pushButton_gtSearch_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_gtSearch_2.setAutoDefault(False)
        self.pushButton_gtSearch_2.setObjectName("pushButton_gtSearch_2")
        self.gridLayout.addWidget(self.pushButton_gtSearch_2, 1, 2, 1, 1)
        self.label_7.raise_()
        self.label_10.raise_()
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(17, 11, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.spinBox_runs = QtWidgets.QSpinBox(self.centralWidget)
        self.spinBox_runs.setMinimum(1)
        self.spinBox_runs.setMaximum(10000)
        self.spinBox_runs.setObjectName("spinBox_runs")
        self.gridLayout_3.addWidget(self.spinBox_runs, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 2, 1, 1)
        self.checkBox_save = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox_save.setObjectName("checkBox_save")
        self.gridLayout_3.addWidget(self.checkBox_save, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_process = QtWidgets.QLabel(self.centralWidget)
        self.label_process.setText("")
        self.label_process.setObjectName("label_process")
        self.horizontalLayout.addWidget(self.label_process)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.PB_aceptar = QtWidgets.QPushButton(self.centralWidget)
        self.PB_aceptar.setDefault(True)
        self.PB_aceptar.setObjectName("PB_aceptar")
        self.horizontalLayout.addWidget(self.PB_aceptar)
        self.PB_cancelar = QtWidgets.QPushButton(self.centralWidget)
        self.PB_cancelar.setObjectName("PB_cancelar")
        self.horizontalLayout.addWidget(self.PB_cancelar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.groupBox_3.raise_()
        self.label_2.raise_()
        self.spinBox_runs.raise_()
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 469, 31))
        self.menuBar.setObjectName("menuBar")
        self.menupf = QtWidgets.QMenu(self.menuBar)
        self.menupf.setTitle("")
        self.menupf.setObjectName("menupf")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menupf.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Particle Filter Toolbox"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Filter design"))
        self.label.setText(_translate("MainWindow", "Filter algorithm:"))
        self.comboBox_filtro.setItemText(0, _translate("MainWindow", "SIS"))
        self.comboBox_filtro.setItemText(1, _translate("MainWindow", "SIR"))
        self.comboBox_filtro.setItemText(2, _translate("MainWindow", "G_PF"))
        self.comboBox_filtro.setItemText(3, _translate("MainWindow", "APF"))
        self.label_4.setText(_translate("MainWindow", "Number of particles:"))
        self.label_Tresample.setText(_translate("MainWindow", "Resampling algorithm:"))
        self.comboBox_Tresample.setItemText(0, _translate("MainWindow", "Multinomial"))
        self.comboBox_Tresample.setItemText(1, _translate("MainWindow", "Systematic"))
        self.comboBox_Tresample.setItemText(2, _translate("MainWindow", "Stratified"))
        self.comboBox_Tresample.setItemText(3, _translate("MainWindow", "Residual"))
        self.label_resample.setText(_translate("MainWindow", "Resampling percent:"))
        self.label_3.setText(_translate("MainWindow", "Estimation algorithm:"))
        self.comboBox_salida.setItemText(0, _translate("MainWindow", "Weighted mean"))
        self.comboBox_salida.setItemText(1, _translate("MainWindow", "Maximum weight"))
        self.comboBox_salida.setItemText(2, _translate("MainWindow", "Robust mean"))
        self.label_salida.setText(_translate("MainWindow", "Robust mean percent:"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Model"))
        self.label_5.setText(_translate("MainWindow", "State space:"))
        self.comboBox_ee.setItemText(0, _translate("MainWindow", "[x, y, Vx, Vy] (dynamic bbox)"))
        self.comboBox_ee.setItemText(1, _translate("MainWindow", "[x, y, Vx, Vy, w]"))
        self.comboBox_ee.setItemText(2, _translate("MainWindow", "[x, y, Vx, Vy, w, Vw]"))
        self.label_6.setText(_translate("MainWindow", "Observation model:"))
        self.comboBox_obsmodel.setItemText(0, _translate("MainWindow", "HSV color-based"))
        self.comboBox_obsmodel.setItemText(1, _translate("MainWindow", "LBP-based"))
        self.groupBox.setTitle(_translate("MainWindow", "Video"))
        self.label_7.setText(_translate("MainWindow", "Input video:"))
        self.pushButton_signal.setText(_translate("MainWindow", "Examine ..."))
        self.label_10.setText(_translate("MainWindow", "Annotations:"))
        self.pushButton_gtSearch_2.setText(_translate("MainWindow", "Examine ..."))
        self.label_2.setText(_translate("MainWindow", "Number of algorithm runs:"))
        self.checkBox_save.setText(_translate("MainWindow", "Save estimation"))
        self.PB_aceptar.setText(_translate("MainWindow", "Run"))
        self.PB_cancelar.setText(_translate("MainWindow", "Cancel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

