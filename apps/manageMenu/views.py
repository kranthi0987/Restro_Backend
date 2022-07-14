from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.manageMenu.models import Menu, SubMenu, Item
from apps.manageMenu.serializer import CreateMenuSerializer, CreateSubMenuSerializer, CreateItemSerializer


# Menu
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_menu(request):
    # Getting the list of patients or create Patient
    if request.method == 'POST':
        serializer = CreateMenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def menu_list(request):
    """
    List all Hotel.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        hotels = Menu.objects.all()
        serializer = CreateMenuSerializer(hotels, context={'request': request}, many=True)
        return Response({'menus': serializer.data})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def menu_list_byid(request):
    """
    List all hotels by Doc id.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        products = Menu.objects.filter(id=request.data['id'])
        serializer = CreateMenuSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def menu_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    try:
        menu = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CreateMenuSerializer(menu, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CreateMenuSerializer(menu, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        menu.delete()
        return Response({'message': 'removed successfully'}, status=status.HTTP_204_NO_CONTENT)


# SubMenu
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_submenu(request):
    # Getting the list of patients or create Patient
    if request.method == 'POST':
        serializer = CreateSubMenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def submenu_list(request):
    """
    List all Hotel.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        hotels = Menu.objects.all()
        serializer = CreateSubMenuSerializer(hotels, context={'request': request}, many=True)
        return Response({'submenu': serializer.data})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def submenu_list_byid(request):
    """
    List all hotels by Doc id.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        products = SubMenu.objects.filter(id=request.data['id'])
        serializer = CreateSubMenuSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def submenu_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    # permission_classes = (IsAuthenticated,)
    # authentication_class = JSONWebTokenAuthentication

    try:
        product = SubMenu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CreateSubMenuSerializer(product, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CreateSubMenuSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Items
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_item(request):
    # Getting the list of patients or create Patient
    if request.method == 'POST':
        serializer = CreateItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def item_list(request):
    """
    List all Hotel.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        hotels = Menu.objects.all()
        serializer = CreateItemSerializer(hotels, context={'request': request}, many=True)
        return Response({'items': serializer.data})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def item_list_byid(request):
    """
    List all hotels by Doc id.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        products = Item.objects.filter(id=request.data['id'])
        serializer = CreateItemSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def item_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    # permission_classes = (IsAuthenticated,)
    # authentication_class = JSONWebTokenAuthentication

    try:
        product = Item.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CreateItemSerializer(product, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CreateItemSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
