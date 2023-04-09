from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# model


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=256)
    price = models.IntegerField()
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )

    size = models.CharField(choices=sizes, max_length=1)
    quantity = models.IntegerField(default=0)
    image = models.URLField(
        max_length=256, default='https://img.freepik.com/free-photo/adorable-kitty-looking-like-it-want-to-hunt_23-2149167099.jpg')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.quantity = 0
        super().save(*args, **kwargs)
        # 생성될 때 stock quantity를 0으로 초기화 로직


class Inbound(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    create_date = models.DateField(auto_now=True)


class Outbound(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    create_date = models.DateField(auto_now=True)
