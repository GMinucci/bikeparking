from parking.models import Payment
from pagseguro.api import PagSeguroItem, PagSeguroApi
from decimal import Decimal

payment_status_pagseguro = (
    (1, 'open'),
    (2, 'under_review'),
    (3, 'confirmed'),
    (7, 'refused'),
)

payment_type_pagseguro = (
    (1, 'credit_card'),
    (2, 'billet'),
    (3, 'online_debit'),
    (4, 'pagseguro_balance'),
    (5, 'oi_paggo'),
    (6, 'account_deposit'),
)


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
        payment.redirect_url = data.get('redirect_url')
    payment.status_code = data.get('status_code')
    payment.save()
    return payment


def pagseguro_load_signal(sender, transaction, **kwargs):
    payment_reference = transaction.get('reference')
    payment = Payment.objects.get(id=payment_reference)
    payment.date = transaction.get('date')
    payment.status = dict(payment_status_pagseguro)[int(transaction.get('status'))]
    if transaction.get('paymentMethod', False):
        payment.payment_type = dict(payment_status_pagseguro)[int(transaction.get('paymentMethod').get('type'))]
    payment.save()
