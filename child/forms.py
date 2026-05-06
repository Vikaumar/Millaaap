from django import forms
from child.models import esehi
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class addmemberform(forms.ModelForm):
	name=forms.CharField(widget=forms.TextInput(
		attrs={
		'class':'form-control',
		'placeholder':'Enter your Name Here'
		}

		))
	mobilenumber=forms.IntegerField(widget=forms.TextInput(
		attrs={
		'class':'form-control',
		'placeholder':'Enter your Mobile Number Here'
		}

		))
	gender=forms.CharField(widget=forms.TextInput(
		attrs={
		'class':'form-control',
		'placeholder':'Enter your Gender'
		}

		))
	address=forms.CharField(widget=forms.TextInput(
		attrs={
		'class':'form-control',
		'placeholder':'Enter your Address'
		}

		))
	zip1=forms.IntegerField(widget=forms.TextInput(
		attrs={
		'class':'form-control',
		'placeholder':'Enter your Zip Code'
		}

		))
	image=forms.ImageField()
	class Meta:
		model=esehi
		fields=['name','mobilenumber','gender','address','zip1','image']
class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()
	class Meta:
		model=User
		fields=['username','email','password1','password2']