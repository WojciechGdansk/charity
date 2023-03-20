from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from giving.models import Donation, Insitution, Category
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from giving.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages


def activate_email(user, request, to_email):
    mail_subject = "Activate your account"
    message = render_to_string('activate_account.html', {
        "user": user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


def recover_password(user, request, to_email):
    mail_subject = "Password recovery"
    message = render_to_string('recover_password.html', {
        "user": user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send()


# Create your views here.
class LandingPage(View):
    def get(self, request):
        supported_institution = set()
        all_donations = Donation.objects.all()
        for institution in all_donations:
            supported_institution.add(institution.institution.name)
        foundations = Insitution.objects.filter(type=1).order_by('id')
        paginator_foundations = Paginator(foundations, 5)
        page = request.GET.get('page')
        # foundations = paginator_foundations.get_page(page)
        non_governmental_organization = Insitution.objects.filter(type=2).order_by('id')
        paginator_nongover = Paginator(non_governmental_organization, 5)
        # non_governmental_organization = paginator_nongover.get_page(page)
        local_collection = Insitution.objects.filter(type=3).order_by('id')
        paginator_local_collections = Paginator(local_collection, 5)
        # local_collection = paginator_local_collections.get_page(page)
        return render(request, 'index.html', context={
            "bags": Donation.objects.aggregate(Sum('quantity'))['quantity__sum'],
            'supported_institutions': len(supported_institution),
            "foundations": foundations,
            "non_governmental_organization": non_governmental_organization,
            "local_collection": local_collection
        })


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        foundations = Insitution.objects.all()
        return render(request, 'form.html', {"categories": categories,
                                             "foundations": foundations})

    def post(self, request):
        categories = request.POST.getlist('categories')
        quantity = request.POST.get('bags')
        organization_name = request.POST.get('organization')
        address = request.POST.get('address')
        city = request.POST.get("city")
        zip_code = request.POST.get("postcode")
        phone_number = request.POST.get("phone")
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get("more_info")
        user = request.user
        try:
            institution = Insitution.objects.get(name=organization_name)
        except ObjectDoesNotExist:
            return redirect(reverse('donate'))
        donation = Donation.objects.create(quantity=quantity, institution=institution, address=address,
                                           phone_number=phone_number, city=city, zip_code=zip_code,
                                           pick_up_date=pick_up_date, pick_up_time=pick_up_time,
                                           pick_up_comment=pick_up_comment, user=user)
        for category in categories:
            try:
                cat = Category.objects.get(name=category)
                donation.categories.add(cat)
            except ObjectDoesNotExist:
                continue

        return redirect(reverse('donate-complate'))


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('main'))
        else:
            messages.error(request, "Błędne dane")
            return redirect(reverse('register'))


# class Login(LoginView):
#     template_name = 'login.html'
#     print("dupa")
#
#     # redirect_authenticated_user = True
#
#     # def get_success_url(self):
#     #     if 'next' in self.request.GET:
#     #         return self.request.GET['next']
#     #     else:
#     #         return reverse_lazy('main')
#     def get(self, request, *args, **kwargs):
#         return render(request, 'login.html')
#
#     def post(self, request, *args, **kwargs):
#         username = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect(reverse('main'))
#         else:
#             return redirect(reverse('register'))


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        username = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        error_msg = ''

        if password != password2:
            error_msg = "Podane hasła nie są identyczne\n"

        if User.objects.filter(username=username).exists():
            error_msg += "Podany użytkownik już istnieje\n"
        try:
            validate_email(username)
        except ValidationError:
            error_msg += "Niepoprawny adres email"

        if error_msg:
            return render(request, "register.html", {'error_msg': error_msg})

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            is_active=False
        )
        activate_email(user, request, user.username)
        return redirect(reverse("login"))


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('main'))


class DonateConfirmation(View):
    def get(self, request):
        return render(request, "form-confirmation.html")


class Profile(View):
    def get(self, request):
        return render(request, 'user_profile.html')


class DonatedItems(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        donations = Donation.objects.filter(user=user).order_by("is_taken", "pick_up_date", "pick_up_date")
        return render(request, 'user_donated.html', {"donations": donations})


class CollectedChangeView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            donation = Donation.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse({"status": "false"}, status=500)
        user = request.user
        if donation.user != user:
            return JsonResponse({"status": "false"}, status=500)
        if donation.is_taken == False:
            donation.is_taken = True
        elif donation.is_taken == True:
            donation.is_taken = False
        donation.save()
        return JsonResponse({"status": "true"}, status=200)


class EditUser(LoginRequiredMixin, View):
    def get(self, request, id):
        user_from_id = User.objects.get(id=id)
        user = request.user
        if user != user_from_id:
            return redirect(reverse('main'))
        return render(request, 'edit_user.html')

    def post(self, request, id):
        user_from_id = User.objects.get(id=id)
        user = request.user
        if user != user_from_id:
            return redirect(reverse('main'))

        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        oldpassword = request.POST.get('oldpassword')

        if password != password2:
            error_msg = "Podane hasła nie są identyczne"
            return render(request, "edit_user.html", {'error_msg': error_msg})

        if user_from_id.check_password(oldpassword) is False:
            error_msg = "Błędne hasło"
            return render(request, "edit_user.html", {'error_msg': error_msg})

        user_from_id.set_password(password)
        user_from_id.save()
        return redirect(reverse('main'))


class Activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(reverse('login'))
        return redirect(reverse('main'))


class PasswordRecovery(View):
    def get(self, request):
        return render(request, "password_recovery.html")

    def post(self, request):
        username = request.POST.get('email')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Nie ma takiego użytkownika")
            return redirect(reverse('main'))
        else:
            recover_password(user, request, user.username)
            messages.success(request, 'Sprawdź pocztę')
            return redirect(reverse('main'))

class Recover(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            return render(request, "set_new_password.html")
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password != password2:
                error_msg = "Podane hasła nie są identyczne"
                return render(request, "set_new_password.html", {'error_msg': error_msg})
            user.set_password(password)
            messages.success(request, "Zmieniono hasło")
            return redirect(reverse('login'))