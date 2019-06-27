from osgeo import ogr, osr


def reproject(geom, source_srid, target_srid):
    """
    Reproject a geometry to srid provided

    It may throws exception when SRID is invalid

    :param geom: (ogr.Geometry) Geometry
    :param source_srid: (int) Input SRID
    :param target_srid: (int) Target SRID
    """
    source = osr.SpatialReference()
    source.ImportFromEPSG(source_srid)

    target = osr.SpatialReference()
    target.ImportFromEPSG(target_srid)
    transform = osr.CoordinateTransformation(source, target)
    geom.Transform(transform)