import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(_("Hasło musi zawierać cyfrę"))

    def get_help_text(self):
        return _("Hasło musi zawierać cyfrę")


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(_("Hasło musi zawierać przynajmniej jedną wielką literę"))

    def get_help_text(self):
        return _("Hasło musi zawierać przynajmniej jedną wielką literę")


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(_("Hasło musi zawierać przynajmniej jedną małą literę"))

    def get_help_text(self):
        return _("Hasło musi zawierać przynajmniej jedną małą literę")


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(_("Hasło musi zawierać: " +
                                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"))

    def get_help_text(self):
        return _("Hasło musi zawierać:" + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?")
