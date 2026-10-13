from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer, DepositSerializer, WithdrawSerializer, TransferSerializer


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        account = self.get_object()
        serializer = DepositSerializer(data=request.data, context={'account': account})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AccountSerializer(account).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        account = self.get_object()
        serializer = WithdrawSerializer(data=request.data, context={'account': account})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AccountSerializer(account).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        account = self.get_object()
        serializer = TransferSerializer(data=request.data, context={'account': account})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(AccountSerializer(account).data, status=status.HTTP_200_OK)
