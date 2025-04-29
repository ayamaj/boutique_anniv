from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import Order, OrderItem
from shopping_cart.cart import Cart
from .forms import OrderCreateForm
import stripe
import logging

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def order_create(request):
    cart = Cart(request)
    if cart.get_total_price() == 0:
        messages.warning(request, _("Votre panier est vide."))
        return redirect('shopping_cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                # Création de la commande
                order = form.save(commit=False)
                order.user = request.user
                order.total_price = cart.get_total_price()
                order.save()  # Première sauvegarde pour obtenir un ID
                
                # Création des articles de commande
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                
                # Mise à jour finale de la commande
                order.save()
                cart.clear()
                request.session['order_id'] = order.id
                return redirect('orders:payment_process', order_id=order.id)
            
            except Exception as e:
                logger.error(f"Erreur création commande: {str(e)}", exc_info=True)
                messages.error(request, _("Une erreur est survenue lors de la création de la commande."))
                return redirect('shopping_cart:cart_detail')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        if hasattr(request.user, 'profile'):
            initial_data.update({
                'phone': request.user.profile.phone,
                'address': request.user.profile.address,
                'postal_code': request.user.profile.postal_code,
                'city': request.user.profile.city,
            })
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form,
    })

@login_required
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_status == 'paid':
        messages.warning(request, _("Cette commande a déjà été payée."))
        return redirect('orders:order_detail', order_id=order.id)
    
    if request.method == 'POST':
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),
                currency='eur',
                metadata={'order_id': order.id},
                automatic_payment_methods={'enabled': True},
            )
            order.stripe_payment_intent = payment_intent['id']
            order.save()
            
            return render(request, 'orders/payment_process.html', {
                'order': order,
                'client_secret': payment_intent['client_secret'],
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            })
        except stripe.error.StripeError as e:
            messages.error(request, _("Une erreur est survenue lors du paiement: {}").format(str(e)))
            return redirect('orders:order_detail', order_id=order.id)
    
    return render(request, 'orders/payment_process.html', {
        'order': order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })

@login_required
def payment_done(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.payment_status = 'paid'
        order.save()
        del request.session['order_id']
        messages.success(request, _('Votre paiement a été effectué avec succès.'))
        return render(request, 'orders/payment_done.html', {'order': order})
    messages.error(request, _('Aucune commande trouvée.'))
    return redirect('products:product_list')

@login_required
def payment_canceled(request):
    messages.warning(request, _('Votre paiement a été annulé.'))
    return render(request, 'orders/payment_canceled.html')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/order_list.html', {'orders': orders})