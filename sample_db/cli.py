#
# This file is part of Sample Database Model.
# Copyright (C) 2019 INPE.
#
# Sample Database Model is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""SampleDB Command Line."""

import click

from lccs_db.cli import create_cli, create_app, init_db as lccs_init_db
from sample_db.models import make_observation, Users
from lccs_db.models import db as _db, LucClassificationSystem

from .config import Config

cli = create_cli(create_app=create_app)

@cli.command()
@click.pass_context
# @pass_config
def init_db(ctx: click.Context):

    """Initial Database."""
    ctx.forward(lccs_init_db)

    click.secho('Creating schema {}...'.format(Config.ACTIVITIES_SCHEMA), fg='green')
    click.secho('Creating EXTENSION postgis ...', fg='green')

    _db.session.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    _db.session.execute("CREATE SCHEMA IF NOT EXISTS {}".format(Config.ACTIVITIES_SCHEMA))
    _db.session.commit()

@cli.command()
@click.pass_context
@click.option('--ifile', type=click.File('r'),
              help='A csv input file for insert in table observation.',
              required=False)
# @pass_config
def insert_observation(ctx: click.Context, ifile):
    """Create table observation."""

    from sample_db_utils import PostgisAccessor, DriversFactory
    import pandas

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
        try:
            luc_system = LucClassificationSystem.get(name=df['name'])
        except BaseException:
            click.secho('Creating Classification System {}'.format(df['name']))
            luc_system = LucClassificationSystem()
            luc_system.authority_name = df['authority_name']
            luc_system.description = df['description']
            luc_system.name = df['name']
            luc_system.version = df['version']
            luc_system.save()

        driver = DriversFactory.make(df['driver'], df['observation'], storager)

        try:
            driver.user = user.id
            driver.system = luc_system

            driver.load_data_sets()
            driver.store(observation_table)
            print('Done {}'.format(driver.__class__.__name__))
        except BaseException as err:
            print(err)


def main(as_module=False):
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    import sys
    cli.main(args=sys.argv[1:], prog_name="python -m sample_db" if as_module else None)