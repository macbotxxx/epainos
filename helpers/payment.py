import json
import requests

from django.conf import settings
from django.core.mail import send_mail


class FlutterWave:
    if settings.TEST_PAYMENT:
        FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY_TEST
    else:
        FLUTTERWAVE_SECRET_KEY = settings.FLUTTERWAVE_SECRET_KEY

    base_url = 'https://api.flutterwave.com/v3/transactions/'

    def verify_payment_flutterwave(self, payment_ref, *args, **kwargs):
        path = 'verify_by_reference?tx_ref='f"{payment_ref}"
       
        headers = {
            "Authorization": f"Bearer {self.FLUTTERWAVE_SECRET_KEY}",
            'Content-Type': 'application/json',
        }

        url = self.base_url + path
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            send_mail(
                'Response',
                f'{response_data}',
                f"{settings.EMAIL_HOST_USER}",
                ['assanamamichael@gmail.com'],
                fail_silently=False,
            )
            return response_data['status'],response_data['data']
        response_data = response.json()
        send_mail(
                'Response',
                f'{response_data}',
                f"{settings.EMAIL_HOST_USER}" ,
                ['assanamamichael@gmail.com'],
                fail_silently=False,
            )
        return response_data['status'],response_data['message']
