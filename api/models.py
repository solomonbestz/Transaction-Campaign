from django.db import models
from django.dispatch import Signal
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


import uuid

user_created = Signal()

class Wallet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(_("balance"), max_digits=1000000, decimal_places=2, default=20000)
    account_name = models.CharField(_("account_name"), max_length=250, default='')
    trans_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return str(self.user)
    
class Transaction(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(2000.00))
    
    
    @property
    def net(self):
        return self.amount
    
    @property
    def total(self):
        return self.amount + self.fee
    
    def __str__(self):
        return str(self.sender)
    

class Campaign(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    duration = models.DurationField()
    start = models.DateField()
    stop = models.DateField()
    status = models.BooleanField(default=False)


    def __str__(self):
        return str(self.title)

    
