from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conta #{self.id} - {self.user.username} - R$ {self.balance}'


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('deposit', 'Depósito'),
        ('withdrawal', 'Saque'),
        ('transfer_out', 'Transferência enviada'),
        ('transfer_in', 'Transferência recebida'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    related_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='related_transactions'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} - R$ {self.amount} - Conta #{self.account_id}'