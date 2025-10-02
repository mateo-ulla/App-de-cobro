from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from .models import db, User, Product, Order, OrderItem, Payment
from .forms import RegisterForm, LoginForm, ProductForm, CheckoutForm
from flask_login import login_user, logout_user, login_required, current_user
from .utils import create_mp_preference
from config import Config

bp = Blueprint("main", __name__)

# home
@bp.route("/")
def index():
    productos = Product.query.all()
    return render_template("index.html", productos=productos)

# registro
@bp.route("/register", methods=["GET", "POST"])
def auth_register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email ya registrado", "warning")
            return redirect(url_for("main.auth_register"))
        u = User(nombre=form.nombre.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash("Cuenta creada, ahora inicia sesión", "success")
        return redirect(url_for("main.auth_login"))
    return render_template("register.html", form=form)

# Login
@bp.route("/login", methods=["GET", "POST"])
def auth_login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.check_password(form.password.data):
            login_user(u)
            flash("Bienvenido, " + u.nombre, "success")
            return redirect(url_for("main.index"))
        flash("Credenciales inválidas", "danger")
    return render_template("login.html", form=form)

# Logout
@bp.route("/logout")
@login_required
def auth_logout():
    logout_user()
    flash("Cerraste sesión", "info")
    return redirect(url_for("main.index"))

# CRUD productos 
@bp.route("/products")
def products():
    productos = Product.query.all()
    return render_template("products.html", productos=productos)

@bp.route("/product/new", methods=["GET", "POST"])
@login_required
def product_new():
    form = ProductForm()
    if form.validate_on_submit():
        p = Product(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            precio=form.precio.data,
            stock=form.stock.data
        )
        db.session.add(p)
        db.session.commit()
        flash("Producto creado", "success")
        return redirect(url_for("main.products"))
    return render_template("product_form.html", form=form)

@bp.route("/product/<int:pid>/edit", methods=["GET", "POST"])
@login_required
def product_edit(pid):
    p = Product.query.get_or_404(pid)
    form = ProductForm(obj=p)
    if form.validate_on_submit():
        p.nombre = form.nombre.data
        p.descripcion = form.descripcion.data
        p.precio = form.precio.data
        p.stock = form.stock.data
        db.session.commit()
        flash("Producto actualizado", "success")
        return redirect(url_for("main.products"))
    return render_template("product_form.html", form=form, producto=p)

@bp.route("/product/<int:pid>/delete", methods=["POST"])
@login_required
def product_delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash("Producto eliminado", "info")
    return redirect(url_for("main.products"))

# carrito 
@bp.route("/cart/add/<int:pid>")
def cart_add(pid):
    producto = Product.query.get_or_404(pid)
    cart = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session["cart"] = cart
    flash(f"{producto.nombre} agregado al carrito", "success")
    return redirect(url_for("main.index"))

@bp.route("/cart")
def cart_view():
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            items.append({"producto": p, "cantidad": qty, "subtotal": p.precio * qty})
            total += p.precio * qty
    return render_template("cart.html", items=items, total=total)

@bp.route("/cart/clear")
def cart_clear():
    session.pop("cart", None)
    flash("Carrito vaciado", "info")
    return redirect(url_for("main.index"))

# checkout
@bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = session.get("cart", {})
    if not cart:
        flash("El carrito está vacío", "warning")
        return redirect(url_for("main.index"))

    # calcular total y crear pedido en DB (estado pendiente)
    total = 0
    items_objs = []
    for pid, qty in cart.items():
        p = Product.query.get(int(pid))
        if p:
            total += p.precio * qty
            items_objs.append((p, qty))

    order = Order(user_id=current_user.id, estado="pendiente", total=total)
    db.session.add(order)
    db.session.commit()
    # crear items
    for p, qty in items_objs:
        oi = OrderItem(order_id=order.id, product_id=p.id, cantidad=qty, precio_unit=p.precio)
        db.session.add(oi)
    db.session.commit()

    form = CheckoutForm()
    form.metodo.data = "mercadopago"
    if form.validate_on_submit():
        metodo = form.metodo.data
        if metodo == "mercadopago":
            # crear preference y redirigir al checkout de Mercado Pago
            preference = create_mp_preference(order, order.items)
            init_point = preference["response"].get("init_point")
            # guardar payment provisional
            pay = Payment(order_id=order.id, metodo="mercadopago", status="created")
            db.session.add(pay)
            db.session.commit()
            # vaciar carrito
            session.pop("cart", None)
            return redirect(init_point)
        else:
            # metodo tarjeta, marca como pagado (simulado)
            pay = Payment(order_id=order.id, metodo="tarjeta_simulada", status="approved")
            order.estado = "pagado"
            db.session.add(pay)
            db.session.commit()
            session.pop("cart", None)
            flash("Pago con tarjeta simulado: pedido pagado", "success")
            return redirect(url_for("main.order_detail", oid=order.id))

    return render_template("checkout.html", order=order, form=form)

# callbacks MP 
@bp.route("/checkout/success")
def mp_success():
    external_ref = request.args.get("external_reference")
    payment_id = request.args.get("payment_id")
    # buscar order y marcar pagado
    if external_ref:
        order = Order.query.get(int(external_ref))
        if order:
            order.estado = "pagado"
            # actualizar payment
            pay = Payment.query.filter_by(order_id=order.id).first()
            if pay:
                pay.status = "approved"
                pay.mp_payment_id = payment_id
            else:
                pay = Payment(order_id=order.id, metodo="mercadopago", status="approved", mp_payment_id=payment_id)
                db.session.add(pay)
            db.session.commit()
            flash("Pago aprobado por Mercado Pago", "success")
            return redirect(url_for("main.order_detail", oid=order.id))
    flash("No se pudo procesar la respuesta de Mercado Pago", "danger")
    return redirect(url_for("main.index"))

@bp.route("/checkout/failure")
def mp_failure():
    flash("Pago rechazado / fallido", "danger")
    return redirect(url_for("main.index"))

@bp.route("/checkout/pending")
def mp_pending():
    flash("Pago pendiente", "warning")
    return redirect(url_for("main.index"))

# detalle de orden
@bp.route("/order/<int:oid>")
@login_required
def order_detail(oid):
    order = Order.query.get_or_404(oid)
    if order.user_id != current_user.id:
        flash("No autorizado", "danger")
        return redirect(url_for("main.index"))
    return render_template("order_detail.html", order=order)
