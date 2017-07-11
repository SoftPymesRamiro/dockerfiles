"""create user table

Revision ID: dc4015614b57
Revises: 
Create Date: 2016-05-11 17:24:20.844065

"""

# revision identifiers, used by Alembic.
revision = 'dc4015614b57'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import TINYINT


def upgrade():
    op.create_table(
        'aspnetusers',
        sa.Column('Id', sa.String(256), primary_key=True),
        sa.Column('FirstName', sa.String(200)),
        sa.Column('LastName', sa.String(200)),
        sa.Column('Email', sa.String(515)),
        sa.Column('PasswordHash', sa.String(2000)),
        sa.Column('SecurityStamp', sa.String(2000)),
        sa.Column('PhoneNumber', sa.String(2000)),
        sa.Column('UserName', sa.String(512)),
        sa.Column('Level', TINYINT),
        sa.Column('AccessFailedCount', sa.Integer),
        sa.Column('LastBranchId', sa.Integer),
        sa.Column('JoinDate', sa.DateTime),
        sa.Column('LockoutEndDateUtc', sa.DateTime),
        sa.Column('ProcessDate', sa.DateTime),
        sa.Column('EmailConfirmed', TINYINT),
        sa.Column('State', TINYINT),
        sa.Column('ChangePasswordOnNextLogin', TINYINT),
        sa.Column('AdminPOS', TINYINT),
        sa.Column('AdminChat', TINYINT),
        sa.Column('AdminSales', TINYINT),
        sa.Column('ImageId', sa.Integer),
        sa.Column('OldPassword', sa.String(2000)),
        sa.Column('Theme', sa.String(6))
    )
    pass


def downgrade():
    op.drop_table('aspnetusers')
