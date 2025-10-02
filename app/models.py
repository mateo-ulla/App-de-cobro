from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    pedidos = db.relationship("Order", backref="usuario", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Producto {self.nombre}>"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    estado = db.Column(db.String(50), default="pendiente")  # pendiente, pagado, cancelado
    total = db.Column(db.Float, nullable=False, default=0.0)
    items = db.relationship("OrderItem", backref="pedido", lazy=True)
    payment = db.relationship("Payment", backref="pedido", uselist=False)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unit = db.Column(db.Float, nullable=False)

    producto = db.relationship("Product")

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    metodo = db.Column(db.String(50))  # 'mercadopago' o 'tarjeta_simulada'
    status = db.Column(db.String(50))
    mp_payment_id = db.Column(db.String(100))  # id devuelto por MP cuando aplique
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
