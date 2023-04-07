from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product
from apps.products.serializers import (ProductCreationSerializer,
                                       ProductListSerializer,
                                       ProductDetailSerializer,
                                       ProductUpdateSerializer)


@extend_schema(tags=["product"])
class ProductCreationView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductCreationSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(seller=request.user)
            serializer.save()
            return Response({"detail": "You Successfully Listed A Product"}, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["product"])
class ProductListView(APIView):
    serializer_class = ProductListSerializer

    def get(self, request):
        product_information = Product.objects.all()
        if not product_information:
            return Response({"detail": "No Products To Show"}, status=status.HTTP_200_OK)
        serializer = ProductListSerializer(product_information, many=True)
        return Response(serializer.data)


@extend_schema(tags=["product"])
class ProductDetailView(APIView):
    serializer_class = ProductDetailSerializer

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product_information = Product.objects.filter(pk=pk)
        if not Product.objects.filter(pk=pk).exists():
            return Response({"message": "Product With This ID Does Not Exists"},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = ProductDetailSerializer(product_information, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["product"])
class ProductUpdateView(APIView):
    serializer_class = ProductUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        product_information = Product.objects.filter(pk=pk).first()
        serializer = ProductUpdateSerializer(instance=product_information, data=request.data, partial=True)
        product_owner = Product.objects.filter(seller=request.user)
        if product_owner == request.user:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Error"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["product"])
class ProductDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        product_information = self.get_object(pk)
        product_information.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
