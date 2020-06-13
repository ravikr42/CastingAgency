import uuid
from datetime import datetime
import random


def generate_guid():
    return str(uuid.uuid4())


def get_datetime(date_string):
    format_str = '%d/%m/%Y'
    datetime_obj = datetime.strptime(date_string, format_str)
    return datetime_obj.date()


def get_datetime_as_str(datetime_obj):
    return datetime_obj.strftime("%d/%m/%Y")


def get_gender_char():
    return ''.join(random.choice('MFU') for x in range(1))
