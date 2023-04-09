from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Product, Inbound, Outbound
from django.db.models import F
from .forms import ProductForm, InboundForm, OutboundForm


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/mall')
    else:
        return redirect('/sign-in')


@login_required
def product_list(request):
    all_product = Product.objects.all()
    return render(request, 'product/product_list.html', {'erp': all_product})


@login_required
def product_create(request):
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product/inputproduct.html', {'productform': form})
    elif request.method == 'POST':
        new_product_form = ProductForm(request.POST)
        if new_product_form.is_valid():
            new_product_form.save()
            return redirect('/adminmall')
        else:
            return redirect('/inputpd')


@login_required
@transaction.atomic
def inbound_create(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'GET':
        inboundinform = InboundForm()
        contents = {
            'inboundform': inboundinform,
        }
        return render(request, 'product/inbound_create.html', contents)

    elif request.method == 'POST':
        inbound_form = InboundForm(request.POST)
        inbound_post_form = inbound_form.save(commit=False)
        inbound_post_form.save()

        # 그냥 바로 product에 붙임
        Product.objects.filter(name=inbound_post_form.name).update(
            quantity=F('quantity') + inbound_post_form.quantity)

        return redirect('/adminmall')


@login_required
def show_mall(request):
    all_product = Product.objects.all()
    return render(request, 'product/mall_list.html', {'shopping': all_product})


@login_required
def outbound_create(request, id):
    if request.method == 'GET':
        outboundinform = OutboundForm()
        contents = {
            'outboundform': outboundinform,
        }
        return render(request, 'product/outbound_create.html', contents)

    elif request.method == 'POST':
        outbound_form = OutboundForm(request.POST)
        outbound_post_form = outbound_form.save(commit=False)
        outbound_post_form.save()

        Product.objects.filter(name=outbound_post_form.name).update(
            quantity=F('quantity') - outbound_post_form.quantity)

        return redirect('/mall')
