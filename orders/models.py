from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('processing', _('En cours de traitement')),
        ('shipped', _('Expédiée')),
        ('delivered', _('Livrée')),
        ('cancelled', _('Annulée')),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', _('En attente')),
        ('paid', _('Payé')),
        ('failed', _('Échoué')),
        ('refunded', _('Remboursé')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    first_name = models.CharField(_('Prénom'), max_length=50)
    last_name = models.CharField(_('Nom'), max_length=50)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Téléphone'), max_length=20)
    address = models.CharField(_('Adresse'), max_length=250)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(_('Date de création'), auto_now_add=True)
    updated = models.DateTimeField(_('Date de mise à jour'), auto_now=True)
    status = models.CharField(_('Statut'), max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(_('Statut du paiement'), max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(_('Prix total'), max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-created']
        verbose_name = _('Commande')
        verbose_name_plural = _('Commandes')

    def __str__(self):
        return f'Commande {self.id} - {self.user.email}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.get_total_cost()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(_('Prix'), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_('Quantité'), default=1)

    class Meta:
        verbose_name = _('Élément de commande')
        verbose_name_plural = _('Éléments de commande')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity