from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Length

class RegisterForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField("Repetir contraseña", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")

class ProductForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    descripcion = TextAreaField("Descripción")
    precio = FloatField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Guardar")

class CheckoutForm(FlaskForm):
    metodo = SelectField("Método de pago", choices=[("mercadopago", "Mercado Pago"), ("tarjeta", "Tarjeta (simulado)")], validators=[DataRequired()])
    submit = SubmitField("Pagar")
