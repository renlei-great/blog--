from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
import json
import jwt
import bcrypt
import datetime
from django.conf import settings

from user.models import User


# Create your views here.

class IndexView(View):
    """首页"""
    def get(self):
        pass


class RegView(View):
    """注册"""

    def gen_token(self, user_id):
        """使用jwt生成token
        jwt参数
        一：一个字段是内容
        二：自己的秘钥
        三：加密方式，默认ＨＳ２５６
        """
        # 使用ｊｗｔ
        return jwt.encode({
                'user_id': user_id,
                'timestamp': int(datetime.datetime.now().timestamp())
            }, settings.SECRET_KEY)

    def post(self, request:HttpRequest):
        """注册处理"""
        str_body = request.body.decode()
        request_body = json.loads(str_body)
        email = request_body.get('email', "")
        if not email:
            return HttpResponseBadRequest  # 请求出错

        user_email = User.objects.filter(email=email)
        if user_email:
            # 此邮箱已经存在
            return HttpResponseBadRequest

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
            return HttpResponseBadRequest

        return JsonResponse({'status': str(self.gen_token(new_user.id))})


