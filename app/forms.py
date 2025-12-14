from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, ValidationError, EqualTo
from sqlalchemy import select

class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[DataRequired(message="Ім'я обов'язкове"), Length(min=4, max=10, message="Від 4 до 10 символів")]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(message="Email обов'язковий"), Email(message="Невірний формат email")]
    )
    phone = StringField(
        "Телефон",
        validators=[Regexp(r'^\+380\d{9}$', message="Формат: +380XXXXXXXXX")]
    )
    subject = SelectField(
        "Тема",
        choices=[('general', 'Загальне'), ('support', 'Підтримка'), ('feedback', 'Відгук')],
        validators=[DataRequired(message="Оберіть тему")]
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[DataRequired(message="Повідомлення обов'язкове"), Length(max=500, message="Максимум 500 символів")]
    )

class LoginForm(FlaskForm):
    username = StringField("Ім'я/Email", validators=[DataRequired(message="Обов'язкове поле"), Length(min=3, max=120)])
    password = PasswordField("Пароль", validators=[DataRequired(message="Пароль обов'язковий"), Length(min=4, max=128, message="Від 4 до 128 символів")])
    remember = BooleanField("Запам'ятати мене")

class RegistrationForm(FlaskForm):
    username = StringField("Ім'я", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=128)])
    password2 = PasswordField("Повторіть пароль", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Зареєструватися")

    def validate_username(self, username):
        from app import db
        from app.users.models import User

        exists = db.session.scalar(select(User).where(User.username == username.data))
        if exists:
            raise ValidationError("Це ім'я вже зайняте.")

    def validate_email(self, email):
        from app import db
        from app.users.models import User

        exists = db.session.scalar(select(User).where(User.email == email.data))
        if exists:
            raise ValidationError("Цей email вже зареєстровано.")