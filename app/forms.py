from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp

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
    username = StringField("Ім'я/Email", validators=[DataRequired(message="Обов'язкове поле")])
    password = PasswordField("Пароль", validators=[DataRequired(message="Пароль обов'язковий"), Length(min=4, max=10, message="Від 4 до 10 символів")])
    remember = BooleanField("Запам'ятати мене")
