from django.shortcuts import render
from django.views import View
from giving.models import Donation, Insitution
from django.db.models import Sum
from django.core.paginator import Paginator

# Create your views here.
class LandingPage(View):
    def get(self, request):
        supported_institution = set()
        all_insitutions = Insitution.objects.all()
        for institution in all_insitutions:
            supported_institution.add(institution.name)
        foundations = Insitution.objects.filter(type=1).order_by('id')
        paginator_foundations = Paginator(foundations,5)
        page = request.GET.get('page')
        foundations = paginator_foundations.get_page(page)
        non_governmental_organization = Insitution.objects.filter(type=2).order_by('id')
        paginator_nongover = Paginator(non_governmental_organization,5)
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
