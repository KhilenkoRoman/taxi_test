from django.shortcuts import render
from django.contrib.auth import authenticate, login
import re
from core.models.cars import Car
from core.models.orders import Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.shortcuts import redirect

def index(request):
    context = {
        'errors': []
    }

    if request.method == 'POST':
        context['name'] = request.POST.get('name', '')
        if not request.POST.get('name'):
            context['errors'].append('введите имя')
        elif not re.search(r'^[а-яА-ЯёЁ ]+$', request.POST.get('name')):
            context['errors'].append('имя - только кириллица')

        context['phone'] = request.POST.get('phone', '')
        if not request.POST.get('phone', ''):
            context['errors'].append('введите телефон')
        elif not re.search(r'^\+380\([0-9]{2}\)[0-9]{3}-[0-9]{2}-[0-9]{2}', request.POST.get('phone')):
            context['errors'].append('не корректный формат телефона \n +380(ХХ)ХХХ-ХХ-ХХ')

        context['order_address'] = request.POST.get('order_address', '')
        if not request.POST.get('order_address'):
            context['errors'].append('введите адресс откуда')

        context['target_address'] = request.POST.get('target_address', '')
        if not request.POST.get('target_address'):
            context['errors'].append('введите адрес куда')

        if not context['errors']:
            free_car = Car.objects.filter(is_available=True).first()
            if free_car:
                order = Order.objects.create(
                    name=request.POST.get('name'),
                    phone_number=request.POST.get('phone'),
                    order_address=request.POST.get('order_address'),
                    target_address=request.POST.get('target_address'),
                    status='active',
                    car=free_car
                )
                free_car.is_available = False
                free_car.save()
                context['result'] = True
                context['car_model'] = free_car.model
                context['order_id'] = order.id
                return render(request, 'index.html', context)
            else:
                context['result'] = False
                return render(request, 'index.html', context)

    return render(request, 'index.html', context)


def sign_up(request):
    context = {
        'errors': []
    }

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('login'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('orders')
        context['errors'].append('wrong login or password')
        context['login'] = username = request.POST.get('login')

    return render(request, 'sign_up.html', context)


def orders(request):
    print('qwe')
    print(request.user)
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'errors': []
    }

    paginator = Paginator(Order.objects.all().order_by('date_created'), 2)

    page = request.GET.get('page')
    try:
        context['orders'] = paginator.page(page)
    except PageNotAnInteger:
        context['orders'] = paginator.page(1)
    except EmptyPage:
        context['orders'] = paginator.page(paginator.num_pages)

    return render(request, 'order_list.html', context)

def order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'errors': []
    }

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")
    context['order'] = order

    return render(request, 'order.html', context)

def end_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'errors': []
    }

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404("Order does not exist")
    context['order'] = order

    if order.status == 'inactive':
        return redirect('order', order_id=order_id)

    order.car.is_available = True
    order.car.save()
    order.status = 'inactive'
    order.car = None
    order.save()
    return redirect('order', order_id=order_id)