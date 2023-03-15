from django.shortcuts import render
from django.views import View
from giving.models import Donation, Insitution
from django.db.models import Sum

# Create your views here.
class LandingPare(View):
    def get(self, request):
        supported_institution = set()
        all_insitutions = Insitution.objects.all()
        for institution in all_insitutions:
            supported_institution.add(institution.name)
        return render(request, 'index.html', context={
            "bags": Donation.objects.aggregate(Sum('quantity'))['quantity__sum'],
            'supported_institutions': len(supported_institution)
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
