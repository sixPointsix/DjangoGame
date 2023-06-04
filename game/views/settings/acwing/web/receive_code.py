from django.shortcuts import redirect
from django.core.cache import cache
from django.contrib.auth import login
from random import randint
from game.models.player.player import Player
from django.contrib.auth.models import User
import requests

# 接收第三方平台的授权码并进行处理
def receive_code(request):
    data = request.GET
    code = data.get('code')
    state = data.get('state')

    if not cache.has_key(state): #匹配不成功，说明收到的不是acwing端的code，可能是恶意破坏，要忽略
        return redirect("index") #重定向到初始的url，通过name="index"实现

    #是acwing端的code
    cache.delete(state);

    #获取access_token和openid
    apply_access_token_url = "https://www.acwing.com/third_party/api/oauth2/access_token/"
    params = {
        'appid': "2094",
        'secret': "d948568b232b4fe9a229a55dbdccfc72",
        'code': code,
    }
    access_token_res = requests.get(apply_access_token_url, params=params).json()

    access_token = access_token_res['access_token']
    openid = access_token_res['openid']

    # 如果已经存在该用户，直接自动登录
    players = Player.objects.filter(openid=openid)
    if players.exists():
        login(request, players[0].user)
        return redirect("index")

    #通过access_token和openid获取用户信息，并注册到自己的数据库中
    get_userinfo_url = "https://www.acwing.com/third_party/api/meta/identity/getinfo/"
    params = {
        "access_token": access_token,
        "openid": openid,
    }

    userinfo_res = requests.get(get_userinfo_url, params=params).json()
    username = userinfo_res['username']
    photo = userinfo_res['photo']

    while User.objects.filter(username=username).exists(): #用户名判重
        username += str(randint(0, 9))

    user = User.objects.create(username=username)
    player = Player.objects.create(user=user, photo=photo, openid=openid)

    login(request, user)
    return redirect("index")

