import os
import bcrypt
import jwt
from user.models import User
from django.http import HttpResponse

def index():

    a = os.path.abspath(__file__)
    print(a)

def index1():
    a = os.path.dirname(os.path.abspath(__file__))
    print(a)



def test(request):
    pwd = 'abc'.encode()
    user = User.objects.get(name='renl')
    print(bcrypt.checkpw(pwd, user.password.encode()+ b'1'))
    return HttpResponse("嗯哼")


