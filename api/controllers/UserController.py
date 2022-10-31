from django.http import JsonResponse
from datetime import datetime , timedelta
import json
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from api.models import MainUser,Token,Estelam,SMS
from django.utils.timezone import make_aware
from rest_framework.decorators import api_view
from api.infrastructure.BasicAuthentication import Check,CheckToken,GetObjByToken,BlankOrTrue,BlankOrElse
from api.infrastructure.serializers.UserSerializers import UserGetSerializer
import random
import string
import requests

random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))
random_number = lambda N: ''.join(random.SystemRandom().choice(string.digits) for _ in range(N))


@csrf_exempt
@api_view(['POST'])
def SignUp(request):
    try:
        # Register A User
        data = json.loads(request.body)
        check = Check(data, ['name', 'phone', 'email', 'age', 'address', 'job'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        phone = data['phone']
        if ((phone == "") | (phone is None)):
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'لطفا شماره همراه خود را وارد کنید'
            }, encoder=JSONEncoder, status=400)
        if MainUser.objects.filter(phone=phone).exists():
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'این شماره همراه قبلا در سیستم ثبت شده است'
            }, encoder=JSONEncoder, status=400)
        isauth = (BlankOrTrue(data['name']) & BlankOrTrue(data['email']) & BlankOrTrue(data['job']))
        user = MainUser.objects.create(name=data['name'], email=data['email'], phone=phone,
                                             address=data['address'], job=data['job'], age=data['age'], isauthenticated=isauth)
        token = random_str(128)
        while Token.objects.filter(token=token).exists():
            token = random_str(128)
        context = []
        Token.objects.create(user=user, token=token)
        obj = UserGetSerializer(user, context={'token': token})
        context.append(obj.data)
        return JsonResponse({
            'success': True,
            'code': '200',
            'data': context
        }, encoder=JSONEncoder)
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ثبت نام کاربر با مشکل مواجه شد'
        }, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def Login(request):
    try:
        # Register A User
        data = json.loads(request.body)
        check = Check(data, ['phone'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        phone = data['phone']
        if ((phone == "") | (phone is None)):
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'لطفا شماره همراه خود را وارد کنید'
            }, encoder=JSONEncoder, status=400)
        if not (MainUser.objects.filter(phone=phone).exists()):
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'کاربری با این شماره تلفن ثبت نشده است لطفا ثبت نام کنید'
            }, encoder=JSONEncoder, status=400)
        phone = data['phone']
        number = random_number(4)
        SMS.objects.filter(phone=phone).all().delete()
        sms = SMS.objects.create(sms=number, phone=phone, valid=datetime.now() + timedelta(minutes=15))
        ApiKey = '3ea47267d2a947285d19c17bc8a5801f'
        body = {"mobile": phone, "method": "sms", "templateID": 9, "code": number,
                "param1": "کد ورود را در اپلیکیشن وارد کنید با تشکر Estelam.ir"}
        header = {'apikey': '3ea47267d2a947285d19c17bc8a5801f'}
        temp = requests.post('https://api.gsotp.com/otp/send', data=json.dumps(body), headers=header)
        print("************** Phone : " + phone + ' ******** CODE : ' + number)
        return JsonResponse({
            'success': True,
            'code': '200',
            'data': 'کد با موفقیت ارسال شد'
        }, encoder=JSONEncoder)
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'لاگین کاربر با مشکل مواجه شد'
        }, encoder=JSONEncoder, status=400)


@csrf_exempt
@api_view(['POST'])
def CheckSMS(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        check = Check(data, ['phone', 'code'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        phone = data['phone']
        code = data['code']
        if SMS.objects.filter(phone=phone).exists():
            smsobj = SMS.objects.filter(phone=phone).get()
            time = smsobj.valid
            if (make_aware(datetime.now()) < time):
                number = smsobj.sms
                if (str(code) == str(number)):
                    SMS.objects.filter(phone=phone).delete()
                    context = []
                    user = MainUser.objects.filter(phone=phone).first()
                    obj = UserGetSerializer(user, context={'token': Token.objects.filter(user=user).first().token})
                    context.append(obj.data)
                    return JsonResponse({
                        'success': True,
                        'code': '200',
                        'data': context
                    }, encoder=JSONEncoder)
                else:
                    return JsonResponse({
                        'success': False,
                        'code': '404',
                        'data': 'کد ارسال شده صحیح نمیباشد لطفا دوباره امتحان کنید'
                    }, encoder=JSONEncoder)
            else:
                return JsonResponse({
                    'success': False,
                    'code': '400',
                    'data': 'انقضاء کد به اتمام رسیده است'
                },encoder=JSONEncoder)
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'کد ارسال شده صحیح نمیباشد'
        }, encoder=JSONEncoder)
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'کد ارسال شده صحیح نمیباشد'
        }, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def GetUser(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        check = Check(data, ['token'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        token = data['token']
        if not Token.objects.filter(token=token).exists():
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'توکن ارسالی معتبر نمیباشد'
            }, encoder=JSONEncoder, status=400)
        context = []
        obj = UserGetSerializer(Token.objects.filter(token=token).first().user, context={'token':token})
        context.append(obj.data)
        return JsonResponse({
            'success': True,
            'code': '200',
            'data': context
        }, encoder=JSONEncoder)
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'درخواست با مشکل مواجه شد'
        }, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def UpdateUser(request):
    try:
        data = json.loads(request.body)
        check = Check(data, ['name', 'phone', 'email', 'age', 'address', 'job'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        token = data['token']
        mainuser = Token.objects.filter(token=token).get().user
        mainuser.name = BlankOrElse(mainuser.name, data['name'])
        mainuser.phone = BlankOrElse(mainuser.phone, data['phone'])
        mainuser.email = BlankOrElse(mainuser.email, data['email'])
        mainuser.age = BlankOrElse(mainuser.age, data['age'])
        mainuser.address = BlankOrElse(mainuser.address, data['address'])
        mainuser.job = BlankOrElse(mainuser.job, data['job'])
        if (BlankOrTrue(data['name']) & BlankOrTrue(data['email']) & BlankOrTrue(data['job'])):
            mainuser.isauthenticated = True
        mainuser.save()
        context = []
        obj = UserGetSerializer(mainuser, context={'token':token})
        context.append(obj.data)
        return JsonResponse({
            'success': True,
            'code': '200',
            'data': context
        }, encoder=JSONEncoder)
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'بروزرسانی کاربر با مشکل مواجه شد'
        }, encoder=JSONEncoder, status=400)