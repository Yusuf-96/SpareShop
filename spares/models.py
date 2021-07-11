from django.conf import settings
from django.db import models
from django.urls import reverse
from cars.models import Car
# Create your models here.


class Item(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    image = models.ImageField(max_length=254)
    description = models.TextField(blank=True, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='Car')
    capacity = models.IntegerField()

    # slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('spares:products', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('spares:add-to-cart', kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
        return reverse('spares:remove-from-cart', kwargs={'pk': self.pk})

    def get_add_to_sale(self):
        return reverse('spares:add-to-sale', kwargs={'pk': self.pk})

    def addtoorder(self):
        return reverse('spares:order', kwargs={'pk': self.pk})

    def sale(self):
        return reverse('spares:sale', kwargs={'pk': self.pk})

    # @staticmethod
    # def get_all_spare_by_carid(car_id):
    #     if car_id:
    #         return Item.objects.filter(car=car_id)
    #     else:
    #         return Item.objects.all()

    def __str__(self):
        return f'{self.item_name}'


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity}'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    # start_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    sale = models.ForeignKey(
        'Sale', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = ('-ordered_date', )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Sale(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.IntegerField()
    sales_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'
