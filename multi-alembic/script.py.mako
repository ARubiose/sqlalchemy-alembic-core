<%!
import re

from database.config import database
db_names = database.get_database_names(starts_with="database")

%>"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()

% for db_name in db_names:

def upgrade_${db_name}() -> None:
    ${context.get("%s_upgrades" % db_name, "pass")}


def downgrade_${db_name}() -> None:
    ${context.get("%s_downgrades" % db_name, "pass")}

% endfor
