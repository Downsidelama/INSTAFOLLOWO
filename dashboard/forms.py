from django import forms


class AddInstagramAccountForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=100)  # Should encrypt this with private key, cba to it rn
    run_type = forms.CharField(max_length=30)
    hashtag = forms.CharField(max_length=30, required=False)
    other_profile = forms.CharField(max_length=30, required=False)
