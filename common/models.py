import uuid

from django.db.models import DateTimeField, Model, UUIDField
from django.utils.translation import gettext_lazy as _


class UUIDV4Model(Model):
    id = UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("UUID v4 primary key"),
    )

    class Meta:
        abstract = True


class TimestampedModel(Model):
    created_at = DateTimeField(
        auto_now_add=True,
        help_text=_("created datetime"),
    )
    updated_at = DateTimeField(auto_now=True, help_text=_("updated datetime"))

    class Meta:
        abstract = True


class BaseModel(UUIDV4Model, TimestampedModel):
    class Meta:
        abstract = True
