import os
import cv2
import numpy as np
import requests
from PIL import Image

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

try:
    from django.utils.encoding import force_str
except ImportError:
    from django.utils.encoding import force_text as force_str

from child.forms import addmemberform
from .forms import UserRegisterForm
from .models import esehi
from .tokens import account_activation_token


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect('/child/login')
    else:
        form = UserRegisterForm()
    return render(request, 'child/register.html', {"form": form})


@login_required
def congrats(request):
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    # Find latest member
    latest_member = esehi.objects.all().order_by('-id').first()
    id = latest_member.id if latest_member else 0
    
    webcam_ok = False
    cam = cv2.VideoCapture(0)
    if cam.isOpened():
        webcam_ok = True
        sample = 0
        # Try reading a test frame to ensure it actually works
        ret, img = cam.read()
        if not ret or img is None:
            webcam_ok = False
        else:
            # Reset and capture
            while True:
                ret, img = cam.read()
                if not ret or img is None:
                    webcam_ok = False
                    break
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    sample = sample + 1
                    cv2.imwrite('DataSet/User.' + str(id) + "." + str(sample) + '.jpg', gray[y:y+h, x:x+w])
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.waitKey(100)
                cv2.imshow("Face", img)
                if sample > 20:
                    break
            cam.release()
            cv2.destroyAllWindows()

    if not webcam_ok:
        print("Webcam fallback triggered: extracting face from uploaded profile picture.")
        if cam.isOpened():
            cam.release()
        if latest_member and latest_member.image:
            img = cv2.imread(latest_member.image.path)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceDetect.detectMultiScale(gray, 1.3, 5)
                if len(faces) > 0:
                    for (x, y, w, h) in faces:
                        for sample in range(1, 22):
                            cv2.imwrite('DataSet/User.' + str(id) + "." + str(sample) + '.jpg', gray[y:y+h, x:x+w])
                else:
                    # Fallback if no face detected in the picture itself: use whole image
                    for sample in range(1, 22):
                        cv2.imwrite('DataSet/User.' + str(id) + "." + str(sample) + '.jpg', gray)
            else:
                print("Failed to read child's uploaded profile picture path:", latest_member.image.path)

    # Train recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'DataSet'
    
    def getImageWithID(path):
        if not os.path.exists(path):
            os.makedirs(path)
        imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.startswith('User.') and f.endswith('.jpg')]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            try:
                faceImg = Image.open(imagePath).convert('L')
                facenp = np.array(faceImg, 'uint8')
                ID = int(os.path.split(imagePath)[-1].split('.')[1])
                faces.append(facenp)
                IDs.append(ID)
            except Exception as e:
                print(f"Error loading image {imagePath}: {e}")
        return IDs, faces

    Ids, faces = getImageWithID(path)
    if len(faces) > 0:
        recognizer.train(faces, np.array(Ids))
        if not os.path.exists('recognizer'):
            os.makedirs('recognizer')
        recognizer.write('recognizer/trainningData.yml')
    else:
        print("No faces found to train.")
    return render(request, 'child/congrats.html')


@login_required
def laststep(request):
    return render(request, 'child/laststep.html')


def home(request):
    return render(request, 'child/index.html')


def login(request):
    return render(request, 'child/login.html')


def success(request): 
    return HttpResponse('successfully uploaded')


@login_required
def addmember(request):
    if request.method == 'POST':
        form = addmemberform(request.POST, request.FILES)
        if form.is_valid():
            form1 = form.save(commit=False)
            form1.user = request.user
            form1.save()
            return redirect('/child/laststep')
    else:
        form = addmemberform()
    return render(request, 'child/addmember.html', {"form": form})


def aboutus(request):
    return render(request, 'child/aboutus.html')


def howitworks(request):
    return render(request, 'child/howitworks.html')


@login_required
def dashboard(request):
    return render(request, 'child/dashboard.html')


@login_required
def allmembers(request):
    return render(request, 'child/allmembers.html')


@login_required
def searchmember(request):
    return render(request, 'child/searchmember.html')


@login_required
def addtolost(request, id):
    # This renders the success message for reporting lost
    return render(request, 'child/addtolost.html')


def get_geoip_data():
    """ Function To Fetch GeoIP region, Latitude & Longitude in a single call """
    try:
        response = requests.get('https://get.geojs.io/v1/ip/geo.json', timeout=5)
        if response.status_code == 200:
            geo_data = response.json()
            return (
                geo_data.get('region', 'Unknown Region'),
                geo_data.get('latitude', '0.0'),
                geo_data.get('longitude', '0.0')
            )
    except Exception as e:
        print(f"GeoIP API call failed: {e}")
    return ('Unknown Region', '0.0', '0.0')


@login_required
def searchresult(request):
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    def getans(Id):
        return esehi.objects.filter(id=Id).first()

    rec = cv2.face.LBPHFaceRecognizer_create()
    rec_file = 'recognizer/trainningData.yml'
    
    if os.path.exists(rec_file):
        rec.read(rec_file)
    else:
        messages.error(request, "Facial model has not been trained yet. Please add a member to train it.")
        return redirect('/child/search/')

    matched_profile = None

    # Check if image file was uploaded via POST
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                try:
                    id, conf = rec.predict(gray[y:y+h, x:x+w])
                    profile = getans(id)
                    if profile is not None:
                        matched_profile = profile
                        break
                except Exception as e:
                    print(f"Prediction failed: {e}")
            if matched_profile is None:
                messages.error(request, "No matching child record found in the uploaded image.")
                return redirect('/child/search/')
        else:
            messages.error(request, "Failed to read the uploaded image file.")
            return redirect('/child/search/')
    else:
        # Webcam Scanner Mode
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            messages.error(request, "Could not access physical webcam. Please upload an image instead.")
            return redirect('/child/search/')

        flag = 0
        loop_count = 0
        while True:
            ret, img = cam.read()
            if not ret or img is None:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                try:
                    id, conf = rec.predict(gray[y:y+h, x:x+w])
                    profile = getans(id)
                    if profile is not None:
                        matched_profile = profile
                        flag = 1
                        break
                except Exception as e:
                    print(f"Prediction failed: {e}")
            cv2.imshow("Face Scanner", img)
            if cv2.waitKey(1) == ord('q') or flag == 1:
                break
            loop_count += 1
            if loop_count > 300:  # Timeout safety limits
                break

        cam.release()
        cv2.destroyAllWindows()

    if matched_profile is not None:
        # Fetch GeoIP information
        region, lat, lon = get_geoip_data()
        
        current_site = get_current_site(request)
        mail_subject = 'Give Permission to access Details of child'
        message = render_to_string('child/acc_active_email.html', {
            'user': request.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(matched_profile.id)),
            'token': account_activation_token.make_token(request.user),
            'region': region,
            'long': lon,
            'lat': lat
        })
        
        # Look up parent email dynamically with a fallback
        to_email = matched_profile.user.email if (matched_profile.user and matched_profile.user.email) else 'admin@example.com'
        
        email = EmailMessage(mail_subject, message, to=[to_email])
        try:
            email.send()
            messages.success(request, f'Child identified! A permission request email has been sent to their parent.')
        except Exception as e:
            messages.warning(request, f'Child identified, but we could not send the permission email: {e}')
            
        return render(request, 'child/searchresult.html', {'profile': matched_profile})
    else:
        messages.error(request, "No matching child profile found in our database.")
        return redirect('/child/search/')


def activate(request, uidb64, token, year):
    try:
        child_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=year)
        child1 = esehi.objects.get(pk=child_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, esehi.DoesNotExist):
        user = None
        child1 = None
        
    if user is not None and child1 is not None and account_activation_token.check_token(user, token):
        child1.perms = True
        child1.uperms = year
        child1.save()
        return HttpResponse('<h2>Access Granted</h2>')
    else:
        return HttpResponse('activation link is invalid!')


def deletefromlost(request, id):
    return HttpResponse("Member has been successfully removed from lost list of our database.")


@login_required
def childdetails(request):
    profile = esehi.objects.filter(perms=True, uperms=request.user.pk).first()
    return render(request, 'child/searchresult.html', {'profile': profile})

