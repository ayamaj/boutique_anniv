from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from .models import Message
from .forms import MessageForm

def contact_form(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save()
            
            # Envoyer un email de notification
            send_mail(
                _('Nouveau message de contact'),
                _('Vous avez reçu un nouveau message de contact de {name} ({email}).\n\nSujet: {subject}\nMessage: {message}').format(
                    name=message.name,
                    email=message.email,
                    subject=message.subject,
                    message=message.message
                ),
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, _('Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.'))
            return redirect('contact:contact_success')
    else:
        form = MessageForm()
    
    return render(request, 'contact/contact_form.html', {'form': form})

def contact_success(request):
    return render(request, 'contact/contact_success.html')
