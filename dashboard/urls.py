from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/new/', views.AddAccount.as_view(), name='add_account'),
    path('accounts/delete/<int:id>', views.DeleteAccount.as_view(), name='delete_account'),
    path('accounts/run/<int:id>', views.RunAccount.as_view(), name='run_account'),
    path('accounts/stop/<int:id>', views.StopAccount.as_view(), name='stop_account'),
    path('profile/', views.profile, name='profile')
]
