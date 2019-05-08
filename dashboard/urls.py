from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/new/', views.AddAccount.as_view(), name='add_account'),
    path('accounts/delete/<int:id>', views.DeleteAccount.as_view(), name='delete_account'),
    path('profile/', views.profile, name='profile')
]
