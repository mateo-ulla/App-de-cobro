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
            "success": "https://127.0.0.1:5000/checkout/success",
            "failure": "https://127.0.0.1:5000/checkout/failure",
            "pending": "https://127.0.0.1:5000/checkout/pending"
        },
        "auto_return": "approved"
    }
    print("[MP preference_data]", preference_data)
    preference_response = sdk.preference().create(preference_data)
    return preference_response
