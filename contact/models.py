from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Message(models.Model):
    STATUS_CHOICES = [
        ('new', _('Nouveau')),
        ('in_progress', _('En cours de traitement')),
        ('replied', _('Répondu')),
        ('closed', _('Fermé')),
    ]

    name = models.CharField(_('Nom'), max_length=100)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Téléphone'), max_length=20, blank=True)
    subject = models.CharField(_('Sujet'), max_length=200)
    message = models.TextField(_('Message'))
    reply = models.TextField(_('Réponse'), blank=True)
    status = models.CharField(_('Statut'), max_length=20, choices=STATUS_CHOICES, default='new')
    created = models.DateTimeField(_('Date de création'), auto_now_add=True)
    updated = models.DateTimeField(_('Date de mise à jour'), auto_now=True)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return f'{self.name} - {self.subject}'
