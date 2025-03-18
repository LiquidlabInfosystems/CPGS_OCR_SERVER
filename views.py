from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
# Create your views here.

def convert_base64_to_image(req):
    pass

def get_licence_number_from_image(req):
    pass

def do_ocr(req):
    base64Image = req.data['basė4image']
    print(base64Image)
    return  Response(status=HTTP_200_OK)