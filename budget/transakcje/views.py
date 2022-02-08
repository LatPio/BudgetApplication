from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from expenses.models import Category, Expense, Budynek
from userincome.models import UserIncome, Source
from django.contrib import messages
from django.core.paginator import Paginator
import os
import json
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from userpreferences.models import UserPreferences
from itertools import chain
from django.db.models import Avg, Max, Min, Sum


def query_search(param):
    return param != '' and param is not None

@login_required(login_url='/authentication/login')
def index(request):

    waluty_data = []
    file_path = os.path.join(settings.BASE_DIR, 'static/currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            waluty_data.append({'name_wal': k, 'value_wal': v})
    orderdata = '-date'
    expenses = Expense.objects.filter(owner=request.user).order_by(orderdata)
    income = UserIncome.objects.filter(owner=request.user).order_by(orderdata)

    sources = Source.objects.filter(owner=request.user)
    categories = Category.objects.filter(owner=request.user)
    budynek = Budynek.objects.filter(owner=request.user)

    kwota_max = request.GET.get('kwota_max')
    kwota_min = request.GET.get('kwota_min')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    szukaj_opis = request.GET.get('szukaj_opis')
    waluta_filter = request.GET.get('waluta_filter')
    category_filter = request.GET.get('category_and_source_filter')
    budynek_filter = request.GET.get('budynek_filter')
    source_filter = request.GET.get('category_and_source_filter')



    if szukaj_opis != '' and szukaj_opis is not None:
        expenses = Expense.objects.filter(
            amount__startswith=szukaj_opis, owner=request.user) | Expense.objects.filter(
            date__startswith=szukaj_opis, owner=request.user) | Expense.objects.filter(
            description__icontains=szukaj_opis, owner=request.user) | Expense.objects.filter(
            category__icontains=szukaj_opis, owner=request.user) | Expense.objects.filter(
            waluta__icontains=szukaj_opis, owner=request.user) | Expense.objects.filter(
            budynek__icontains=szukaj_opis, owner=request.user).order_by(orderdata)

        income = UserIncome.objects.filter(
            amount__startswith=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            date__startswith=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            description__icontains=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            source__icontains=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            waluta__icontains=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            budynek__icontains=szukaj_opis, owner=request.user)

        if not (expenses or income):
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            income = UserIncome.objects.filter(owner=request.user)

            transactions = chain(expenses, income)

            transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

            context = {
                'transakcje': transactionSorted,
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
                'sources': sources

            }
            return render(request, 'transakcje/index.html', context)

    if query_search(kwota_min):
        expenses = expenses.filter(amount__gte=kwota_min)
        income = income.filter(amount__gte=kwota_min)
        if not (expenses or income):
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            income = UserIncome.objects.filter(owner=request.user)

            transactions = chain(expenses, income)

            transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

            context = {
                'transakcje': transactionSorted,
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
                'sources': sources

            }
            return render(request, 'transakcje/index.html', context)

    if query_search(kwota_max):
        expenses = expenses.filter(amount__lt=kwota_max)
        income = income.filter(amount__lt=kwota_max)
        if not (expenses or income):
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            income = UserIncome.objects.filter(owner=request.user)

            transactions = chain(expenses, income)

            transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

            context = {
                'transakcje': transactionSorted,
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
                'sources': sources

            }
            return render(request, 'transakcje/index.html', context)

    if query_search(date_max):
        expenses = expenses.filter(date__lte=date_max)
        income = income.filter(date__lte=date_max)
        if not (expenses or income):
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            income = UserIncome.objects.filter(owner=request.user)

            transactions = chain(expenses, income)

            transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

            context = {
                'transakcje': transactionSorted,
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
                'sources': sources

            }
            return render(request, 'transakcje/index.html', context)

    if query_search(date_min):
        expenses = expenses.filter(date__gte=date_min)
        income = income.filter(date__gte=date_min)
        if not (expenses or income):
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            income = UserIncome.objects.filter(owner=request.user)

            transactions = chain(expenses, income)

            transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

            context = {
                'transakcje': transactionSorted,
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
                'sources': sources

            }
            return render(request, 'transakcje/index.html', context)


    if query_search(budynek_filter) and budynek_filter != 'Lokalizacja':
        expenses = expenses.filter(budynek__contains=budynek_filter)
        income = income.filter(budynek__contains=budynek_filter)
        if not (expenses or income):
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            income = UserIncome.objects.filter(owner=request.user)

            transactions = chain(expenses, income)
            transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

            context = {
                'transakcje': transactionSorted,
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
                'sources': sources

            }
            return render(request, 'transakcje/index.html', context)

    if query_search(waluta_filter) and waluta_filter != 'Waluta':
        expenses = expenses.filter(waluta__contains=waluta_filter)
        income = income.filter(waluta__contains=waluta_filter)
        if not (expenses or income):
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            income = UserIncome.objects.filter(owner=request.user)

            transactions = chain(expenses, income)

            transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

            context = {
                'transakcje': transactionSorted,
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
                'sources': sources

            }
            return render(request, 'expenses/index.html', context)

    if query_search(category_filter) and category_filter != 'Kategoria':
        expenses = expenses.filter(category__contains=category_filter)
        income = income.filter(source__contains=category_filter)
        if not (expenses or income):
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user).order_by(orderdata)
            income = UserIncome.objects.filter(owner=request.user).order_by(orderdata)

            transactions = chain(expenses, income)

            transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

            context = {
                'transakcje': transactionSorted,
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'sources': sources,
                'currencies': waluty_data,

            }
            return render(request, 'transakcje/index.html', context)






    transactions = chain(expenses, income)

    transactionSorted = sorted(transactions, key=lambda instance: instance.date, reverse=True)

    context = {
        'transakcje': transactionSorted,
        'expenses': expenses,
        'categories': categories,
        'budynki': budynek,
        'sources': sources,
        'currencies': waluty_data,

    }
    return render(request, 'transakcje/index.html', context)