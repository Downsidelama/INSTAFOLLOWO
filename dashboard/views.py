from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from .models import InstagramAccount
from .forms import AddInstagramAccountForm
from .entity.run_type import RunType


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
        'run_types': RunType.get_types_and_descriptions(),
    }
    return render(request, 'dashboard/accounts.html', context)


@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')


class AddAccount(LoginRequiredMixin, View):
    def get(self, request):
        context = {"errors": [], "run_types": RunType.get_types_and_descriptions()}
        return render(request, 'dashboard/add_account.html', context=context)

    def post(self, request: HttpRequest):
        context = {"errors": [], "run_types": RunType.get_types_and_descriptions()}
        add_account_form = AddInstagramAccountForm(request.POST)

        if add_account_form.is_valid():
            errors = []
            instagram_account = InstagramAccount()
            instagram_account.username = add_account_form.cleaned_data.get('username')
            instagram_account.user_id = request.user
            instagram_account.started = False
            instagram_account.hashtag = add_account_form.cleaned_data.get("hashtag")
            instagram_account.other_profile = add_account_form.cleaned_data.get("other_profile")
            if len(instagram_account.hashtag) == 0 and len(instagram_account.other_profile) == 0:
                errors.append("Fill in either the hashtag or the other profile field.")
            instagram_account.run_type = add_account_form.cleaned_data.get("run_type")
            if instagram_account.run_type not in RunType.get_run_types():
                errors.append("Invalid run type!")

            if len(errors) == 0:
                instagram_account.save()
                return redirect(reverse('dashboard:accounts'))
            else:
                context.get("errors").extend(errors)
                return render(request, 'dashboard/add_account.html', context=context)
        else:
            context = {"errors": ["Please fill in the fields."], "run_types": RunType.get_types_and_descriptions()}
            return render(request, 'dashboard/add_account.html', context=context)
            # return redirect(reverse('dashboard:add_account'))


class DeleteAccount(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, id, *args, **kwargs):
        instagram_account = InstagramAccount.objects.get(id=id)
        if request.user == instagram_account.user_id:
            instagram_account.delete()
        return redirect(reverse('dashboard:accounts'))


class BotStatus(LoginRequiredMixin, View):
    def get(self, request):
        pass
