from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Wallet, Campaign, Transaction
from api.serializers import WalletSerializer, CampaignSerializer, TransactionSerializer


class WalletList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        serializer_context = {
            'request': request
        }
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True, context=serializer_context)
        return Response(serializer.data)

class WalletDetail(APIView):
    """Get user wallet
    """
    def get_object(self, uid):
        try:
            wallet = Wallet.objects.get(uid=uid)
            self.check_object_permissions(self.request, wallet)
            return wallet
        except Wallet.DoesNotExist:
            raise Http404
        
    def get(self, request, uid, format=None):
        serializer_context = {
            'request': request
        }
        wallet = self.get_object(uid)
        serializer = WalletSerializer(wallet, context=serializer_context)
        # print(serializer.data)
        return Response(serializer.data)

class CampaignList(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        serializer_context = {
            'request': request
        }
        campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(campaigns,  many=True, context=serializer_context)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CampaignDetail(APIView):
    permission_classes = [IsAdminUser]
    def get_object(self, uid):
        try:
            campaign = Campaign.objects.get(uid=uid)
            return campaign
        except Campaign.DoesNotExist:
            raise Http404
        
    def get(self, request, uid, format=None):
        serializer_context = {
            'request': request
        }
        campaign = self.get_object(uid)
        serializer = CampaignSerializer(campaign, context=serializer_context)
        return Response(serializer.data)
    
    def put(self, request, uid, format=None):
        campaign = self.get_object(uid)
        serializer = CampaignSerializer(campaign, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uid, format=None):
        campaign = self.get_object(uid)
        campaign.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TransactionList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer_context = {
            'request': request
        }
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions,  many=True, context=serializer_context)
        return Response(serializer.data)
    

    def post(self, request, format=None):
        campaign = Campaign.objects.all()[:1].get()
        wallet = Wallet.objects.get(user=request.user)

        transaction = Transaction(sender=wallet.user, amount = request.data["amount"])
        
        if campaign.status and wallet.trans_count < 3:
            transaction.fee = 0
            wallet.trans_count += 1
            wallet.balance -= transaction.total
        else:
            wallet.balance -= transaction.total

        if wallet.balance < transaction.total:
            transaction.delete()
            return Response("Insufficient Balance")
        wallet.save()
        serializer = TransactionSerializer(data=model_to_dict(transaction))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TransactionDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self, uid):
        try:
            transaction = Transaction.objects.get(uid=uid)
            return transaction
        except Transaction.DoesNotExist:
            raise Http404
        
    def get(self, request, uid, format=None):
        serializer_context = {
            'request': request
        }
        transaction = self.get_object(uid)
        serializer = TransactionSerializer(transaction, context=serializer_context)
        return Response(serializer.data)