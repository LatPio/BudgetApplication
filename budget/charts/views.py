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
    categories1 = Expense.objects.filter(owner=request.user).values_list('category', flat=True)
    categories = set()
    for x in categories1:
        categories.add(x)

    sources1 = UserIncome.objects.filter(owner=request.user).values_list('source', flat=True)
    sources = set()
    for x in sources1:
        sources.add(x)

    budynek1 = chain((Expense.objects.filter(owner=request.user).values_list('budynek', flat=True)), (UserIncome.objects.filter(owner=request.user).values_list('budynek', flat=True)))
    budynek = set()

    for x in budynek1:
        budynek.add(x)

    months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpierń', 'Wrzesień',
              'Październik', 'Listopad', 'Grudzień']

    today = datetime.now()

    allDate = chain((Expense.objects.filter(owner=request.user).annotate(year=ExtractYear('date'))),
                    (UserIncome.objects.filter(owner=request.user).annotate(year=ExtractYear('date'))))


    waluta_usera = UserPreferences.objects.get(user=request.user)

    monthsgrab = months
    if request.method == 'POST':
        monthsgrab = request.POST.getlist('mont')

        if monthsgrab.__len__() == 0:
            monthsgrab = months


    namesOfLocations = budynek

    namesOfSources = sources

    namesOfCategories = categories

    locationes = namesOfLocations

    if request.method == 'POST':
        locationes = request.POST.getlist('location')

        if locationes.__len__() == 0:
            locationes = namesOfLocations



    colorsForChart = ['#1ba3c6', '#2cb5c0', '#30bcad', '#21B087', '#33a65c', '#57a337', '#a2b627', '#d5bb21', '#f8b620',
                      '#f89217', '#f06719', '#e03426', '#f64971', '#fc719e', '#eb73b3', '#ce69be', '#a26dc2', '#7873c0',
                      '#4f7cba', " rgba(158, 03, 69, 0.8) ", " rgba(200, 103, 19, 0.8) ", " rgba(8, 03, 69, 0.8)",
                      "#ff6384", "#e896fb", "#4fa9b9", "#4fa9b9",
                      "#beca87", "#1e3937", "#93b4bd", "#19e95a", "#9138a3", "#27fc2d"]

    unique_years = set()

    for x in allDate:
        unique_years.add(x.year)

    # limiting to picked locations

    monthlydata_income_filteredBy_Category_Location = {}
    for but in locationes:
        picketInformation = {}
        for sour in sources:
            sourcesMonhlydata = []
            for miech in range(1, 13):
                information = (UserIncome.objects.filter(owner=request.user).filter(
                    date__year=today.year).filter(date__month=miech).filter(waluta=waluta_usera.currency)).filter(
                    source=sour).filter(budynek=but).aggregate(Sum('amount'))
                if information['amount__sum'] is None:
                    information['amount__sum'] = 0

                sourcesMonhlydata.append(float(information['amount__sum']))
            picketInformation[sour] = sourcesMonhlydata
        monthlydata_income_filteredBy_Category_Location[but] = picketInformation


    monthlydata_income_filteredBy_Category_Location_SumedByLocation = sumOverPickedLocations(monthlydata_income_filteredBy_Category_Location, namesOfSources, locationes)

    monthlydata_income_filteredBy_Category_Location_SumedByLocation_CherryPick = monthValueGrab(
        monthlydata_income_filteredBy_Category_Location_SumedByLocation, monthsgrab)

    zipedDataIncome = [{'key': t[0], 'values': t[1], 'color': t[2]} for t in
                       zip(monthlydata_income_filteredBy_Category_Location_SumedByLocation_CherryPick,
                           monthlydata_income_filteredBy_Category_Location_SumedByLocation_CherryPick.values(),
                           colorsForChart)]




    monthlydata_expanse_filteredBy_Category_Location = {}
    for but in locationes:
        picketInformation = {}
        for cat in categories:
            categoryMonhlydata = []
            for miech in range(1, 13):
                information = (Expense.objects.filter(owner=request.user).filter(
                    date__year=today.year).filter(date__month=miech).filter(waluta=waluta_usera.currency)).filter(
                    category=cat).filter(budynek=but).aggregate(
                    Sum('amount'))
                if information['amount__sum'] is None:
                    information['amount__sum'] = 0
                categoryMonhlydata.append(float(information['amount__sum']))
            picketInformation[cat] = categoryMonhlydata

        monthlydata_expanse_filteredBy_Category_Location[but] = picketInformation

    # print(monthlydata_expanse_filteredBy_Category_Location)

    monthlydata_expanse_filteredBy_Category_Location_SumedByLocation = sumOverPickedLocations(monthlydata_expanse_filteredBy_Category_Location, namesOfCategories, locationes)
    # Limiting by user to checked months

    monthlydata_expanse_filteredBy_Category_Location_SumedByLocation_CherryPick = monthValueGrab(monthlydata_expanse_filteredBy_Category_Location_SumedByLocation, monthsgrab)



    zipedDataExpanse = [{'key': t[0], 'values': t[1], 'color': t[2]} for t in
                        zip(monthlydata_expanse_filteredBy_Category_Location_SumedByLocation_CherryPick,
                            monthlydata_expanse_filteredBy_Category_Location_SumedByLocation_CherryPick.values(), colorsForChart)]



    context = {

        'zipedDataExpanse': zipedDataExpanse,
        'zipedDataIncome': zipedDataIncome,
        'today': today,
        'roki': unique_years,
        'months': months,
        'monthsgrab': monthsgrab,
        'budynek': budynek,
        'locationes': locationes

    }
    return render(request, 'charts/index.html', context)


@login_required(login_url='/authentication/login')
def chartYearView(request, rok):
    categories1 = Expense.objects.filter(owner=request.user).values_list('category', flat=True)
    categories = set()
    for x in categories1:
        categories.add(x)

    sources1 = UserIncome.objects.filter(owner=request.user).values_list('source', flat=True)
    sources = set()
    for x in sources1:
        sources.add(x)

    budynek1 = chain((Expense.objects.filter(owner=request.user).values_list('budynek', flat=True)),
                     (UserIncome.objects.filter(owner=request.user).values_list('budynek', flat=True)))
    budynek = set()

    for x in budynek1:
        budynek.add(x)

    months = ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpierń', 'Wrzesień',
              'Październik', 'Listopad', 'Grudzień']

    today = datetime.now()

    allDate = chain((Expense.objects.filter(owner=request.user).annotate(year=ExtractYear('date'))),
                    (UserIncome.objects.filter(owner=request.user).annotate(year=ExtractYear('date'))))
    unique_years = set()

    for x in allDate:
        unique_years.add(x.year)


    waluta_usera = UserPreferences.objects.get(user=request.user)

    monthsgrab = months
    if request.method == 'POST':
        monthsgrab = request.POST.getlist('mont')

        if monthsgrab.__len__() == 0:
            monthsgrab = months

    namesOfLocations = budynek

    namesOfSources = sources

    namesOfCategories = categories

    locationes = namesOfLocations

    if request.method == 'POST':
        locationes = request.POST.getlist('location')

        if locationes.__len__() == 0:
            locationes = namesOfLocations

    colorsForChart = ['#1ba3c6', '#2cb5c0', '#30bcad', '#21B087', '#33a65c', '#57a337', '#a2b627', '#d5bb21', '#f8b620',
                      '#f89217', '#f06719', '#e03426', '#f64971', '#fc719e', '#eb73b3', '#ce69be', '#a26dc2', '#7873c0',
                      '#4f7cba', " rgba(158, 03, 69, 0.8) ", " rgba(200, 103, 19, 0.8) ", " rgba(8, 03, 69, 0.8)",
                      "#ff6384", "#e896fb", "#4fa9b9", "#4fa9b9",
                      "#beca87", "#1e3937", "#93b4bd", "#19e95a", "#9138a3", "#27fc2d"]


    # limiting to picked locations

    monthlydata_income_filteredBy_Category_Location = {}
    for but in locationes:
        picketInformation = {}
        for sour in sources:
            sourcesMonhlydata = []
            for miech in range(1, 13):
                information = (UserIncome.objects.filter(owner=request.user).filter(
                    date__year=rok).filter(date__month=miech).filter(waluta=waluta_usera.currency)).filter(
                    source=sour).filter(budynek=but).aggregate(Sum('amount'))
                if information['amount__sum'] is None:
                    information['amount__sum'] = 0

                sourcesMonhlydata.append(float(information['amount__sum']))
            picketInformation[sour] = sourcesMonhlydata
        monthlydata_income_filteredBy_Category_Location[but] = picketInformation

    monthlydata_income_filteredBy_Category_Location_SumedByLocation = sumOverPickedLocations(
        monthlydata_income_filteredBy_Category_Location, namesOfSources, locationes)

    monthlydata_income_filteredBy_Category_Location_SumedByLocation_CherryPick = monthValueGrab(
        monthlydata_income_filteredBy_Category_Location_SumedByLocation, monthsgrab)

    zipedDataIncome = [{'key': t[0], 'values': t[1], 'color': t[2]} for t in
                       zip(monthlydata_income_filteredBy_Category_Location_SumedByLocation_CherryPick,
                           monthlydata_income_filteredBy_Category_Location_SumedByLocation_CherryPick.values(),
                           colorsForChart)]


    monthlydata_expanse_filteredBy_Category_Location = {}
    for but in locationes:
        picketInformation = {}
        for cat in categories:
            categoryMonhlydata = []
            for miech in range(1, 13):
                information = (Expense.objects.filter(owner=request.user).filter(
                    date__year=rok).filter(date__month=miech).filter(waluta=waluta_usera.currency)).filter(
                    category=cat).filter(budynek=but).aggregate(
                    Sum('amount'))
                if information['amount__sum'] is None:
                    information['amount__sum'] = 0
                categoryMonhlydata.append(float(information['amount__sum']))
            picketInformation[cat] = categoryMonhlydata

        monthlydata_expanse_filteredBy_Category_Location[but] = picketInformation



    monthlydata_expanse_filteredBy_Category_Location_SumedByLocation = sumOverPickedLocations(
        monthlydata_expanse_filteredBy_Category_Location, namesOfCategories, locationes)
    # Limiting by user to checked months

    monthlydata_expanse_filteredBy_Category_Location_SumedByLocation_CherryPick = monthValueGrab(
        monthlydata_expanse_filteredBy_Category_Location_SumedByLocation, monthsgrab)


    zipedDataExpanse = [{'key': t[0], 'values': t[1], 'color': t[2]} for t in
                        zip(monthlydata_expanse_filteredBy_Category_Location_SumedByLocation_CherryPick,
                            monthlydata_expanse_filteredBy_Category_Location_SumedByLocation_CherryPick.values(),
                            colorsForChart)]

    context = {

        'zipedDataExpanse': zipedDataExpanse,
        'zipedDataIncome': zipedDataIncome,
        'today': today,
        'roki': unique_years,
        'months': months,
        'monthsgrab': monthsgrab,
        'budynek': budynek,
        'locationes': locationes,
        'rok': rok,

    }
    return render(request, 'charts/chartYearView.html', context)


def monthValueGrab(dictionary, monthsPicked):
    handPickedValuesByMonth = {}
    for key in dictionary:
        pickedDataMonths = []
        if 'Styczeń' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(0)))
        if 'Luty' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(1)))
        if 'Marzec' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(2)))
        if 'Kwiecień' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(3)))
        if 'Maj' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(4)))
        if 'Czerwiec' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(5)))
        if 'Lipiec' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(6)))
        if 'Sierpierń' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(7)))
        if 'Wrzesień' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(8)))
        if 'Październik' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(9)))
        if 'Listopad' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(10)))
        if 'Grudzień' in monthsPicked:
            pickedDataMonths.append(float(dictionary[key].__getitem__(11)))
        handPickedValuesByMonth[key] = pickedDataMonths

    return (handPickedValuesByMonth)


def sumOverPickedLocations(dictionary2D, names_to_keys, locations):

    twoD_array_to_One_D_array= {}
    for bud in locations:
        for key in dictionary2D[bud]:
            twoD_array_to_One_D_array[key + ' ' + bud] = dictionary2D[bud][key]

    result = {}
    for keys in names_to_keys:
        data = []
        sum_data = list()
        for key in twoD_array_to_One_D_array.keys():
            if key.startswith(str(keys)):
                data.append(twoD_array_to_One_D_array[key])
        for monthly_data in range(0, len(data[0])):
            temp = 0
            for tuplesOfData in range(0, len(data)):
                temp = temp + data[tuplesOfData][monthly_data]
            sum_data.append(temp)
        result[keys] = sum_data

    return (result)


