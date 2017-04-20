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

import os.path

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc

# Import the code for the dialog
from Dialog.archeocaddialog import ArcheoCADDialog
from Dialog.archeoCadRectDialog import RectangleDialog




class ArcheoCAD:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'archeocad_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ArcheoCADDialog()
        self.dlgRect = RectangleDialog()

    def initGui(self):
        #Create plugin Toolbar
        self.toolBar = self.iface.addToolBar("ArcheoCAD")
        self.toolBar.setObjectName("ArcheoCAD")
        
        #Polygon-Circle-Ellipse
        
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/archeocad/icons/ArcheoIcon.png"),
            QCoreApplication.translate(u"ArcheoCAD", "Poly-Circle-Ellipse"), self.iface.mainWindow())        
     
        # connect the action to the run method
        self.action.triggered.connect(self.run)
       
        # Add the the action to the  toolbar and menu item
        self.toolBar.addAction(self.action)        
        self.iface.addPluginToMenu(u"&ArcheoCAD", self.action)
        self.iface.addPluginToVectorMenu(u"&ArcheoCAD", self.action)
        
      
        #Rectangle
        self.actionRectangle = QAction(
            QIcon(":/plugins/archeocad/icons/ArcheoIcon2.png"),
            QCoreApplication.translate(u"ArcheoCAD", "Rectangle"), self.iface.mainWindow())
        
        self.actionRectangle.triggered.connect(self.runRect)        
        
        self.toolBar.addAction(self.actionRectangle)   
        self.iface.addPluginToMenu(u"&ArcheoCAD", self.actionRectangle)
        self.iface.addPluginToVectorMenu(u"&ArcheoCAD", self.actionRectangle)
        # separator
        self.toolBar.addSeparator()
        
        # help
        self.helpAction = QAction(QIcon(":/plugins/archeocad/icons/help.svg"),
                                  QCoreApplication.translate(u"ArcheoCAD", "help"), self.iface.mainWindow())
        self.helpAction.triggered.connect(self.help)
        self.iface.addPluginToMenu(u"&ArcheoCAD", self.helpAction)
        self.iface.addPluginToVectorMenu(u"&ArcheoCAD", self.helpAction)
        
    def help(self):
        if QCoreApplication.translate(u"ArcheoCAD", "help") == "aide":
            help_file = "file:///{}/help/build/html/fr/index.html".format(os.path.dirname(__file__))
        else:
            help_file = "file:///{}/help/build/html/en/index.html".format(os.path.dirname(__file__)) 
        QDesktopServices().openUrl(QUrl(help_file))
         
    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&ArcheoCAD", self.action)
        self.iface.removePluginMenu(u"&ArcheoCAD", self.actionRectangle)
        self.iface.removePluginMenu(u"&ArcheoCAD", self.helpAction)
        self.iface.removePluginVectorMenu(u"&ArcheoCAD", self.action)
        self.iface.removePluginVectorMenu(u"&ArcheoCAD", self.actionRectangle)
        self.iface.removePluginVectorMenu(u"&ArcheoCAD", self.helpAction)
        self.iface.removeToolBarIcon(self.action)
        self.iface.removeToolBarIcon(self.actionRectangle)
        del self.toolBar

    # run method that performs all the real work
    def run(self):
        #update the available vectorial layers
        self.dlg.populateLayerList()
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            #self.dlg.hide()
            pass
                    
    def runRect(self):
        #update the available vectorial layers
        self.dlgRect.populateLayerList()
        # show the dialog
        self.dlgRect.show()
        # Run the dialog event loop
        result = self.dlgRect.exec_()
        # See if OK was pressed
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            #self.dlgRect.hide()
            pass