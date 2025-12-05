"""Initial schema for publications and channels

Revision ID: 001
Revises: 
Create Date: 2025-11-17

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create publishing_channels table
    op.create_table(
        'publishing_channels',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('channel_type', sa.String(length=32), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('configuration', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('ix_publishing_channels_channel_type', 'publishing_channels', ['channel_type'])
    op.create_index('ix_publishing_channels_is_active', 'publishing_channels', ['is_active'])

    # Create publishing_subscribers table
    op.create_table(
        'publishing_subscribers',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('preferred_channels', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('topic_interests', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('frequency_settings', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('personalization_data', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('subscription_status', sa.String(length=32), nullable=False, server_default='active'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_publishing_subscribers_email', 'publishing_subscribers', ['email'])
    op.create_index('ix_publishing_subscribers_subscription_status', 'publishing_subscribers', ['subscription_status'])

    # Create publishing_publications table
    op.create_table(
        'publishing_publications',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('publication_type', sa.String(length=32), nullable=False),
        sa.Column('scheduled_time', sa.DateTime(), nullable=False),
        sa.Column('published_time', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False, server_default='scheduled'),
        sa.Column('content_ids', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('channels', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('channel_results', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('engagement_metrics', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('personalization_applied', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('error_details', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_publishing_publications_publication_type', 'publishing_publications', ['publication_type'])
    op.create_index('ix_publishing_publications_status', 'publishing_publications', ['status'])
    op.create_index('ix_publishing_publications_scheduled_time', 'publishing_publications', ['scheduled_time'])

    # Create publishing_templates table
    op.create_table(
        'publishing_templates',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('template_type', sa.String(length=32), nullable=False),
        sa.Column('content_structure', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('formatting_rules', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('branding_elements', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('variable_definitions', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('usage_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_publishing_templates_template_type', 'publishing_templates', ['template_type'])
    op.create_index('ix_publishing_templates_is_active', 'publishing_templates', ['is_active'])

    # Create publishing_analytics table
    op.create_table(
        'publishing_analytics',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('publication_id', sa.String(length=36), nullable=False),
        sa.Column('channel_type', sa.String(length=32), nullable=False),
        sa.Column('metric_type', sa.String(length=32), nullable=False),
        sa.Column('metric_value', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('recorded_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_publishing_analytics_publication_id', 'publishing_analytics', ['publication_id'])
    op.create_index('ix_publishing_analytics_channel_type', 'publishing_analytics', ['channel_type'])
    op.create_index('ix_publishing_analytics_metric_type', 'publishing_analytics', ['metric_type'])
    op.create_index('ix_publishing_analytics_recorded_at', 'publishing_analytics', ['recorded_at'])


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_table('publishing_analytics')
    op.drop_table('publishing_templates')
    op.drop_table('publishing_publications')
    op.drop_table('publishing_subscribers')
    op.drop_table('publishing_channels')

