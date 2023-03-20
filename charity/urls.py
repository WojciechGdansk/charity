"""charity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from giving import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.LandingPage.as_view(), name='main'),
    path('donate/', views.AddDonation.as_view(), name="donate"),
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('donated/', views.DonateConfirmation.as_view(), name='donate-complate'),
    path('user_profile/', views.Profile.as_view(), name='user-profile'),
    path('donated_by_user/', views.DonatedItems.as_view(), name='donated-items'),
    path('change_if_collected/<int:id>', views.CollectedChangeView.as_view(), name='collected-change'),
    path('edit_password/<int:id>', views.EditUser.as_view(), name='edit-password'),
    path('activate/<uidb64>/<token>', views.Activate.as_view(), name='activate'),
    path('recover_password/', views.PasswordRecovery.as_view(), name='recover'),
    path('recover/<uidb64>/<token>', views.Recover.as_view(), name='recover-check'),
]
