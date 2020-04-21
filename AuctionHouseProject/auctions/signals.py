from django.shortcuts import get_object_or_404
from .models import RegForAuction
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    print("Inside Signal....")
    if ipn.payment_status == 'Completed':
        # payment was successful
        reg_for_auction = get_object_or_404(RegForAuction, invoice_no=ipn.invoice)
        print("object created....")
        if reg_for_auction.current_auction_id.registration_fees <= ipn.mc_gross:
            # mark the order as paid
            print("saving........")
            reg_for_auction.payment_status = "Completed"
            reg_for_auction.save()