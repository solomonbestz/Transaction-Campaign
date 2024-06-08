from django.contrib import admin

from api.models import Wallet, Campaign,Transaction


admin.site.register(Wallet)
admin.site.register(Campaign)
admin.site.register(Transaction)