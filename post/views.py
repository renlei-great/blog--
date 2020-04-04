from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.http import HttpResponseBadRequest, HttpResponseNotFound
import simplejson
import datetime
import math

from user.views import authenticate
from .models import Post, Content


@authenticate
def pub(request:HttpRequest):
    """新增"""
    try:
        payload = simplejson.loads(request.body)
        # 添加新数据项
        post = Post()
        post.title = payload['title']
        # post.pubdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))  # 解决时区问题
        post.author = request.user
        post.save()

        content = Content()
        content.post = post
        content.content = payload['content']
        content.save()

        return JsonResponse({'post_id': post.id})

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def get(request, post_id):
    """读文章"""
    try:
        post = Post.objects.get(pk=int(post_id))

        return JsonResponse({
            'post':
                {
                    'post_id': post_id,
                    'title': post.title,
                    'author': post.author.name,
                    'author_id': post.author.id,
                    'pubdate': post.pubdate.timestamp(),
                    'content': post.content.content,
                }
        })
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def validate(name:str, d:dict, cvt_func, default, val_func):
    """
    抽出公用的验证数据方法，进行封装
     try:
        获取页码
        page = request.GET.get('page')
        page = int(page)
        page = page if page > 0 else 1
    except Exception as e:
        print(e)
        page = 1
    """
    try:
        ret = d.get(name)
        ret = cvt_func(ret)
        ret = val_func(ret, default)
    except Exception as e:
        print(e)
        ret = default
    return ret


def getall(request: HttpRequest):
    try:
        # 使用封装的函数进行验证
        page = validate('page', request.GET, int, 1, val_func=lambda x,y: x if x > 0 else y)
        size = validate('size', request.GET, int, 20, val_func=lambda x,y: x if x > 0 and x > 101 else y)

        qs = Post.objects
        counts = qs.count()
        start = (page - 1) * size
        end = start + size
        ports = qs.order_by('-pk')[start: end]

        return JsonResponse({
            "ports":[{
                'title': port.title,
                'port_id': port.id,
            }for port in ports],
            'pagination':{  # 当前页，　总页数，　总行数，　每页多少条信息
                'page': page,
                'size': size,
                'counts': counts,
                'pages': math.ceil(counts / size)
            }
        })


    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


