from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import stripe
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods


stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_item(request, item_id):
    """Получение Stripe Session ID для оплаты товаров"""
    item = get_object_or_404(Item, id=item_id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": item.currency,
                "product_data": {"name": item.name, "description": item.description},
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=request.build_absolute_uri('/') + '?success=true',
        cancel_url=request.build_absolute_uri('/') + '?cancel=true',
    )

    return JsonResponse({"session_id": session.id})


def item_detail(request, item_id):
    """Просмотр конкретного товара и его покупка по кнопке Buy"""
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail.html', {
        'item': item,
        'public_key': settings.STRIPE_PUBLIC_KEY,
    })


def buy_order(request, order_id):
    """Получение Stripe Session ID для оплаты заказа"""
    order = get_object_or_404(Order, id=order_id)
    line_items = []

    for item in order.items.all():
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {'name': item.name},
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
            'tax_rates': [order.tax.stripe_tax_id] if order.tax and order.tax.stripe_tax_id else [],
        })

    session_data = {
        "payment_method_types": ["card"],
        "line_items": line_items,
        "mode": "payment",
        "success_url": request.build_absolute_uri('/') + '?success=true',
        "cancel_url": request.build_absolute_uri('/') + '?cancel=true',
    }

    if order.discount and order.discount.stripe_coupon_id:
        session_data["discounts"] = [{"coupon": order.discount.stripe_coupon_id}]

    session = stripe.checkout.Session.create(**session_data)
    return JsonResponse({"session_id": session.id})


@csrf_exempt
@require_POST
def payment_intent(request, item_id):
    """Оплата с помощью Intent"""
    item = get_object_or_404(Item, id=item_id)

    intent = stripe.PaymentIntent.create(
        amount=int(item.price * 100),
        currency=item.currency,
        payment_method_types=["card"],
    )

    return JsonResponse({"client_secret": intent.client_secret})


def payment_intent_page(request, item_id):
    """Страница для оплаты с помощью Intent"""
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'payment_intent.html', {
        'item': item,
        'public_key': settings.STRIPE_PUBLIC_KEY,
    })

@csrf_exempt
@require_http_methods(['POST'])
def create_order(request):
    """Создание заказа"""
    order = Order.objects.create()
    return JsonResponse({"order_id": order.id})


@csrf_exempt
@require_http_methods(['POST'])
def add_item_to_cart(request, item_id, order_id):
    """Добавление товара в корзину"""
    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(Item, id=item_id)
    order.items.add(item)
    return JsonResponse({'msg': f'Item {item.name} added to cart'})


def view_order(request, order_id):
    """Просмотр заказа"""
    order = get_object_or_404(Order, id=order_id)
    items = [{"name": i.name, "price": float(i.price)} for i in order.items.all()]
    return JsonResponse({"order_id": order.id, "items": items})


def render_order(request):
    """Страница для составления и оплаты заказа"""
    items = Item.objects.all()
    discounts = Discount.objects.all()
    tax = Tax.objects.all()
    return render(request, 'order_page.html', {
        'items': items,
        'public_key': settings.STRIPE_PUBLIC_KEY,
        'discounts': discounts,
        'tax': tax,
    })


def result_payment(request):
    """Результат оплаты: success/cancel"""
    success = request.GET.get('success')

    if success:
        return render(request, 'success_payment.html')
    return render(request, 'cancel_payment.html')


@csrf_exempt
@require_http_methods(['POST'])
def add_discount_to_order(request, order_id, discount_id):
    """Добавление скидки к заказу"""
    order = get_object_or_404(Order, id=order_id)
    discount = get_object_or_404(Discount, id=discount_id)
    order.discount.add(discount)
    return JsonResponse({'msg': f'Discount {discount.name} added to order'})


@csrf_exempt
@require_http_methods(['POST'])
def add_tax_to_order(request, order_id, tax_id):
    """Добавление налога к заказу"""
    order = get_object_or_404(Order, id=order_id)
    tax = get_object_or_404(Tax, id=tax_id)
    order.tax.add(tax)
    return JsonResponse({'msg': f'Tax {tax.name} added to order'})


