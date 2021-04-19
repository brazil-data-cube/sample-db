#
# This file is part of Sample Database Model.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Command-Line Interface for the Sample Database Model ."""
import json

import click
from bdc_db.cli import cli
from bdc_db.db import db as _db
from flask.cli import with_appcontext
from lccs_db.utils import get_mimetype
from sample_db_utils.factory import factory

import sample_db.utils as utils
from sample_db.models.observations import make_view_observation
from sample_db.models.users import Users


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
@click.option('--user_full_name', type=click.STRING, required=True, help='The user full name.')
@click.option('--observation_table_name', type=click.STRING, required=True, help='The observation table name.')
@click.option('--mappings', type=click.Path(exists=True, readable=True), required=True,
              help='Mappings used for location columns in file.')
@click.option('--classification_system_name', type=click.STRING, required=True, help='The classification system name.')
@click.option('--classification_system_version', type=click.STRING, required=True,
              help='The classification system version.')
@click.option('--observation_file', type=click.Path(exists=True), required=True,
              help='File path with the observation to insert')
@click.option('--obs_already_exist', is_flag=True, default=True, required=False)
def insert_observation(verbose, user_full_name, observation_table_name, mappings, classification_system_name,
                       classification_system_version, observation_file, obs_already_exist):
    """Insert a new observation."""
    print(mappings)
    if verbose:
        click.secho(f'Insert observation {observation_table_name}..', bold=True, fg='yellow')

    with open(mappings, "r") as m:
        mappings_json = json.load(m)

    if 'collect_date' not in mappings_json:
        mappings_json['collect_date'] = None

    observation_drive_type = get_mimetype(observation_file)

    driver_klass = factory.get(observation_drive_type)

    args = dict()

    args["mappings_json"] = mappings_json
    args["observation_file"] = observation_file
    args["obs_already_exist"] = obs_already_exist

    affected_rows = utils.create_observation(user_full_name=user_full_name,
                                             observation_table_name=observation_table_name,
                                             classification_system_name=classification_system_name,
                                             classification_system_version=classification_system_version,
                                             driver_type=driver_klass, **args)

    click.secho(f'Observations {observation_table_name} loaded!', bold=True, fg='green')

    if verbose:
        click.secho(f'\tNumber of observations inserted {affected_rows}.', bold=False, fg='black')


@sample.command()
@with_appcontext
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('--user_full_name', type=click.STRING, required=True, help='The user full name.')
@click.option('--observation_table_name', type=click.STRING, required=True, help='The observation table name.')
@click.option('--dataset_name', type=click.STRING, required=True, help='The dataset name.')
@click.option('--dataset_identifier', type=click.STRING, required=True, help='The dataset identifier.')
@click.option('--public/--no-public', required=True, default=False, help='Is this dataset public?.')
@click.option('--start_date', type=click.STRING, required=True, help='The dataset start date.')
@click.option('--end_date', type=click.STRING, required=True, help='The dataset end date.')
@click.option('--version', type=click.STRING, required=True, help='The dataset version.')
@click.option('--collect_method', type=click.STRING, required=True, help='The dataset collect method.')
@click.option('--description', type=click.STRING, required=True, help='The dataset description.')
@click.option('--classification_system_name', type=click.STRING, required=True, help='The classification system name.')
@click.option('--classification_system_version', type=click.STRING, required=True,
              help='The classification system version.')
@click.option('--metadata_file',  type=click.Path(exists=True, readable=True), help='A JSON metadata file.', required=False)
def create_dataset(verbose, user_full_name, observation_table_name, dataset_name, dataset_identifier, public,
                   start_date, end_date, version,
                   collect_method, description, classification_system_name, classification_system_version,
                   metadata_file):
    """Create a new dataset."""
    if verbose:
        click.secho(f'Create new dataset {dataset_name}..', bold=True, fg='yellow')

    metadata_json = None

    if metadata_file:
        with open(metadata_file, "r") as f:
            metadata_json = json.load(f)

    args = dict()

    args["name"] = dataset_name
    args["identifier"] = dataset_identifier
    args["is_public"] = public
    args["start_date"] = start_date
    args["end_date"] = end_date
    args["version"] = version
    args["description"] = description
    args["metadata_json"] = metadata_json

    utils.create_dataset(user_full_name=user_full_name, classification_system_name=classification_system_name,
                         classification_system_version=classification_system_version,
                         collect_method_name=collect_method,
                         observation_name=observation_table_name, **args)

    click.secho(f'Dataset {dataset_name} loaded!', bold=True, fg='green')

    if verbose:
        click.secho(f'\tFinished !.', bold=False, fg='black')


@sample.command()
@with_appcontext
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('--observation_table_name', type=click.STRING, help='A name of observation table.', required=True)
def create_view_observation(verbose, observation_table_name):
    """Create View observation."""
    if verbose:
        click.secho(f'Create view for {observation_table_name}..', bold=True, fg='yellow')
        
    table_name = f'{observation_table_name}_observations'

    obs_table_name = f'v_{table_name}'
    
    t = make_view_observation(table_name=table_name, obs_table_name=obs_table_name)

    if t:
        click.secho(f'View {obs_table_name} created.', bold=True, fg='black')
    else:
        click.secho(f"Error while creating view {obs_table_name}.", bold=True, fg='yellow')

    if verbose:
        click.secho('\tFinished!', bold=False, fg='black')


def main(as_module=False):
    """Run run the library module as a script."""
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    import sys
    cli.main(args=sys.argv[1:], prog_name="python -m sample_db" if as_module else None)
