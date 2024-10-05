from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from myapp.models import UserProfile, Reviews, OrderSummary

# from myapp.models import UserProfile


class RegistrationForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':"mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-blue-500 focus:ring focus:ring-blue-200"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':"mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-blue-500 focus:ring focus:ring-blue-200"}))


    class Meta:

        model = User

        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class':'mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-blue-500 focus:ring focus:ring-blue-200'}),
            'email': forms.TextInput(attrs={'class':'mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-blue-500 focus:ring focus:ring-blue-200'}) 
        }



class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':"mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-blue-500 focus:ring focus:ring-blue-200"}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"mt-1 block w-full border border-gray-300 rounded-md p-2 focus:border-blue-500 focus:ring focus:ring-blue-200"}))


class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = ['bio', 'profile_pic']
    

class ReviewForm(forms.ModelForm):

    comment = forms.CharField(widget = forms.Textarea(attrs={'class':'mt-1 p-2 border border-gray-300 rounded w-full focus:outline-none focus:ring focus:ring-blue-200'}))
    
    rating = forms.IntegerField(widget= forms.TextInput(attrs={'class': 'mt-1 p-2 border border-gray-300 rounded w-full focus:outline-none focus:ring focus:ring-blue-200'}))

    class Meta:

        model = Reviews

        fields = ['comment', 'rating']


class DeliveryForm(forms.ModelForm):

    class Meta:

        model = OrderSummary

        fields = ['phone', 'email', 'delivery_address', 'pin', 'payment_method']

       
    