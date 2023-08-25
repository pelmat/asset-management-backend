from django.dispatch import receiver
from django.db.models.signals import pre_save
from .utils import generate_base_id, multi_receiver
from .models import (
    Customership,
    License,
    Contract,
    Application,
    Service,
    Server,
    Directory,
    Integration,
    Provider,
    Keyword,
    KeywordSet,
    KeywordLabel,
)


@multi_receiver(
    pre_save,
    senders=[
        Customership,
        License,
        Contract,
        Application,
        Service,
        Server,
        Directory,
        Integration,
        Provider,
        Keyword,
        KeywordSet,
        KeywordLabel,
    ],
)
def on_pre_save(sender, instance, **kwargs):
    """Signal that fills and validates core id values for the instance before saving."""
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Set the specific id related values when the object gets first made.
        token = generate_base_id(sender)
        instance.base_id = f"{sender.model_prefix}-{token}"
        instance.base_token = token
        instance.id_prefix = instance.model_prefix
        pass
    else:
        # TODO: Validate that the base_id has not changed on update.
        if not obj.base_id == instance.base_id:
            # Not done.
            print("Base_id for some reason has changed, prevent!")
