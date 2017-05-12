from django.http import JsonResponse
from django.middleware.csrf import get_token
from . import eyedetect
# from . import eyedetect2
import uuid
import os
from django.views.decorators.csrf import csrf_exempt
import thread
from models import Record
from django.core import serializers

def getToken(request):
    return JsonResponse({'token':get_token(request)})

@csrf_exempt
def findLandmark(request):
    
    user, user_id = (str(request.FILES['img']).split('.')[0]).split('-')
    uuidFileName = str(uuid.uuid4())
    handle_uploaded_file(request.FILES['img'], uuidFileName)
    img = eyedetect.openJPG('./eyeDetectServer/image/'+uuidFileName)
    leftEye, rightEye, lPupil, rPupil = eyedetect.findLandmarks(img, uuidFileName)
    
    thread.start_new_thread(delete_uploaded_file,(uuidFileName,))

    # landmark = []
    return JsonResponse({
        'leftEye': leftEye,
        'rightEye': rightEye,
        'lPupil': lPupil,
        'rPupil': rPupil
    })

@csrf_exempt
def findLandmarkYUV(request):
    user, user_id = (str(request.FILES['img']).split('.')[0]).split('-')
    uuidFileName = str(uuid.uuid4())
    handle_uploaded_file(request.FILES['img'], uuidFileName)
    img = eyedetect.openYUV('./eyeDetectServer/image/'+uuidFileName)
    leftEye, rightEye, lPupil, rPupil = eyedetect.findLandmarks(img, uuidFileName)
    
    thread.start_new_thread(delete_uploaded_file,(uuidFileName,))
    # landmark = []
    return JsonResponse({
        'leftEye': leftEye,
        'rightEye': rightEye,
        'lPupil': lPupil,
        'rPupil': rPupil
    })

@csrf_exempt
def isBlink(request):
    user, user_id = (str(request.FILES['img']).split('.')[0]).split('-')
    uuidFileName = str(uuid.uuid4())
    handle_uploaded_file(request.FILES['img'], uuidFileName)
    img = eyedetect.openYUV('./eyeDetectServer/image/'+uuidFileName)
    leftEye, rightEye, lPupil, rPupil = eyedetect.findLandmarks(img, uuidFileName)
    
    if(len(leftEye) == 0):
        r = Record(user_id=user_id, blink=-1)
        return JsonResponse({"blink":-1})
        
    EAR = (eyedetect.getEAR(leftEye)+eyedetect.getEAR(rightEye))/2
    threshold = (float)(request.POST.get('threshold'))
    if(EAR > threshold):
        r = Record(user_id=user_id, blink=1)
        r.save()
        return JsonResponse({"blink":1})
    return JsonResponse({"blink":0})

def getRecord(request):
    r = Record.objects.all().filter(user_id=request.GET.get('id'))
    r = serializers.serialize('json',r)
    return JsonResponse({ "record" : r})
    

# def getEAR(request):
#     uuidFileName = str(uuid.uuid4())+".jpg"
#     # uuidFileName = "a.jpg"
#     handle_uploaded_file(request.FILES['img'], uuidFileName)
#     EAR = eyedetect2.getEAR('./eyeDetectServer/image/'+uuidFileName)
#     os.remove('./eyeDetectServer/image/'+uuidFileName)
#     # landmark = []
#     return JsonResponse({'EAR':EAR})    

def handle_uploaded_file(f,fileName):
    with open('./eyeDetectServer/image/'+str(fileName),'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def delete_uploaded_file(fileName):
    os.remove('./eyeDetectServer/image/'+fileName)