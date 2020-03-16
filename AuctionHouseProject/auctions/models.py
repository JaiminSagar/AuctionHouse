from django.db import models
from django.contrib import auth
from django.views import generic
from django.utils import timezone
from django.urls import reverse,reverse_lazy

# Create your models here.

class User(auth.models.User,auth.models.PermissionsMixin):
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=13)
    birth_date =models.DateField()
    # proof_document= models.FileField()
    image = models.ImageField()
    profile_setup = models.BooleanField(default=False)

    def __str__(self):
        return '@{}'.format(self.username)

#add became Agent and agentuser model.....

# class BecomeAgent(models.Model):
#     email =models.EmailField()
#     address = models.CharField(max_length=255)
#     mobile = models.CharField(max_length=255)
#     proof_document= models.FileField()
#     resume_document =models.FileField()
#     # image = models.ImageField()
#     contacted = models.BooleanField(default=False)
#
#     def migrate_details(self):
#         if self.contacted == True:
#             agent = AgentUser(address=self.address,mobile =self.mobile,proof_document=self.proof_document,resume_document=self.resume_document,contacted=self.contacted)
#             agent.save()

    # def __str__(self):
    #     return '@{}'.format(self.username)

class AgentUser(auth.models.User,auth.models.PermissionsMixin):
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    birth_date= models.DateField()
    proof_document= models.FileField()
    resume_document =models.FileField()
    image = models.ImageField()
    interview_date =models.DateTimeField()
    interviewed = models.BooleanField(default=False)
    contacted = models.BooleanField(default=True)
    approved =models.BooleanField(default=False)

    def agent_approved(self):
        self.approved = True

class Property(models.Model):
    propery_type  = models.CharField(max_length=50)


class PropertyReg(models.Model):
    user = models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE)
    property_type = models.ForeignKey(Property,related_name='property',on_delete=models.CASCADE)
    property_address = models.CharField(max_length=255)
    #Thia for map implimentation using some api url
    # property_location = models.URLField()
    #property_description will be only edited by agentUser
    property_description =models.TextField(max_length=2000)


class MakeAnOffer(models.Model):
    property_id= models.ForeignKey(PropertyReg,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    offer_amount = models.CharField(max_length=10)

class CurrentAuction(models.Model):
    property_id= models.ForeignKey(PropertyReg,on_delete=models.CASCADE)


#other models like employee wo will schedule the auction
