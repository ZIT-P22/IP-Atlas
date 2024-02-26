"""Initial migration.

Revision ID: f8403cadc21b
Revises: 
Create Date: 2024-02-24 00:06:33.976554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8403cadc21b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('audit_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('action_type', sa.String(), nullable=False),
    sa.Column('table_name', sa.String(), nullable=False),
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discovered_devices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mac_address', sa.String(), nullable=True),
    sa.Column('ipv4', sa.String(), nullable=False),
    sa.Column('ipv6', sa.String(), nullable=True),
    sa.Column('hostname', sa.String(), nullable=True),
    sa.Column('first_seen', sa.DateTime(), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('blacklist', sa.Boolean(), nullable=True),
    sa.Column('used', sa.Boolean(), nullable=True),
    sa.Column('vendor', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('discovered_devices', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_discovered_devices_hostname'), ['hostname'], unique=False)
        batch_op.create_index(batch_op.f('ix_discovered_devices_ipv4'), ['ipv4'], unique=False)
        batch_op.create_index(batch_op.f('ix_discovered_devices_ipv6'), ['ipv6'], unique=False)
        batch_op.create_index(batch_op.f('ix_discovered_devices_mac_address'), ['mac_address'], unique=False)

    op.create_table('hosts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hostname', sa.String(), nullable=False),
    sa.Column('ipv4', sa.String(), nullable=False),
    sa.Column('ipv6', sa.String(), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('hosts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_hosts_hostname'), ['hostname'], unique=True)
        batch_op.create_index(batch_op.f('ix_hosts_ipv4'), ['ipv4'], unique=False)
        batch_op.create_index(batch_op.f('ix_hosts_ipv6'), ['ipv6'], unique=False)

    op.create_table('statistics',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('stat_key', sa.String(), nullable=False),
    sa.Column('stat_value', sa.Integer(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('statistics', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_statistics_stat_key'), ['stat_key'], unique=False)

    op.create_table('tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tag_name', sa.String(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tags_tag_name'), ['tag_name'], unique=True)

    op.create_table('host_tags',
    sa.Column('host_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('host_id', 'tag_id')
    )
    op.create_table('ports',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=True),
    sa.Column('port_number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('portsFB',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('host_id', sa.Integer(), nullable=True),
    sa.Column('portFB_number', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('portsFB')
    op.drop_table('ports')
    op.drop_table('host_tags')
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tags_tag_name'))

    op.drop_table('tags')
    with op.batch_alter_table('statistics', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_statistics_stat_key'))

    op.drop_table('statistics')
    with op.batch_alter_table('hosts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_hosts_ipv6'))
        batch_op.drop_index(batch_op.f('ix_hosts_ipv4'))
        batch_op.drop_index(batch_op.f('ix_hosts_hostname'))

    op.drop_table('hosts')
    with op.batch_alter_table('discovered_devices', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_discovered_devices_mac_address'))
        batch_op.drop_index(batch_op.f('ix_discovered_devices_ipv6'))
        batch_op.drop_index(batch_op.f('ix_discovered_devices_ipv4'))
        batch_op.drop_index(batch_op.f('ix_discovered_devices_hostname'))

    op.drop_table('discovered_devices')
    op.drop_table('audit_logs')
    # ### end Alembic commands ###