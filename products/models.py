from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(models.Model):
    name = models.CharField(_('Nom'), max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Catégorie')
        verbose_name_plural = _('Catégories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,
                                related_name='products',
                                on_delete=models.CASCADE,
                                verbose_name=_('Catégorie'))
    name = models.CharField(_('Nom'), max_length=200, db_index=True)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(_('Image'), upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(_('Description'), blank=True)
    price = models.DecimalField(_('Prix'), max_digits=10, decimal_places=2)
    available = models.BooleanField(_('Disponible'), default=True)
    created = models.DateTimeField(_('Date de création'), auto_now_add=True)
    updated = models.DateTimeField(_('Date de mise à jour'), auto_now=True)
    featured = models.BooleanField(_('Mis en avant'), default=False)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
        verbose_name = _('Produit')
        verbose_name_plural = _('Produits')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])
