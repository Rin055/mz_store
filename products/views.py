
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ProductPagination
from .serializers import ProductSerializer

# @api_view(['GET', 'POST'])
# def products(request):
#     if request.method == "GET":
#         products = Product.objects.all()
#         product_list = []

#         for product in products:
#             product_data = {
#                 'id': product.id,
#                 'name': product.name,
#                 'description': product.description,
#                 'price': product.price,
#                 'currency': product.currency,
#             }
#             product_list.append(product_data)

#         return Response({'products': product_list})
#     elif request.method == "POST":
#         data = request.data
#         serializer = ProductSerializer(data=data)
#         if serializer.is_valid():
#             new_product = Product.objects.create(
#                 name=data.get("name"),
#                 description=data.get("description"),
#                 price=data.get("price"),
#                 currency=data.get("currency"),
#             )

#             return Response({"new product": {
#                 'id': new_product.id,
#                 'name': new_product.name,
#                 'description': new_product.description,
#                 'price': new_product.price,
#                 'currency': new_product.currency,
#             }}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def products(request):
    if request.method == "GET":
        queryset = Product.objects.all()

        price = request.GET.get('price')
        if price is not None:
            queryset = queryset.filter(price=price)

        currency = request.GET.get('currency')
        if currency:
            queryset = queryset.filter(currency=currency)

        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        paginator = ProductPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            product = serializer.save()

            return Response({"new product": product.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from .serializers import ReviewSerializer, CartSerializer
from .models import Review, Cart


@api_view(['GET', 'POST'])
def review_view(request):
    if request.method == 'GET':
        queryset = Review.objects.all()

        product_id = request.GET.get('product_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        rating = request.GET.get('rating')
        if rating:
            queryset = queryset.filter(rating=rating)

        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(content__icontains=search)

        paginator = ProductPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ReviewSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            review = serializer.save()
            return Response(
                {'id': review.id, 'message': 'Review created successfully!'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class ProductView(APIView):
    def get(self, request):
        queryset = Product.objects.all()

        price = request.GET.get('price')
        if price is not None:
            queryset = queryset.filter(price=price)

        currency = request.GET.get('currency')
        if currency:
            queryset = queryset.filter(currency=currency)

        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        paginator = ProductPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    










from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)

from .models import Product
from .serializers import ProductSerializer


class ProductAPIView(RetrieveModelMixin,
                    CreateModelMixin,
                    ListModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['price', 'currency']
    search_fields = ['name', 'description']
    pagination_class = ProductPagination

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    



from rest_framework.permissions import IsAuthenticated

from .models import FavoriteProduct  
from .serializers import FavoriteProductSerializer  


class FavoriteProductViewSet(ListModelMixin,
                            CreateModelMixin,
                            DestroyModelMixin,
                            RetrieveModelMixin,
                            GenericAPIView):
    
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['product', 'user']
    search_fields = ['product__name']
    pagination_class = ProductPagination

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)








class CartView(ListModelMixin,
            CreateModelMixin,
            GenericAPIView):
    
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['products', 'user']
    search_fields = ['products__name']
    pagination_class = ProductPagination

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, pk=None, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


from .models import ProductTag
from .serializers import ProductTagSerializer

class TagView(ListModelMixin, GenericAPIView):
    
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    pagination_class = ProductPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

class TagList(ListAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    pagination_class = ProductPagination


class ReviewView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['product', 'rating']
    search_fields = ['content']
    pagination_class = ProductPagination

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(product_id=self.kwargs['product_id'])
        return queryset













class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['price', 'currency']
    search_fields = ['name', 'description']
    pagination_class = ProductPagination


    # http_method_names = ['get', 'post', 'delete']




















from .models import ProductImage
from .serializers import ProductImageSerializer


class ProductImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['product']
    search_fields = ['product__name']
    pagination_class = ProductPagination

    def get_queryset(self):
        return self.queryset.filter(product__id=self.kwargs['product_pk'])
