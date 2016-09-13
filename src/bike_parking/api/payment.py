from parking.models import Payment
from pagseguro.api import PagSeguroItem, PagSeguroApi
from decimal import Decimal


def create_payment_attempt(rental):
    payment = Payment.create(rental)
    payment.save()
    return create_pagseguro_cart(payment)


def create_pagseguro_item(rental):
    two_decimals = Decimal(10) ** -2
    return PagSeguroItem(
        id=rental.id,
        description=rental.get_rental_type_display(),
        quantity=1,
        amount=rental.total.quantize(two_decimals))


def create_pagseguro_cart(payment):
    cart = PagSeguroApi(reference=payment.id)
    cart.add_item(create_pagseguro_item(payment.rental))
    data = cart.checkout()
    if data.get('success', False):
        payment.code = data.get('code')
        payment.date = data.get('date')
        payment.redirect_url = data.get('redirect_url')
    payment.status_code = data.get('status_code')
    payment.save()
    return payment


def pagseguro_load_signal(sender, transaction, **kwargs):
    print transaction
