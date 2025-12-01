from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.fields import DateTimeLocalField

class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=150)])
    content = TextAreaField("Текст", validators=[DataRequired()])
    enabled = BooleanField("Опубліковано")
    publish_date = DateTimeLocalField("Дата публікації", format='%Y-%m-%dT%H:%M', validators=[Optional()])
    category = SelectField(
        "Категорія",
        choices=[("news", "News"), ("publication", "Publication"), ("tech", "Tech"), ("other", "Other")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Save")
