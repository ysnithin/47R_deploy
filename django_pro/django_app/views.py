from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from .serializers import CloudTableSerializers
from .models import CloudTable
from django.views.decorators.csrf import csrf_exempt
import cloudinary
# Create your views here.


def welcome(req):
    return HttpResponse("welcome to mani app from render")


def sample(req):
    return JsonResponse({"msg":"json response from render"})

@csrf_exempt
def reg_user(req):
    if req.method=="POST":
        try:
           user_id=req.POST.get("id")
           user_name=req.POST.get('name')
           user_email=req.POST.get('email')
           user_mob=req.POST.get('mob')
           user_image=req.FILES.get('profile')
           img_url=cloudinary.uploader.upload(user_image)
           print(img_url["secure_url"])


           new_user=CloudTable.objects.create(id=user_id,email=user_email,name=user_name,mob=user_mob,profile_pic=img_url["secure_url"])

           return JsonResponse({"msg":"User Created successfully!","details":list(new_user.values())})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error":"Only POST method allowed"}, status=405)





    # user_data=json.loads(req.body)
    # new_user=CloudTable.objects.create(id=user_data["id"],name=user_data["name"],email=user_data["email"],mob=user_data["mob"])
    # return JsonResponse({"msg":"user created successfully"})
