import os
import js2py
import sqlite3
from django.template.loader import render_to_string
import cv2
from django.contrib.auth.models import User
import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from PIL import Image
from django.core.mail import send_mail
from child.forms import addmemberform
from django.template import Template,Context
from .forms import UserRegisterForm
from .models import esehi
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
import requests

def register(request):
  if request.method=='POST':
    form=UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username=form.cleaned_data.get('username')
      messages.success(request,f'Account Created for {username}!')
      return redirect('/child/login')
  else:
    form=UserRegisterForm()
  return render(request,'child/register.html',{"form":form})
@login_required
def congrats(request):
  faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  cam=cv2.VideoCapture(0)
  members=esehi.objects.all()
  id=0
  for member in members:
    if(id<member.id):
      id=member.id
  sample=0
  while(True):
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        sample=sample+1
        cv2.imwrite('DataSet/User.'+str(id)+"."+str(sample)+'.jpg',gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(100)
    cv2.imshow("Face",img);
    if(sample>20):
        break
  cam.release()
  cv2.destroyAllWindows()
  recognizer=cv2.face.LBPHFaceRecognizer_create();
  path='DataSet'
  def getImageWithID(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
      faceImg=Image.open(imagePath).convert('L')
      facenp=np.array(faceImg,'uint8')
      ID=int(os.path.split(imagePath)[-1].split('.')[1])
      faces.append(facenp)
      IDs.append(ID)
      cv2.waitKey(10)
    return IDs,faces
  Ids,faces=getImageWithID(path)
  recognizer.train(faces,np.array(Ids))
  recognizer.write('recognizer/trainningData.yml')
  return render(request,'child/congrats.html')
@login_required
def laststep(request):
  return render(request,'child/laststep.html')
def home(request):
  return render(request,'child/index.html')
def login(request):
	return render(request,'child/login.html')
def success(request): 
    return HttpResponse('successfuly uploaded')
@login_required
def addmember(request):
  if request.method == 'POST':
    form = addmemberform(request.POST,request.FILES)
    if form.is_valid():
      form1=form.save(commit=False)
      form1.user=request.user
      form1.save()
      return redirect('/child/laststep')
  else:
    form = addmemberform()
  return render(request, 'child/addmember.html',{"form":form})
def aboutus(request):
	return render(request,'child/aboutus.html')
def howitworks(request):
	return render(request,'child/howitworks.html')
@login_required
def dashboard(request):
  return render(request,'child/dashboard.html')
@login_required
def allmembers(request):
  print((esehi.objects.all().count()) > 0)
  return render(request,'child/allmembers.html')
@login_required
def searchmember(request):
  return render(request,'child/searchmember.html')
@login_required
def addtolost(request,id):
  data = esehi.objects.filter(id=id).values()
#  u=lost(**data[0])
#  u.save()
  return render(request,'child/addtolost.html')
def display_ip():
    """  Function To Print GeoIP Latitude & Longitude """
    ip_request = requests.get('https://get.geojs.io/v1/ip.json')
    my_ip = ip_request.json()['ip']
    geo_request = requests.get('https://get.geojs.io/v1/ip/geo/' +my_ip + '.json')
    geo_data = geo_request.json()
    a=[geo_data['region'],geo_data['latitude'],geo_data['longitude']]
    return a
@login_required
def searchresult(request):
  faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  def getans(Id):
        conn = sqlite3.connect("db.sqlite3")
        cmd = "SELECT * from child_esehi WHERE id="+str(Id)
        cursor = conn.execute(cmd)
        profile = None
        for row in cursor:
            profile = row
        conn.close()
        return profile
  cam=cv2.VideoCapture(0)
  rec=cv2.face.LBPHFaceRecognizer_create();
  rec.read('recognizer\\trainningData.yml')
  id=0
  flag=0
  font=cv2.FONT_HERSHEY_COMPLEX_SMALL
  while(True):
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        profile = getans(id)
        if profile!=None:
          print(profile)
          cv2.destroyAllWindows()
          flag=1
          break
        #cv2.putText(img,str(id),(x,y+h), font, 4,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow("Face",img);
    if(cv2.waitKey(1)==ord('q') or flag==1):
        break;
  cam.release()
  cv2.destroyAllWindows()
  current_site=get_current_site(request)
  mail_subject='Give Permisssion to access Details of child'
  ip_request = requests.get('https://get.geojs.io/v1/ip.json')
  my_ip = ip_request.json()['ip']  # ip_request.json() => {ip: 'XXX.XXX.XX.X'}
  geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
  geo_request = requests.get(geo_request_url)
  geo_data = geo_request.json()
  r=display_ip()
  message = render_to_string('child/acc_active_email.html',{'user':request.user,'domain':current_site.domain,'uid':urlsafe_base64_encode(force_bytes(id)),'token':account_activation_token.make_token(request.user),'region':r[0],'long':r[1],'lat':r[2]})
  to_email='akeshav53@gmail.com'
  email=EmailMessage(mail_subject,message,to=[to_email])
  email.send()
  messages.success(request,f'We have sent the confirmation mail')
  return redirect('/child')
 # return render(request,'child/searchresult.html',{'profile':profile})

def activate(request,uidb64,token,year):
  try:
    child_id=force_text(urlsafe_base64_decode(uidb64))
    user=User.objects.get(pk=year)
    child1=esehi.objects.get(pk=child_id)
  except (TypeError,ValueError,OverflowError,User.DoesNotExist):
    user=None
  if user is not None and account_activation_token.check_token(user,token):
    child1.perms=True
    child1.uperms=year
    child1.save()
    return HttpResponse('<h2>Access Granted</h2>')
  else:
    return HttpResponse('activation link is invalid!')

def deletefromlost(request,id):
  #lost.objects.filter(id=id).delete()
  return HttpResponse("Member has been successfully removed from lost list of our database.")

def childdetails(request):
  conn = sqlite3.connect("db.sqlite3")
  cmd = "SELECT * from child_esehi WHERE perms=1 AND uperms="+str(request.user.pk)
  cursor = conn.execute(cmd)
  profile=None
  for row in cursor:
    print(row)
    profile = row
  conn.close()
  return render(request,'child/searchresult.html',{'profile':profile})
