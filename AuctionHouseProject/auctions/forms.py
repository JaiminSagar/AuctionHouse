from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models
from django import forms


class UserCreateForm(UserCreationForm):
    class Meta():
        fields=('username','email','password1','password2')
        model=get_user_model()

    #Custom Label for model that is predefined in auth.
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label='Email Address'

class ProfileSetupForm():
    class Meta():
        fields=('image','address','mobile','proof_document')
        models=get_user_model()

class BecomeAgentForm(UserCreationForm, forms.ModelForm):
    class Meta():
        model = models.AgentUser
        fields=('username','first_name','last_name','email','mobile','birth_date','address','image','resume_document','proof_document')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email Address'
        self.fields['mobile'].label = 'Mobile Number'
        self.fields['birth_date'].label = 'Birth Date'
        self.fields['address'].label = 'Address'
        self.fields['image'].label = 'Profile Image'
        self.fields['resume_document'] = 'Resume'
        self.fields['proof_document'] = 'Any Valid Id Proof'


class MakeAnOffer():
    class Meta():
        models =models.MakeAnOffer
        fields=('title','first_name','last_name','email','offer_amount')
# class AgentCreateFrom(UserCreateForm):
#     class Meta():
#         fields=('username','email','password1','password2')
#         model=get_user_model()
