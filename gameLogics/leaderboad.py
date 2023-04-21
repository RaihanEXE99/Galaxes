from .models import *

def myRank(request):
    user = request.user
    ga = GameAccount.objects.get(user=user)
    # allGa = [x for x in GameAccount.objects.all().order_by('-credits')]
    # # print(allGa)
    # index = allGa.index(gm)
    alist = [x for x in GameAccount.objects.all().order_by('-credits')]
    allGa = []
    for x in alist:
        spl = x.ship_info['week_s']+1
        # print(x.credits,spl,(x.credits/spl))
        obj = {
            "username":x.user.username,
            "weeks":x.ship_info['week_s'],
            "credits":x.credits,
            "points":(x.credits/spl)
        }
        allGa.append(obj)
    allGa.sort(key=lambda x: x['points'], reverse=True)
    index = None
    for i,v in enumerate(allGa):
        if v['username'] == ga.user.username:
            index=i
            break
    return (index+1)

