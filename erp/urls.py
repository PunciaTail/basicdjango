from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('inputpd/', views.product_create, name='inputpd'),
    path('mall/', views.show_mall, name='mall'),
    path('adminmall/', views.product_list, name='adminmall'),
    path('inbound/<int:id>', views.inbound_create, name='inbound'),
    path('outbound/<int:id>', views.outbound_create, name='outbound'),
]
