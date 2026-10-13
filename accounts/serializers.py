from decimal import Decimal
from django.db import transaction as db_transaction
from rest_framework import serializers
from .models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount', 'related_account', 'timestamp']
        read_only_fields = ['type', 'related_account', 'timestamp']


class AccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Account
        fields = ['id', 'username', 'balance', 'transactions', 'created_at']
        read_only_fields = ['balance']


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))

    def save(self, **kwargs):
        account = self.context['account']
        amount = self.validated_data['amount']

        account.balance += amount
        account.save()

        Transaction.objects.create(account=account, type='deposit', amount=amount)
        return account


class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))

    def validate_amount(self, value):
        account = self.context['account']
        if value > account.balance:
            raise serializers.ValidationError('Saldo insuficiente.')
        return value

    def save(self, **kwargs):
        account = self.context['account']
        amount = self.validated_data['amount']

        account.balance -= amount
        account.save()

        Transaction.objects.create(account=account, type='withdrawal', amount=amount)
        return account


class TransferSerializer(serializers.Serializer):
    to_account = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))

    def validate_to_account(self, value):
        if not Account.objects.filter(id=value).exists():
            raise serializers.ValidationError('Conta de destino não encontrada.')
        return value

    def validate(self, data):
        origin = self.context['account']
        if data['to_account'] == origin.id:
            raise serializers.ValidationError('Não é possível transferir para a própria conta.')
        if data['amount'] > origin.balance:
            raise serializers.ValidationError('Saldo insuficiente.')
        return data

    def save(self, **kwargs):
        origin = self.context['account']
        amount = self.validated_data['amount']
        destination = Account.objects.get(id=self.validated_data['to_account'])

        with db_transaction.atomic():
            origin.balance -= amount
            origin.save()

            destination.balance += amount
            destination.save()

            Transaction.objects.create(
                account=origin, type='transfer_out', amount=amount, related_account=destination
            )
            Transaction.objects.create(
                account=destination, type='transfer_in', amount=amount, related_account=origin
            )

        return origin