from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import MenuItem
from .serializers import MenuItemSerializer
from django.core.paginator import Paginator, EmptyPage

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, throttle_classes

from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle

from .throttles import TenCallsPerMinute

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()
        category_name = request.query_params.get('category__title')
        to_price = request.query_params.get('price')
        search = request.query_params.get('title')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('page', default=2)

        if category_name:
            items = items.filter(category__title=category_name)

        if to_price:
            items = items.filter(price__lte=to_price)

        if search:
            items = items.filter(title__icontains=search)

        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(page)
        except EmptyPage:
            items = []

        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def single_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'GET':
        serializer = MenuItemSerializer(item)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MenuItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Some secret message"})
    else:
        return Response({'message':"User not authorized"}, 403)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"Successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message":"Successful message for logged in users only"})