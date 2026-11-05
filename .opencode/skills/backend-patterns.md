# backend-patterns: FastAPI + SQLAlchemy Project Standards

Quick reference for backend code in this project.

## Structure

```
app/
  api/v1/        # Routes (thin, no logic)
  services/      # Business logic
  models/        # SQLAlchemy ORM
  schemas/       # Pydantic request/response
  auth/          # JWT, password, RBAC deps
  ai/            # Langflow client, dialog, guardrails
```

## Endpoint pattern

```python
@router.get("/items/{id}", response_model=ItemResponse)
async def get_item(
    id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ItemResponse:
    service = ItemService(session)
    item = await service.get(id, user_id=user.id)
    if not item:
        raise HTTPException(404, "Item not found")
    return item
```

Routes call services. Services use session. Return Pydantic models or raise HTTPException.

## Service pattern

```python
class ItemService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, id: uuid.UUID, user_id: uuid.UUID) -> Item | None:
        result = await self.session.execute(
            select(Item).where(Item.id == id, Item.user_id == user_id)
        )
        return result.scalars().one_or_none()
```

## Model

```python
class Item(Base):
    __tablename__ = "items"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
```

## Schema

```python
class ItemResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime
    model_config = {"from_attributes": True}
```

## Error handling

- Validation → Pydantic (auto 422)
- Not found → HTTPException(404)
- Unauthorized → HTTPException(401)
- Forbidden → HTTPException(403)
- Business error → HTTPException(400, detail=RFC7807Problem)

## Config

Read via `app/core/config.py` Settings. Never `os.environ` elsewhere.

## Type hints

Everywhere. Use `result.scalars().one_or_none()` for SQLAlchemy (mypy inference better than `scalar_one_or_none()`).

## Async

All endpoints async. All DB calls async (`AsyncSession`, `await session.execute()`).
