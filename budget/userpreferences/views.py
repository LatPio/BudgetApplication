from django.shortcuts import render, redirect
import os
import json
from django.conf import settings
from .models import UserPreferences
from django.contrib import messages
from expenses.models import Budynek, Category
from userincome.models import Source
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required(login_url='/authentication/login')
def index(request):

    categories = Category.objects.filter(owner=request.user)
    budynek = Budynek.objects.filter(owner=request.user)
    source = Source.objects.filter(owner=request.user)


    curency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'static/currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            curency_data.append({'name': k, 'value': v})

    exists = UserPreferences.objects.filter(user=request.user).exists()
    user_preferences = None

    if exists:
        user_preferences = UserPreferences.objects.get(user=request.user)

    if request.method == 'GET':

        return render(request, 'preferences/index.html', {"currencies": curency_data,
                                                          'user_preferences': user_preferences,
                                                          'category': categories,
                                                          'budynek': budynek,
                                                          'source': source})
    else:
        currency = request.POST['currency']
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:

            UserPreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {"currencies": curency_data,
                                                          'user_preferences': user_preferences,
                                                          'category': categories,
                                                          'budynek': budynek,
                                                          'source': source})


@login_required(login_url='/authentication/login')
def add_category(request):
    context = {
        'values': request.POST
    }
    if request.method == "GET":
        return render(request, "preferences/add_category.html", context)

    if request.method == "POST":

        nazwa = request.POST['nazwa']

        if not nazwa:
            messages.error(request, 'Wymagane wprowadznie kategroi')
            return render(request, 'preferences/add_category.html', context)

        Category.objects.create(owner=request.user,
                                name=nazwa)
        messages.success(request, 'Kategoria zapisana Poprawnie ')

        return redirect('preferences')


@login_required(login_url='/authentication/login')
def delete_category(request, id):
    categories = Category.objects.get(pk=id)
    categories.delete()
    messages.success(request, 'Kategoria Usunięta')
    return redirect('preferences')


@login_required(login_url='/authentication/login')
def edit_category(request, id):
    category = Category.objects.get(pk=id)
    context = {
        "category": category
    }
    if request.method == "GET":
        return render(request, "preferences/edit_category.html", context)

    if request.method == "POST":

        nazwa = request.POST['nazwa']

        if not nazwa:
            messages.error(request, 'Należy podać kategorię')
            return render(request, 'preferences/edit_category.html', context)

        category.owner = request.user
        category.name = nazwa

        category.save()
        messages.success(request, 'Kategoria dodaana pozytwynie ')

        return redirect('preferences')




@login_required(login_url='/authentication/login')
def add_budynek(request):
    context = {
        'values': request.POST
    }
    if request.method == "GET":
        return render(request, "preferences/add_budynek.html", context)

    if request.method == "POST":

        nazwa = request.POST['nazwa']

        if not nazwa:
            messages.error(request, 'Wymagane wprowadznie lokalizacji')
            return render(request, 'preferences/add_budynek.html', context)

        Budynek.objects.create(owner=request.user, name=nazwa)
        messages.success(request, 'Lokazliacja zapisana poprawnie ')

        return redirect('preferences')


@login_required(login_url='/authentication/login')
def delete_budynek(request, id):
    budynek = Budynek.objects.get(pk=id)
    budynek.delete()
    messages.success(request, 'Kategoria Usunięta')
    return redirect('preferences')


@login_required(login_url='/authentication/login')
def edit_budynek(request, id):
    budynek = Budynek.objects.get(pk=id)
    context = {
        "budynek": budynek
    }
    if request.method == "GET":
        return render(request, "preferences/edit_budynek.html", context)

    if request.method == "POST":

        nazwa = request.POST['nazwa']

        if not nazwa:
            messages.error(request, 'Należy podać lokalizację')
            return render(request, 'preferences/edit_category.html', context)

        budynek.owner = request.user
        budynek.name = nazwa

        budynek.save()
        messages.success(request, 'Lokalizacja dodaana pozytwynie ')

        return redirect('preferences')


@login_required(login_url='/authentication/login')
def add_source(request):
    context = {
        'values': request.POST
    }
    if request.method == "GET":
        return render(request, "preferences/add_source.html", context)

    if request.method == "POST":

        nazwa = request.POST['nazwa']

        if not nazwa:
            messages.error(request, 'Wymagane wprowadznie Źródła')
            return render(request, 'preferences/add_source.html', context)

        Source.objects.create(owner=request.user,
                                name=nazwa)
        messages.success(request, 'Źródło zapisane poprawine')

        return redirect('preferences')


@login_required(login_url='/authentication/login')
def delete_source(request, id):
    source = Source.objects.get(pk=id)
    source.delete()
    messages.success(request, 'Źródło Usunięte')
    return redirect('preferences')


@login_required(login_url='/authentication/login')
def edit_source(request, id):
    source = Source.objects.get(pk=id)
    context = {
        "source": source
    }
    if request.method == "GET":
        return render(request, "preferences/edit_source.html", context)

    if request.method == "POST":

        nazwa = request.POST['nazwa']

        if not nazwa:
            messages.error(request, 'Należy podać Źródło')
            return render(request, 'preferences/edit_source.html', context)

        source.owner = request.user
        source.name = nazwa

        source.save()
        messages.success(request, 'Kategoria dodaana pozytwynie ')

        return redirect('preferences')