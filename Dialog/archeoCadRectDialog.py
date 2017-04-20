# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ArcheoCAD
                                 A QGIS plugin
 Génération d'une couche vectorielle de Polygone, Rectangle, Cercle et Ellipse.
                             -------------------
        begin                : 2014-04-08
        copyright            : (C) 2014 by Nariman Hatami - INRAP
        email                : nariman.hatami@inrap.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#using Unicode for all strings
from __future__ import unicode_literals



import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from ..ui.ui_archeocad_Rect import Ui_ArcheoRect
from archeocadSuperDialog import ArcheoCadSuperDialog

from ..toolbox.ArcheoUtilities import Utilities, ArcheoEnconding
from ..toolbox.ArcheoExceptions import *
from ..core.RectOrientationValue import RectOrientationValue
from ..core.ArcheoEngine import Engine



class RectangleDialog(ArcheoCadSuperDialog, Ui_ArcheoRect):
    def __init__(self):
        ArcheoCadSuperDialog.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        QObject.connect(self.ButtonBrowse, SIGNAL('clicked()'), self.outFile)
        QObject.connect(self.comboPointLayer, SIGNAL('currentIndexChanged(QString)'), self.updateFieldCombos)
        self.populateEncodings(ArcheoEnconding.getEncodings())   
        self.populateLayerList()      
            
    def inputCheck(self):
        """Verifies whether the input is valid."""
        
        layer = self.selectedLayer()
        if layer is None:
            msg = QtGui.QApplication.translate("RectDialog", "Please specify an input layer.", None, QtGui.QApplication.UnicodeUTF8)
            QMessageBox.warning(self, 'ArcheoCAD', msg)
            return False
        provider = layer.dataProvider()    
        if (provider.featureCount() < 2):
            msg = QtGui.QApplication.translate("RectDialog","Please select an input layer with at least 2 points.", None, QtGui.QApplication.UnicodeUTF8) 
            QMessageBox.warning(self, 'ArcheoCAD', msg)
            return False
        if self.chkBoxFieldGroup.isChecked() and self.groupAttrName() == '':
            msg = QtGui.QApplication.translate("RectDialog","Please specify an input field for the gathering of the points.", None, QtGui.QApplication.UnicodeUTF8)
            QMessageBox.warning(self, 'ArcheoCAD', msg)
            return False
        if self.doubleSpinBoxWidth.value() <= 0:
            msg = QtGui.QApplication.translate("RectDialog","Please enter a strictly positive value for the rectangle's width", None, QtGui.QApplication.UnicodeUTF8)
            QMessageBox.warning(self, 'ArcheoCAD', msg)
            return False
        extension = os.path.splitext(self.getOutputFilePath())[1][1:]
        if self.getOutputFilePath() == '' or extension != 'shp': 
            msg = QtGui.QApplication.translate("RectDialog","Please specify an output shapefile.", None, QtGui.QApplication.UnicodeUTF8)
            QMessageBox.warning(self, 'ArcheoCAD', msg)
            return False
        return True
     
    def accept(self):
        if not self.inputCheck():
            return
        layer = self.selectedLayer()
        ArcheoEnconding.setDefaultEncoding(self.outputEncoding())
        if self.radioButtonRight.isChecked():
            RectOrientation = RectOrientationValue.Right
        else:
            RectOrientation = RectOrientationValue.Left             
        engine = Engine(
            layer,
            self.getOutputFilePath(),
            self.outputEncoding(),
            self.getGeoChoiceAttr(),
            None, # number of vertices
            self.chkBoxSelected.isChecked(),
            self.groupAttrName(),
            None, # sort
            RectOrientation,
            self.doubleSpinBoxWidth.value()
            )
        try:
            engine.createShapefile()
        except (FileDeletionError, Exception) as e:
            message = e.message
            QMessageBox.warning(self, 'ArcheoCAD', message)
            logMsg = '\n'.join(engine.getLogger())
            if logMsg:
                QMessageBox.warning(self, 'ArcheoCAD', logMsg)
            return        
        self.showWarning(engine) 
        self.addShapeToCanvas()
        #uncheck the checkbox, clear the output file name and hide the dialog window
        self.hideDialog()
