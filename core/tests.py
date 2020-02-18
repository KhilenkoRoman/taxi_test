from django.test import TestCase
from core.models import Rate
from datetime import datetime


class PaymentsTestCase(TestCase):
    def setUp(self):
        Rate.objects.bulk_create([
            Rate(start_date='2019-12-30', end_date='2020-01-02', buy_rate='24.45', sell_rate='24.95', currency='USD'),
            Rate(start_date='2020-01-03', end_date='2020-01-14', buy_rate='24.15', sell_rate='24.55', currency='USD'),
            Rate(start_date='2020-01-15', end_date='2020-01-17', buy_rate='24.45', sell_rate='24.95', currency='USD')
        ])

    def test_new_date(self):
        rate = Rate(start_date=datetime.strptime('10.02.2020', '%d.%m.%Y').date(), buy_rate='24.45', sell_rate='24.95', currency='USD')
        rate.save()

        rates = Rate.objects.all()
        self.assertEquals(rates.count(), 4, 'cant save new rate to db')
        self.assertEquals(rates[2].end_date, datetime.strptime('9.02.2020', '%d.%m.%Y').date(), 'wrong date in previous rate')

    def test_insert_rate(self):
        rate = Rate(start_date=datetime.strptime('10.01.2020', '%d.%m.%Y').date(), buy_rate='24.45', sell_rate='24.95', currency='USD')
        rate.save()

        rates = Rate.objects.all()
        self.assertEquals(rates.count(), 4, 'cant save new rate to db')
        self.assertEquals(rates[3].end_date, datetime.strptime('14.01.2020', '%d.%m.%Y').date(), 'wrong inserted end date')
        self.assertEquals(rates[1].end_date, datetime.strptime('09.01.2020', '%d.%m.%Y').date(), 'wrong end date in previous rate')

    def test_delete_rate(self):
        rates = Rate.objects.all()
        rates[1].delete()

        self.assertEquals(rates.count(), 2, 'cant save new rate to db')

        for r in rates:
            print(r.id, r.start_date, r.end_date)

        self.assertEquals(rates[0].end_date, datetime.strptime('14.01.2020', '%d.%m.%Y').date(), 'wrong date in previous rate')
