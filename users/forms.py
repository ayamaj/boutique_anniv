from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')})
    )
    first_name = forms.CharField(
        label=_('Prénom'),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Prénom')})
    )
    last_name = forms.CharField(
        label=_('Nom'),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nom')})
    )
    phone = forms.CharField(
        label=_('Téléphone'),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Téléphone')})
    )
    address = forms.CharField(
        label=_('Adresse'),
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Adresse'), 'rows': 3})
    )
    postal_code = forms.CharField(
        label=_('Code postal'),
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Code postal')})
    )
    city = forms.CharField(
        label=_('Ville'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ville')})
    )
    newsletter = forms.BooleanField(
        label=_('Je souhaite recevoir la newsletter'),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'postal_code', 'city', 'newsletter', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Mot de passe')})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Confirmation du mot de passe')})
        self.fields['newsletter'].widget.attrs.update({'class': 'form-check-input'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Cette adresse email est déjà utilisée.'))
        return email

class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label=_('Prénom'),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label=_('Nom'),
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label=_('Téléphone'),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label=_('Adresse'),
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    postal_code = forms.CharField(
        label=_('Code postal'),
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        label=_('Ville'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    newsletter = forms.BooleanField(
        label=_('Je souhaite recevoir la newsletter'),
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'postal_code', 'city', 'newsletter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)  # Supprimer le champ password qui n'est pas nécessaire 