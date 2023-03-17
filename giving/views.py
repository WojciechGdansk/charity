from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse
from django.views import View
from giving.models import Donation, Insitution, Category
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


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
            return redirect(reverse('register'))


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
