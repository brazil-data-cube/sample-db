#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Command Line."""
from json import loads as json_load

import click
from lccs_db.cli import create_app, create_cli
from lccs_db.cli import init_db as lccs_init_db
from lccs_db.models import LucClassificationSystem
from lccs_db.models import db as _db

from sample_db.models import (CollectMethod, Datasets, Users, make_observation,
                              make_view_observation)

from .config import Config


def verify_class_system_exist(class_system_name):
    """Verify if a classification system exist."""
    try:
        class_system = LucClassificationSystem.get(name=class_system_name)
        return class_system
    except BaseException:
        return None

cli = create_cli(create_app=create_app)


@cli.command()
@click.pass_context
# @pass_config
def init_db(ctx: click.Context):
    """Initialize Database."""
    ctx.forward(lccs_init_db)

    click.secho('Creating schema {}...'.format(Config.SAMPLEDB_ACTIVITIES_SCHEMA), fg='green')
    click.secho('Creating EXTENSION postgis ...', fg='green')

    _db.session.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    _db.session.execute("CREATE SCHEMA IF NOT EXISTS {}".format(Config.SAMPLEDB_ACTIVITIES_SCHEMA))
    _db.session.commit()

@cli.command()
@click.pass_context
@click.option('--ifile', type=click.File('r'),
              help='A csv input file for insert in table observation.',
              required=False)
# @pass_config
def insert_observation(ctx: click.Context, ifile):
    """Create table observation."""
    import pandas
    from sample_db_utils import DriversFactory, PostgisAccessor

    dataframe = pandas.read_csv(ifile)

    for index, df in dataframe.iterrows():

        observation_name = df['observation_table_name']

        observation_table = make_observation(table_name=observation_name, create=True)

        _db.session.commit()

        storager = PostgisAccessor()

        click.secho('table {} create'.format(observation_name))

        try:
            user = Users.get(full_name=df['user'])
        except BaseException:
            print("User does not exist!")
            return

        luc_system = verify_class_system_exist(df['name'])

        if luc_system:
            print("Classification System {} already exist".format(luc_system.name))
        else:
            click.secho('Creating Classification System {}'.format(df['name']))
            luc_system = LucClassificationSystem()
            luc_system.authority_name = df['authority_name']
            luc_system.description = df['description']
            luc_system.name = df['name']
            luc_system.version = df['version']
            luc_system.save()

            print("Classification System {} Insert".format(luc_system.name))

        driver = DriversFactory.make(df['driver'], df['observation'], storager)

        try:
            driver.user = user.id
            driver.system = luc_system

            driver.load_data_sets()
            driver.store(observation_table)
            print('Done {}'.format(driver.__class__.__name__))
        except BaseException as err:
            print(err)

@cli.command()
@click.pass_context
@click.option('--ifile', type=click.File('r'),
              help='A csv input file for insert dataset.',
              required=False)
def insert_dataset(ctx: click.Context, ifile):
    """Insert a dataset giving a csv file."""
    import pandas

    dataframe = pandas.read_csv(ifile)

    for index, df in dataframe.iterrows():
        try:
            classification_system = LucClassificationSystem.get(name=df['classification_system'])
            user = Users.get(full_name=df['user'])
            collect_method = CollectMethod.get(name=df['collect_method'])
        except BaseException:
            print("Classification System does not exist!")
            return

        metadata_json = df['metadata_json']

        with open(metadata_json) as json_data:
            file = json_load(json_data.read())

            dataset = Datasets(classification_system_id=classification_system.id,
                               user_id=user.id,
                               name=df['name'],
                               start_date=df['start_date'],
                               end_date=df['end_date'],
                               collect_method_id=collect_method.id,
                               observation_table_name=df['obs_table_name'],
                               version=df['version'],
                               
                               description=df['description'],
                               metadata_json=file)

            _db.session.add(dataset)
            _db.session.commit()

        click.echo("DataSet Adicionado {}".format(df['name']))


@cli.command()
@click.pass_context
@click.option('--name', type=click.STRING,
              help='A name of table observation.',
              required=False)
def create_view_observation(ctx: click.Context, name):
    """Create View observation."""
    obs_table_name = "v_" + name

    t = make_view_observation(table_name=name, obs_table_name=obs_table_name)

    if t:
        click.echo("View {} Create".format(obs_table_name))
    else:
        click.echo("Error while creating view {}".format(obs_table_name))


def main(as_module=False):
    """Run run the library module as a script."""
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    import sys
    cli.main(args=sys.argv[1:], prog_name="python -m sample_db" if as_module else None)
