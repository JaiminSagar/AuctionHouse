from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models
from django import forms
# from django import forms


class UserCreateForm(UserCreationForm):

    class Meta():
        fields=('username','email','password1','password2')
        model =models.User

    #Custom Label for model that is predefined in auth.
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label='Email Address'

class ProfileSetupForm(forms.ModelForm):

    # def save(self, commit=True):
    #     user= models.User()

    class Meta():
        fields=('image','first_name','last_name','address','mobile','birth_date','city','state','pincode')
        model=models.User
        widgets={

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobile'].label = 'Enter Mobile Number'
        self.fields['birth_date'].label = 'Ente Your Birth Date'
        self.fields['address'].label = 'Enter Your Address'
        self.fields['image'].label = 'Select Your Profile Image:'


class BecomeAgentForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput)
    class Meta():
        fields=('first_name','last_name','email','mobile','birth_date','address','image','resume_document','proof_document')
        model = models.AgentUser
#later work.............
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'class': ''}),
        #     'last_name': forms.TextInput(attrs={'class': ''}),
        #     'email': forms.TextInput(attrs={'class': ''}),
        #     'mobile': forms.TextInput(attrs={'class': ''}),
        #     'birth_date': forms.TextInput(attrs={'class': ''}),
        #     'address': forms.Textarea(attrs={'class': ''}),
        #     'image': forms.FileInput(attrs={'class': ''}),
        #     'resume_document': forms.FileInput(attrs={'class': ''}),
        #     'proof_document': forms.FileInput(attrs={'class': ''}),
            # first two classes are predefinead somewhere other two are our class
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       # self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email Address'
        self.fields['mobile'].label = 'Enter Mobile Number'
        self.fields['birth_date'].label = 'Ente Your Birth Date'
        self.fields['address'].label = 'Enter Your Address'
        self.fields['image'].label = 'Select Your Profile Image:'
        self.fields['resume_document'].label = 'Your Resume:'
        self.fields['proof_document'].label = 'Any Valid Id Proof:'
        # self.fields['first_name'].size = 12
        # self.fields['password1'].disabled =True
        # self.fields['password1'].type = 'hidden'


class MakeAnOffer():
    class Meta():
        models =models.MakeAnOffer
        fields=('title','first_name','last_name','email','offer_amount')
# class AgentCreateFrom(UserCreateForm):
#     class Meta():
#         fields=('username','email','password1','password2')
#         model=get_user_model()
