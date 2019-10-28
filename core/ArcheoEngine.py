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

# #debug
# from pydevd import *
# #debug

from itertools import groupby
import math
from copy import deepcopy

from PyQt5.QtCore import *
from PyQt5 import QtGui
from qgis.core import *

from .GeoEnum import GeoEnum
from .RectOrientationValue import RectOrientationValue
from ..toolbox.ArcheoExceptions import *



class Engine(object):
    
    def __init__(self, layer, filename, encoding, geoAttr, numCircleVertices, 
                 entitiesSelected, groupAttr = None, sortAttr = None, rectOrient = None, rectSideLen = None):
        self.layer = layer
        self.fileName = filename
        self.encoding = encoding    
        self.geoAttr = geoAttr
        self.numCircleVertices = numCircleVertices
        self.EntitiesSelected = entitiesSelected
        self.groupAttr = groupAttr
        self.sortAttr = sortAttr
        self.rectOrient = rectOrient
        self.rectSideLen = rectSideLen
        self.logger = []
        self.FeatureCounter = 0
        self.CreateMethodDict = {GeoEnum.Cercle : self.createCircle,
                              GeoEnum.Ellipse : self.createEllipse,
                              GeoEnum.Poly : self.createPolygon}
    
    # inspired from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def createShapefile(self):
        """Creates the output shapefile."""
        
        check = QFile(self.fileName)
        if check.exists():
            if not QgsVectorFileWriter.deleteShapeFile(self.fileName):
                raise FileDeletionError(self.fileName)
        provider = self.layer.dataProvider()
        writer = QgsVectorFileWriter(self.fileName, self.encoding, provider.fields(), QgsWkbTypes.Polygon, self.layer.crs(), driverName = 'ESRI Shapefile')       
        for feature in self.iterateFeatures():
            writer.addFeature(feature)
            self.FeatureCounter += 1
        if self.FeatureCounter == 0:
            del writer    
            if not QgsVectorFileWriter.deleteShapeFile(self.fileName):
                msg = QCoreApplication.translate("Engine","No feature was created. The {} shapefile was deleted.\n")
                raise FileDeletionError(msg + self.fileName)
            raise NoFeatureCreatedError(self.fileName)
        del writer
    
    # inspired from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def iterateFeatures(self):
        """Iterates over features with vertices in the input layer.
        For each consecutive group of points with the same value for the
        given attribute, yields a "WKBPolygon" (Circle, Ellipse, Rectangle 
        or general Polygon) using those points."""
        
        for key, pts in self.iterationGroups():            
            try:               
                # calls the specific feature creation method (using a dictionary) depending on 
                # the output geometry choice (circle, ellipse etc.) 
                provider = self.layer.dataProvider()
                geomAttrIdx = provider.fieldNameIndex(self.geoAttr)
                if geomAttrIdx < 0:
                    raise UnknownAttributeError(self.layer.name, self.groupAttr)                              
                points = [p for p in pts]                
                attributes = points[0][1]
                geom = str(attributes[geomAttrIdx]).upper()
                if self.sortAttr and GeoEnum.determineGeom(geom) == GeoEnum.Poly:
                    sortAttrIdx = provider.fieldNameIndex(self.sortAttr)
                    if sortAttrIdx < 0:
                        raise UnknownAttributeError(self.layer.name, self.sortAttr)
                    points = sorted(points, key = lambda p : (p[1][sortAttrIdx]))         
                pointList = [point[0] for point in points]
                if self.rectOrient is not None: # we are in the Rectangle Dialog case
                    if GeoEnum.determineGeom(geom) == GeoEnum.Rect:
                        feature = self.createRectangle(pointList, attributes)                        
                    elif GeoEnum.determineGeom(geom) in [GeoEnum.Poly, GeoEnum.Cercle, GeoEnum.Ellipse]:
                        continue
                    else:
                        msg = QCoreApplication.translate("Engine","At least one group of point contains an invalid output geometry: {}")
                        raise ValueError(msg.format(geom))
                else:
                    if GeoEnum.determineGeom(geom) == GeoEnum.Rect:
                        continue
                    else:
                        feature = self.CreateMethodDict[GeoEnum.determineGeom(geom)](pointList, attributes)
                     
            except ValueError as e:
                msg = QCoreApplication.translate("Engine","key: {0}-value: {1}\n")
                self.logWarning(msg.format(key, e))
            except KeyError as e:
                msg = QCoreApplication.translate("Engine","At least one group of point contains an invalid output geometry: {}")
                self.logWarning(msg.format(geom))           
            else:
                yield feature
    
    # inspired from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo            
    def iterationGroups(self):
        """Iterates over the input layer grouping by attribute.    
        Returns an iterator of (key, points) pairs where key is the
        attribute value and points is an iterator of (QgsPointXY,
        attributes) pairs."""

        points = self.iteratePoints()
        provider = self.layer.dataProvider()       
        geomAttrIdx = provider.fieldNameIndex(self.geoAttr)
        if geomAttrIdx < 0:
            raise UnknownAttributeError(self.layer.name, self.geoAttr)       
        if self.groupAttr:
            grpAttrIdx = provider.fieldNameIndex(self.groupAttr)                      
            if grpAttrIdx < 0:
                raise UnknownAttributeError(self.layer.name, self.groupAttr)
            points = sorted(points, key = lambda p : (GeoEnum.determineGeom(p[1][geomAttrIdx]), p[1][grpAttrIdx]))                               
            return groupby(points, lambda p: (GeoEnum.determineGeom(p[1][geomAttrIdx]), p[1][grpAttrIdx]))
        else:
            points = sorted(points, key = lambda p : GeoEnum.determineGeom(p[1][geomAttrIdx]))
            return groupby(points, lambda p: GeoEnum.determineGeom(p[1][geomAttrIdx]))
    
    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo
    def iteratePoints(self):
        """Iterates over the features of the input layer.
        Yields pairs of (QgsPointXY, attributes)."""
              
        provider = self.layer.dataProvider()
        #create a QgsFeatureRequest with this condition : in selectedFeatureIds
        if self.EntitiesSelected :
            selectedFeatureIds = self.layer.selectedFeatureIds()         
            selectedFeatureReq = QgsFeatureRequest().setFilterFids(selectedFeatureIds) 
            features = provider.getFeatures(selectedFeatureReq)    
        else:            
            features = provider.getFeatures()
        feature = QgsFeature()
        while(features.nextFeature(feature)):       
            geom = feature.geometry().asPoint()
            attributes = feature.attributes()
            yield(QgsPointXY(geom.x(), geom.y()), attributes)
    
    # adopted from 'points2one Plugin'
    # Copyright (C) 2010 Pavol Kapusta
    # Copyright (C) 2010, 2013 Goyo    
    def createPolygon(self, pointList, attributes):
        """Returns a feature with given vertices.    
        Vertices are given as (QgsPointXY, attributeMap) pairs. The
        returned feature is a polygon (WKBPolygon)."""
        
        if len(pointList) < 3:
            msg = QCoreApplication.translate("Engine","Can not create a polygon out of {} points.")
            raise ValueError(msg.format(len(pointList)))             
        geom = QgsGeometry.fromPolygonXY([pointList])               
        feature = QgsFeature()                     
        feature.setGeometry(geom)
        feature.setAttributes(attributes)
        return feature
    
    def createCircle(self, pointList, attributes):
        
        if len(pointList) != 2 :
            msg = QCoreApplication.translate("Engine","Can not create a circle out of {} point(s).")
            raise ValueError(msg.format(len(pointList)))        
        circlePoints = []        
        # Digitize the circle using its parametric equation
        angleStep = 2*math.pi/self.numCircleVertices
        center = QgsPointXY((pointList[0].x() + pointList[1].x())/2, 
                           (pointList[0].y() + pointList[1].y())/2)        
        distanceCal = QgsDistanceArea()
        radius = distanceCal.measureLine(center, pointList[1])        
        alpha = 0
        for i in range(self.numCircleVertices): 
            alpha += angleStep
            xi = radius*math.cos(alpha) + center.x()
            yi = radius*math.sin(alpha) + center.y()
            circlePoints.append(QgsPointXY(xi, yi))
        #creating the feature                           
        circleGeom = QgsGeometry.fromPolygonXY([circlePoints])
        feature = QgsFeature()
        feature.setGeometry(circleGeom)
        feature.setAttributes(attributes)
        return feature
    
    # Mainly from :
    # Inkscape's "Ellipse by 5 Points Extension" 
    # Copyright (c) 2012 Stuart Pernsteiner
    def createEllipse(self, pointList, attributes):
        if len(pointList) < 5 :
            msg = QCoreApplication.translate("Engine","To create an Ellipse 5 points are needed.")
            raise ValueError(msg)
        if len(pointList) > 5 : # in this case only the first 5 points are used
            msg = QCoreApplication.translate("Engine","There were too many points ({}), only 5  of them were used to create the ellipse.") 
            self.logWarning(msg)
        # this translation is for avoiding floating point precision issues
        baryC = MathTools.barycenter(pointList)
        pointListBC = []
        for pt in pointList : 
            pointListBC.append((pt[0] - baryC[0], pt[1] - baryC[1]))                         
        # find the center and the axes of by solving the conic equation :
        # ax2 + bxy + cy2 + dx + ey + f = 0
        conic = MathTools.conicEquation(pointListBC)
        [a, b, c, d, e, f] = conic
        # conditions for the existence of an ellipse 
        if MathTools.bareissDeterminant([[a, b/2, d/2], [b/2, c, e/2], [d/2, e/2, f]]) == 0 or a*c - b*b/4 <= 0:
            msg = QCoreApplication.translate("Engine","Could not find the ellipse passing by these five points.") 
            raise ValueError(msg)     
        cX = (b*e - 2*c*d) / (4*a*c - b*b)
        cY = (d*b - 2*a*e) / (4*a*c - b*b)
        center = (cX, cY)        
        [axisDir1, axisDir2] = MathTools.ellipseAxes(conic)
        axisLen1 = MathTools.ellipseAxisLen(conic, center, axisDir1)
        axisLen2 = MathTools.ellipseAxisLen(conic, center, axisDir2)    
        if axisLen1 > axisLen2:
                majorDir = axisDir1
                majorLen = axisLen1
                minorLen = axisLen2
        else:
                majorDir = axisDir2
                majorLen = axisLen2
                minorLen = axisLen1
        rotAngle = math.atan2(majorDir[1], majorDir[0])       
        # creating an ellipse with it's major axis parallel to the X axis
        # using its parametric equation
        # rotating each point using the angle of the major axis
        ellipsePoints = []          
        angleStep = 2*math.pi/self.numCircleVertices
        alpha = 0
        for i in range(self.numCircleVertices): 
            alpha += angleStep          
            xi = majorLen*math.cos(alpha) + center[0]
            yi = minorLen*math.sin(alpha) + center[1]
            (xi, yi) = MathTools.rotation((xi, yi), rotAngle, center)
            # center of mass translation backwards
            (xi, yi) = (xi + baryC[0], yi + baryC[1])
            ellipsePoints.append(QgsPointXY(xi, yi))                  
        #creating the feature
        ellipseGeom = QgsGeometry.fromPolygonXY([ellipsePoints])
        feature = QgsFeature()
        feature.setGeometry(ellipseGeom)
        feature.setAttributes(attributes)
        return feature
    
    def createRectangle(self, pointList, attributes):
        
        if len(pointList) != 2 :
            msg =  QCoreApplication.translate("Engine","Exactly 2 points are needed to create a rectangle.")
            raise ValueError(msg)
        rectanglePoints = []        
        p1 = pointList[1]
        p2 = pointList[0]
        rectanglePoints.append(p1)
        rectanglePoints.append(p2)
        #Generate the to other points of the rectangle
        azimuth = p1.azimuth(p2)
        if self.rectOrient == RectOrientationValue.Right:
            vertical = azimuth - 90
        else:
            vertical = azimuth + 90
        vertRad = math.radians(vertical)
        cosA = math.sin(vertRad)
        cosB = math.cos(vertRad)
        p3 = QgsPointXY((p2.x() + self.rectSideLen*cosA),
                      (p2.y() + self.rectSideLen*cosB))
        p4 = QgsPointXY((p1.x() + self.rectSideLen*cosA),
                       (p1.y() + self.rectSideLen*cosB))
        rectanglePoints.append(p3)
        rectanglePoints.append(p4)
        rectangleGeometry = QgsGeometry.fromPolygonXY([rectanglePoints])
        feature = QgsFeature()
        feature.setGeometry(rectangleGeometry)
        feature.setAttributes(attributes)
        return feature       
            
    def logWarning(self, message):
        """Logs a warning."""
        
        self.logger.append(message)

    def getLogger(self):
        """Returns the list of logged warnings."""
        
        return self.logger
    
    
    
    
    
class MathTools(object):
    """Contains static methods that are used for creating ellipses."""
        
    # adopted from Inkscape's "Ellipse by 5 Points Extension" 
    # Copyright (c) 2012 Stuart Pernsteiner
    # Algorithm from:
    # Yap, Chee, "Linear Systems", Fundamental Problems of Algorithmic Algebra    
    # http://cs.nyu.edu/~yap/book/alge/ftpSite/l10.ps.gz
    @staticmethod
    def bareissDeterminant(inMatrix):
        """Computes the determinant of the matrix using Bareiss algorithm.""" 
      
        matrix = deepcopy(inMatrix)
        size = len(matrix)
        lastAkk = 1
        for k in range(size - 1):
            if lastAkk == 0:
                return 0
            for i in range(k + 1, size):
                for j in range(k + 1, size):
                    matrix[i][j] = (matrix[i][j]*matrix[k][k] - matrix[i][k]*matrix[k][j])/lastAkk
            lastAkk = matrix[k][k]
        return matrix[size - 1][size - 1]
                
    # adopted from Inkscape's "Ellipse by 5 Points Extension" 
    # Copyright (c) 2012 Stuart Pernsteiner
    # developed using : 
    # http://math.fullerton.edu/mathews/n2003/conicfit/ConicFitMod/Links/ConicFitMod_lnk_9.html
    @staticmethod
    def conicEquation(points):
        """Computes the equation of the conic section passing through five given points."""
        
        rowMajorMatrix = []
        for i in range(5):            
            (x, y) = points[i]
            row = [x*x, x*y, y*y, x, y, 1]
            rowMajorMatrix.append(row)
        fullMatrix = []
        for i in range(6):
            col = []
            for j in range(5):
                col.append(rowMajorMatrix[j][i])
            fullMatrix.append(col)
        coeffs = []
        sign = 1
        for i in range(6):
            matrix = []
            for j in range(6):
                if j == i:
                    continue
                matrix.append(fullMatrix[j])
            coeffs.append(MathTools.bareissDeterminant(matrix)*sign)
            sign = -sign
        return coeffs
    
    # adopted from Inkscape's "Ellipse by 5 Points Extension" 
    # Copyright (c) 2012 Stuart Pernsteiner   
    @staticmethod
    def ellipseAxes(conic):
        """Compute the axis directions of the ellipse."""
    
        [a, b, c, d, e, f] = conic
        # Compute the eigenvalues of
        #    /  a   b/2 \
        #    \ b/2   c  /
        # This algorithm is from
        # http://www.math.harvard.edu/archive/21b_fall_04/exhibits/2dmatrices/index.html
        ma = a
        mb = b/2
        mc = b/2
        md = c
        mDet = ma*md - mb*mc
        mTrace = ma + md
    
        (l1, l2) = MathTools.solveQuadratic(1, -mTrace, mDet);
             
        if mb == 0:
            return [(0, 1), (1, 0)]
        else:
            return [(mb, l1 - ma), (mb, l2 - ma)]
    
    # adopted from Inkscape's "Ellipse by 5 Points Extension" 
    # Copyright (c) 2012 Stuart Pernsteiner
    @staticmethod
    def ellipseAxisLen(conic, center, direction):
        """ Compute the axis length as a multiple of the magnitude of 'direction'"""
        
        [a, b, c, d, e, f] = conic
        (cx, cy) = center
        (dx, dy) = direction
    
        dLen = math.sqrt(dx*dx + dy*dy)
        dx /= dLen
        dy /= dLen
    
        # Solve for t:
        #   a*x^2 + b*x*y + c*y^2 + d*x + e*y + f = 0
        #   x = cx + t * dx
        #   y = cy + t * dy
        # by substituting, we get  qa*t^2 + qb*t + qc = 0, where:
        qa = a*dx*dx + b*dx*dy + c*dy*dy
        qb = a*2*cx*dx + b*(cx*dy + cy*dx) + c*2*cy*dy + d*dx + e*dy
        qc = a*cx*cx + b*cx*cy + c*cy*cy + d*cx + e*cy + f    
        (t1, t2) = MathTools.solveQuadratic(qa, qb, qc)    
        return max(t1, t2)

    @staticmethod        
    def solveQuadratic(a, b, c):
        
        if (b*b - 4*a*c) < 0:
            msg = QCoreApplication.translate("Engine","Could not find the ellipse passing by these five points.") 
            raise ValueError(msg)
        discRoot = math.sqrt(b*b - 4*a*c)
        x1 = (-b + discRoot) / (2*a)
        x2 = (-b - discRoot) / (2*a)
        return (x1, x2)
    
    @staticmethod
    def rotation(p, rotAngle, c):       
        # translation
        xT = p[0] - c[0]
        yT = p[1] - c[1]
        # rotation over the origin
        xR = xT*math.cos(rotAngle) - yT*math.sin(rotAngle)
        yR = xT*math.sin(rotAngle) + yT*math.cos(rotAngle)
        # translation back
        newX = xR + c[0]
        newY = yR + c[1]
        return (newX, newY)
    
    @staticmethod
    def barycenter(points):
        
        nPts = len(points)
        sumX = 0
        sumY = 0
        for pt in points :
            sumX += pt.x()
            sumY += pt.y()           
        return (sumX/nPts, sumY/nPts)
    
    