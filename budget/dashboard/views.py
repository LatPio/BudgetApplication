from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.datetime_safe import datetime
from expenses.models import Category, Expense, Budynek
from userincome.models import UserIncome, Source
from userpreferences.models import UserPreferences
from itertools import chain
from django.db.models import Sum
from django.db.models.functions import ExtractYear


@login_required(login_url='/authentication/login')
def index(request):
    today = datetime.now()
    actualdate = datetime.now()

    def first3(s):
        return s[0:3]

    waluta_usera = UserPreferences.objects.get(user=request.user)

    val = first3(waluta_usera.currency)


    sumExpenses = (Expense.objects.filter(owner=request.user).filter(date__year=actualdate.year).filter(
        waluta=waluta_usera.currency)).aggregate(
        Sum('amount'))
    if sumExpenses['amount__sum'] is None:
        sumExpenses['amount__sum'] = 0

    sumIncome = (UserIncome.objects.filter(owner=request.user).filter(date__year=actualdate.year).filter(
        waluta=waluta_usera.currency)).aggregate(
        Sum('amount'))
    if sumIncome['amount__sum'] is None:
        sumIncome['amount__sum'] = 0

    balance = sumIncome['amount__sum'] - sumExpenses['amount__sum']

    allDate = chain((Expense.objects.filter(owner=request.user).annotate(year=ExtractYear('date'))),
                    (UserIncome.objects.filter(owner=request.user).annotate(year=ExtractYear('date'))))

    unique_years = set()
    for x in allDate:
        unique_years.add(x.year)

    # Separation of expense and income for months

    monthlydataExpanse = []
    for miech in range(1, 13):
        information = (Expense.objects.filter(owner=request.user).filter(
            date__year=actualdate.year).filter(date__month=miech).filter(waluta=waluta_usera.currency)).aggregate(
            Sum('amount'))
        if information['amount__sum'] is None:
            information['amount__sum'] = 0
        monthlydataExpanse.append(float(information['amount__sum']))
    monthlydataIncome = []
    for miech in range(1, 13):
        information = (UserIncome.objects.filter(owner=request.user).filter(
            date__year=actualdate.year).filter(date__month=miech).filter(waluta=waluta_usera.currency)).aggregate(
            Sum('amount'))
        if information['amount__sum'] is None:
            information['amount__sum'] = 0
        monthlydataIncome.append(float(information['amount__sum']))

    # Seprartion of expensen and income for months

    context = {
        'sumExpenses': sumExpenses,
        'sumIncome': sumIncome,
        'waluta_usera': waluta_usera,
        'val': val,
        'balance': balance,
        'roki': unique_years,
        'today': today,
        'monthlydataExpanse': monthlydataExpanse,
        'monthlydataIncome': monthlydataIncome

    }

    return render(request, 'dashboard/index.html', context)


@login_required(login_url='/authentication/login')
def yearView(request, rok):
    def first3(s):
        return s[0:3]

    waluta_usera = UserPreferences.objects.get(user=request.user)

    val = first3(waluta_usera.currency)


    sumExpenses = (Expense.objects.filter(owner=request.user).filter(date__year=rok).filter(
        waluta=waluta_usera.currency)).aggregate(
        Sum('amount'))
    if sumExpenses['amount__sum'] is None:
        sumExpenses['amount__sum'] = 0

    sumIncome = (UserIncome.objects.filter(owner=request.user).filter(date__year=rok).filter(
        waluta=waluta_usera.currency)).aggregate(
        Sum('amount'))
    if sumIncome['amount__sum'] is None:
        sumIncome['amount__sum'] = 0

    balance = sumIncome['amount__sum'] - sumExpenses['amount__sum']

    allDate = chain((Expense.objects.filter(owner=request.user).annotate(year=ExtractYear('date'))),
                    (UserIncome.objects.filter(owner=request.user).annotate(year=ExtractYear('date'))))

    unqueYears = set()
    for x in allDate:
        unqueYears.add(x.year)


    # Seprartion of expensen anfd invome for months

    monthlydataExpanse = []
    for miech in range(1, 13):
        information = (Expense.objects.filter(owner=request.user).filter(
            date__year=rok).filter(date__month=miech).filter(waluta=waluta_usera.currency)).aggregate(
            Sum('amount'))
        if information['amount__sum'] is None:
            information['amount__sum'] = 0
        monthlydataExpanse.append(float(information['amount__sum']))
    monthlydataIncome = []
    for miech in range(1, 13):
        information = (UserIncome.objects.filter(owner=request.user).filter(
            date__year=rok).filter(date__month=miech).filter(waluta=waluta_usera.currency)).aggregate(
            Sum('amount'))
        if information['amount__sum'] is None:
            information['amount__sum'] = 0
        monthlydataIncome.append(float(information['amount__sum']))

    context = {
        'sumExpenses': sumExpenses,
        'sumIncome': sumIncome,
        'waluta_usera': waluta_usera,
        'val': val,
        'balance': balance,
        'roki': unqueYears,
        'monthlydataExpanse': monthlydataExpanse,
        'monthlydataIncome': monthlydataIncome,
        'viewYear': rok

    }
    return render(request, 'dashboard/yearView.html', context)
