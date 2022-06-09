from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.hotelMangement.models import Hotels
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
    List all Hotels.
    """
    # Getting the list of Hotels
    if request.method == 'POST':
        hotels = Hotels.objects.all()
        serializer = CreateHotelSerializer(hotels, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def hotel_list_byid(request):
    """
    List all hotels by Doc id.
    """
    # Getting the list of Hotel
    if request.method == 'POST':
        products = Hotels.objects.filter(doc_id_id=request.data['doc_id'])
        serializer = CreateHotelSerializer(products, context={'request': request}, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def patient_count_by_id(request):
    """
    List all products, or create a new product.
    """
    # Getting the list of patients or create Patient
    if request.method == 'POST':
        products = Hotels.objects.filter(doc_id_id=request.data['doc_id']).count()
        return Response(products)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def hotel_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    # permission_classes = (IsAuthenticated,)
    # authentication_class = JSONWebTokenAuthentication

    try:
        product = Hotels.objects.get(pk=pk)
    except Hotels.DoesNotExist:
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
