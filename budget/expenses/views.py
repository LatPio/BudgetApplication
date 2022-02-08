
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense, Budynek

from django.contrib import messages
from django.core.paginator import Paginator
import os
import json
from django.conf import settings

from userpreferences.models import UserPreferences




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


    # categories = Category.objects.filter(owner=request.user)

    categories1 = Expense.objects.filter(owner=request.user).values_list('category', flat=True)
    categories = set()
    for x in categories1:
        categories.add(x)

    # budynek = Budynek.objects.filter(owner=request.user)

    budynek1 = Expense.objects.filter(owner=request.user).values_list('budynek', flat=True)
    budynek = set()

    for x in budynek1:
        budynek.add(x)



    expenses = Expense.objects.filter(owner=request.user).order_by(orderdata)
    kwota_max = request.GET.get('kwota_max')
    kwota_min = request.GET.get('kwota_min')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    szukaj_opis = request.GET.get('szukaj_opis')
    waluta_filter = request.GET.get('waluta_filter')
    category_filter = request.GET.get('category_filter')
    budynek_filter = request.GET.get('budynek_filter')

    if szukaj_opis != '' and szukaj_opis is not None:
        expenses = Expense.objects.filter(
            amount__startswith=szukaj_opis, owner=request.user) | Expense.objects.filter(
            date__startswith=szukaj_opis, owner=request.user) | Expense.objects.filter(
            description__icontains=szukaj_opis, owner=request.user) | Expense.objects.filter(
            category__icontains=szukaj_opis, owner=request.user) | Expense.objects.filter(
            waluta__icontains=szukaj_opis, owner=request.user) | Expense.objects.filter(
            budynek__icontains=szukaj_opis, owner=request.user).order_by(orderdata)

        if not expenses:
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            context = {

                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'expenses/index.html', context)

    if query_search(kwota_min):
        expenses = expenses.filter(amount__gte=kwota_min)

        if not expenses:
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            context = {

                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'expenses/index.html', context)

    if query_search(kwota_max):
        expenses = expenses.filter(amount__lt=kwota_max)

        if not expenses:
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            context = {

                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'expenses/index.html', context)

    if query_search(date_max):
        expenses = expenses.filter(date__lte=date_max)

        if not expenses:
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            context = {

                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'expenses/index.html', context)

    if query_search(date_min):
        expenses = expenses.filter(date__gte=date_min)

        if not expenses:
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            context = {

                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,

            }
            return render(request, 'expenses/index.html', context)


    if query_search(budynek_filter) and budynek_filter != 'Kościół':
        expenses = expenses.filter(budynek__contains=budynek_filter)

        if not expenses:
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            context = {
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
            }
            return render(request, 'expenses/index.html', context)

    if query_search(waluta_filter) and waluta_filter != 'Waluta':
        expenses = expenses.filter(waluta__contains=waluta_filter)

        if not expenses:
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            context = {
                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,
            }
            return render(request, 'expenses/index.html', context)

    if query_search(category_filter) and category_filter != 'Kategoria':
        expenses = expenses.filter(category__contains=category_filter)
        if not expenses:
            messages.error(request, 'Brak wyników')
            expenses = Expense.objects.filter(owner=request.user)
            context = {

                'expenses': expenses,
                'categories': categories,
                'budynki': budynek,
                'currencies': waluty_data,


            }
            return render(request, 'expenses/index.html', context)



    paginator = Paginator(expenses, 20)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)



    context = {

        'expenses': expenses,
        'categories': categories,
        'budynki': budynek,
        'page_obj': page_obj,
        'currencies': waluty_data,

    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
def add_expense(request):

    waluty_data = []
    file_path = os.path.join(settings.BASE_DIR, 'static/currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            waluty_data.append({'name_wal': k, 'value_wal': v})

    waluta_usera = UserPreferences.objects.get(user=request.user)


    categories = Category.objects.filter(owner=request.user)
    budynek = Budynek.objects.filter(owner=request.user)
    context = {
        'categories': categories,
        'values': request.POST,
        'waluta_usera': waluta_usera,
        'currencies': waluty_data,
        'budynki': budynek,
    }

    if request.method == "GET":
        return render(request, 'expenses/add_expanses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Kwota jest wymagana')
            return render(request, 'expenses/add_expanses.html', context)

        description = request.POST['description']

        if not description:
            messages.error(request, 'Opis jest wymagany')
            return render(request, 'expenses/add_expanses.html', context)

        date = request.POST['expense_date']

        if not date:
            messages.error(request, 'Data jest wymagana')
            return render(request, 'expenses/add_expanses.html', context)

        waluta = request.POST['waluta']
        category = request.POST.get('category', 'Nie podano')

        budynek = request.POST.get('budynek', 'Nie podano')



        Expense.objects.create(owner=request.user,
                               amount=amount,
                               waluta=waluta,
                               budynek=budynek,
                               date=date,
                               category=category,
                               description=description)
        messages.success(request, 'Expense saved successfully ')

        return redirect('expenses')

@login_required(login_url='/authentication/login')
def expense_edit(request, id):

    waluty_data = []
    file_path = os.path.join(settings.BASE_DIR, 'static/currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            waluty_data.append({'name_wal': k, 'value_wal': v})

    waluta_usera = UserPreferences.objects.get(user=request.user)



    expense = Expense.objects.get(pk=id)
    categories = Category.objects.filter(owner=request.user)
    budynek = Budynek.objects.filter(owner=request.user)
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
        'waluta_usera': waluta_usera,
        'currencies': waluty_data,
        'budynki': budynek,
    }
    if request.method == "GET":
        return render(request, "expenses/edit-expense.html", context)

    if request.method == "POST":

        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Kwota jest wymagana')
            return render(request, 'expenses/edit_expanse.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']

        waluta = request.POST['waluta']

        category = request.POST.get('category', 'Nie podano')

        budynek = request.POST.get('budynek', 'Nie podano')
        if not description:
            messages.error(request, 'Opis jest wymagany')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.waluta = waluta
        expense.budynek = budynek
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated successfully ')

        return redirect('expenses')

    # else:
    #
    #     messages.info(request, 'Handling postpone')
    #
    #     return render(request, "expenses/edit-expense.html", context)

@login_required(login_url='/authentication/login')
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted')
    return redirect('expenses')


# def export_csv(request):
#
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=Expenses'+str(datetime.datetime.now())+'.csv'
#
#     writer = csv.writer(response)
#     writer.writerow(['Amount', 'Description', 'Category', 'Date'])
#
#     expenses = Expense.objects.filter(owner=request.user)
#
#     for expense in expenses:
#         writer.writerow([expense.amount, expense.description, expense.category, expense.date])
#
#     return response
#
# def export_excel(request):
#
#
#
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename=Zestawienie Transakcji ' + str(datetime.datetime.now()) + '.xls'
#
#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Wydatki')
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#
#     columns = ['Kwota', 'Waluta', 'Lokalizajca', 'Kategoria', 'Opis', 'Data']
#
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)
#
#     font_style = xlwt.XFStyle()
#
#     rows = Expense.objects.filter(owner=request.user).values_list('amount', 'waluta', 'budynek', 'category', 'description', 'date')
#
#     for row in rows:
#         row_num+=1
#
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, str(row[col_num]), font_style)
#
#     # wb.save(response)
#
#
#     ws2 = wb.add_sheet('Przychody')
#     row_num1 = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     #
#     columns1 = ['Kwota', 'Waluta', 'Lokalizajca', 'Źródło', 'Opis', 'Data']
#     #
#     for col_num in range(len(columns1)):
#         ws2.write(row_num1, col_num, columns1[col_num], font_style)
#
#     font_style = xlwt.XFStyle()
#
#     rows1 = UserIncome.objects.filter(owner=request.user).values_list('amount', 'waluta', 'budynek', 'source',
#                                                                   'description', 'date')
#
#     for row in rows1:
#         row_num1 += 1
#
#         for col_num in range(len(row)):
#             ws2.write(row_num1, col_num, str(row[col_num]), font_style)
#     #
#     #
#     wb.save(response)
#
#     return response



