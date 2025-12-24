from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    op.create_table(
        'cloud_account',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('config_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'scan_run',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('tool', sa.String(), nullable=False),
        sa.Column('provider', sa.String(), nullable=True),
        sa.Column('scope_json', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('artifact_prefix', sa.String(), nullable=True),
        sa.Column('error', sa.Text(), nullable=True)
    )
    op.create_table(
        'artifact',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('scan_run_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_run.id')),
        sa.Column('tool', sa.String(), nullable=False),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('object_uri', sa.String(), nullable=False),
        sa.Column('sha256', sa.String(), nullable=True),
        sa.Column('size', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'resource',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('canonical_id', sa.String(), nullable=False, unique=True),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('account_id', sa.String(), nullable=True),
        sa.Column('tags_json', sa.JSON(), nullable=True),
        sa.Column('attributes_json', sa.JSON(), nullable=True),
        sa.Column('first_seen', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_seen', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'relationship',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('src_resource_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('resource.id')),
        sa.Column('dst_resource_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('resource.id')),
        sa.Column('rel_type', sa.String(), nullable=False),
        sa.Column('attributes_json', sa.JSON(), nullable=True),
        sa.Column('first_seen', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_seen', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'finding',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('scan_run_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('scan_run.id')),
        sa.Column('tool', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('rule_id', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('provider', sa.String(), nullable=True),
        sa.Column('service', sa.String(), nullable=True),
        sa.Column('region', sa.String(), nullable=True),
        sa.Column('canonical_resource_id', sa.String(), nullable=True),
        sa.Column('evidence_json', sa.JSON(), nullable=True),
        sa.Column('references_json', sa.JSON(), nullable=True),
        sa.Column('remediation_json', sa.JSON(), nullable=True),
        sa.Column('dedupe_key', sa.String(), nullable=True),
        sa.Column('first_seen', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('last_seen', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('status', sa.String(), nullable=False)
    )
    op.create_table(
        'alert',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('source_tool', sa.String(), nullable=False),
        sa.Column('provider', sa.String(), nullable=True),
        sa.Column('canonical_resource_id', sa.String(), nullable=True),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('event_json', sa.JSON(), nullable=True),
        sa.Column('occurred_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'ai_session',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('request_json', sa.JSON(), nullable=True),
        sa.Column('response_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'audit_log',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('actor', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('target_type', sa.String(), nullable=True),
        sa.Column('target_id', sa.String(), nullable=True),
        sa.Column('payload_json', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_table(
        'remediation_action',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('finding_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('finding.id')),
        sa.Column('action_type', sa.String(), nullable=False),
        sa.Column('plan_json', sa.JSON(), nullable=True),
        sa.Column('apply_status', sa.String(), nullable=True),
        sa.Column('applied_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('audit_log_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('audit_log.id'), nullable=True)
    )


def downgrade():
    op.drop_table('remediation_action')
    op.drop_table('audit_log')
    op.drop_table('ai_session')
    op.drop_table('alert')
    op.drop_table('finding')
    op.drop_table('relationship')
    op.drop_table('resource')
    op.drop_table('artifact')
    op.drop_table('scan_run')
    op.drop_table('cloud_account')
