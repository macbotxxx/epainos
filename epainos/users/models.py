import uuid
import random

from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from helpers.basemodels import BaseModel
from helpers.payment import FlutterWave

from .managers import UserManager


def generate_random_10_digits():
    return "".join([str(random.randint(0, 9)) for _ in range(10)])


class User(AbstractUser):
    """
    Default custom user model for epainos.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True, help_text=_("The unique identifier of the agent.")
    )
    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

class Contestant(BaseModel):
    contestant_id = models.CharField(
        verbose_name=_("Contestant ID"),
        max_length=10,
        null=True,
        blank=True,
        help_text=_("this hold the contestant id which will be automatically generated")
    )

    name = CharField(_("Name of Contestant"), blank=True, max_length=255)

    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=100,
        null=True,
        help_text=_("this hold the First Name of the contestant")
    )

    middle_name = models.CharField(
        verbose_name=_("Middle Name"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_("this hold the middle name of the contestant")
    )

    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=100,
        null=True,
        help_text=_("this hold the last name of the contestant ")
    )

    stage_name = models.CharField(
        verbose_name=_("Stage Name"),
        max_length=100,
        null=True,
        help_text=_("this hold the stage name of the contestant ")
    )

    contestant_inspiration = models.CharField(
        verbose_name=_("Contestant Inspiration"),
        max_length=50,
        null=True,
        help_text=_("this hold the contestant inspiration toward the competition")
    )

    number_of_vote = models.IntegerField(
        verbose_name=_("Contestant Inspiration"),
        default=0,
        null=True,
        blank=True,
        help_text=_("this displays the contestant vote count")
    )

    contestant_images = models.ManyToManyField(
        'ContestantImage',
    )

    contestant_videos =  models.JSONField(default=list)

    def save(self, *args, **kwargs) -> None:
        self.name = self.first_name + " " + self.middle_name + " " + self.last_name
        while not self.contestant_id:
            contestant_id = generate_random_10_digits()
            object_with_similar_ref = Contestant.objects.filter(contestant_id=contestant_id)
            if not object_with_similar_ref:
                self.contestant_id = contestant_id
        super().save(*args, **kwargs)

    class Meta:
        ordering = [
            "-created_date",
        ]
        verbose_name = _("Contestant Profile")
        verbose_name_plural = _("Contestant Profile")


class ContestantImage(BaseModel):
    image = models.ImageField(
        verbose_name=_("Contestant Images"),
        null=True,
        upload_to='images/',
        help_text=_("this hold the contestant image")
        )

    def __str__(self):
        return "Contestant Image"

    class Meta:
        ordering = [
            "-created_date",
        ]
        verbose_name = _("Contestant Image")
        verbose_name_plural = _("Contestant Image")


class ContestantVideo(BaseModel):
    video_file = models.FileField(
        verbose_name=_("Video File"),
        upload_to='videos/'
        )

    def __str__(self):
        return "Contestant Video"
    
    class Meta:
        ordering = [
            "-created_date",
        ]
        verbose_name = _("Contestant Video")
        verbose_name_plural = _("Contestant Video")


class Transactions(BaseModel):
    contestant = models.ForeignKey(
        Contestant, on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Contestant Account"),
        help_text=_("this hold the contestant account details")
    )

    amount_paid = models.DecimalField(
        verbose_name=_("Amount Paid"),
        max_digits=20,
        decimal_places=2,
        null=True,
        help_text=_("this hold the amount paid")
    )

    payment_ref = models.CharField(
        verbose_name=_("Transaction Ref"),
        max_length=100,
        null=True,
        help_text=_("this hold the Transaction Ref for the current transaction ")
    )

    voter_name = models.CharField(
        verbose_name=_("Voter Name"),
        max_length=100,
        null=True,
        help_text=_("this hold the Voter name of the contestant ")
    )

    voter_email = models.EmailField(
        verbose_name=_("Voter Email"),
        null=True,
        help_text=_("this hold the Voter email of the contestant ")
    )

    voter_phone_number = models.BigIntegerField(
        verbose_name=_("Voter phone Number"),
        null=True,
        blank=True,
        help_text=_("this displays the voter phone number")
    )

    settled = models.BooleanField(
        verbose_name=_("Payment Settled"),
        default=False,
        null=True
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=100,
        null=True,
        help_text=_("this hold the Voter name of the contestant ")
    )

    # def verify_payment_flutterwave(self):
    #     # paystack = PayStack()
    #     flutterwave = FlutterWave()
    #     status, result = flutterwave.verify_payment_flutterwave(self.payment_ref, self.amount_paid)
    #     if status == 'success':
    #         self.settled = True
    #         self.status = result['status']
    #         self.amount_paid = result['amount']

    #     self.save()

    #     return True

    class Meta:
        ordering = [
            "-created_date",
        ]
        verbose_name = _("Transactions")
        verbose_name_plural = _("Transactions")