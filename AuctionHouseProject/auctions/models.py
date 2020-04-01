from djongo import models
from django.contrib import auth
from django.views import generic
from django.utils import timezone
from django.urls import reverse,reverse_lazy

# Create your models here.
class  State(models.Model):
    state_name= models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.state_name)

class City(models.Model):
    state= models.ForeignKey(State,on_delete=models.CASCADE)
    city_name =models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.city_name)


class User(auth.models.User,auth.models.PermissionsMixin):
    profile_setup = models.BooleanField(default=False)
    user_type= models.CharField(default="user",max_length=10)
    def __str__(self):
        return "{}".format(self.username)

    def profile_set(self):
        self.profile_setup=True
        self.save()

class UserDetails(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default='To be Setup')
    mobile = models.CharField(max_length=13, default='To be Setup')
    birth_date = models.DateField(blank=True)
    pincode = models.CharField(max_length=6, default='000000')
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    # proof_document= models.FileField()
    image = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return '@{}'.format(self.user)

    def get_absolute_url(self):
        return reverse_lazy('auctions:profile_detail', kwargs={'pk': self.pk})  # This represent after doing Comment Where user should redirect

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

class AgentUser(auth.models.User, auth.models.PermissionsMixin):
    user_type =models.CharField(max_length=10,default="agent")
    address = models.TextField(max_length=255)
    pincode = models.CharField(max_length=6, default='000000')
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    state= models.ForeignKey(State,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=255)
    birth_date= models.DateField(blank=True)
    proof_document= models.FileField(blank=True, upload_to='agent_proof_document')
    resume_document =models.FileField(blank=True, upload_to='agent_resume_document')
    image = models.ImageField(blank=True, upload_to='agent_image')
    interview_date =models.DateTimeField(blank=True)
    interviewed = models.BooleanField(default=False,blank=True)
    contacted = models.BooleanField(default=True)
    approved =models.BooleanField(default=False)

    def agent_approved(self):
        self.approved = True
        self.save()

    def __str__(self):
        return '@{}'.format(self.username)


    def get_absolute_url(self):
        return reverse_lazy('auctions:agent_profile', kwargs={'pk': self.pk})  # This represent after doing Comment Where user should redirect


    class Meta:
        verbose_name=('AgentUser')
        verbose_name_plural =('AgentUsers')

class Property(models.Model):
    propery_type  = models.CharField(max_length=50)

    def __str__(self):
        return self.propery_type



class PropertyReg(models.Model):
    user = models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE)
    property_type = models.ForeignKey(Property,related_name='property',on_delete=models.CASCADE)
    property_address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6, default='000000')
    city = models.CharField(max_length=30, default='Place to be Selected.')
    state = models.CharField(max_length=30, default='To be Selected')
    #Thia for map implimentation using some api url
    # property_location = models.URLField()
    #property_description will be only edited by agentUser
    property_description = models.CharField(max_length=2000, default='')
    agent_id = models.ForeignKey(AgentUser,related_name='who_approves',on_delete=models.CASCADE)
    approved_date = models.DateTimeField()
    approved = models.BooleanField(default=False)
    pre_set_amount = models.IntegerField(default=0)
    scheduled_status = models.BooleanField(default=False)
    current_auction_status = models.BooleanField(default=False)
    viewinghours = models.CharField(max_length=20, default="None2")

    def get_absolute_url(self):
        return reverse_lazy('auctions:agent_property_details', kwargs={'pk': self.pk})



def generate_filename(self, filename):
    url = "property/id_%s/files/%s" % (str(self.property_reg.pk), filename)
    return url

class PropertyFilesUpload(models.Model):
    property_reg = models.ForeignKey(PropertyReg, related_name='property_files',on_delete=models.CASCADE)
    document = models.FileField(blank=True, upload_to=generate_filename)


def generate_image_name(self, filename):
    url = "property/id_%s/images/%s" % (str(self.property_reg.pk), filename)
    return url

class PropertyImagesUpload(models.Model):
    property_reg = models.ForeignKey(PropertyReg, related_name='property_images',on_delete=models.CASCADE)
    image = models.FileField(blank=True, upload_to=generate_image_name)




class MakeAnOffer(models.Model):
    property_id= models.ForeignKey(PropertyReg,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    offer_amount = models.CharField(max_length=10)

class CurrentAuction(models.Model):
    property_id= models.ForeignKey(PropertyReg,related_name='property',on_delete=models.CASCADE)
    registration_fees =models.IntegerField()
    auction_start_date = models.DateTimeField()
    auction_end_date = models.DateTimeField()

    increment_ratio = models.FloatField()
    current_amount =models.IntegerField()

    #viewinhours....
    def get_absolute_url(self):
        return reverse_lazy('auctions:auction_detail', kwargs={'pk': self.pk})


class BiddingOfProperty(models.Model):
    current_auction_id=models.ForeignKey(CurrentAuction,related_name='property_bid',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_bid',on_delete=models.CASCADE)
    user_bid_amount =models.IntegerField()
    bid_time =models.DateTimeField()


class RegForAuction(models.Model):
    current_auction_id = models.ForeignKey(CurrentAuction, related_name='current_auction', on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=12)
    user = models.ForeignKey(User,related_name='register',on_delete=models.CASCADE)


#other models like employee wo will schedule the auction
