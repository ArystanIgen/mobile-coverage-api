"""${message}

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


def upgrade():
    pre_upgrade()

    ${upgrades if upgrades else "pass"}
    post_upgrade()


def downgrade():
    pre_downgrade()

    ${downgrades if downgrades else "pass"}


    post_downgrade()


def pre_upgrade():
    pass


def post_upgrade():

    pass


def pre_downgrade():
    pass


def post_downgrade():
    pass