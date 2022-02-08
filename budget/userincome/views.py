import datetime
from django.shortcuts import render, redirect
from .models import Source, UserIncome
from expenses.models import Budynek
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import os
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse



# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        income = UserIncome.objects.filter(
            amount__startswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__startswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            waluta__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            budynek__icontains=search_str, owner=request.user)

        data = income.values()

        return JsonResponse(list(data), safe=False)


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

    # sources = Source.objects.filter(owner=request.user)

    sources1 = UserIncome.objects.filter(owner=request.user).values_list('source', flat=True)
    sources = set()
    for x in sources1:
        sources.add(x)

    # budynek = Budynek.objects.filter(owner=request.user)

    budynek1 = UserIncome.objects.filter(owner=request.user).values_list('budynek', flat=True)
    budynek = set()

    for x in budynek1:
        budynek.add(x)


    income = UserIncome.objects.filter(owner=request.user).order_by(orderdata)
    kwota_max = request.GET.get('kwota_max')
    kwota_min = request.GET.get('kwota_min')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    szukaj_opis = request.GET.get('szukaj_opis')
    waluta_filter = request.GET.get('waluta_filter')
    source_filter = request.GET.get('source_filter')
    budynek_filter = request.GET.get('budynek_filter')

    if szukaj_opis != '' and szukaj_opis is not None:
        income = UserIncome.objects.filter(
            amount__startswith=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            date__startswith=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            description__icontains=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            source__icontains=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            waluta__icontains=szukaj_opis, owner=request.user) | UserIncome.objects.filter(
            budynek__icontains=szukaj_opis, owner=request.user)


        if not income:
            messages.error(request, 'Brak wyników')
            income = UserIncome.objects.filter(owner=request.user)
            context = {

                'income': income,
                'sources': sources,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'income/index.html', context)

    if query_search(kwota_min):
        income = income.filter(amount__gte=kwota_min)

        if not income:
            messages.error(request, 'Brak wyników')
            income = UserIncome.objects.filter(owner=request.user)
            context = {

                'income': income,
                'sources': sources,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'income/index.html', context)

    if query_search(kwota_max):
        income = income.filter(amount__lt=kwota_max)

        if not income:
            messages.error(request, 'Brak wyników')
            income = UserIncome.objects.filter(owner=request.user)
            context = {

                'income': income,
                'sources': sources,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'income/index.html', context)

    if query_search(date_max):
        income = income.filter(date__lte=date_max)

        if not income:
            messages.error(request, 'Brak wyników')
            income = UserIncome.objects.filter(owner=request.user)
            context = {

                'income': income,
                'sources': sources,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'income/index.html', context)

    if query_search(date_min):
        income = income.filter(date__gte=date_min)

        if not income:
            messages.error(request, 'Brak wyników')
            income = UserIncome.objects.filter(owner=request.user)
            context = {

                'income': income,
                'sources': sources,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'income/index.html', context)

    if query_search(budynek_filter) and budynek_filter != 'Kościół':
        income = income.filter(budynek__contains=budynek_filter)

        if not income:
            messages.error(request, 'Brak wyników')
            income = UserIncome.objects.filter(owner=request.user)
            context = {
                'income': income,
                'sources': sources,
                'budynki': budynek,
                'currencies': waluty_data,
            }
            return render(request, 'income/index.html', context)

    if query_search(waluta_filter) and waluta_filter != 'Waluta':
        income = income.filter(waluta__contains=waluta_filter)

        if not income:
            messages.error(request, 'Brak wyników')
            income = UserIncome.objects.filter(owner=request.user)
            context = {
                'income': income,
                'sources': sources,
                'budynki': budynek,
                'currencies': waluty_data,
            }
            return render(request, 'income/index.html', context)

    if query_search(source_filter) and source_filter != 'Źródło':
        income = income.filter(source__contains=source_filter)
        if not income:
            messages.error(request, 'Brak wyników')
            income = UserIncome.objects.filter(owner=request.user)
            context = {

                'income': income,
                'sources': sources,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'income/index.html', context)

    paginator = Paginator(income, 20)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)


    context = {
        'income': income,
        'page_obj': page_obj,
        'currencies': waluty_data,
        'sources': sources,
        'budynki': budynek,
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):

    waluty_data = []
    file_path = os.path.join(settings.BASE_DIR, 'static/currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            waluty_data.append({'name_wal': k, 'value_wal': v})


    waluta_usera = UserPreferences.objects.get(user=request.user)


    sources = Source.objects.filter(owner=request.user)
    budynek = Budynek.objects.filter(owner=request.user)
    context = {
        'sources': sources,
        'values': request.POST,
        'waluta_usera': waluta_usera,
        'currencies': waluty_data,
        'budynki': budynek
    }
    if request.method == "GET":
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Kwota jest Wymagana')
            return render(request, 'income/add_income.html', context)

        description = request.POST['description']

        if not description:
            messages.error(request, 'Opis jest Wymagany')
            return render(request, 'income/add_income.html', context)

        date = request.POST['income_date']

        if not date:
            messages.error(request, 'Data jest wymagana')
            return render(request, 'income/add_income.html', context)

        waluta = request.POST['waluta']
        source = request.POST.get('source', 'Nie podano')


        budynek = request.POST.get('budynek', 'Nie podano')



        UserIncome.objects.create(owner=request.user,
                                  amount=amount,
                                  waluta=waluta,
                                  budynek=budynek,
                                  date=date,
                                  source=source,
                                  description=description)
        messages.success(request, 'Wpis zapisany Poprawnie ')

        return redirect('income')


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    # lista walut do wybouru
    waluty_data = []
    file_path = os.path.join(settings.BASE_DIR, 'static/currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            waluty_data.append({'name_wal': k, 'value_wal': v})
    # koniec listy wyboru wluty
    # domyślna waluta
    waluta_usera = UserPreferences.objects.get(user=request.user)
    # koniec domylsmna waluta

    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.filter(owner=request.user)
    budynek = Budynek.objects.filter(owner=request.user)
    context = {
        'income': income,
        'values': income,
        'sources': sources,
        'waluta_usera': waluta_usera,
        'currencies': waluty_data,
        'budynki': budynek,
    }
    if request.method == "GET":
        return render(request, "income/edit_income.html", context)

    if request.method == "POST":

        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Kwota jest wymagana')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        
        waluta = request.POST['waluta']
        source = request.POST.get('source', 'Nie podano')

        budynek = request.POST.get('budynek', 'Nie podano')

        if not description:
            messages.error(request, 'Opis jest wymagany')
            return render(request, 'income/edit_income.html', context)

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.waluta = waluta
        income.budynek = budynek

        income.save()
        messages.success(request, 'income updated successfully ')

        return redirect('income')




@login_required(login_url='/authentication/login')
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Wpływ został usunięty')
    return redirect('income')
