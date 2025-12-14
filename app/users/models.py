from app import db
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, Text
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.posts.models import Post

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")