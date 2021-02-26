#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Command-Line Interface for the Sample Database Model ."""
import click
import json
from bdc_db.cli import cli
from bdc_db.db import db as _db
from flask.cli import with_appcontext
from lccs_db.utils import get_mimetype
from sample_db_utils.factory import factory

from .models import Users
from .utils import create_dataset


@cli.group()
def sample():
    """Sample database commands."""


@sample.command()
@with_appcontext
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('--full_name', type=click.STRING, required=True, help='The user full name.')
@click.option('--email', type=click.STRING, required=True, help='The user email.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def insert_user(verbose, full_name, email, password):
    """Insert user."""
    if verbose:
        click.secho(f'Insert {full_name} user..', bold=True, fg='yellow')
    
    with _db.session.begin_nested():
        user = Users(full_name=full_name, email=email, password=password)
        
        _db.session.add(user)
    
    _db.session.commit()
    
    click.secho(f'User {full_name} insert!', bold=True, fg='green')


@sample.command()
@with_appcontext
@click.option('-v', '--verbose', is_flag=True, default=False)
# @click.option('--dataset_json', type=click.File('r'),
#               help='A JSON input file with all parameters (required if the others is omitted).',
#               required=False)
@click.option('--user_full_name', type=click.STRING, required=True, help='The user full name.')
@click.option('--observation_table_name', type=click.STRING, required=True, help='The observation table name.')
@click.option('--dataset_name', type=click.STRING, required=True, help='The dataset name.')
@click.option('--start_date', type=click.STRING, required=True, help='The dataset start date.')
@click.option('--end_date', type=click.STRING, required=True, help='The dataset end date.')
@click.option('--version', type=click.STRING, required=True, help='The dataset version.')
@click.option('--collect_method', type=click.STRING, required=True, help='The dataset collect method.')
@click.option('--description', type=click.STRING, required=True, help='The dataset description.')
@click.option('--mappings', type=click.Path(exists=True, readable=True), required=True, help='Mappings used for location columns in file.')
@click.option('--classification_system_name', type=click.STRING, required=True, help='The classification system name.')
@click.option('--classification_system_version', type=click.STRING, required=True,
              help='The classification system version.')
@click.option('--metadata_file',  type=click.Path(exists=True, readable=True), help='A JSON metadata file.', required=True)
@click.option('--observation_file', type=click.Path(exists=True), required=True,
              help='File path with the observation to insert')
@click.option('--obs_already_exist', is_flag=True, default=False)
def insert_dataset(verbose, user_full_name, observation_table_name, dataset_name, start_date, end_date,
                   version, collect_method, description, mappings, classification_system_name,
                   classification_system_version,
                   metadata_file, observation_file, obs_already_exist):
    """Create a new dataset."""
    if verbose:
        click.secho(f'Create new dataset {dataset_name}..', bold=True, fg='yellow')

    with open(mappings, "r") as m:
        mappings_json = json.load(m)
    
    if 'collect_date' not in mappings_json:
        mappings_json['collect_date'] = None
    
    with open(metadata_file, "r") as f:
        metadata_json = json.load(f)
    
    observation_drive_type = get_mimetype(observation_file)
    
    driver_klass = factory.get(observation_drive_type)
    
    dataset_info = dict()
    
    dataset_info["mappings_json"] = mappings_json
    dataset_info["observation_file"] = observation_file
    dataset_info["dataset_name"] = dataset_name
    dataset_info["collect_method"] = collect_method
    dataset_info["start_date"] = start_date
    dataset_info["end_date"] = end_date
    dataset_info["version"] = version
    dataset_info["description"] = description
    dataset_info["metadata_json"] = metadata_json
    dataset_info["obs_already_exist"] = obs_already_exist
    
    affected_rows = create_dataset(user_full_name=user_full_name,
                                   observation_table_name=observation_table_name,
                                   classification_system_name=classification_system_name,
                                   classification_system_version=classification_system_version,
                                   driver_type=driver_klass, **dataset_info)

    print("terminnou")


def main(as_module=False):
    """Run run the library module as a script."""
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    import sys
    cli.main(args=sys.argv[1:], prog_name="python -m sample_db" if as_module else None)
