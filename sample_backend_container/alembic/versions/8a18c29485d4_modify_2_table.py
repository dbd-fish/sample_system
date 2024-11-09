"""Modify 2 table

Revision ID: 8a18c29485d4
Revises: 9495f1990b25
Create Date: 2024-11-09 14:34:02.330152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a18c29485d4'
down_revision: Union[str, None] = '9495f1990b25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample_table3',
    sa.Column('idsss', sa.Integer(), nullable=False),
    sa.Column('namesss', sa.String(), nullable=True),
    sa.Column('descriptionsss', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('idsss')
    )
    op.create_index(op.f('ix_sample_table3_idsss'), 'sample_table3', ['idsss'], unique=False)
    op.create_index(op.f('ix_sample_table3_namesss'), 'sample_table3', ['namesss'], unique=False)
    op.create_table('sample_table2',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('related_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['related_id'], ['sample_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sample_table2_id'), 'sample_table2', ['id'], unique=False)
    op.drop_index('ix_sample_table2rrrr_id', table_name='sample_table2rrrr')
    op.drop_table('sample_table2rrrr')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sample_table2rrrr',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('related_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['related_id'], ['sample_table.id'], name='sample_table2rrrr_related_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='sample_table2rrrr_pkey')
    )
    op.create_index('ix_sample_table2rrrr_id', 'sample_table2rrrr', ['id'], unique=False)
    op.drop_index(op.f('ix_sample_table2_id'), table_name='sample_table2')
    op.drop_table('sample_table2')
    op.drop_index(op.f('ix_sample_table3_namesss'), table_name='sample_table3')
    op.drop_index(op.f('ix_sample_table3_idsss'), table_name='sample_table3')
    op.drop_table('sample_table3')
    # ### end Alembic commands ###
