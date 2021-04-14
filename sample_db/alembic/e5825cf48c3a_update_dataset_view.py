"""update dataset view.

Revision ID: e5825cf48c3a
Revises: e988feb44852
Create Date: 2021-04-09 10:35:12.789683

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm.session import Session
from lccs_db.models import LucClassificationSystem
from sample_db.models import Datasets, CollectMethod, Users, DatasetView

# revision identifiers, used by Alembic.
revision = 'e5825cf48c3a'
down_revision = 'e988feb44852'
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
                    "users.full_name AS user_name, collect_method.name AS collect_method, " \
                    "datasets.identifier, datasets.is_public " \
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