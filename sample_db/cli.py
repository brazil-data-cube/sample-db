#
# This file is part of SAMPLE-DB.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Command-Line Interface for the Sample Database Model ."""
import json

import click
from bdc_db.cli import cli
from flask.cli import with_appcontext
from lccs_db.utils import get_mimetype

import sample_db.utils as utils


@cli.group()
def sample():
    """Sample database commands."""


@sample.command()
@with_appcontext
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('--user_id', type=click.INT, required=True, help='The user id.')
@click.option('--name', type=click.STRING, required=True, help='The dataset name.')
@click.option('--version', type=click.STRING, required=True, help='The dataset version.')
@click.option('--mappings', type=click.Path(exists=True, readable=True), required=False,
              default=None,help='Mappings used for location columns in file.')
@click.option('--dataset_file', type=click.Path(exists=True), required=True,
              help='File path with the data to insert')
def insert_dataset_data(verbose, name, user_id, version, dataset_file, mappings):
    """Insert data into a dataset table."""
    if verbose:
        click.secho(f'Insert data into dataset {name}..', bold=True, fg='yellow')

    if mappings is not None:
        with open(mappings, "r") as m:
            mappings_json = json.load(m)

        if 'collect_date' not in mappings_json:
            mappings_json['collect_date'] = None

    mimetype = get_mimetype(dataset_file)

    args = dict()

    args["mappings_json"] = mappings_json

    ds, affected_rows = utils.add_dataset_data_file(user_id=user_id,
                                                    dataset_name=name,
                                                    dataset_version=version,
                                                    dataset_file=dataset_file,
                                                    mimetype=mimetype, **args)

    if affected_rows is not None:
        click.secho(f'Data loaded into dataset {name} !', bold=True, fg='green')

        if verbose:
            click.secho(f'\tNumber of data inserted {affected_rows}.', bold=False, fg='black')

    else:
        click.secho(f'Error while inserting data into dataset {name}', bold=True, fg='green')


@sample.command()
@with_appcontext
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('--name', type=click.STRING, required=True, help='The dataset name.')
@click.option('--title', type=click.STRING, required=True, help='The dataset identifier.')
@click.option('--version', type=click.STRING, required=True, help='The dataset version.')
@click.option('--version_predecessor', type=click.STRING, required=False, help='The dataset version predecessor.')
@click.option('--version_successor', type=click.STRING, required=False, help='The dataset version successor.')
@click.option('--description', type=click.STRING, required=True, help='The dataset description.')
@click.option('--start_date', type=click.STRING, required=True, help='The dataset start date.')
@click.option('--end_date', type=click.STRING, required=True, help='The dataset end date.')
@click.option('--public/--no-public', required=True, default=False, help='Is this dataset public?.')
@click.option('--collect_method_id', type=click.INT, required=True, help='The dataset collect method id.')
@click.option('--classification_system_id', type=click.INT, required=True, help='The classification system id.')
@click.option('--metadata_file', type=click.Path(exists=True, readable=True), help='A JSON metadata file.',
              required=False)
@click.option('--user_id', type=click.INT, required=True, help='The user id.')
def create_dataset(verbose, user_id, name, title, public,
                   start_date, end_date, version, version_predecessor, version_successor,
                   collect_method_id, description, classification_system_id,
                   metadata_file):
    """Create a new dataset."""
    if verbose:
        click.secho(f'Create new dataset {name}..', bold=True, fg='yellow')

    metadata_json = None

    if metadata_file:
        with open(metadata_file, "r") as f:
            metadata_json = json.load(f)

    args = dict()

    args["name"] = name
    args["title"] = title
    args["is_public"] = public
    args["start_date"] = start_date
    args["end_date"] = end_date
    args["version"] = version
    args["description"] = description
    args["metadata_json"] = metadata_json

    if version_predecessor:
        args["version_predecessor"] = version_predecessor
    if version_successor:
        args["version_successor"] = version_successor

    utils.create_dataset(user_id=user_id,
                         classification_system_id=classification_system_id,
                         collect_method_id=collect_method_id,
                         dataset_name=name, **args)

    click.secho(f'Dataset {name} created!', bold=True, fg='green')

    if verbose:
        click.secho(f'\tFinished !.', bold=False, fg='black')


@sample.command()
@with_appcontext
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('--name', type=click.STRING, required=True, help='The dataset name.')
@click.option('--version', type=click.STRING, required=True, help='The dataset version.')
def create_view_dataset_table(verbose, name, version):
    """Create View dataset-table."""
    if verbose:
        click.secho(f'Create view for {name}..', bold=True, fg='yellow')

        utils.create_view(dataset_name=name, dataset_version=version)

        click.secho(f'View of dataset {name} created.', bold=True, fg='black')

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        utils.create_view(dataset_name=name, dataset_version=version)

        click.secho(f'View of dataset {name} created.', bold=True, fg='black')


@sample.command()
@with_appcontext
@click.option('-v', '--verbose', is_flag=True, default=False)
@click.option('--name', type=click.STRING, required=True, help='The dataset name.')
@click.option('--version', type=click.STRING, required=True, help='The dataset version.')
def delete_dataset(verbose, name, version):
    """Delete a specific dataset and dataset-table."""
    if verbose:
        click.secho(f'Deleting the dataset {name}..', bold=True, fg='yellow')

        utils.delete_dataset_table(dataset_name=name, dataset_version=version)

        click.secho('\tFinished!', bold=False, fg='black')

    else:
        utils.delete_dataset_table(dataset_name=name, dataset_version=version)

        click.secho(f'Dataset {name} deleted!', bold=False, fg='yellow')


def main(as_module=False):
    """Run run the library module as a script."""
    # TODO omit sys.argv once https://github.com/pallets/click/issues/536 is fixed
    import sys
    cli.main(args=sys.argv[1:], prog_name="python -m sample_db" if as_module else None)
