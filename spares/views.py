from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Extract
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from .models import Item, OrderItem, Order, Sale
from cars.models import Car
from django.db.models import Q

# Create your views here.


class HomePageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        spares = Item.objects.all()
        paginate_by = 1
        cars = Car.objects.all()
        template_name = 'spares/index.html'
        context = {
            'spares': spares,
            'cars': cars
        }
        return render(request, template_name, context)

    # def get(self, request, *args, **kwargs):
    #     spares = None
    #     cars = Car.objects.all()
    #     carId = request.GET.get('car_id')
    #     if carId:
    #         print("Your in Bmw cars")
    #         spares = Item.objects.filter(carId)
    #     else:
    #         print("you in all products")
    #         spares = Item.objects.all()
    #     template_name = 'spares/index.html'
    #     context = {
    #         'spares': spares,
    #         'cars':cars
    #     }
    #     return render(request, template_name, context)

    def get_seccuss_url(self):
        return reverse("spares:product-order")


class CarView(View):
    def get(self, request, id, *args, **kwargs):
        car_item = Car.objects.all()
        cars = Car.objects.get(id=id)
        spares = Item.objects.filter(car=cars)
        template_name = 'spares/car_category.html'
        context = {
            'spares': spares,
            'cars': 'cars',
            'car_item': car_item
        }
        return render(request, template_name, context)


class OrderPageView(View):
    def get(self, request, pk, *args, **kwargs):
        products = Item.objects.get(pk=pk)
        orders = get_object_or_404(Order, user=request.user, ordered=False)
        order_items = OrderItem.objects.filter(order=orders)
        template_name = 'spares/order_page.html'
        context = {
            'products': products,
            'order_items': order_items,
            'orders': orders
        }
        return render(request, template_name, context)

    def get_seccuss_url(self):
        return reverse("spares:product-order")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            orders = get_object_or_404(Order, user=request.user, ordered=False)
            order_items = OrderItem.objects.filter(order=orders)
            template_name = 'spares/order_summary.html'
            context = {
                'order_items': order_items,
                'orders': orders
            }
            return render(request, template_name, context)
        except ObjectDoesNotExist:
            return redirect('/')


class OrderView(View):
    def get(self, request, pk,  *args, **kwargs):
        item = get_object_or_404(Item, pk=pk)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
            else:
                order.items.add(order_item)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(
                user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            order.save()

        return redirect("spares:products", pk=pk)


class SalesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "spares/sale_summary.html")

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        try:
            amount = order.get_total()

            # create sales
            sales = Sale()
            sales.user = self.request.user
            sales.amount = amount
            sales.save()

            # asseign sale to order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.sale = sales
            order.save()

            return redirect('spares:sale-summary')
        except ObjectDoesNotExist:
            print("item saled successefully")
            return redirect('spares:sale-summary')


class SalesSummaryView(View):
    def get(self, request, *args, **kwargs):

        template_name = 'spares/sale_summary.html'
        sales = Sale.objects.all()
        orders = Order.objects.exclude(user=request.user, ordered=False)
        paginate_by = 1
        context = {
            'orders': orders,
            'sales': sales,
        }
        return render(request, template_name, context)


def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
    return redirect("spares:products", pk=pk)


def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                ordered=False,
                user=request.user
            )[0]
            order.items.remove(order_item)
        else:
            return redirect("spares:products")
    else:
        return redirect("spares:products")
    return redirect("/")


def remove_single_item_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                ordered=False,
                user=request.user
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                return redirect('/')
        else:
            return redirect("spares:products")
    return redirect('spares:products', pk=pk)
