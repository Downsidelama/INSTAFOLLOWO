from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import InstagramAccount


@login_required
def index(request):
    context = {
        'user_number': User.objects.count(),
        'insta_number': InstagramAccount.objects.count(),
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def accounts(request):
    context = {
        'accounts': list(InstagramAccount.objects.filter(user_id=request.user.id)),
        'account_count': InstagramAccount.objects.filter(user_id=request.user.id).count(),
    }
    return render(request, 'dashboard/accounts.html', context)


@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')


class AddAccount(LoginRequiredMixin, View):
    def get(self, request):
        return redirect(reverse('dashboard:accounts'))
