from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest, HttpResponse
import simplejson
import jwt
import bcrypt
import datetime
from django.conf import settings

from user.models import User

# token的最大生存时间
AUTH_EXPIR = 60*60*8


def gen_token(user_id):
    """使用jwt生成token
    jwt参数
    一：一个字段是内容
    二：自己的秘钥
    三：加密方式，默认ＨＳ２５６
    """
    # 使用ｊｗｔ
    return jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIR  # 使用字段exp可以让jwt自带token超时验证　在最后面加一个　＋　整数
    }, settings.SECRET_KEY)


def authenticate(func):
    """是否登录验证"""
    def wrapper(request):
        try:
            # 获取token
            token = request.META.get('HTTP_JWT').encode()
            # 处理业务，验证是否登录
            payload = jwt.decode(token, settings.SECRET_KEY)  # 自动会验证是否超时，如果超时会抛出异常
            # timestamp = payload.get('timestamp')
            # if (datetime.datetime.now().timestamp() - int(timestamp)) > TIMEOUT_TOKEN:
            #     return HttpResponse(status=401)
            # 已经登录
            # 在数据库中查询出此用户
            user_id = payload.get('user_id')
            user = User.objects.get(pk=user_id)
            request.user = user
        except Exception as e:
            print(e)
            # 没有登录
            return HttpResponse(status=401)

        return func(request)
    return wrapper


# /user/test
@authenticate
def test(request:HttpRequest):
    """测试"""
    pass
    return JsonResponse({'status': 'success'})


class IndexView(View):
    """首页"""
    def get(self):
        pass


class RegView(View):
    """注册"""
    def post(self, request:HttpRequest):
        """注册处理"""
        str_body = request.body.decode()
        request_body = simplejson.loads(str_body)
        email = request_body.get('email', "")
        if not email:
            return HttpResponseBadRequest()  # 请求出错

        user_email = User.objects.filter(email=email)
        if user_email:
            # 此邮箱已经存在
            return HttpResponseBadRequest()

        # 接受数据
        name = request_body.get('name')
        pwd = request_body.get('password')

        # 处理逻辑
        new_user = User()
        new_user.name = name
        # 使用bcrypt对数据库存储的密码进行加密显示
        new_user.password = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())
        new_user.email = email

        try:
            new_user.save()
        except Exception as e:
            return HttpResponseBadRequest()

        return JsonResponse({'status': str(gen_token(new_user.id))})


class LoginView(View):
    """用户登录"""
    def post(self, request:HttpRequest):
        """登录提交"""
        try:
            # 获取提交数据
            dict_body = simplejson.loads(request.body.decode())

            pwd = dict_body.get('password')
            email = dict_body.get('email')

            # 检查是否有此用户
            user = User.objects.filter(email=email).first()
            if not user:
                return HttpResponseBadRequest()

            # 检查此用户的密码是否正确
            if not bcrypt.checkpw(pwd.encode(), user.password.encode()):
                return HttpResponseBadRequest()

            # 验证通过
            return JsonResponse({
                'user':{
                    'user_id':user.id,
                    'user_name': user.name,
                    'user_email': user.email,
                },
                'token': gen_token(user.id).decode()
            })
        except Exception as e:
            print(e)
            return HttpResponseBadRequest()




