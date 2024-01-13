import hashlib
from django.conf import settings


def md5(data_srting):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_srting.encode('utf-8'))
    return obj.hexdigest()
