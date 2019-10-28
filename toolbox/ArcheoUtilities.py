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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSettings, QTextCodec, QCoreApplication



from qgis.core import *
from qgis.gui import *

from os.path import splitext
from os.path import dirname
from os.path import basename

#debug
# import pydevd
#debug


# All methods of this class were adopted from 'points2one Plugin'
# Copyright (C) 2010 Pavol Kapusta
# Copyright (C) 2010, 2013 Goyo
class Utilities(object):
  
    # Returns a list of names of all layers in QgsMapLayerRegistry
#     @staticmethod
#     def getLayerNames(geoTypes):
#     #    pydevd.settrace()
#         mapLayers = QgsProject.instance().mapLayers()
#         layers = []  
#         for name, layer in mapLayers.items():
#             if (layer.type() == QgsMapLayer.VectorLayer) and (layer.geometryType() in geoTypes):
#                 layers.append(unicode(layer.name()))
#         return layers
    
    
    #Return QgsVectorLayer from a layer name ( as string )
    #adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
    @staticmethod
    def getVectorLayerByName(layerName):
#         if layerName is None:
#             return None
        mapLayers = QgsProject.instance().mapLayers()
        for name, layer in mapLayers.items():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == layerName:
                if layer.isValid():
                    return layer
                else:
                    return None    
    
    @staticmethod
    def saveFileDialog(parent): 
        """Shows a save file dialog and returns the selected file path."""
        
        settings = QtCore.QSettings()
        key = '/UI/lastShapefileDir'
        outDir = settings.value(key)
        filter = 'Shapefiles (*.shp)'
        SaveOutPutShapeMsg = QCoreApplication.translate("Utility","Save output shapefile")
        outFilePath, _filter = QtWidgets.QFileDialog.getSaveFileName(parent, SaveOutPutShapeMsg, outDir, filter)
        return outFilePath
     
    # Adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
    @staticmethod
    def addShapeToCanvas(shapeFilePath):
        """adds a vector layer to the canvas based on the input shapefile path"""
        
        layerName = basename(shapeFilePath)
        root, ext = splitext(layerName)
        if ext == '.shp':
            layerName = root
        newLayer = QgsVectorLayer(shapeFilePath, layerName, "ogr")
        ret = QgsProject.instance().addMapLayer(newLayer)
        return ret
    
    
    
    
    
# All methods of this class were adopted from 'points2one Plugin'
# Copyright (C) 2010 Pavol Kapusta
# Copyright (C) 2010, 2013 Goyo  
class ArcheoEnconding(object):
  
    @staticmethod
    def getEncodings():
        """Returns a list of available encodings. static."""
        
        return [str(unicode(QTextCodec.codecForMib(mib).name().data(), encoding = 'utf-8'))
                 for mib in QTextCodec.availableMibs()]
    
    @staticmethod    
    def getDefaultEncoding(default = 'System'):
        """Returns the default encoding. static"""
        
        settings = QSettings()
        return settings.value('/UI/encoding', default)
        
    @staticmethod
    def setDefaultEncoding(encoding):
        """Sets the default encoding. static"""
        
        # Make sure encoding is not blank.
        encoding = encoding or 'System'
        settings = QSettings()
        settings.setValue('/UI/encoding', encoding)
