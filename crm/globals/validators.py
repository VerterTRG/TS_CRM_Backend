from django.core.validators import RegexValidator


def create_digits_validator(field_name:str):
        regex = '^[0-9]*$'
        message = f'{field_name.upper()} должен содержать только цифры'
        code = 'invalid_digits'

        return RegexValidator(regex=regex, message=message, code=code)