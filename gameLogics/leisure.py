from .models import *
import random

def dENV_setLeisure(request):
    denv = dotENV.objects.get(user=request.user)
    com_info = denv.com_info
    com_info['leisureList'] = randomizeLeisureList(request) 

    dotENV.objects.filter(user=request.user).update(
        com_info=com_info
    )
    

def allLeisurePrice(ship_info):
    clen = len(ship_info['crews'])
    plist = [
        {"weeks":1,"sr" : 10,"price" : int((clen*10*1000)/2)},
        {"weeks":2,"sr" : 30,"price" : int((clen*30*1000)/2)},
        {"weeks":3,"sr" : 50,"price" : int((clen*50*1000)/2)},
        {"weeks":4,"sr" : 90,"price" : int((clen*90*1000)/2)},
    ]
    return plist

def randomizeLeisureList(request):
    ga = GameAccount.objects.get(user=request.user)
    ship_info = ga.ship_info
    plist = allLeisurePrice(ship_info)
    ri = random.randint(1,4)
    flist = random.sample(plist,ri)
    return flist

def getleisurePrice(request,weeks):
    ga = GameAccount.objects.get(user=request.user)
    ship_info = ga.ship_info
    plist = allLeisurePrice(ship_info)
    for x in plist:
        if x['weeks'] == weeks:
            return x

def confirmPaymentLeisure(request,weeks):
    priceObj = getleisurePrice(request,int(weeks))
    ga = GameAccount.objects.get(user=request.user)
    # ERRORS
    credits = ga.credits
    if credits <= priceObj['price']:
        return {
            "res":"Failed",
            "reason":"Insufficient funds!"
        }
    # ENDERROS
    ship_info = ga.ship_info
    ship_info['week_s'] += int(weeks)
    GameAccount.objects.filter(user=request.user).update(
        credits=credits- priceObj['price'],
        ship_info=ship_info
    )
    bulkReduceStress(request,priceObj['sr'])
    return {
        "res":"Success"
    }

def bulkReduceStress(request,per):
    ga = GameAccount.objects.get(user=request.user)
    ins = ga.ship_info
    crews = ins['crews']
    for i,crew in enumerate(crews):
        newStress = float("{0:.1f}".format(crew['stress'] - crew['stress']*(per/100)))
        if newStress <= 0:
            crew['stress'] = 0
        else:
            crew['stress'] = newStress
    GameAccount.objects.filter(user=request.user).update(ship_info=ins)
