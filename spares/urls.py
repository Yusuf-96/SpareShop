from django.urls import path
from .views import (
    HomePageView, OrderPageView, OrderSummaryView,
    add_to_cart, remove_from_cart, remove_single_item_from_cart, OrderView, CarView, SalesView, SalesSummaryView
)

app_name = 'spares'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:pk>/product-order/', OrderPageView.as_view(), name='products'),
    path('<int:pk>/order/', OrderView.as_view(), name='order'),
    path('<int:pk>/sale/', SalesView.as_view(), name='sale'),
    path('car/<int:id>/', CarView.as_view(), name='car'),
    path('<int:pk>/add-to-cart', add_to_cart, name='add-to-cart'),
    path('<int:pk>/remove-from-cart', remove_from_cart, name='remove-from-cart'),
    path('<int:pk>/remove-item-from-cart',
         remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('sale-summary/', SalesSummaryView.as_view(), name='sale-summary'),
    # path('product-order/<slug:slug>', OrderPageView.as_view(), name='products'),
]
