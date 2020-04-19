from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus import DatePickerInput,DateTimePickerInput
from . import models
from django import forms
from django.forms import DateTimeInput


class UserCreateForm(UserCreationForm):

    class Meta():
        fields=('username','first_name','last_name','email','password1','password2')
        model =models.User

    #Custom Label for model that is predefined in auth.
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label='Email Address'

class CreateAuctionManager(UserCreationForm):

    class Meta():
        fields=('username','first_name','last_name','email','password1','password2')
        model =models.AuctionManager

class ProfileSetupForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.FileInput(attrs={'class':'custom-file','style':'opacity:100;position:relative;z-index: 0;','class':'btn btn-default'}))
    class Meta():
        fields=('image','address','mobile','birth_date','city','state','pincode')
        model=models.UserDetails

class ProfileUpdateForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.FileInput(attrs={'class':'custom-file','style':'opacity:100;position:relative;z-index: 0;','class':'btn btn-default'}))
    class Meta():
        fields=('image','address','mobile','city','state','pincode')
        model=models.UserDetails

class AgentProfileForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.FileInput(attrs={'class':'custom-file','style':'opacity:100;position:relative;z-index: 0;','class':'btn btn-default'}))

    class Meta():
        fields=('image','address','mobile','city','state','pincode')
        model =models.AgentUser


class BecomeAgentForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.FileInput(attrs={'style':'opacity:100;position:relative;z-index: 0;','class':'btn btn-default'}))
    resume_document=forms.ImageField(widget=forms.FileInput(attrs={'style':'opacity:100;position:relative;z-index: 0;','class':'btn btn-default'}))
    proof_document=forms.ImageField(widget=forms.FileInput(attrs={'style':'opacity:100;position:relative;z-index: 0;','class':'btn btn-default'}))

    class Meta():
        fields=('first_name','last_name','email','mobile','birth_date','address','city','state','pincode','image','resume_document','proof_document')
        model = models.AgentUser
#later work.............
        widgets = {
        #     'first_name': forms.TextInput(attrs={'class': ''}),
        #     'last_name': forms.TextInput(attrs={'class': ''}),
        #     'email': forms.TextInput(attrs={'class': ''}),
        #     'mobile': forms.TextInput(attrs={'class': ''}),
            'birth_date': forms.DateInput(),
        #     'address': forms.Textarea(attrs={'class': ''}),
        #     'image': forms.FileInput(attrs={'class': ''}),
        #     'resume_document': forms.FileInput(attrs={'class': ''}),
        #     'proof_document': forms.FileInput(attrs={'class': ''}),
            # first two classes are predefinead somewhere other two are our class
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email Address'
        self.fields['mobile'].label = 'Enter Mobile Number'
        self.fields['birth_date'].label = 'Enter Your Birth Date'
        self.fields['address'].label = 'Enter Your Address'
        self.fields['image'].label = 'Select Your Profile Image:'
        self.fields['resume_document'].label = 'Your Resume:'
        self.fields['proof_document'].label = 'Any Valid Id Proof:'
        # self.fields['first_name'].size = 12
        # self.fields['password1'].disabled =True
        # self.fields['password1'].type = 'hidden'


# class MakeAnOffer():
#     class Meta():
#         models =models.MakeAnOffer
#         fields=('title','first_name','last_name','email','offer_amount')



class ApplyEvaluationForm(forms.ModelForm):
    class Meta():
        model = models.PropertyReg
        fields = ('property_type', 'property_address','city','state','pincode')


class PropertyDescriptionForm(forms.ModelForm):
    property_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}))

    class Meta():
        model = models.PropertyReg
        fields = ('property_description','pre_set_amount')


class PropertyFilesUploadForm(forms.ModelForm):
    document = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,'style':'opacity:100;position:relative;z-index: 0;','class':'btn btn-default'}))

    class Meta():
        model = models.PropertyFilesUpload
        fields = ('document',)


class PropertyImagesUploadForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True,'style':'opacity:100;position:relative;z-index: 0;','class':'btn btn-default'}))


    class Meta():
        model = models.PropertyImagesUpload
        fields = ('image',)

class SchedulAuctionForm(forms.ModelForm):
    auction_start_date=forms.DateTimeField(widget=DateTimeInput(attrs={'class':'datetimepicker'},format='%Y-%m-%d %H:%M:%S'))
    auction_end_date = forms.DateTimeField(widget=DateTimeInput(attrs={'class':'datetimepicker'},format='%Y-%m-%d %H:%M:%S'))
    class Meta():
        fields=('auction_start_date','auction_end_date')
        model = models.CurrentAuction
        # widgets = {
        #     'auction_start_date': forms.DateTimeInput(),
        #     'auction_end_date': forms.DateTimeInput(attrs={'class':'datetimepicker',}),
        # }

class MakeAnOffer(forms.ModelForm):
    class Meta():
        fields=('title','first_name','last_name','email','mobile','enquiry')
        model = models.MakeAnOffer

