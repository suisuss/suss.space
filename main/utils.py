from flask_mail import Message
from flaskapp import mail


def send_message_email(name, message, email, phone=None):
    msg = Message('SUSS.SPACE - Message Recieved',
                  sender='',
                  recipients=[''])
    if phone != None:
        msg.body = f'''{name} - {email} - {phone}
{message}'''
    else:
        msg.body = f'''{name} - {email} - {phone}
{message}'''
    mail.send(msg)


def arabic_to_roman(number):
    conv = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
            [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
            [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'],
            [1, 'I']]
    result = ''
    for denom, roman_digit in conv:
        result += roman_digit*(number//denom)
        number %= denom
    return result
