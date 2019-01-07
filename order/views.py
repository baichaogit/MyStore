from django.shortcuts import render

# Create your views here.


def cart_views(request):
    return render(request, 'cart.html')




def pay_views(request):
    return render(request, 'place_order.html')