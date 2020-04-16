import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AuctionHouseProject.settings")
from django.utils import timezone
from datetime import timedelta
print(timezone.now())

a=timezone.now()
b=timezone.now()+timedelta(seconds=600)
print(b)
print(a.minute-b.minute)
print((a-b).microseconds)
print(a.second)
