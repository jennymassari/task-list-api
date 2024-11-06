from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from ..db import db


class Task(db.Model):
    
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)
