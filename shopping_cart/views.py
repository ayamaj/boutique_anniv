from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from products.models import Product
from .cart import Cart

# Create your views here.

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override', False) == 'true'
    cart.add(product=product, quantity=quantity, override_quantity=override)
    messages.success(request, _('Le produit a été ajouté au panier.'))
    return redirect('shopping_cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, _('Le produit a été retiré du panier.'))
    return redirect('shopping_cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, _('La quantité a été mise à jour.'))
    else:
        cart.remove(product)
        messages.success(request, _('Le produit a été retiré du panier.'))
    return redirect('shopping_cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shopping_cart/cart_detail.html', {'cart': cart})
