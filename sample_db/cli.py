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

from .config import Config

cli = create_cli(create_app=create_app)

@cli.command()
@click.pass_context
# @pass_config
def init_db(ctx: click.Context):
    from lccs_db.models import db as _db
    """Initial Database."""
    ctx.forward(lccs_init_db)

    click.secho('Creating schema {}...'.format(Config.ACTIVITIES_SCHEMA), fg='green')
    click.secho('Creating EXTENSION postgis ...', fg='green')

    _db.session.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    _db.session.execute("CREATE SCHEMA IF NOT EXISTS {}".format(Config.ACTIVITIES_SCHEMA))
    _db.session.commit()
