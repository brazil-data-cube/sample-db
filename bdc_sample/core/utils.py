"""
This file contains code utilities of Brazil Data Cubes sampledb
"""

from io import IOBase
import os
from tempfile import SpooledTemporaryFile
from zipfile import ZipFile
from osgeo import osr
from werkzeug.datastructures import FileStorage


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

    def set_default_value_for(key, object_reference):
        obj = dict()

        value = object_reference.get(key)
        if isinstance(value, str):
            obj.update(dict(key=object_reference[key]))
        elif not value:
            obj.setdefault('key', key)
        else:
            obj.update(object_reference[key])

        object_reference[key] = obj

    if not mappings:
        raise TypeError('Invalid mappings')

    if not mappings.get('class_name'):
        mappings['class_name'] = 'label'

    if not mappings.get('geom'):
        if not mappings.get('latitude') and not mappings.get('longitude'):
            mappings['latitude'] = 'latitude'
            mappings['longitude'] = 'longitude'

    set_default_value_for('start_date', mappings)
    set_default_value_for('end_date', mappings)

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


def is_stream(entry):
    """Returns if the provided entry is readable as stream-like"""

    return isinstance(entry, IOBase) or \
           isinstance(entry, SpooledTemporaryFile) or \
           isinstance(entry, FileStorage)