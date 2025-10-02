from config import Config
import mercadopago

def create_mp_preference(order, items):
    sdk = mercadopago.SDK(Config.MP_ACCESS_TOKEN)
    preference_items = []
    for it in items:
        preference_items.append({
            "title": it.producto.nombre,
            "quantity": int(it.cantidad),
            "unit_price": float(it.precio_unit)
        })
    preference_data = {
        "items": preference_items,
        "external_reference": str(order.id),
        "back_urls": {
            "success": "http://localhost:5000/checkout/success",
            "failure": "http://localhost:5000/checkout/failure",
            "pending": "http://localhost:5000/checkout/pending"
        },
        "auto_return": "approved"
    }
    preference_response = sdk.preference().create(preference_data)
    return preference_response
