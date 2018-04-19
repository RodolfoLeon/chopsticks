# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def reg_validation(self,postData):
        errors=[]
        name=postData['name']
        alias=postData['alias']
        email=postData['email']
        password=postData['password']
        password_ver=postData['password_ver']

        if len(name)<0:
            errors.append('Name field cannot be empty.')
        elif len(name)<3:
            errors.append('Name field requires at least three characters.')
        if len(alias)<0:
            errors.append('Alias cannot be empty.')
        elif len(alias)<3:
            errors.append('Alias should be at least three characters.')
        if len(email) is 0:
            errors.append('Email cannot be left empty.')
        elif not EMAIL_REGEX.match(email):
            errors.append('Email is not in a valid format')
        if len(password) is 0:
            errors.append('Password field is required.')
        elif len(password)<8:
            errors.append('The password must be at least 8 characters long.')
        elif password != password_ver:
            errors.append('Password and password confirmation must match.')

        if len(errors)>0:
            return (False, errors)
        else:
            result = self.filter(alias=alias)
            if len(result)>0:
                errors.append('Alias already exists. Please log in.')
                return (False, errors)
            else:
                new_user = self.create(
                    name=name,
                    alias=alias,
                    email=email,
                    password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                )
                return (True, new_user)

    def log_validation(self,postData):
        errors=[]
        email=postData['lemail']
        password=postData['lpassword']

        if len(email) is 0:
            errors.append('Email field is required for login.')
        if len(password) is 0:
            errors.append('Password is required')
        elif not EMAIL_REGEX.match(email):
            errors.append('Email is not in a valid format')
        if len(errors) > 0:
            return (False, errors)
        else:
            login = self.filter(email=email)
            if len(login)>0:
                user = login[0]
                if bcrypt.checkpw(password.encode(), user.password.encode()):
                    return (True, user)
                else:
                    errors.append('Invalid username or password. Please verify and try again.')
                    return (False, errors)
            else:
                errors.append('Invalid username or password. Please verify and try again')
                return (False, errors)
        

class QuoteManager(models.Manager):
    def quote_validation(self, postData, id):
        errors=[]
        author=postData['author']
        quote=postData['quotes']

        if len(author) is 0:
            errors.append('The author field cannot be empty')
        elif len(author)<3:
            errors.append('The author field must be at least three characters long.')
        if len(quote) is 0:
            errors.append('Quote field cannot be empty.')
        elif len(quote) < 10:
            errors.append('The quotes field must be at least 10 characters long.')
        
        if len(errors)>0:
            return (False, errors)
        else:
            new_quote=self.create(
                author=author,
                quote=quote,
                posted_by=User.objects.get(id=id)
            )
            return (True, new_quote)
        


class User(models.Model):
    name=models.CharField(max_length=255)
    alias=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=255)
    objects=UserManager()
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Quote(models.Model):
    author=models.CharField(max_length=255)
    quote=models.CharField(max_length=255)
    posted_by=models.ForeignKey(User, related_name='posted')
    liked_by=models.ManyToManyField(User, related_name='liked')
    objects=QuoteManager()

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author