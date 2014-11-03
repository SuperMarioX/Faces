"""
Statement:
    Contains the util class or methods
Author:
    Will
Date:
    2014.11.02
Notes:
    We still have problems in email validating
"""

# -*- coding: utf-8 -*-
import re

class Validator(object):
    username_regex = re.compile(u'^[_a-zA-Z0-9\u4e00-\u9fa5]{2,14}$')
    chinese_regex = re.compile(r'^[\u4e00-\u9fa5]+$')
    alphanum_regex = re.compile(r'^[_a-zA-Z0-9]+$')
    email_regex = re.compile(r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  #dot-atom
                             r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"'  # quoted-string
                             r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)  # domain

    password_regex = re.compile(r'[a-zA-Z0-9@#$%^&+=]{4,}')

    @classmethod
    def validate_username(cls, username):
        if cls.username_regex.match(username):
            length=0
            for ch in username:
                if cls.chinese_regex.match(ch):
                    length+=2
                else:
                    length+=1
            if length <= 14:
                return True, None
        return False, "Invalid username. The username should be less than 7 chinese or 14 characters, numbers or with underlines."


    @classmethod
    def validate_email(cls, email):
        """
            The syntax checking is simply copied from djongo framework, showed
            on http://stackoverflow.com/questions/3217682/checking-validity-of-email-in-django-python
        """
        email_regex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        if len(email) > 7:
            if re.match(email_regex, email):
                return True
        return False


    @classmethod
    def validate_password(cls, password):
        if cls.password_regex.match(password):
            return True, None
        else:
            return False, "Invalid password. Should be more than length 7"

