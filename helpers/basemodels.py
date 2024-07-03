import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

NULL_AND_BLANK = {"null": True, "blank": True}


class BaseModel(models.Model):
    id = models.UUIDField(
        verbose_name=_("ID"),
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        help_text=_("The unique identifier of an object."),
    )

    created_date = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name=_("Created"),
        help_text=_(
            """Timestamp when the record was created. The date and time
            are displayed in the Timezone from where request is made.
            e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC"""
        ),
    )

    modified_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name=_("Updated"),
        **NULL_AND_BLANK,
        help_text=_(
            """Timestamp when the record was modified. The date and
            time are displayed in the Timezone from where request
            is made. e.g. 2019-14-29T00:15:09Z for April 29, 2019 0:15:09 UTC
            """
        ),
    )

    # Metadata
    class Meta:
        abstract = True
        verbose_name = _("Base Model")
        verbose_name_plural = _("Base Model")