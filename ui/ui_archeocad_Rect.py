# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_archeocad_Rect.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ArcheoRect(object):
    def setupUi(self, ArcheoRect):
        ArcheoRect.setObjectName("ArcheoRect")
        ArcheoRect.resize(348, 729)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ArcheoRect.sizePolicy().hasHeightForWidth())
        ArcheoRect.setSizePolicy(sizePolicy)
        ArcheoRect.setMinimumSize(QtCore.QSize(330, 669))
        ArcheoRect.setMaximumSize(QtCore.QSize(16777215, 16777215))
        ArcheoRect.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.gridLayout = QtWidgets.QGridLayout(ArcheoRect)
        self.gridLayout.setObjectName("gridLayout")
        self.gBox_pointLayer = QtWidgets.QGroupBox(ArcheoRect)
        self.gBox_pointLayer.setObjectName("gBox_pointLayer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gBox_pointLayer)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.qgsComboPointLayer = QgsMapLayerComboBox(self.gBox_pointLayer)
        self.qgsComboPointLayer.setObjectName("qgsComboPointLayer")
        self.gridLayout_2.addWidget(self.qgsComboPointLayer, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chkBoxSelected = QtWidgets.QCheckBox(self.gBox_pointLayer)
        self.chkBoxSelected.setObjectName("chkBoxSelected")
        self.horizontalLayout_2.addWidget(self.chkBoxSelected)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.TxtLabel_geoChoice = QtWidgets.QLabel(self.gBox_pointLayer)
        self.TxtLabel_geoChoice.setObjectName("TxtLabel_geoChoice")
        self.verticalLayout.addWidget(self.TxtLabel_geoChoice)
        self.TxtLable_geoChoice2 = QtWidgets.QLabel(self.gBox_pointLayer)
        self.TxtLable_geoChoice2.setObjectName("TxtLable_geoChoice2")
        self.verticalLayout.addWidget(self.TxtLable_geoChoice2)
        self.comboGeoChoice = QtWidgets.QComboBox(self.gBox_pointLayer)
        self.comboGeoChoice.setObjectName("comboGeoChoice")
        self.verticalLayout.addWidget(self.comboGeoChoice)
        self.gridLayout_2.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.gBox_pointLayer, 0, 0, 1, 1)
        self.gBox_multipleTr = QtWidgets.QGroupBox(ArcheoRect)
        self.gBox_multipleTr.setObjectName("gBox_multipleTr")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gBox_multipleTr)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chkBoxFieldGroup = QtWidgets.QCheckBox(self.gBox_multipleTr)
        self.chkBoxFieldGroup.setObjectName("chkBoxFieldGroup")
        self.horizontalLayout.addWidget(self.chkBoxFieldGroup)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_regroup = QtWidgets.QLabel(self.gBox_multipleTr)
        self.label_regroup.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_regroup.setObjectName("label_regroup")
        self.verticalLayout_4.addWidget(self.label_regroup)
        self.comboGroup = QtWidgets.QComboBox(self.gBox_multipleTr)
        self.comboGroup.setEnabled(False)
        self.comboGroup.setObjectName("comboGroup")
        self.verticalLayout_4.addWidget(self.comboGroup)
        self.gridLayout_3.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.gBox_multipleTr, 1, 0, 1, 1)
        self.gBox_multipleTr_2 = QtWidgets.QGroupBox(ArcheoRect)
        self.gBox_multipleTr_2.setObjectName("gBox_multipleTr_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.gBox_multipleTr_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_Width = QtWidgets.QLabel(self.gBox_multipleTr_2)
        self.label_Width.setObjectName("label_Width")
        self.horizontalLayout_3.addWidget(self.label_Width)
        self.doubleSpinBoxWidth = QtWidgets.QDoubleSpinBox(self.gBox_multipleTr_2)
        self.doubleSpinBoxWidth.setDecimals(2)
        self.doubleSpinBoxWidth.setMaximum(999999999.99)
        self.doubleSpinBoxWidth.setObjectName("doubleSpinBoxWidth")
        self.horizontalLayout_3.addWidget(self.doubleSpinBoxWidth)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_orientation = QtWidgets.QLabel(self.gBox_multipleTr_2)
        self.label_orientation.setObjectName("label_orientation")
        self.verticalLayout_2.addWidget(self.label_orientation)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.radioButtonLeft = QtWidgets.QRadioButton(self.gBox_multipleTr_2)
        self.radioButtonLeft.setChecked(False)
        self.radioButtonLeft.setObjectName("radioButtonLeft")
        self.horizontalLayout_6.addWidget(self.radioButtonLeft)
        self.radioButtonRight = QtWidgets.QRadioButton(self.gBox_multipleTr_2)
        self.radioButtonRight.setChecked(True)
        self.radioButtonRight.setObjectName("radioButtonRight")
        self.horizontalLayout_6.addWidget(self.radioButtonRight)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.gridLayout_4.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.gBox_multipleTr_2, 2, 0, 1, 1)
        self.gBox_Output = QtWidgets.QGroupBox(ArcheoRect)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gBox_Output.sizePolicy().hasHeightForWidth())
        self.gBox_Output.setSizePolicy(sizePolicy)
        self.gBox_Output.setObjectName("gBox_Output")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.gBox_Output)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_enconding = QtWidgets.QLabel(self.gBox_Output)
        self.label_enconding.setObjectName("label_enconding")
        self.horizontalLayout_5.addWidget(self.label_enconding)
        self.comboEncoding = QtWidgets.QComboBox(self.gBox_Output)
        self.comboEncoding.setObjectName("comboEncoding")
        self.horizontalLayout_5.addWidget(self.comboEncoding)
        self.gridLayout_5.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.outFileLine = QtWidgets.QLineEdit(self.gBox_Output)
        self.outFileLine.setObjectName("outFileLine")
        self.horizontalLayout_4.addWidget(self.outFileLine)
        self.ButtonBrowse = QtWidgets.QPushButton(self.gBox_Output)
        self.ButtonBrowse.setObjectName("ButtonBrowse")
        self.horizontalLayout_4.addWidget(self.ButtonBrowse)
        self.gridLayout_5.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.radioButPolyG = QtWidgets.QRadioButton(self.gBox_Output)
        self.radioButPolyG.setChecked(True)
        self.radioButPolyG.setObjectName("radioButPolyG")
        self.horizontalLayout_7.addWidget(self.radioButPolyG)
        self.radioButPolyL = QtWidgets.QRadioButton(self.gBox_Output)
        self.radioButPolyL.setObjectName("radioButPolyL")
        self.horizontalLayout_7.addWidget(self.radioButPolyL)
        self.gridLayout_5.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.gBox_Output, 3, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ArcheoRect)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)

        self.retranslateUi(ArcheoRect)
        self.buttonBox.accepted.connect(ArcheoRect.accept)
        self.buttonBox.rejected.connect(ArcheoRect.reject)
        self.chkBoxFieldGroup.toggled['bool'].connect(self.comboGroup.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ArcheoRect)

    def retranslateUi(self, ArcheoRect):
        _translate = QtCore.QCoreApplication.translate
        ArcheoRect.setWindowTitle(_translate("ArcheoRect", "ArcheoCAD Rectangle"))
        self.gBox_pointLayer.setTitle(_translate("ArcheoRect", "Input point layer"))
        self.chkBoxSelected.setText(_translate("ArcheoRect", "Create output features using only selected points"))
        self.TxtLabel_geoChoice.setText(_translate("ArcheoRect", "Input field containing the output geometry"))
        self.TxtLable_geoChoice2.setText(_translate("ArcheoRect", "(rectangle)"))
        self.gBox_multipleTr.setTitle(_translate("ArcheoRect", "Regrouping field"))
        self.chkBoxFieldGroup.setText(_translate("ArcheoRect", "Regrouping points based on a specific field"))
        self.label_regroup.setText(_translate("ArcheoRect", "Input field to be used to regroup points "))
        self.gBox_multipleTr_2.setTitle(_translate("ArcheoRect", "Rectangle"))
        self.label_Width.setText(_translate("ArcheoRect", "Width (map\'s unit)"))
        self.label_orientation.setText(_translate("ArcheoRect", "Direction choice for creating the rectangle :"))
        self.radioButtonLeft.setText(_translate("ArcheoRect", "left"))
        self.radioButtonRight.setText(_translate("ArcheoRect", "right"))
        self.gBox_Output.setTitle(_translate("ArcheoRect", "Output shapefile"))
        self.label_enconding.setText(_translate("ArcheoRect", "Character encoding"))
        self.ButtonBrowse.setText(_translate("ArcheoRect", "browse"))
        self.radioButPolyG.setText(_translate("ArcheoRect", "Polygon"))
        self.radioButPolyL.setText(_translate("ArcheoRect", "Polyline"))
from qgsmaplayercombobox import QgsMapLayerComboBox
