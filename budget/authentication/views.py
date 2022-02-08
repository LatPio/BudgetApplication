from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from budget.settings import EMAIL_HOST_USER

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from userpreferences.models import UserPreferences
from expenses.models import Budynek, Category
from userincome.models import Source

import threading

# Create your views here.
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Nazwa Użytkownika powinna zawierać tylko cyfry oraz litery'}, status=400)


        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Nazwa Użytkownika zajęta'}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Nieprawidłowy adres e-mail'}, status=400)


        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'podany adres e-mail jest już przypisany do konta'}, status=409)
        return JsonResponse({'email_valid': True})


class RegisrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):


        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # currency = 'PLN - Polish Zloty'
        currency = 'Wybierz główną walutę'
        category = 'Stwórz własne w zakładce: Główne ustawienia'

        context = {'fieldValues': request.POST}

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():

                if len(password) < 6:
                    messages.error(request, 'password to short')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)

                user.is_active = False
                user.save()

                user_preferences = UserPreferences.objects.create(user=user, currency=currency)
                user_preferences.currency = currency
                user_preferences.save()

                # user_preferences1 = Category.objects.create(owner=user, name=category)
                # user_preferences1.name = category
                # user_preferences1.save()
                #
                # user_preferences2 = Source.objects.create(owner=user, name=category)
                # user_preferences2.name = category
                # user_preferences2.save()
                #
                #
                # user_preferences3 = Budynek.objects.create(owner=user, name=category)
                # user_preferences3.name = category
                # user_preferences3.save()


                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

                activate_url = 'http://' + domain + link

                email_subject = "Activate your acount"
                email_body = 'Witamy ' + user.username + '. Użyj tego linka do weyfikacji twojego konta: \n' + activate_url


                email = EmailMessage(
                    email_subject,
                    email_body,
                    EMAIL_HOST_USER,
                    [email],
                )

                EmailThread(email).start()

                messages.success(request, 'Konto zostało utworzone poprawnie. Sprawdź skrzynkę e-mali i aktuwuj konto dostarczonym linkiem.')
                return render(request, 'authentication/register.html')

        # messages.success(request, 'Sukces, utworzyłeś nowe konto')
        # messages.warning(request, 'Uwaga, utworzyłeś nowe konto')
        # messages.info(request, 'Informacja, utworzyłeś nowe konto')
        messages.error(request, 'Coś poszło nie tak... Powtórz rejestrację')

        return render(request, 'authentication/register.html')




class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login' + '?message=' + 'Użytkownik został już aktywowany')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Konto zostało porawnie aktywowane')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Witamy, ' + user.username + ' Jestś zalogowany')
                    return redirect('dashboard')

                messages.error(request, 'Konto nie jest aktywne, sprwadź e-mail')
                return render(request, 'authentication/login.html')

            messages.error(request, 'Niepoprawne dane, spróbuj ponownie  ')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Proszę uzupełnić wszsytkie pola ')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Zostałeś wylogowany')
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset_pass.html')

    def post(self, request):
        context = {'fieldValues': request.POST}

        email = request.POST['email']

        if not email:
            messages.error(request, 'Proszę podać prawidłowy adres e-mail')
            return render(request, 'authentication/reset_pass.html', context)


        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password',
                           kwargs={'uidb64': email_contents['uid'],
                                   'token': email_contents['token']
                                   })

            reset_url = 'http://' + current_site.domain + link

            email_subject = "Instrukcje do zmiany Hasła"
            email_body = 'Witamy ' '. Użyj tego linka do zresetowania twojego chasła: \n' + reset_url


            email = EmailMessage(
                email_subject,
                email_body,
                EMAIL_HOST_USER,
                [email],
            )

            EmailThread(email).start()

        messages.success(request, 'Wysłaliśmy do Ciebie e-maila z linkiem do zmiany hasła')



        return render(request, 'authentication/reset_pass.html')




class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        context = {
            'uidb64' : uidb64,
            'token': token,

        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.info(request, 'Link do resetowania chasła nie prawidłowy, wygeneruj ponownie')
                return render(request, 'authentication/set_new_password.html', context)

        except Exception as identifier:
            pass
        return render(request, 'authentication/set_new_password.html', context)



    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,

        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Hasła nie są takie same')
            return render(request, 'authentication/set_new_password.html', context)

        if len(password) < 6:
            messages.error(request, 'Zbyt krótkie hasło')
            return render(request, 'authentication/set_new_password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Hasło poprawnie zmienione, możesz teraz zalogować nowym hasłem')
            return redirect('login')
        except Exception as identifier:
            messages.info(request, 'Coś poszło nie tak, ponów operacje')
            return render(request, 'authentication/set_new_password.html', context)




