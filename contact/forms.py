from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Votre nom')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Votre email')}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Votre téléphone (optionnel)')}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Sujet de votre message')}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Votre message'), 'rows': 5}),
        }
        labels = {
            'name': _('Nom'),
            'email': _('Email'),
            'phone': _('Téléphone'),
            'subject': _('Sujet'),
            'message': _('Message'),
        } 