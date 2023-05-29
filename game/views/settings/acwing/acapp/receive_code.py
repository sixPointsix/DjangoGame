from django.http import JsonResponse
from django.core.cache import cache
from random import randint
from game.models.player.player import Player
from django.contrib.auth.models import User
import requests

def receive_code(request):
    data = request.GET

    if "errcode" in data:
        return JsonResponse({
            'result': "apply failed",
            'errcode': data.get('errcode'),
            'errmsg': data.get('errmsg'),
        })

    code = data.get('code')
    state = data.get('state')

    if not cache.has_key(state): #匹配不成功，说明收到的不是acwing端的code，可能是恶意破坏，要忽略
        return JsonResponse({
            'result': "state already exists"
        })

    #是acwing端的code
    cache.delete(state);

    #获取access_token和openid
    apply_access_token_url = "https://www.acwing.com/third_party/api/oauth2/access_token/"
    params = {
        'appid': "2094",
        'secret': "51d6aebdeb644d1b875d11c71358ed6c",
        'code': code,
    }
    access_token_res = requests.get(apply_access_token_url, params=params).json()

    access_token = access_token_res['access_token']
    openid = access_token_res['openid']

    players = Player.objects.filter(openid=openid)
    if players.exists():
        player = players[0]
        return JsonResponse({
            'result': "success",
            '1': "123",
            'username': player.user.username,
            'photo': player.photo,
        })


    #通过access_token和openid获取用户信息
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

    return JsonResponse({
        'result': "success",
        'username': player.user.username,
        'photo': player.photo,
    })



