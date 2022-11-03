from django.http import JsonResponse
from datetime import datetime , timedelta
import json
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from api.models import MainUser,Token,Estelam,SMS,Staff,EstelamFile,Status
from django.utils.timezone import make_aware
from rest_framework.decorators import api_view
from api.infrastructure.BasicAuthentication import Check,CheckToken,GetObjByToken,BlankOrTrue,BlankOrElse
from api.infrastructure.serializers.EstelamSerializers import EstelamLatestStatusSerializer,StatusSerializer,EstelamSerializer,EstelamUserGetSerializer
import random
import string
import requests


random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))
random_number = lambda N: ''.join(random.SystemRandom().choice(string.digits) for _ in range(N))


@csrf_exempt
@api_view(['POST'])
def AddStatus(request):
    try:
        data = json.loads(request.body)
        check = Check(data, ['staffcode', 'tracknumber', 'description', 'file'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        staffcode = data['staffcode']
        if ((staffcode == "") | (staffcode is None)):
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'لطفا کد پرسنلی را وارد کنید'
            }, encoder=JSONEncoder, status=400)
        staff = Staff.objects.filter(staffcode=staffcode).first()
        if not staff:
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'پرسنل موجود نمیباشد'
            }, encoder=JSONEncoder, status=400)
        estelam = Estelam.objects.filter(trackingnumber=data['tracknumber']).first()
        if not estelam:
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'استعلام یافت نشد'
            }, encoder=JSONEncoder, status=400)
        file = None
        if request.FILES['file'] is not None:
            file = request.FILES['file']
        status = Status.objects.create(estelam=estelam,staff=staff,description=data['description'],file=file)
        obj = StatusSerializer(status,context={'staffname':staff.name,'staffcode':staff.staffcode})
        context = []
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
            'data': 'ثبت وضعیت با مشکل مواجه شد'
        }, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def GetStaffEstelams(request):
    try:
        data = json.loads(request.body)
        check = Check(data, ['staffcode'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        staffcode = data['staffcode']
        if ((staffcode == "") | (staffcode is None)):
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'لطفا کد پرسنلی را وارد کنید'
            }, encoder=JSONEncoder, status=400)
        staff = Staff.objects.filter(staffcode=staffcode).first()
        if not staff:
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'پرسنل موجود نمیباشد'
            }, encoder=JSONEncoder, status=400)
        estelams = Estelam.objects.filter(staff=staff).all()
        context = []
        for estelam in estelams:
            obj = EstelamUserGetSerializer(estelam,context={'username':estelam.user.name,'userphone':estelam.user.phone})
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
            'data': 'دریافت استعلام ها با مشکل مواجه شد'
        }, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def StaffLogin(request):
    try:
        data = json.loads(request.body)
        check = Check(data, ['staffcode','password'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        staffcode = data['staffcode']
        if ((staffcode == "") | (staffcode is None)):
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'لطفا کد پرسنلی را وارد کنید'
            }, encoder=JSONEncoder, status=400)
        staff = Staff.objects.filter(staffcode=staffcode).first()
        if not staff:
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'پرسنل موجود نمیباشد'
            }, encoder=JSONEncoder, status=400)
        password = data['password']
        if staff.password == password:
            return JsonResponse({
                'success': True,
                'code': '200',
                'data': True
            }, encoder=JSONEncoder)
        return JsonResponse({
            'success': False,
            'code': '404',
            'data': 'رمز عبور اشتباه است'
        }, encoder=JSONEncoder)
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'دریافت استعلام ها با مشکل مواجه شد'
        }, encoder=JSONEncoder)

