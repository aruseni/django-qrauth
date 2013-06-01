import os
import string
import hashlib

from django.conf import settings

def generate_random_string(length,
                           stringset="".join(
                               [string.ascii_letters+string.digits]
                           )):
    """
    Returns a string with `length` characters chosen from `stringset`
    >>> len(generate_random_string(20) == 20 
    """
    return "".join([stringset[i%len(stringset)] \
        for i in [ord(x) for x in os.urandom(length)]])

def salted_hash(string):
    return hashlib.sha1(":)".join([
        string,
        settings.SECRET_KEY,
    ])).hexdigest()
