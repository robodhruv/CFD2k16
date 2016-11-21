from django import forms

class uploadform(forms.Form):
	
	docfile=forms.FileField(label='Select an image')

