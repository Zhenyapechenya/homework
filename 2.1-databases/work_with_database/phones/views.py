from django.http import HttpResponse
from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    context = {}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {}
    return render(request, template, context)


def create_phone(request):
    phone = Phone(name='test', price=0.00, lte_exists=True)
    phone.save()
    return HttpResponse(f'all good. new phone {phone.name}, {phone.price}')

def list_phone(request):
    phone_objects = Phone.objects.all()
    phones = [f'{p.name}, {p.price}, {p.slug}' for p in phone_objects]
    return HttpResponse('<br>'.join(phones))