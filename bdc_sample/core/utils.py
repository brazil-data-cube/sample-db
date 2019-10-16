"""
This file contains code utilities of Brazil Data Cubes sampledb
"""

import os
from zipfile import ZipFile
from osgeo import osr


def validate_mappings(mappings):
    """
    Validates a class mappings of Data sets

    A mapping consists in a dictionary which maps the expected keys with
    provided keys in dataset.

    The well-known properties are:

    - geom : Geometry field.
    - latitude: Latitude field (when geom is not provided)
    - lontigude: Lontigude field (when geom is not provided)
    - class_name: Sample class. Default is "label"
    - start_date: Start date field. Default is "start_date"
    - end_date: End date field. Default is "end_date"
    """
    if not mappings:
        raise TypeError('Invalid mappings')

    if not mappings.get('class_name'):
        mappings['class_name'] = 'label'
        # raise KeyError('Invalid mappings: Key "class_name" is required.')

    if not mappings.get('geom'):
        if not mappings.get('latitude') and not mappings.get('longitude'):
            mappings['latitude'] = 'latitude'
            mappings['longitude'] = 'longitude'

    if not mappings.get('start_date'):
        mappings['start_date'] = 'start_date'
    if not mappings.get('end_date'):
        mappings['end_date'] = 'end_date'


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


def unzip(stream, destination):
    """
    Uncompress the zip file to the destination. The input
    may be a file or bytes representing opened file

    Args:
        stream (str, io.Bytes) - File to extract
        destination (str) - Destination directory
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

    with ZipFile(stream) as zip_object:
        zip_object.extractall(destination)
