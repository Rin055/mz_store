from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer
from products.pagination import ProductPagination

User = get_user_model()


@api_view(['GET', 'POST'])
def user_view(request):
    users = User.objects.all()

    username = request.GET.get('username')
    if username:
        users = users.filter(username=username)

    email = request.GET.get('email')
    if email:
        users = users.filter(email=email)

    first_name = request.GET.get('first_name')
    if first_name:
        users = users.filter(first_name=first_name)

    last_name = request.GET.get('last_name')
    if last_name:
        users = users.filter(last_name=last_name)

    search = request.GET.get('search')
    if search:
        users = users.filter(
            username__icontains=search
        ) | users.filter(
            email__icontains=search
        ) | users.filter(
            first_name__icontains=search
        ) | users.filter(
            last_name__icontains=search
        )

    paginator = ProductPagination()
    page = paginator.paginate_queryset(users, request)
    user_list = []

    for user in page:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        user_list.append(user_data)

    return paginator.get_paginated_response({'users': user_list})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for browsing users with filters/search/pagination."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email', 'first_name', 'last_name']
