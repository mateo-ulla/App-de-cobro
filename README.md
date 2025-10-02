# App de Cobro

App de ejemplo en Flask para simular compras y métodos de pago: tarjeta simulada y Mercado Pago (Checkout Pro).

## Características

- Registro, inicio de sesión y logout con Flask-Login.
- CRUD básico de productos (agregar/editar/eliminar).
- Carrito en sesión, creación de pedidos.
- Integración con Mercado Pago (crear preference y redirigir a checkout).
- Simulación de pago con tarjeta.
- Frontend responsivo con Bootstrap; plantillas Jinja2.
- Modelos con SQLAlchemy.
- Formularios con Flask-WTF.

## Requisitos

- Python 3.10+
- VS Code

## Instalación

```bash
git clone <tu-repo>.git
cd app-de-cobro
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
