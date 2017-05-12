from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^getToken$', api.getToken),
    url(r'^findLandmark$', api.findLandmark),
    url(r'^findLandmarkYUV$', api.findLandmarkYUV),
    url(r'^getRecord$', api.getRecord),
    url(r'^isBlink$', api.isBlink),
]
    # url(r'^getEAR$', api.getEAR)
