from operator import attrgetter

from .models import Rental, Payment
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class ConciseTransaction:
    transaction_type = None
    status = None
    date = None
    parking_lot_name = None

    def __init__(self, input):
        if type(input) is Rental:
            self.transaction_type = 'Aluguel'
            self.status = input.get_rental_status_display()
            self.date = input.last_update
            self.parking_lot_name = input.parking_space.parking_lot.name
        else:
            self.transaction_type = 'Pagamento'
            self.status = input.get_status_display()
            self.date = input.last_update
            self.parking_lot_name = input.rental.parking_space.parking_lot.name


def set_range_month_filter(date):
    monthly_start_date = date + relativedelta(day=1)
    monthly_end_date = date + relativedelta(day=1, months=+1, days=-1)
    return [monthly_start_date, monthly_end_date]


def rentals_per_parking_lot_each_month(user):
    rentals = Rental.objects.filter(
        start_time__range=set_range_month_filter(timezone.now()),
        parking_space__parking_lot__owner__user=user
    )
    report = {}
    for rent in rentals:
        if rent.parking_space.parking_lot.name not in report:
            report[rent.parking_space.parking_lot.name] = 1
        else:
            report[rent.parking_space.parking_lot.name] += 1
    return report


def latest_transactions(user, max_amount):
    rentals = Rental.objects.filter(parking_space__parking_lot__owner__user=user)
    payments = Payment.objects.filter(rental__parking_space__parking_lot__owner__user=user)
    transactions = []
    for rental in rentals:
        transactions.append(ConciseTransaction(rental))
    for payment in payments:
        transactions.append(ConciseTransaction(payment))
    transactions = sorted(transactions, key=lambda transaction: transaction.date, reverse=True)
    return transactions[:max_amount]
