from __future__ import unicode_literals

import archieml

from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ArchieMLData(object):
    def __init__(self, text):
        self.text = text
        self.data = archieml.loads(text)

    def __str__(self):
        return self.text


class ArchieMLField(models.TextField):
    description = 'Store content in ArchieML specification and retrieve python object'

    def from_db_value(self, value, expression, connection, context):
        if isinstance(value, six.string_types):
            return ArchieMLData(value)
        return None

    def to_python(self, value):
        if isinstance(value, six.string_types):
            return ArchieMLData(value)
        if isinstance(value, ArchieMLData):
            return value
        return None

    def get_prep_value(self, value):
        if isinstance(value, six.string_types):
            return value
        if isinstance(value, ArchieMLData):
            return value.text
        return None
