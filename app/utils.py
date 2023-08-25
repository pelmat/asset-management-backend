from secrets import token_urlsafe
from .exceptions import TokenGenerationException


def generate_base_id(sender) -> str:
    """
    Generate a unique secret to be used as base_id.

    If this loop fails there may be too many instances in the DB or the generation
    got extremely unlucky in which case consider raising the base_id length in the model with a higher urlsafe value.
    """
    for _ in range(1, 5):
        token = token_urlsafe(8)
        found = sender.objects.filter(base_token=token).first()

        if not found:
            return token
    raise TokenGenerationException


def multi_receiver(signal, senders, **kwargs):
    """
    Receiver to be used as a signal decorator that lets you specify multiple models.

    Use: @multi_receiver(pre_save, senders=[ModelFirst, ModelSecond, ...])
    """

    def decorator(receiver_func):
        for sender in senders:
            if isinstance(signal, (list, tuple)):
                for s in signal:
                    s.connect(receiver_func, sender=sender, **kwargs)
            else:
                signal.connect(receiver_func, sender=sender, **kwargs)
        return receiver_func

    return decorator


def is_valid_int(param_value):
    if param_value.isdigit():
        return int(param_value)


def query_param_validator(request, param):
    '''
    A common query parameter validator.

    Specific parameters that need validation come here.
    '''
    if request:
        if param == 'nested_max_count':
            nested_max_count = is_valid_int(request.query_params.get(param, ''))
            if nested_max_count is not None:
                return nested_max_count
