from django.http import JsonResponse
from datetime import datetime , timedelta
import json
from json import JSONEncoder
from django.views.decorators.csrf import csrf_exempt
from api.models import MainUser,Token,Estelam,SMS,Staff,EstelamFile,Status
from django.utils.timezone import make_aware
from rest_framework.decorators import api_view
from api.infrastructure.BasicAuthentication import Check,CheckToken,GetObjByToken,BlankOrTrue,BlankOrElse
from api.infrastructure.serializers.EstelamSerializers import EstelamLatestStatusSerializer,StatusSerializer,EstelamSerializer
import random
import string
import requests

random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))
random_number = lambda N: ''.join(random.SystemRandom().choice(string.digits) for _ in range(N))


@csrf_exempt
@api_view(['POST'])
def AddEstelam(request):
    try:
        data = json.loads(request.body)
        check = Check(data, ['phone', 'description', 'files'])
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
        if not MainUser.objects.filter(phone=phone).exists():
            user = MainUser.objects.create(phone=phone)
            token = random_str(128)
            while Token.objects.filter(token=token).exists():
                token = random_str(128)
            Token.objects.create(user=user, token=token)
            MainUser.save()
            Token.save()

        # TODO: Test Below Code To See If It Does Return The Staff With The Lowest Load ...
        staff = Staff.objects.all().order_by('load')[0]
        #print("***************************   "+ staff.load)

        tracknumber = random_number(7)
        while Estelam.objects.filter(trackingnumber=tracknumber).exists():
            tracknumber = random_number(7)
        estelam = Estelam.objects.create(user=MainUser.objects.filter(phone=phone),staff=staff,
                                         description=data['description'],trackingnumber=tracknumber)
        files = request.FILES.getlist('files')
        for file in files:
            EstelamFile.objects.create(estelam=estelam,file=file)
        status = Status.objects.create(estelam=estelam,staff=staff,description="در انتظار بررسی")
        context = []
        obj = EstelamLatestStatusSerializer(estelam,context={'staffname':staff.name,'staffcode':staff.staffcode,
                                                        'status':status.description,'statusissuedat':status.issuedat})
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
            'data': 'ثبت استعلام با مشکل مواجه شد'
        }, encoder=JSONEncoder)


# TODO : Requester Must Be Authneticated
@csrf_exempt
@api_view(['POST'])
def GetEstelamDetails(request):
    try:
        data = json.loads(request.body)
        check = Check(data, ['tracknumber'])
        if not (check is True):
            return check
    except:
        return JsonResponse({
            'success': False,
            'code': '400',
            'data': 'ساختار ارسال داده درست نمیباشد'
        }, encoder=JSONEncoder, status=400)
    try:
        tracknumber = data['tracknumber']
        if ((tracknumber == "") | (tracknumber is None)):
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'لطفا کد پیگیری استعلام را وارد کنید'
            }, encoder=JSONEncoder, status=400)
        estelam = Estelam.objects.filter(trackingnumber=tracknumber).first()
        if not estelam:
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'استعلامی با مشخصات زیر پیدا نشد'
            }, encoder=JSONEncoder, status=400)
        statuss = Status.objects.filter(estelam=estelam).all()
        subcontext = []
        for status in statuss:
            obj = StatusSerializer(status,context={'staffname':status.staff.name,'staffcode':status.staff.staffcode})
            subcontext.append(obj.data)
        context = []
        obj = EstelamSerializer(estelam,context={'status':subcontext})
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
            'data': 'دریافت استعلام با مشکل مواجه شد'
        }, encoder=JSONEncoder)


@csrf_exempt
@api_view(['POST'])
def GetAllUserEstelams(request):
    try:
        data = json.loads(request.body)
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
        if ((token == "") | (token is None)):
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'لطفا توکن کاربر را وارد کنید'
            }, encoder=JSONEncoder, status=400)
        user = Token.objects.filter(token=token).first().user
        if not user:
            return JsonResponse({
                'success': False,
                'code': '400',
                'data': 'کاربر پیدا نشد'
            }, encoder=JSONEncoder, status=400)
        estelams = Estelam.objects.filter(user=user).all()
        context = []
        for estelam in estelams:
            status = Status.objects.order_by('issuedat').first()
            obj = EstelamLatestStatusSerializer(estelam, context={'staffname': status.staff.name, 'staffcode': status.staff.staffcode,
                                                                  'status': status.description,
                                                                  'statusissuedat': status.issuedat})
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