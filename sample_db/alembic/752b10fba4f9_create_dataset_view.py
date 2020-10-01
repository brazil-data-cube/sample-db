"""create dataset view.

Revision ID: 752b10fba4f9
Revises: e6ed17b95ec0
Create Date: 2020-05-06 18:06:52.673286

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm.session import Session
from lccs_db.models import LucClassificationSystem
from sample_db.models import Datasets, CollectMethod, Users, DatasetView



# revision identifiers, used by Alembic.
revision = '752b10fba4f9'
down_revision = 'e6ed17b95ec0'
branch_labels = ()
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    session = Session(bind=op.get_bind())
    session.execute("CREATE OR REPLACE VIEW {} AS " \
                    "SELECT datasets.created_at, datasets.updated_at, datasets.id, datasets.name, " \
                    "datasets.start_date, datasets.end_date, datasets.observation_table_name, " \
                    "datasets.midias_table_name, datasets.metadata_json, datasets.version, " \
                    "datasets.description, class_systems.name AS classification_system_name, " \
                    "users.full_name AS user_name, collect_method.name AS collect_method " \
                    "FROM {} AS datasets, {} AS class_systems, {} AS users, {} AS collect_method " \
                    "WHERE users.id = datasets.user_id " \
                    "AND class_systems.id = datasets.classification_system_id " \
                    "AND collect_method.id = datasets.collect_method_id;"
                    .format(DatasetView.__table__,
                            Datasets.__table__,
                            LucClassificationSystem.__table__,
                            Users.__table__,
                            CollectMethod.__table__)
                    )
    session.commit()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    session = Session(bind=op.get_bind())
    session.execute('DROP VIEW {};'.format(DatasetView.__table__))
    session.commit()
    # ### end Alembic commands ###
