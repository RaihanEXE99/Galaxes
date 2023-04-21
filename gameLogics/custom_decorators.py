from functools import wraps
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.http import JsonResponse, request

from .models import GameAccount

def GameInitRequired(function=None, login_required=True, redirect_field_name="/", login_url=None):
    def is_customer(u):
        if login_required and not u.is_authenticated:
            return False
        return GameAccount.objects.filter(user=u,game_init=True).exists()
    actual_decorator = user_passes_test(
        is_customer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    else:
        return actual_decorator

# def GameInitCheck(function=None, login_required=True, redirect_field_name="/", login_url=None):
#     def is_customer(u):
#         if login_required and not u.is_authenticated:
#             return False
#         return GameAccount.objects.filter(user=u).exists()
#     actual_decorator = user_passes_test(
#         is_customer,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     else:
#         return actual_decorator