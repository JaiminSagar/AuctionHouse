from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from . import models

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

class BecomeAgentForm():
    class Meta():
        models=models.BecomeAgent

class MakeAnOffer():
    class Meta():
        models =models.MakeAnOffer
        fields=('title','first_name','last_name','email','offer_amount')
# class AgentCreateFrom(UserCreateForm):
#     class Meta():
#         fields=('username','email','password1','password2')
#         model=get_user_model()
