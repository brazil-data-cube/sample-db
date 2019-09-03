"""
This file contains code utilities of Brazil Data Cubes sampledb
"""

from osgeo import osr


def reproject(geom, source_srid, target_srid):
    """
    Reproject a geometry to srid provided

    It may throws exception when SRID is invalid

    Args:
        geom (ogr.Geometry): Geometry
        source_srid (int): Input SRID
        target_srid (int): Target SRID
    """
    source = osr.SpatialReference()

    if isinstance(source_srid, int):
        source.ImportFromEPSG(source_srid)
    else:
        source.ImportFromProj4(source_srid)

    target = osr.SpatialReference()

    if isinstance(target_srid, int):
        target.ImportFromEPSG(target_srid)
    else:
        target.ImportFromProj4(target_srid)

    transform = osr.CoordinateTransformation(source, target)
    geom.Transform(transform)
