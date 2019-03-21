from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import InstagramAccount


@login_required
def index(request):
    return render(request, 'dashboard/index.html')


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
