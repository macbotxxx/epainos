import requests
import json
from django.conf import settings
from celery import shared_task
from config import celery_app
from celery.schedules import crontab

from .models import User


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def sendSMS(phone_number):
    """
    this obtain the auth token from geniopay using the
    login details from the user account creation such as 
    email and password .
    """
    try:
        SMS_TOKEN = settings.SMS_TOKEN
        sms_number = phone_number
        response = requests.post(
            url="https://app.smartsmssolutions.com/io/api/client/v1/sms/",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "Cookie": "PHPSESSID=3387ec366ff1642db51e96328fcc0c95",
            },
            data={
                "token": SMS_TOKEN,
                "sender": "epainos",
                "to": sms_number,
                "message": "Thank you for your valuable support. Your participation truly makes a difference!",
                "type": "0",
                "routing": "2",
            }, timeout=15)
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
