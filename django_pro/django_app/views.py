from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from .serializers import CloudTableSerializers
from .models import CloudTable
from django.views.decorators.csrf import csrf_exempt
import cloudinary
import bcrypt
import jwt
import datetime
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


def welcome(req):
    return HttpResponse("welcome to mani app from render")


def sample(req):
    return JsonResponse({"msg":"json response from render"})


def is_valid_user(req):
    try:
        cookie_token=req.COOKIES.get("my_first_cookie")
        data=jwt.decode(jwt=cookie_token,key='django-insecure-x9(p1mezxn$(-icbw$*az)1+6luk)k%u-4ng!9@k-$kts%pqt6',algorithms=['HS256'])
        return data
    except:
        return False


def get_users(req):
    if req.method=="GET":
        # print(dir(req)[0])  #COOKIES
        if is_valid_user(req)["valid_user"]:
            users=CloudTable.objects.all()
            serializer=CloudTableSerializers(users,many=True)
            return JsonResponse(serializer.data,safe=False)
        else:
            res=HttpResponse("invalid_user_details")
            res.delete_cookie("my_first_cookie")
            return res
    else:
        return JsonResponse({"error":"Only GET method allowed"}, status=405)


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
        #    print(img_url["secure_url"])

        #    print(user_email,type(user_email))
           user_email=user_email.encode("utf-8") ##to convert str data to byte format
        #    print(user_email,type(user_email))
           ##bcrypt code
           u_salt=bcrypt.gensalt(rounds=14)   #generatesalt    abc123  bcd234  cde345 
        #    print(u_salt)

           encrypted_email=bcrypt.hashpw(password=user_email,salt=u_salt)
        #    print(encrypted_email,"after hashing",type(encrypted_email))


           encrypted_email=encrypted_email.decode("utf-8")  ##to convert byte code to string (because for storing)
        #    print(encrypted_email,"after hasing",type(encrypted_email))

           new_user=CloudTable.objects.create(id=user_id,email=encrypted_email,name=user_name,mob=user_mob,profile_pic=img_url["secure_url"])
           send_mail(subject="welcome mail",
                     message="thank you registering!!",
                     recipient_list=[user_email],from_email=settings.EMAIL_HOST_USER)
           return JsonResponse({"msg":"User Created successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error":"Only POST method allowed"}, status=405)


    # user_data=json.loads(req.body)
    # new_user=CloudTable.objects.create(id=user_data["id"],name=user_data["name"],email=user_data["email"],mob=user_data["mob"])
    # return JsonResponse({"msg":"user created successfully"})



def login_user(req):
    user_data=json.loads(req.body)
    user=CloudTable.objects.get(id=user_data["id"])
    serialized_data=CloudTableSerializers(user)

    encrypted_email=serialized_data.data["email"]
    user_email=user_data["email"]

    is_same=bcrypt.checkpw(user_email.encode("utf-8"),encrypted_email.encode("utf-8"))
    # print(is_same)      # True (returns in boolean value)

    #creating payload
    user_payload={
        "name":serialized_data.data["name"],
        "email":serialized_data.data["email"],
        # "name":"jonny",
        # "email":"pawan@gmail.com",
        "valid_user":True,
        "iat":datetime.datetime.utcnow(),
        "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=50)
    }
    token=jwt.encode(payload=user_payload,key='django-insecure-x9(p1mezxn$(-icbw$*az)1+6luk)k%u-4ng!9@k-$kts%pqt6',algorithm="HS256")
    print(token)

    user_Data=jwt.decode(jwt=token,key='django-insecure-x9(p1mezxn$(-icbw$*az)1+6luk)k%u-4ng!9@k-$kts%pqt6',algorithms="HS256")
    print(user_Data)


    if is_same:
        # return HttpResponse(f'welcome to the app {serialized_data.data["name"]}')
        res=HttpResponse("cookie is set in the browser")

        res.set_cookie(
            key="my_first_cookie",  ## cookie name
            value=token,            ## what data to be stored
            httponly=True,          ## It dont allow JS(frontend)
            max_age=1800               ## till when the cookie is valid(only in second)
            )
        return res
    else:
        return HttpResponse("Invalid Credentials")