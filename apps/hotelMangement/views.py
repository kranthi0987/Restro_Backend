from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.hotelMangement.models import Hotel
from apps.hotelMangement.serializer import CreateHotelSerializer


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_hotel(request):
    # Getting the list of patients or create Patient
    if request.method == 'POST':
        serializer = CreateHotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def hotel_list(request):
    """
    List all Hotel.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        hotels = Hotel.objects.all()
        serializer = CreateHotelSerializer(hotels, context={'request': request}, many=True)
        return Response({'hotels':serializer.data})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def hotel_list_byid(request):
    """
    List all hotels by Doc id.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        products = Hotel.objects.filter(id=request.data['id'])
        serializer = CreateHotelSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def hotel_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    # permission_classes = (IsAuthenticated,)
    # authentication_class = JSONWebTokenAuthentication

    try:
        product = Hotel.objects.get(pk=pk)
    except Hotel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CreateHotelSerializer(product, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CreateHotelSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
