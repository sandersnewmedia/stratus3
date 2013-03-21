import re

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

key_re = re.compile(r'^[a-zA-Z0-9_]+$')
validate_key = RegexValidator(key_re, _("Enter a valid 'key' consisting of letters, numbers, underscores."), 'invalid')
