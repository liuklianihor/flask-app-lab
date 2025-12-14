from datetime import datetime
from app import db
from sqlalchemy import Enum, text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime, Text
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.users.models import User

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    category: Mapped[str] = mapped_column(
        Enum("news", "publication", "tech", "other", name="category_enum"),
        nullable=False,
        server_default="other",
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("1"))

    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f"<Post id={self.id} title={self.title!r}>"
    
class Tag(db.Model):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")
