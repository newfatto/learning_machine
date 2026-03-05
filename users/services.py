import stripe
from config.settings import STRIPE_API_KEY,DATABASES

stripe.api_key = STRIPE_API_KEY

def create_stripe_product(*, name: str) -> stripe.Product:
    """Создаёт продукт в stripe"""
    return stripe.Product.create(name=name)


def create_stripe_price(*, amount: int, product_id: str) -> stripe.Price:
    """Создаёт цену в stripe"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount*100,
        product=product_id,
    )

def create_stripe_session(*, price_id: str, success_url: str, cancel_url: str) -> stripe.checkout.Session:
    """
    Создать Checkout Session в Stripe.
    """

    return stripe.checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )