from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from django.views import View
from giving.models import Donation, Insitution
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.core.validators import validate_email


# Create your views here.
class LandingPage(View):
    def get(self, request):
        supported_institution = set()
        all_insitutions = Insitution.objects.all()
        for institution in all_insitutions:
            supported_institution.add(institution.name)
        foundations = Insitution.objects.filter(type=1).order_by('id')
        paginator_foundations = Paginator(foundations, 5)
        page = request.GET.get('page')
        foundations = paginator_foundations.get_page(page)
        non_governmental_organization = Insitution.objects.filter(type=2).order_by('id')
        paginator_nongover = Paginator(non_governmental_organization, 5)
        non_governmental_organization = paginator_nongover.get_page(page)
        local_collection = Insitution.objects.filter(type=3).order_by('id')
        paginator_local_collections = Paginator(local_collection, 5)
        local_collection = paginator_local_collections.get_page(page)
        return render(request, 'index.html', context={
            "bags": Donation.objects.aggregate(Sum('quantity'))['quantity__sum'],
            'supported_institutions': len(supported_institution),
            "foundations": foundations,
            "non_governmental_organization": non_governmental_organization,
            "local_collection": local_collection
        })


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


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

        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        return redirect(reverse("login"))
