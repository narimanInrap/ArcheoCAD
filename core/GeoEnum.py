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

class GeoEnum(object):
    PolyList = ['POLY', 'POLYGON', 'POLYGONE', 'POLYG', 'PG', 'P']
    CercleList = ['CERCLE', 'CIRCLE', 'CRCL', 'C']
    EllipseList = ['ELLIPSE', 'OVAL', 'OVALE', 'ELPS', 'E', 'O']
    RectList = ['RECT', 'RECTANGLE', 'R']
    LineList = ['LINE', 'LIGNE', 'L', 'LN', 'POLYLINE', 'PL', 'POLYLIGNE']
    
    Poly = 1
    Cercle = 2
    Ellipse = 3
    Rect = 4
    Line = 5
    
    @staticmethod
    def determineGeom(inGeom):
        
        geom = str(inGeom)
        if geom.upper() in GeoEnum.PolyList:
            return GeoEnum.Poly
        if geom.upper() in GeoEnum.CercleList:
            return GeoEnum.Cercle
        if geom.upper() in GeoEnum.EllipseList:
            return GeoEnum.Ellipse
        if geom.upper() in GeoEnum.RectList:
            return GeoEnum.Rect
        if geom.upper() in GeoEnum.LineList:
            return GeoEnum.Line
        return -1