import os
from app import create_app, db
from app.models import User, Product

# crear la app y contexto
app = create_app()

with app.app_context():
    # reiniciar la base de datos
    db.drop_all()
    db.create_all()

    # usuario de prueba
    user = User(nombre="Admin", email="admin@tienda.com")
    user.set_password("123456") 
    db.session.add(user)

    productos = [
        Product(
            nombre="iPhone 14 Pro",
            descripcion="Apple iPhone 14 Pro 128GB - Pantalla OLED Super Retina XDR",
            precio=1399.99,
            stock=10
        ),
        Product(
            nombre="Samsung Galaxy S23",
            descripcion="Samsung Galaxy S23 256GB - Cámara triple, Snapdragon 8 Gen 2",
            precio=1199.99,
            stock=15
        ),
        Product(
            nombre="Motorola Edge 40",
            descripcion="Motorola Edge 40 256GB - Pantalla OLED 6.6'', carga rápida 68W",
            precio=699.99,
            stock=20
        ),
        Product(
            nombre="Xiaomi 13 Pro",
            descripcion="Xiaomi 13 Pro 256GB - Snapdragon 8 Gen 2, Cámara Leica",
            precio=899.99,
            stock=12
        ),
        Product(
            nombre="iPhone 13",
            descripcion="Apple iPhone 13 128GB - Pantalla OLED, procesador A15 Bionic",
            precio=999.99,
            stock=18
        ),
        Product(
            nombre="Samsung Galaxy A54",
            descripcion="Samsung Galaxy A54 128GB - Excelente gama media con pantalla Super AMOLED",
            precio=449.99,
            stock=30
        ),
        Product(
            nombre="Motorola Moto G73",
            descripcion="Motorola Moto G73 128GB - Pantalla FHD+ de 6.5'', batería de 5000mAh",
            precio=299.99,
            stock=25
        ),
        Product(
            nombre="Xiaomi Redmi Note 12",
            descripcion="Xiaomi Redmi Note 12 128GB - Cámara de 50MP, pantalla AMOLED 120Hz",
            precio=249.99,
            stock=40
        ),
    ]

    db.session.add_all(productos)
    db.session.commit()
