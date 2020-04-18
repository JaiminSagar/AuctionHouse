from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.AgentUser)
admin.site.register(models.UserDetails)
admin.site.register(models.Property)
admin.site.register(models.PropertyReg)
admin.site.register(models.CurrentAuction)
admin.site.register(models.BiddingOfProperty)
admin.site.register(models.RegForAuction)
admin.site.register(models.State)
admin.site.register(models.City)
admin.site.register(models.ContactUs)
admin.site.register(models.AuctionManager)
