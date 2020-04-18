from . import models
import django_filters
from django import forms

class AuctionFilter(django_filters.FilterSet):
    class Meta:
        model = models.CurrentAuction
        fields = ('property_id__property_type','property_id__city','property_id__state','current_auction_status', 'auction_finished_status','registration_fees',)
