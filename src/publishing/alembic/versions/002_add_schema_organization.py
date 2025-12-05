"""Add schema organization for publishing module

Revision ID: 002
Revises: 001
Create Date: 2025-11-17

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create schemas
    op.execute(text('CREATE SCHEMA IF NOT EXISTS publishing_channels'))
    op.execute(text('CREATE SCHEMA IF NOT EXISTS publishing_publications'))
    op.execute(text('CREATE SCHEMA IF NOT EXISTS publishing_subscribers'))
    op.execute(text('CREATE SCHEMA IF NOT EXISTS publishing_templates'))
    op.execute(text('CREATE SCHEMA IF NOT EXISTS publishing_analytics'))
    
    # Get connection to check if old tables exist
    conn = op.get_bind()
    
    # Check if old tables exist by querying information_schema
    inspector = sa.inspect(conn)
    existing_tables = inspector.get_table_names(schema='public')
    
    # Helper function to check if table exists
    def table_exists(table_name):
        return table_name in existing_tables
    
    # Move publishing_channels -> publishing_channels.channels
    if table_exists('publishing_channels'):
        # Create new table in schema
        op.create_table(
            'channels',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.Column('channel_type', sa.String(length=32), nullable=False),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
            sa.Column('configuration', sa.JSON(), nullable=False, server_default='{}'),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('name'),
            schema='publishing_channels'
        )
        # Copy data
        op.execute(text("""
            INSERT INTO publishing_channels.channels 
            SELECT * FROM public.publishing_channels
        """))
        # Create indexes
        op.create_index('ix_channels_channel_type', 'channels', ['channel_type'], schema='publishing_channels')
        op.create_index('ix_channels_is_active', 'channels', ['is_active'], schema='publishing_channels')
        # Drop old table
        op.drop_table('publishing_channels')
    
    # Move publishing_publications -> publishing_publications.publications
    if table_exists('publishing_publications'):
        op.create_table(
            'publications',
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
            sa.PrimaryKeyConstraint('id'),
            schema='publishing_publications'
        )
        op.execute(text("""
            INSERT INTO publishing_publications.publications 
            SELECT * FROM public.publishing_publications
        """))
        op.create_index('ix_publications_publication_type', 'publications', ['publication_type'], schema='publishing_publications')
        op.create_index('ix_publications_status', 'publications', ['status'], schema='publishing_publications')
        op.create_index('ix_publications_scheduled_time', 'publications', ['scheduled_time'], schema='publishing_publications')
        op.drop_table('publishing_publications')
    
    # Move publishing_subscribers -> publishing_subscribers.subscribers
    if table_exists('publishing_subscribers'):
        op.create_table(
            'subscribers',
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
            sa.UniqueConstraint('email'),
            schema='publishing_subscribers'
        )
        op.execute(text("""
            INSERT INTO publishing_subscribers.subscribers 
            SELECT * FROM public.publishing_subscribers
        """))
        op.create_index('ix_subscribers_email', 'subscribers', ['email'], schema='publishing_subscribers')
        op.create_index('ix_subscribers_subscription_status', 'subscribers', ['subscription_status'], schema='publishing_subscribers')
        op.drop_table('publishing_subscribers')
    
    # Move publishing_templates -> publishing_templates.templates
    if table_exists('publishing_templates'):
        op.create_table(
            'templates',
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
            sa.PrimaryKeyConstraint('id'),
            schema='publishing_templates'
        )
        op.execute(text("""
            INSERT INTO publishing_templates.templates 
            SELECT * FROM public.publishing_templates
        """))
        op.create_index('ix_templates_template_type', 'templates', ['template_type'], schema='publishing_templates')
        op.create_index('ix_templates_is_active', 'templates', ['is_active'], schema='publishing_templates')
        op.drop_table('publishing_templates')
    
    # Move publishing_analytics -> publishing_analytics.analytics
    if table_exists('publishing_analytics'):
        op.create_table(
            'analytics',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('publication_id', sa.String(length=36), nullable=False),
            sa.Column('channel_type', sa.String(length=32), nullable=False),
            sa.Column('metric_type', sa.String(length=32), nullable=False),
            sa.Column('metric_value', sa.Float(), nullable=False, server_default='0.0'),
            sa.Column('user_id', sa.String(length=36), nullable=True),
            sa.Column('metadata_json', sa.JSON(), nullable=False, server_default='{}'),
            sa.Column('recorded_at', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            schema='publishing_analytics'
        )
        op.execute(text("""
            INSERT INTO publishing_analytics.analytics 
            SELECT * FROM public.publishing_analytics
        """))
        op.create_index('ix_analytics_publication_id', 'analytics', ['publication_id'], schema='publishing_analytics')
        op.create_index('ix_analytics_channel_type', 'analytics', ['channel_type'], schema='publishing_analytics')
        op.create_index('ix_analytics_metric_type', 'analytics', ['metric_type'], schema='publishing_analytics')
        op.create_index('ix_analytics_recorded_at', 'analytics', ['recorded_at'], schema='publishing_analytics')
        op.drop_table('publishing_analytics')


def downgrade() -> None:
    # Reverse the migration: move tables back to public schema with old names
    
    # Get connection
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # Helper function to check if table exists in schema
    def table_exists_in_schema(schema_name, table_name):
        try:
            tables = inspector.get_table_names(schema=schema_name)
            return table_name in tables
        except:
            return False
    
    # Move channels back to public.publishing_channels
    if table_exists_in_schema('publishing_channels', 'channels'):
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
        op.execute(text("""
            INSERT INTO public.publishing_channels 
            SELECT * FROM publishing_channels.channels
        """))
        op.create_index('ix_publishing_channels_channel_type', 'publishing_channels', ['channel_type'])
        op.create_index('ix_publishing_channels_is_active', 'publishing_channels', ['is_active'])
        op.drop_table('channels', schema='publishing_channels')
    
    # Move publications back
    if table_exists_in_schema('publishing_publications', 'publications'):
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
        op.execute(text("""
            INSERT INTO public.publishing_publications 
            SELECT * FROM publishing_publications.publications
        """))
        op.create_index('ix_publishing_publications_publication_type', 'publishing_publications', ['publication_type'])
        op.create_index('ix_publishing_publications_status', 'publishing_publications', ['status'])
        op.create_index('ix_publishing_publications_scheduled_time', 'publishing_publications', ['scheduled_time'])
        op.drop_table('publications', schema='publishing_publications')
    
    # Move subscribers back
    if table_exists_in_schema('publishing_subscribers', 'subscribers'):
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
        op.execute(text("""
            INSERT INTO public.publishing_subscribers 
            SELECT * FROM publishing_subscribers.subscribers
        """))
        op.create_index('ix_publishing_subscribers_email', 'publishing_subscribers', ['email'])
        op.create_index('ix_publishing_subscribers_subscription_status', 'publishing_subscribers', ['subscription_status'])
        op.drop_table('subscribers', schema='publishing_subscribers')
    
    # Move templates back
    if table_exists_in_schema('publishing_templates', 'templates'):
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
        op.execute(text("""
            INSERT INTO public.publishing_templates 
            SELECT * FROM publishing_templates.templates
        """))
        op.create_index('ix_publishing_templates_template_type', 'publishing_templates', ['template_type'])
        op.create_index('ix_publishing_templates_is_active', 'publishing_templates', ['is_active'])
        op.drop_table('templates', schema='publishing_templates')
    
    # Move analytics back
    if table_exists_in_schema('publishing_analytics', 'analytics'):
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
        op.execute(text("""
            INSERT INTO public.publishing_analytics 
            SELECT * FROM publishing_analytics.analytics
        """))
        op.create_index('ix_publishing_analytics_publication_id', 'publishing_analytics', ['publication_id'])
        op.create_index('ix_publishing_analytics_channel_type', 'publishing_analytics', ['channel_type'])
        op.create_index('ix_publishing_analytics_metric_type', 'publishing_analytics', ['metric_type'])
        op.create_index('ix_publishing_analytics_recorded_at', 'publishing_analytics', ['recorded_at'])
        op.drop_table('analytics', schema='publishing_analytics')
    
    # Drop schemas
    op.execute(text('DROP SCHEMA IF EXISTS publishing_channels'))
    op.execute(text('DROP SCHEMA IF EXISTS publishing_publications'))
    op.execute(text('DROP SCHEMA IF EXISTS publishing_subscribers'))
    op.execute(text('DROP SCHEMA IF EXISTS publishing_templates'))
    op.execute(text('DROP SCHEMA IF EXISTS publishing_analytics'))

