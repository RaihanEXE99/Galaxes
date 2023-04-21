from django.shortcuts import redirect, render
from django.http import JsonResponse, request
from .views import *
from .models import *
import random

def shipBay(request):
    return render(request,"gameLogics/srBay/shipBay.html")

def showBuyableShips(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])

    myGameAccount = response['myGameAccount']
    gameAccount = GameAccount.objects.get(user=request.user)
    ship_info = gameAccount.ship_info
    denv = dotENV.objects.get(user=request.user)
    ships = denv.com_info['buyableShips']

    return render(request,"gameLogics/srBay/buyShip/buyShip.html",{
        "cred":f'{myGameAccount.credits:,}',
        "myGameAccount" : myGameAccount,
        "ship_info":ship_info,
        "ships" : ships
    })

def dENV_setBuyableShip(request):
    gameAccount = GameAccount.objects.get(user=request.user)
    ship_info = gameAccount.ship_info

    
    allShips = Ships.objects.all()
    ri = random.randint(3,5)
    ships = random.sample([x for x in allShips],ri)

    objShips = []
    for ship_model in ships:
        if ship_model.name == ship_info['ship']['name']:
            ships.remove(ship_model)
        else:
            obj={
                "ship_condition" : 100,
                "mid" : ship_model.mid,
                "name" : ship_model.name, 
                "size" : ship_model.size,
                "type" : ship_model.type, 
                "value" : ship_model.value,
                "crew" : ship_model.crew,
                "cargo" : ship_model.cargo,
                "fuel" : ship_model.fuel,
                "passengers" : ship_model.passengers,
                "upgrade_slot" : ship_model.upgrade_slot,
                "rid" : ship_model.rid.id,
                "upgrade1" : ship_model.upgrade1,
                "upgrade2" : ship_model.upgrade2,
                "upgrade3" : ship_model.upgrade3,
                "upgrade4" : ship_model.upgrade4,
                "upgrade5" : ship_model.upgrade5,
            }
            objShips.append(obj)
    
    denv = dotENV.objects.get(user=request.user)
    com_info = denv.com_info
    com_info['buyableShips'] = objShips 

    dotENV.objects.filter(user=request.user).update(
        com_info=com_info
    )
    
def purchaeShip(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])

    if request.method == "POST":
        ship_name = request.POST['ship_name']
        res = purchaseShipFinal(request,ship_name)
        if res['res'] == "Success":
            return redirect("/")
        else:
            return errorSample(res['reason'])
    else:
        return errorSample("Invalid Request!")

def purchaseShipFinal(request,ship_name):
    mg = GameAccount.objects.get(user=request.user)
    ship_info = mg.ship_info
    ship_model = Ships.objects.filter(name=ship_name)[0]
    value = ship_model.value

    if mg.credits < value:
        return {
            "res":"Failed",
            "reason":"Insufficient funds!"
        }
    
    clen = len(ship_info['crews'])

    if clen > ship_model.crew:
        rem = clen - ship_model.crew
        for _ in range(rem):
            ship_info['crews'].pop()

    ship_info["ship"]= {
        "ship_condition" : 100,
        "mid" : ship_model.mid,
        "name" : ship_model.name, 
        "size" : ship_model.size,
        "type" : ship_model.type, 
        "value" : ship_model.value,
        "crew" : ship_model.crew,
        "cargo" : ship_model.cargo,
        "fuel" : ship_model.fuel,
        "passengers" : ship_model.passengers,
        "upgrade_slot" : ship_model.upgrade_slot,
        "rid" : ship_model.rid.id,
        "upgrade1" : ship_model.upgrade1,
        "upgrade2" : ship_model.upgrade2,
        "upgrade3" : ship_model.upgrade3,
        "upgrade4" : ship_model.upgrade4,
        "upgrade5" : ship_model.upgrade5,
    }
    GameAccount.objects.filter(user=request.user).update(
        ship_info=ship_info
    )
    dENV_setBuyableShip(request)
    return {
        "res" : "Success"
    }


# REPAIR
def repair(request):
    COST = 2000
    ga = GameAccount.objects.get(user=request.user)
    ship_info = ga.ship_info
    condition = ship_info['ship_condition']
    needImprove = 100-condition

    print(condition,ga.credits)

    info = None
    maxim = 0
    if needImprove == 0 or ga.credits < 0:
        maxim = 0
        info = f"Repair not possible in this moment"
    elif needImprove*COST>ga.credits:
        maxim = ga.credits/2000
        info = f"Repair Your Ship. This will cost {int(maxim*COST)}$ ({(maxim)}% Improvement)"
    else:
        maxim = needImprove
        info = f"Repair Your Ship. This will cost {int(maxim*COST)}$ ({(maxim)}% Improvement)"
    
    return render(request,"gameLogics/srBay/repair/repair.html",{
        "cred":f'{ga.credits:,}',
        "myGameAccount" : ga,
        "ship_info":ship_info,
        "maxim" : maxim,
        "cost":maxim*COST,
        "info":info
    })

def maxRepair(request):
    COST = 2000
    ga = GameAccount.objects.get(user=request.user)
    ship_info = ga.ship_info
    condition = ship_info['ship_condition']
    needImprove = 100-condition
    

    maxim = 0
    if needImprove == 0 or ga.credits < 0:
        maxim = 0
    elif needImprove*COST>ga.credits:
        maxim = ga.credits/2000
    else:
        maxim = needImprove
    ship_info['ship_condition'] = ship_info['ship_condition']+maxim
    
    if ship_info['ship_condition'] > 100 : ship_info['ship_condition'] = 100
    
    GameAccount.objects.filter(user=request.user).update(
        credits= ga.credits - int(maxim*2000),
        ship_info=ship_info
    )
    return redirect("/")


# def showBuyableShips(request):
#     response = checkGameAccountState(request)
#     if response['res'] == "error":
#         return errorSample(response['reason'])
#     if response['res'] == "success":
#         return redirect(response['redirect'])

#     myGameAccount = response['myGameAccount']
#     gameAccount = GameAccount.objects.get(user=request.user)
#     ship_info = gameAccount.ship_info

    
#     allShips = Ships.objects.all()
#     ri = random.randint(3,5)
#     ships = random.sample([x for x in allShips],ri)

#     for s in ships:
#         if s.name == ship_info['ship']['name']:
#             ships.remove(s)

#     return render(request,"gameLogics/srBay/buyShip/buyShip.html",{
#         "cred":f'{myGameAccount.credits:,}',
#         "myGameAccount" : myGameAccount,
#         "ship_info":ship_info,
#         "ships" : ships
#     })

def checkGameAccountState(request):
    user = request.user
    if not user.is_authenticated:
        return {"res":"error","reason":"user doesn't exist!"}

    myGameAccount = GameAccount.objects.filter(user=user)
    if not myGameAccount:
        return {"res":"success","redirect":"gameLogics:areYouReady"}
    
    try:
        ship = myGameAccount[0].ship_info['ship']
        return {"res":"ok","user":user,"myGameAccount" : myGameAccount[0],"ship":ship}
    except:
        return {"res":"success","redirect":"gameLogics:selectShip"}

def errorSample(stitle):
    return redirect("account:sampleFuture",title=stitle)