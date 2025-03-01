"""['Add mentors']

Revision ID: 510c7beb3da9
Revises: 29fa2391d93a
Create Date: 2025-03-01 10:20:29.874635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '510c7beb3da9'
down_revision = '29fa2391d93a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mentor_skill',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('file_id', sa.Uuid(), nullable=True),
    sa.Column('mentor_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['mentor_id'], ['mentor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('mentor', sa.Column('contacts', sa.ARRAY(sa.String(), dimensions=1), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mentor', 'contacts')
    op.drop_table('mentor_skill')
    # ### end Alembic commands ###