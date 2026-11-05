"""add ai_runs table

Revision ID: 0003
Revises: 0002
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_runs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        # ponytail: FK to conversations added in SPEC-005 migration when table exists
        sa.Column("conversation_id", UUID(as_uuid=True), nullable=True),
        sa.Column("flow_name", sa.String(255), nullable=False),
        sa.Column("variant", sa.String(20), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("tokens_in", sa.Integer(), nullable=True),
        sa.Column("tokens_out", sa.Integer(), nullable=True),
        sa.Column("fallback_used", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_ai_runs_flow_name", "ai_runs", ["flow_name"])
    op.create_index("ix_ai_runs_conversation_id", "ai_runs", ["conversation_id"])


def downgrade() -> None:
    op.drop_index("ix_ai_runs_conversation_id")
    op.drop_index("ix_ai_runs_flow_name")
    op.drop_table("ai_runs")
