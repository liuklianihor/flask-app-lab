from datetime import datetime
from app import db
from sqlalchemy import Enum, text

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(
        Enum('news', 'publication', 'tech', 'other', name='category_enum'),
        nullable=False,
        default='other'
    )

    is_active = db.Column(db.Boolean, nullable=False, server_default=text("1"))
    author = db.Column(db.String(20), nullable=False, server_default=text("'Anonymous'"))

    def __repr__(self):
        return f"<Post id={self.id} title={self.title!r}>"
