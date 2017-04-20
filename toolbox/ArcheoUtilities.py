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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings, QTextCodec

from qgis.core import *
from qgis.gui import *

from os.path import splitext
from os.path import dirname
from os.path import basename


# All methods of this class were adopted from 'points2one Plugin'
# Copyright (C) 2010 Pavol Kapusta
# Copyright (C) 2010, 2013 Goyo
class Utilities(object):
  
    # Returns a list of names of all layers in QgsMapLayerRegistry
    @staticmethod
    def getLayerNames(geoTypes):
        mapLayers = QgsMapLayerRegistry.instance().mapLayers()    
        layers = []  
        for name, layer in mapLayers.iteritems():
            if (layer.type() == QgsMapLayer.VectorLayer) and (layer.geometryType() in geoTypes):
                layers.append(unicode(layer.name()))
        return layers
    
    
    #Return QgsVectorLayer from a layer name ( as string )
    #adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
    @staticmethod
    def getVectorLayerByName(layerName):
#         if layerName is None:
#             return None
        mapLayers = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in mapLayers.iteritems():
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
        SaveOutPutShapeMsg = QtGui.QApplication.translate("Utility","Save output shapefile", None, QtGui.QApplication.UnicodeUTF8) 
        outFilePath = QtGui.QFileDialog.getSaveFileName(parent, SaveOutPutShapeMsg, outDir, filter)
        outFilePath = unicode(outFilePath)
        if outFilePath:
            root, ext = splitext(outFilePath)
            if ext.upper() != '.SHP':
                outFilePath = '%s.shp' % outFilePath
            outDir = dirname(outFilePath)
            settings.setValue(key, outDir)
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
        ret = QgsMapLayerRegistry.instance().addMapLayer(newLayer)
        return ret
    
    
    
    
    
# All methods of this class were adopted from 'points2one Plugin'
# Copyright (C) 2010 Pavol Kapusta
# Copyright (C) 2010, 2013 Goyo  
class ArcheoEnconding(object):
  
    @staticmethod
    def getEncodings():
        """Returns a list of available encodings static."""
        
        return [unicode(QTextCodec.codecForMib(mib).name())
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
