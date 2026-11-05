# alembic-flow: Migration Workflow

Manual migration creation (autogenerate had Docker permission issues).

## Create migration

```bash
cd backend
# Generate stub
alembic revision -m "add_table_name"
# Edit migrations/versions/XXXX_add_table_name.py
# Write upgrade() and downgrade() by hand
```

## Migration template

```python
"""add items table

Revision ID: 0003
Revises: 0002
"""
from typing import Sequence
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = '0003'
down_revision = '0002'

def upgrade() -> None:
    op.create_table(
        'items',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('ix_items_user_id', 'items', ['user_id'])

def downgrade() -> None:
    op.drop_index('ix_items_user_id')
    op.drop_table('items')
```

## Apply

```bash
make migrate  # or: cd backend && alembic upgrade head
```

## Verify

```bash
# Check applied
docker exec learnfl0w-backend alembic current

# Check tables
docker exec learnfl0w-db psql -U learnfl0w -c "\d items"
```

## Rules

- Never edit applied migrations
- ForeignKey constraints explicit
- Indexes for foreign keys and common queries
- downgrade() must undo upgrade()
- Run in Docker to match prod environment
