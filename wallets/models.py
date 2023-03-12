from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blockchain(models.Model):
    title = models.CharField(
        'Blockchain',
        max_length=10,
    )
    name = models.CharField(
        'Full blockchain name',
        max_length=50,
    )
    def __str__(self):
        return self.title


class Wallet(models.Model):
    wallet_address = models.CharField(
        'Wallet',
        max_length=50,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Wallet owner',
        related_name='wallet_owner',
    )
    blockchains = models.ManyToManyField(Blockchain, related_name='blockchain')

    def __str__(self):
        return self.wallet_address


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
    )
    blockchain = models.ForeignKey(
        Blockchain,
        on_delete=models.CASCADE,
    )
    block_number = models.CharField(
        'Block number',
        max_length=20,
    )
    hash = models.CharField(
        'Tx hash',
        max_length=50,
    )
    tx_from = models.CharField(
        'Sender',
        max_length=50,
    )
    tx_to = models.CharField(
        'Reciever',
        max_length=50,
    )
    token_name = models.CharField(
        'Token name',
        max_length=100,
        blank=True,
    )
    token_symbol = models.CharField(
        'Token symbol',
        max_length=100,
    )
    value = models.CharField(
        'Value',
        max_length=20,
    )
    time_stamp = models.DateTimeField()
    add_time = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.hash

