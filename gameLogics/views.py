# from os import read
from django.shortcuts import redirect, render
from django.http import JsonResponse, request
from pathlib import Path
import csv,random,math
from .models import Ships,Crews,GameAccount,Location,Commodities,dotENV
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .custom_decorators import GameInitRequired
from .shop_logics import *
from .admin import super_init_sec
from .marketplace import validateBuy,validateSell,updateMplace
from .travel import getMyNextLocation,getDistance
from .travel import addStress,reduceShipCondition,addCIVILWAR
from .randomEvents import executeRevent
from . import DISPCARGE,CHARGE,HIGHESTNEGBALANCE,TAXRANGE
from .leaderboad import *
from .terminal import *
from .leisure import *
from .srBay import *
from .lender import denvFirstSetLoanOffer,setLoanOffer,cutInterest,isNloan,initShipLoan,isSloan,cutShipInterest

ERROR = JsonResponse({"Response" : "ERROR (X)"})


now = int(datetime.now().strftime("%d"))

# -------------------____ACCOUNT_____-----------------
# Create your views here.
def allRanks(request):
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
    return render(request,"gameLogics/leaderboard.html",{
        "allGa":allGa
    })

@login_required
def areYouReady(request):
    user = request.user

    # C: user login check
    if not request.user.is_authenticated:
        return errorSample("Please login first / Invalid user !!!")
    
    # c: user game account check
    myGameAccount = GameAccount.objects.filter(user=user)
    if myGameAccount:
        ship = myGameAccount[0].ship_info['ship']
        if not ship:
            return redirect("gameLogics:selectShip")
        return redirect("gameLogics:mainGameDashboard")

    return render(request,"gameLogics/areYouReady.html")

@login_required
def createGameAccount(request):
    user = request.user
    if not user.is_authenticated:
        return errorSample("user not found!")
    
    myGameAccount = GameAccount.objects.filter(user=user)

    if myGameAccount:
        try:
            ship = myGameAccount[0].ship_info['ship']
            if not ship:
                return redirect("gameLogics:selectShip")
            else:
                return redirect("gameLogics:mainGameDashboard")
        except :
            return redirect("gameLogics:mainGameDashboard")
    
    create = GameAccount(user=user)
    create.save()

    return redirect("gameLogics:selectShip")

# @login_required
# def selectShipAsCaptain(request):
#     def prepare_dotENV(gameAccount):
#         user = gameAccount.user
#         location = gameAccount.location.name
#         commoditiesList=setCommoditiePrice(location)
        
#         com_json_info = {
#             "json_info" : commoditiesList,
#             "travel" : 1,
#             "terminal":getRandomCrews(request),
#         }
#         location_json_info = {
#             "json_info" : "empty"
#         }
#         denv = dotENV.objects.get_or_create(
#             user=user,
#             ga = gameAccount,
#             com_info=com_json_info,
#             location_info=location_json_info
#         )
#         dENV_setBuyableShip(request)
#         dENV_setLeisure(request)
#         denvFirstSetLoanOffer(request)

#     def asCaptain(request):
#         ga = GameAccount.objects.get(user=user)
#         ship_info = ga.ship_info
#         ship_info['ship_condition'] = 25
#         ship_info['title'] = "Captain"
#         GameAccount.objects.filter(user=request.user).update(
#             ship_info = ship_info
#         )
#         initShipLoan(request)
    
#     user = request.user
#     if not user.is_authenticated:
#         return errorSample("user not found!")
    
#     myGameAccount = GameAccount.objects.filter(user=user)

#     if myGameAccount:
#         try:
#             ship = myGameAccount[0].ship_info['ship']
#             if not ship:
#                 create = GameAccount(user=user)
#                 create.save()
#             else:
#                 return redirect("gameLogics:mainGameDashboard")
#         except :
#             return errorSample("Invalid Url! 404'As-Captain-Starting")
#     else:
#         create = GameAccount(user=user)
#         create.save()
        
#     # GA Created
#     ships = Ships.objects.all()
#     small = []
#     for ship in ships:
#         if ship.size == "Small" : small.append(ship)
    

#     small = random.sample(small, 1)[0]
#     ship_id = small.id
#     choosenShip = Ships.objects.get(id=int(ship_id))
#     randomCredit = (random.randint(1, 5))*100000

#     GameAccount.objects.filter(user=user).update(credits=randomCredit)
    
#     updatedGAccount = GameAccount.objects.get(user=user)
#     giveRandomCrewmateAndCredit(updatedGAccount,user,choosenShip)
#     gameAc2Again = GameAccount.objects.get(user=user)
#     prepare_dotENV(gameAc2Again)

#     asCaptain(request)

#     return redirect("gameLogics:gameStarting")
@login_required
def selectShipAsCaptain(request):
    def prepare_dotENV(gameAccount):
        user = gameAccount.user
        location = gameAccount.location.name
        commoditiesList=setCommoditiePrice(location)
        
        com_json_info = {
            "json_info" : commoditiesList,
            "travel" : 1,
            "terminal":getRandomCrews(request),
        }
        location_json_info = {
            "json_info" : "empty"
        }
        denv = dotENV.objects.get_or_create(
            user=user,
            ga = gameAccount,
            com_info=com_json_info,
            location_info=location_json_info
        )
        dENV_setBuyableShip(request)
        dENV_setLeisure(request)
        denvFirstSetLoanOffer(request)

    def asCaptain(request):
        ga = GameAccount.objects.get(user=user)
        ship_info = ga.ship_info
        ship_info['ship_condition'] = 25
        ship_info['title'] = "Captain"
        GameAccount.objects.filter(user=request.user).update(
            ship_info = ship_info
        )
        initShipLoan(request)
    
    user = request.user
    if request.method == "POST":
        ship_id = request.POST['ship_idX']
        choosenShip = Ships.objects.get(id=int(ship_id))
        randomCredit = (random.randint(1, 5))*100000

        GameAccount.objects.filter(user=user).update(credits=randomCredit)
        
        updatedGAccount = GameAccount.objects.get(user=user)
        giveRandomCrewmateAndCredit(updatedGAccount,user,choosenShip)
        gameAc2Again = GameAccount.objects.get(user=user)
        prepare_dotENV(gameAc2Again)
        asCaptain(request)
        # return redirect("/")
        return redirect("gameLogics:gameStarting")

@login_required
def selectShip(request):
    def prepare_dotENV(gameAccount):
        user = gameAccount.user
        location = gameAccount.location.name
        commoditiesList=setCommoditiePrice(location)
        
        com_json_info = {
            "json_info" : commoditiesList,
            "travel" : 1,
            "terminal":getRandomCrews(request),
        }
        location_json_info = {
            "json_info" : "empty"
        }
        denv = dotENV.objects.get_or_create(
            user=user,
            ga = gameAccount,
            com_info=com_json_info,
            location_info=location_json_info
        )
        dENV_setBuyableShip(request)
        dENV_setLeisure(request)
        denvFirstSetLoanOffer(request)

    user = request.user
    if not user.is_authenticated:
        return errorSample("user not found!")
    
    myGameAccount = GameAccount.objects.filter(user=user)
    if not myGameAccount:
        return errorSample("Game Account Doesent exist")
    
    try:
        ship = myGameAccount[0].ship_info['ship']
        if ship:
            return redirect("gameLogics:mainGameDashboard")
    except:
        pass

    if request.method == "POST":
        ship_id = request.POST['ship_id']
        try:
            that_id = int(ship_id)
        except:
            return errorSample("Please select a ship first!")
        choosenShip = Ships.objects.get(id=int(ship_id))
        randomCredit = (random.randint(1, 5))*100000

        GameAccount.objects.filter(user=user).update(credits=randomCredit)
        
        updatedGAccount = GameAccount.objects.get(user=user)
        giveRandomCrewmateAndCredit(updatedGAccount,user,choosenShip)
        gameAc2Again = GameAccount.objects.get(user=user)
        prepare_dotENV(gameAc2Again)
        return redirect("gameLogics:gameStarting")

    ships = Ships.objects.all()
    medium = []
    small = []
    for ship in ships:
        if ship.size == "Medium": medium.append(ship) 
        elif ship.size == "Small" : small.append(ship)
    

    small = random.sample(small, 2)
    medium = random.sample(medium, 3)
    collectedShips = medium+small

    # CAPTAIN
    ships = Ships.objects.all()
    small = []
    for ship in ships:
        if ship.size == "Small" : small.append(ship)
    

    small = random.sample(small, 1)[0]
    # EndCaptain
    return render(request,"gameLogics/selectShip.html",{
        "ships" : collectedShips,
        "small" : small
    })


@login_required
@GameInitRequired
def gameStarting(request):
    user = request.user
    gameAccount =GameAccount.objects.get(user=user)
    return render(request,"gameLogics/gameStarting.html",{
        "location": gameAccount.location,
        "gameAccount" : gameAccount
    })


# Super Helper
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

    


# --------------------______MAIN GAME_________--------------
@login_required
def mainGameDashboard(request):
    
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])

    #Update
    updateMplace(request)
    #

    myGameAccount = response['myGameAccount']
    
    location = myGameAccount.location

    chargeBABLE = 0
    emptyCharge = myGameAccount.ship_info['fuel']['capacity'] - myGameAccount.ship_info['fuel']['filled']
    possible = int(myGameAccount.credits/CHARGE)

    if possible == 0 or emptyCharge == 0:
        costCharge = 0
        possible = 0
    else:
        if possible >= emptyCharge:
            chargeBABLE = emptyCharge
            possible = emptyCharge
        elif possible < emptyCharge:
            chargeBABLE = possible
        costCharge = chargeBABLE*CHARGE

    disC =  math.ceil(getDistance(myGameAccount.location.name,getMyNextLocation(myGameAccount))/DISPCARGE)
    if myGameAccount.credits < 0:
        possible = 0
        costCharge = 0

    # UN
    tax = myGameAccount.ship_info['tax']['pay']
    cwage = myGameAccount.ship_info['cwage']['pay']
    myrank = myRank(request)
    # UN
    # TEST
    try:
        stress = "{0:.1f}".format(sum([x['stress'] for x in myGameAccount.ship_info['crews']])/(len(myGameAccount.ship_info['crews'])*10)*100)
    except:
        stress = 0
        
    crewsCAP = Ships.objects.filter(name=myGameAccount.ship_info['ship']['name'])[0].crew
    crewsIHave = len(myGameAccount.ship_info['crews'])
    # TEST
    htmlFile = None
    if myGameAccount.ship_info['title'] == "Purser":
        htmlFile = "gameLogics/mainDashboard/dashboardPurser.html"
    if myGameAccount.ship_info['title'] == "Captain":
        htmlFile = "gameLogics/mainDashboard/dashboard.html"
    return render(request,htmlFile,{
        "cred":f'{myGameAccount.credits:,}',
        "crews" : myGameAccount.ship_info['crews'],
        "location" : location,
        "myGameAccount" : myGameAccount,
        "nextLocation":getMyNextLocation(myGameAccount),
        "dis":getDistance(location.name,getMyNextLocation(myGameAccount)),
        "disC":disC,
        "fullChargeC":emptyCharge,
        "fullCharge":f'{emptyCharge*CHARGE:,}',
        "possibleChargeC":possible,
        "costCharge":f'{costCharge:,}',
        "tax": f'{tax:,}',
        "next_location":Location.objects.filter(name=getMyNextLocation(myGameAccount))[0],
        "RR_FEE":f'{int(location.docking_fee/10):,}',
        "docking_fee":f'{int(Location.objects.filter(name=getMyNextLocation(myGameAccount))[0].docking_fee / 10):,}',
        "cwage":f'{cwage:,}',
        "ship_info":myGameAccount.ship_info,
        "myrank":myrank,
        "stress":stress,
        "crewsCAP" : crewsCAP,
        "crewsIHave" : crewsIHave,
    })


@login_required
def refillCharge(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])


    myGameAccount = response['myGameAccount']
    
    chargeBABLE = 0
    emptyCharge = myGameAccount.ship_info['fuel']['capacity'] - myGameAccount.ship_info['fuel']['filled']
    possible = int(myGameAccount.credits/CHARGE)
    
    if possible == 0 :
        return redirect("/")
        # return errorSample("You dont have enough money to buy charges⚡ 😢")
    
    elif emptyCharge == 0:
        return errorSample("Already Full Charge⚡")

    elif possible >= emptyCharge:
        chargeBABLE = emptyCharge
        possible = emptyCharge
    elif possible < emptyCharge:
        chargeBABLE = possible
    costCharge = chargeBABLE*CHARGE
    
    charging = myGameAccount.ship_info['fuel']['filled'] + possible
    final = myGameAccount.ship_info
    final['fuel']['filled']=charging

    if myGameAccount.credits < 0:
        return redirect("/")
    GameAccount.objects.filter(user=request.user).update(
        credits = myGameAccount.credits-costCharge,
        ship_info = final
    )
    return redirect("/")

@login_required
def locations(request):

    mg = GameAccount.objects.get(user=request.user)
    rid = mg.ship_info['ship']['rid']
    # routes = Route.objects.get(id=rid).route_details
    routes = [x.name for x in Location.objects.all()]

    chargeBABLE = 0
    emptyCharge = mg.ship_info['fuel']['capacity'] - mg.ship_info['fuel']['filled']
    possible = int(mg.credits/CHARGE)

    if possible == 0 or emptyCharge == 0:
        costCharge = 0
        possible = 0
    else:
        if possible >= emptyCharge:
            chargeBABLE = emptyCharge
            possible = emptyCharge
        elif possible < emptyCharge:
            chargeBABLE = possible
        costCharge = chargeBABLE*CHARGE

    rlist = []
    for route in routes:
        if mg.location.name == route : pass
        else:
            obj = {}
            disC =  math.ceil(getDistance(mg.location.name,route)/DISPCARGE)
            obj["location"] = route
            obj["distance"] = disC
            obj["docking_fee"] = int(Location.objects.filter(name=route)[0].docking_fee / 10)
            for x in mg.ship_info['location']['cwar']:
                if x['location'] == route:
                    obj['ban'] = x['ban'] - mg.ship_info['week_s']
            rlist.append(obj)

    # TEST
    # print(rlist)
    return render(request,"gameLogics/locations/locations.html",{
        "rlist":rlist
    })


@login_required
@GameInitRequired
def clickNextLocation(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])
    
    

    if response['myGameAccount'].ship_info['title'] == "Purser":
        return purserNL(request,response)

    if response['myGameAccount'].ship_info['title'] == "Captain":
        return captainNL(request,response)

# Snext
def purserNL(request,response):
    alerts = []

    crewMembers = response['myGameAccount'].ship_info['crews']
    myGameAccount = response['myGameAccount']
    new_location = getMyNextLocation(myGameAccount)

    # print()
    charges =  math.ceil(getDistance(myGameAccount.location.name,new_location)/DISPCARGE)
    # costOnTravel = charges*150000

    final = myGameAccount.ship_info
    if (final['fuel']['filled'] - charges) < 0:
        return redirect("gameLogics:criticalSituation",info="Sorry We dont have enough charge ⚡",step="Go Back & Purchase Charge")
    final['fuel']['filled'] = final['fuel']['filled'] - charges

    crewSalary = sum([c['weeklySalary'] for c in crewMembers])
    final['cwage']['pay'] += crewSalary*charges


    docker_fees = int(Location.objects.filter(name=new_location)[0].docking_fee/10)

    if len(myGameAccount.ship_info['crews'])==0:
        # return redirect("gameLogics:criticalSituation",info="You Have Lost All Of Your Crewmates 😢 (GAME OVER)",step="None")
        return redirect("gameLogics:criticalSituation",info=f"You have lost your entire crew and cannot continue. The ship’s owner has recalled ({myGameAccount.ship_info['ship']['name']}) and relieved you of your position.",step="None")
    
    if myGameAccount.credits < HIGHESTNEGBALANCE:
        return redirect("gameLogics:criticalSituation",info="You can't pay docking fee! High Negative Balance 😢. (Over -500K)",step="Go Back & Do something")

    if myGameAccount.ship_info['tax']['pay'] > TAXRANGE:
        return redirect("gameLogics:criticalSituation",info="Your Taxes Due is higher than 5000K",step="Go Back & Pay")

    if myGameAccount.ship_info['cwage']['pay'] > myGameAccount.ship_info['cwage']['range']:
        return redirect("gameLogics:criticalSituation",info="Crew revolted over unpaid wages and have abandoned their posts. Your ship is empty and cannot operate. The ship’s owner has relieved you from your position.",step="Go Back & Try To Pay Wage")

    
    # Add Stress
    alerts_Stress = addStress(myGameAccount,charges)
    
    if alerts_Stress != None:
        for al in alerts_Stress:
            alerts.append(al)
    
    alert_ship_condition = reduceShipCondition(myGameAccount,charges)

    if alert_ship_condition: alerts.append(alert_ship_condition)

    # END STRESS
    final['week_s'] += charges
    
    GameAccount.objects.filter(user=request.user).update(
        credits=myGameAccount.credits - docker_fees,
        location=Location.objects.filter(name=new_location)[0],
        ship_info=final
    )

    location = new_location
    commoditiesList=setCommoditiePrice(location)
    
    com_json_info = {
        "json_info" : commoditiesList,
        "travel" : 1,
        "terminal":getRandomCrews(request),
        "loanOffer":setLoanOffer(request),
    }
    if isNloan(request):
        com_json_info['nLoan'] = cutInterest(request)
    if isSloan(request):
        com_json_info['shipLoan'] = cutShipInterest(request)

    dotENV.objects.filter(user=request.user).update(
        com_info=com_json_info,
    )
    dENV_setBuyableShip(request)
    dENV_setLeisure(request)
    

    allevents = executeRevent(request,charges)
    if alerts == [] and allevents == []: return redirect("/")

    # print(allevents)
    return render(request,"gameLogics/inbetween/inbetween.html",{
        "alerts":alerts,
        "allevents":allevents
    })

def captainNL(request,response):
    alerts = []

    if request.method != "POST":
        return errorSample("You dont have enough money to pay tax!")
    
    loc = request.POST['loc']
    crewMembers = response['myGameAccount'].ship_info['crews']
    myGameAccount = response['myGameAccount']
    # new_location = getMyNextLocation(myGameAccount)
    new_location = loc

    # print()
    charges =  math.ceil(getDistance(myGameAccount.location.name,new_location)/DISPCARGE)
    # costOnTravel = charges*150000

    final = myGameAccount.ship_info
    if (final['fuel']['filled'] - charges) < 0:
        return redirect("gameLogics:criticalSituation",info="Sorry We dont have enough charge ⚡",step="Go Back & Purchase Charge")
    final['fuel']['filled'] = final['fuel']['filled'] - charges

    crewSalary = sum([c['weeklySalary'] for c in crewMembers])
    final['cwage']['pay'] += crewSalary*charges


    docker_fees = int(Location.objects.filter(name=new_location)[0].docking_fee/10)

    if len(myGameAccount.ship_info['crews'])==0:
        # return redirect("gameLogics:criticalSituation",info="You Have Lost All Of Your Crewmates 😢 (GAME OVER)",step="None")
        return redirect("gameLogics:criticalSituation",info=f"You have lost your entire crew and cannot continue. The ship’s owner has recalled ({myGameAccount.ship_info['ship']['name']}) and relieved you of your position.",step="None")
    
    if myGameAccount.credits < HIGHESTNEGBALANCE:
        return redirect("gameLogics:criticalSituation",info="You can't pay docking fee! High Negative Balance 😢. (Over -500K)",step="Go Back & Do something")

    if myGameAccount.ship_info['tax']['pay'] > TAXRANGE:
        return redirect("gameLogics:criticalSituation",info="Your Taxes Due is higher than 5000K",step="Go Back & Pay")

    if myGameAccount.ship_info['cwage']['pay'] > myGameAccount.ship_info['cwage']['range']:
        return redirect("gameLogics:criticalSituation",info="Crew revolted over unpaid wages and have abandoned their posts. Your ship is empty and cannot operate. The ship’s owner has relieved you from your position.",step="Go Back & Try To Pay Wage")

    
    # Add Stress
    alerts_Stress = addStress(myGameAccount,charges)
    
    if alerts_Stress != None:
        for al in alerts_Stress:
            alerts.append(al)
    
    alert_ship_condition = reduceShipCondition(myGameAccount,charges)

    if alert_ship_condition: alerts.append(alert_ship_condition)

    # END STRESS
    final['week_s'] += charges

    final = addCIVILWAR(request,final)
    GameAccount.objects.filter(user=request.user).update(
        credits=myGameAccount.credits - docker_fees,
        location=Location.objects.filter(name=new_location)[0],
        ship_info=final
    )

    location = new_location
    commoditiesList=setCommoditiePrice(location)
    
    com_json_info = {
        "json_info" : commoditiesList,
        "travel" : 1,
        "terminal":getRandomCrews(request),
        "loanOffer":setLoanOffer(request),
    }
    if isNloan(request):
        com_json_info['nLoan'] = cutInterest(request)
    if isSloan(request):
        com_json_info['shipLoan'] = cutShipInterest(request)

    dotENV.objects.filter(user=request.user).update(
        com_info=com_json_info,
    )
    dENV_setBuyableShip(request)
    dENV_setLeisure(request)

    allevents = executeRevent(request,charges)
    if alerts == [] and allevents == []: return redirect("/")

    # print(allevents)
    return render(request,"gameLogics/inbetween/inbetween.html",{
        "alerts":alerts,
        "allevents":allevents
    })

@login_required
@GameInitRequired
def inbetween(request):
    alerts = []
    obj={}
    obj['title'] = "❌ Your Crewmate left job!"
    obj['details'] = "MR. Hello , MRS. Portman Left their Job . Because of high stress."
    alerts.append(obj)
    obj = {}
    obj['title'] = "Your Crewmates stress is getting high "
    obj['details'] = "MR. Cokaniam's stress is 10. Plase Do something, Try to reduce their stress!"
    alerts.append(obj)
    return render(request,"gameLogics/inbetween/inbetween.html",{
        "alerts":alerts
    })

@login_required
@GameInitRequired
def payTax(request):
    if request.method == "POST":
        user = request.user
        ga = GameAccount.objects.get(user=user)
        credit = ga.credits
        tax = ga.ship_info['tax']['pay']

        insSI = ga.ship_info
        
        if credit < tax:
            return errorSample("You dont have enough money to pay tax!")
        else:
            # print(credit,tax)
            insSI['tax']['pay'] = 0
            GameAccount.objects.filter(user=user).update(
                credits=credit-tax,
                ship_info=insSI
            )
            return redirect("/")
        
    return errorSample("Invalid URL!")

@login_required
@GameInitRequired
def payWages(request):
    if request.method == "POST":
        user = request.user
        ga = GameAccount.objects.get(user=user)
        credit = ga.credits
        wages = ga.ship_info['cwage']['pay']

        insSI = ga.ship_info
        
        if credit < wages:
            return errorSample("You dont have enough money to pay wages!")
        else:
            if insSI["cwage"]["pay"] == 0:
                pass
            else:
                ins = ga.ship_info
                crews = ins['crews']
                for i,crew in enumerate(crews):
                    newStress = float("{0:.1f}".format(crew['stress'] - crew['stress']*(15/100)))
                    if newStress <= 0:
                        crew['stress'] = 0
                    else:
                        crew['stress'] = newStress
                GameAccount.objects.filter(user=user).update(ship_info=ins)
                
            insSI['cwage']['pay'] = 0
            GameAccount.objects.filter(user=user).update(
                credits=credit-wages,
                ship_info=insSI
            )

            

            return redirect("/")
        
    return errorSample("Invalid URL!")

@login_required
@GameInitRequired
def RandR(request):
    user = request.user
    myGameAccount = GameAccount.objects.get(user=user)
    docking_fee = int(myGameAccount.location.docking_fee)/10
    
    denv = dotENV.objects.get(user=request.user)

    state = denv.com_info['travel']

    if state == 0:
        return errorSample(f"Two weeks on {myGameAccount.location.name} is prohibited.Unable to allow your crew another week of R&R here.")

    # print(myGameAccount.credits , docking_fee)
    if myGameAccount.credits < docking_fee:
        return errorSample("You dont have enough money!")

    newBalance = myGameAccount.credits - docking_fee
    GameAccount.objects.filter(user=user).update(credits=newBalance)

    ins = myGameAccount.ship_info
    crews = ins['crews']

    for i,crew in enumerate(crews):
        newStress = float("{0:.1f}".format(crew['stress'] - crew['stress']*(40/100)))
        if newStress <= 0:
            crew['stress'] = 0
            # print(crew['stress'])
        else:
            crew['stress'] = newStress
            # print(crew['stress'])
    GameAccount.objects.filter(user=user).update(ship_info=ins)

    ins2 = denv.com_info
    ins2['travel'] = 0
    dotENV.objects.filter(user=user).update(com_info=ins2)

    return redirect("/")

@login_required
@GameInitRequired
def marketplace(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])
    myGameAccount = response['myGameAccount']
    comList = getCommoditiePrice(request.user)
    gameAccount = GameAccount.objects.get(user=request.user)
    ship_info = gameAccount.ship_info
    coms = gameAccount.ship_info['coms']
    for com in comList:
        try:
            com["ship_stock"] = coms[com['name']]
        except:
            com["ship_stock"] = 0
            GameAccount.objects.filter(user=request.user).update(
                ship_info=ship_info
            )
        
    return render(request,"gameLogics/marketplace/marketplace.html",{
        "cred":f'{myGameAccount.credits:,}',
        "myGameAccount" : myGameAccount,
        "commoditiesList" : comList,
        "ship_info":ship_info
    })

@login_required
def buyItem(request):
    if request.method == "POST":
        user = request.user
        product = request.POST['product']
        quantity = request.POST['quantity']
        if int(quantity)<=0: return redirect("gameLogics:marketplace")

        res = validateBuy(product,quantity,user)
        # print(res)
        if res['res'] == "Error":
            return render(request,"gameLogics/sample/failed-purchase.html",{
                "reason":res['reason']
            })
        return redirect("gameLogics:marketplace")

@login_required
def sellItem(request):
    if request.method == "POST":
        user = request.user
        product = request.POST['product']
        quantity = request.POST['quantity']
        if int(quantity)<=0: return redirect("gameLogics:marketplace")

        res = validateSell(product,quantity,user)
        # print(res)
        if res['res'] == "Error":
            return render(request,"gameLogics/sample/failed-purchase.html",{
                "reason":res['reason']
            })
        return redirect("gameLogics:marketplace")

@login_required
def terminal(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])
    myGameAccount = response['myGameAccount']
    gameAccount = GameAccount.objects.get(user=request.user)
    ship_info = gameAccount.ship_info
    denv = dotENV.objects.get(user=request.user)
    rc = denv.com_info['terminal']


    return render(request,"gameLogics/terminal/terminal.html",{
        "cred":f'{myGameAccount.credits:,}',
        "myGameAccount" : myGameAccount,
        "ship_info":ship_info,
        "rc":rc
    })

@login_required
def hiringCrew(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])

    if request.method == "POST":
        crew_id = request.POST['crew_id']
        res = hiring(request,crew_id)
        if res['res'] == "Success":
            return redirect("/")
        else:
            return errorSample(res['reason'])
    else:
        return errorSample("Invalid Request!")

@login_required
def leisure(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])
    myGameAccount = response['myGameAccount']
    gameAccount = GameAccount.objects.get(user=request.user)
    ship_info = gameAccount.ship_info

    denv = dotENV.objects.get(user=request.user)
    com_info = denv.com_info
    plist = com_info['leisureList']

    try:
        stress = "{0:.1f}".format(sum([x['stress'] for x in myGameAccount.ship_info['crews']])/(len(myGameAccount.ship_info['crews'])*10)*100)
    except:
        stress = 0

    return render(request,"gameLogics/leisure/leisure.html",{
        "cred":f'{myGameAccount.credits:,}',
        "myGameAccount" : myGameAccount,
        "ship_info":ship_info,
        "plist":plist,
        "stress":stress,
        "crews":myGameAccount.ship_info['crews']
    })

def payLeisure(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])

    if request.method == "POST":
        weeks = request.POST['weeks']
        res = confirmPaymentLeisure(request,weeks)
        if res['res'] == "Success":
            return redirect("/")
        else:
            return errorSample(res['reason'])
    else:
        return errorSample("Invalid Request!")


@login_required
def criticalSituation(request,info,step):
    return render(request,"gameLogics/sample/criticalSituation.html",{
        "info":info,
        "step":step
    })


@login_required
def deleteGameAccount(request):
    GameAccount.objects.filter(user=request.user).delete()
    dotENV.objects.filter(user=request.user).delete()
    return redirect("/")
# ----------____END_____----------

# Helper ROUTES
def init_ships(request,csv_to_db):
    if csv_to_db != "si":
        return redirect("/")
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(BASE_DIR) + "/gameLogics/csv/Ships.csv"
    with open(path) as f:
        reader = csv.reader(f)
        count = 1
        for row in reader:
            created = Ships.objects.get_or_create(
                mid=count,
                name = row[0],
                size = row[1],
                type = row[2],
                value = modValue(row[3]),
                crew = int(row[4]),
                cargo = modValue(row[5]),
                fuel = int(row[6]),
                passengers = int(row[7]),
                upgrade_slot = int(row[8]),
                upgrade1 = row[9],
                upgrade2 = row[10],
                upgrade3 = row[11],
                upgrade4 = row[12],
                upgrade5 = row[13],
                rid=Route.objects.filter(rid=row[14])[0]
                )
            count += 1
    return JsonResponse({
        "return" : str(BASE_DIR) + "/gameLogics/Ships.csv"
    })

def init_crews(request,csv_to_db):
    if csv_to_db != "si":
        return redirect("/")
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(BASE_DIR) + "/gameLogics/csv/Crew.csv"
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            created = Crews.objects.get_or_create(
                name = row[0],
                profession = row[1],
                weeklySalary = modValue(row[2]),
                fromW = row[3],
                health = int(row[4]),
                stress = int(row[5]),
                resolve = int(row[6]),
                hunger = int(row[7]),
                condition1 = row[8],
                condition2 = row[9],
                condition3 = row[10],
                )
    return JsonResponse({
        "return" : str(BASE_DIR) + "/gameLogics/csv/Crew.csv"
    })

def init_locations(request,csv_to_db):
    if csv_to_db != "si":
        return redirect("/")
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(BASE_DIR) + "/gameLogics/csv/locations.csv"
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            created = Location.objects.get_or_create(
                name = row[1],
                gains_tax_rate = row[2],
                docking_fee = row[3],
                weekly_interest = row[4],
                marketplace = row[5],
                repair_bay = row[6],
                med_bay = row[7],
                pasengers_crew = row[8],
                missions_reqs = row[9],
                lender = row[10],
                storage = row[11],
                ship_dealer = row[12],
                leisure = row[13],
            )
    return JsonResponse({
        "return" : str(BASE_DIR) + "/gameLogics/csv/Crew.csv"
    })

def init_commodities(request,csv_to_db):
    if csv_to_db != "si":
        return redirect("/")
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(BASE_DIR) + "/gameLogics/csv/Commodities.csv"
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            created = Commodities.objects.get_or_create(
                name = row[0],
                min_price = row[1],
                max_price = row[2],

                fragile = bool(row[3]),
                perishable = bool(row[4]),
                edible = bool(row[5]),

                earth = row[6],
                moon = row[7],
                mars = row[8],
                phobos = row[9],
                deimos = row[10],
                europa = row[11],
                titan = row[12],
                ganymede = row[13],
                enceladus = row[14],
                io = row[15],
                callisto = row[16],
                triton = row[17],
            )
    return JsonResponse({
        "return" : str(BASE_DIR) + "/gameLogics/csv/Commodities.csv"
    })

def super_init(request,csv_to_db):
    if csv_to_db != "si":
        return redirect("/")
    return super_init_sec()

# Helper Functions
def modValue(strAmount):
        ammount = strAmount.replace("$","").replace(".00","").replace(",","")
        return int(ammount)

def errorSample(stitle):
    return redirect("account:sampleFuture",title=stitle)

def giveRandomCrewmateAndCredit(gameAccount,user,ship_mod):
    def welcome_init_new_location(gameAccount,user):
        locations = Location.objects.all()
        locationList = []
        for location in locations:
            locationList.append(location)
        
        location = random.sample(locationList,1)[0]
        GameAccount.objects.filter(user=user).update(location=location)

        setCommoditiePrice(location.name)
    ship_model = Ships.objects.get(id=ship_mod.id)
    n = ship_model.crew
    crewmates = Crews.objects.all()
    randomCrewmates = random.sample(list(crewmates), n)
        
    welcome_init_new_location(gameAccount,user)
    clist = []
    for crews in randomCrewmates:
        obj = {}
        obj['name']=crews.name
        obj['profession']=crews.profession
        obj['weeklySalary']=crews.weeklySalary
        obj['fromW']=crews.fromW
        obj['health']=crews.health
        obj['stress']=crews.stress
        obj['resolve']=crews.resolve
        obj['hunger']=crews.hunger
        obj['condition1']=crews.condition1
        obj['condition2']=crews.condition2
        obj['condition3']=crews.condition3
        clist.append(obj)
    ship_info_dict = {
        "ship": {
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
        },
        "week_s":0,
        "title":"Purser",
        "ship_condition":100,
        "cargo" : {
            "total":ship_model.cargo,
            "filled":0
            },
        "coms":{},
        "fuel" : {
            # "filled":int(gameAccount.ship.fuel/2),
            "filled":int(ship_model.fuel),
            "capacity":ship_model.fuel
        },
        "tax":{
            "pay":0,
        },
        "cwage":{
            "pay":0,
            "range":sum([ c['weeklySalary'] for c in clist] )*12,
        },
        "crews":clist,
        "location":{
            "cwar":[]
        }
    }
    coms = Commodities.objects.all()
    for com in coms:
        ship_info_dict["coms"][com.name]=0
                
    GameAccount.objects.filter(user=user).update(game_init=True,ship_info=ship_info_dict)


def setCommoditiePrice(location_name):
        commodities = []
        if location_name == "Earth":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.earth.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(10,100,10)
                if comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Mars":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.mars.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                if comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Earth Moon":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.moon.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Phobos":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.phobos.split("|")
                # print(comlist['name'],comlist['available'],comlist['sp'])
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Deimos":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.deimos.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Europa":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.europa.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0

                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Titan":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.titan.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Ganymede":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.ganymede.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)

        elif location_name == "Enceladus":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.enceladus.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Io":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.io.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Callisto":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.callisto.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        elif location_name == "Triton":
            coms = Commodities.objects.all()
            for com in coms:
                comlist = {}
                comlist['id'] = com.id
                comlist['name'] = com.name
                comlist['min_price'] = com.min_price
                comlist['max_price'] = com.max_price
                
                comlist['available'],comlist['sp'] = com.triton.split("|")
                
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(50,250,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        return commodities

def getCommoditiePrice(user):
        commodities = []
        dotenv = dotENV.objects.get(user=user)
        com_info = dotenv.com_info['json_info']
        for v in com_info:
            commodities.append(v)
        return commodities


# ---------------------PRACTICE-------------
def supertest(request):
    return JsonResponse({})