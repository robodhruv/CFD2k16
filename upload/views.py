from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import forms
from . import models
# Create your views here.
def home(request):
	return HttpResponse("Hello")


def upload_pic(request):
	if request.method=="POST":
		print("post")
		
		image= request.POST['file']
		print("image recieved")
		return render(request,'upload/display.html',{'image':image})

	else:
		print("not post")
		form=forms.uploadform()
		return render(request,'upload/upload.html',{'form':form})

def list(request):
	print("hello")
	if request.method=='POST':
		form=forms.uploadform(request.POST)
		newd = models.ExampleModel(model_pic = request.FILES['docfile'])
		newd.save()
		all_objects=models.ExampleModel.objects.all()
		return render(request,'upload/display.html',{'documents':all_objects})
		#return HttpResponse("Form not valid")
	else:
		form=forms.uploadform()
		return render(request,'upload/upload.html',{'form':form})

def showimage(request):
	if request.method=='POST':
		img_url = request.POST['img_url']

		return render(request,'upload/image.html',{'img_url':img_url})

	else:
		return render(request,'upload/geturl.html')