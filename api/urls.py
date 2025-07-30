from django.urls import path
from .views import *


urlpatterns = [
    path('buy/<int:item_id>/', buy_item, name='buy'),
    path('item/<int:item_id>/', item_detail, name='item'),
    path('buy-order/<int:order_id>/', buy_order, name='buy_order'),
    path('payment-intent/<int:item_id>/', payment_intent, name='payment_intent'),
    path('payment-intent-page/<int:item_id>/', payment_intent_page, name='payment_intent_page'),
    path('order/create/', create_order, name='create_order'),
    path('order/<int:order_id>/add/<int:item_id>/', add_item_to_cart, name='add_item_to_order'),
    path('order/<int:order_id>/', view_order, name='view_order'),
    path('order-page/', render_order, name='order_page'),
    path('', result_payment, name='result_payment'),
    path('order/<int:order_id>/add-discount/<int:discount_id>/', add_discount_to_order),
    path('order/<int:order_id>/add-tax/<int:tax_id>/', add_tax_to_order),
]