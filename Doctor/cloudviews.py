from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages




credentials = {
  "apikey": "3fViUPOG2xzUv8TotadCOCthAfYesMGW-wUYPECEyJsX",
  "endpoints": "https://s3.us-east.cloud-object-storage.appdomain.cloud",
  "iam_apikey_description": "Auto-generated for key a947c635-fc0e-47e7-96ab-27ab7a4b4bec",
  "iam_apikey_name": "doctor",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/b84e912f902c449aac9ef8f4264b807b::serviceid:ServiceId-4244405d-4056-4120-ae7e-83960085f210",
  "resource_instance_id": "crn:v1:bluemix:public:cloud-object-storage:global:a/b84e912f902c449aac9ef8f4264b807b:4a2f97d0-54d9-4a36-9965-9195a1b5f128::"
}
import ibm_boto3
from ibm_botocore.client import Config, ClientError



def save_to_cloud(request, pk):
    image = Images.objects.get(id=pk)
    src = image.Image_Consultation
    cos = ibm_boto3.client(service_name='s3',
    ibm_api_key_id=credentials['apikey'],
    ibm_service_instance_id=credentials['iam_serviceid_crn'],
    config=Config(signature_version='oauth'),
    endpoint_url=credentials['endpoints'])
    cos.upload_file(Filename='C:/Users/Fedi/Desktop/DoctorProject/'+str(src), Bucket=credentials['iam_apikey_name'],Key=str(image.Image_Consultation)[max(index for index, item in enumerate(str(image.Image_Consultation)) if item == '/')+1:])
    messages.success(request, 'Image Uploaded to your IBM Cloud Instance')

    return redirect('consultation_image', pk)

