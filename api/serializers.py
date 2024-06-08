from api.models import Wallet, Transaction, Campaign
from rest_framework import serializers


class WalletSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Wallet
        fields = ['uid', 'balance','user', 'account_name', 'created', 'trans_count']

# class TransactionSerializer(serializers.HyperlinkedModelSerializer):
#     sender = serializers.Field(source='sender', read_only=True)
#     class Meta:
#         model = Transaction
#         fields = ['uid', 'sender', 'amount', 'fee', 'total']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('uid', 'sender', 'amount', 'fee', 'total')

class CampaignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Campaign
        fields = ['uid', 'title', 'description', 'duration', 'start', 'stop', 'status']