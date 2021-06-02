import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("A senha deve conter pelo menos um número."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "A senha deve conter pelo menos um número."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra maiúscula."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "A senha deve conter pelo menos uma letra maiúscula."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra minúscula."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "A senha deve conter pelo menos uma letra minúscula."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos um símbolo."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "A senha deve conter pelo menos um símbolo."
        )