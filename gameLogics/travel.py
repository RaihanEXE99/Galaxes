from .models import *
import random

MAIN_ROUTE = ["Earth","Earth Moon","Mars","Phobos","Deimos","Europa","Titan","Ganymede","Enceladus","Io","Callisto","Triton"]

def getMyNextLocation(gameAccount):
    ship = gameAccount.ship_info['ship']
    shipRoute_OBJ = Route.objects.get(rid=ship['rid'])
    routeList = shipRoute_OBJ.route_details
    
    myCurrentLocation = gameAccount.location.name


    nextLocation = None
    if myCurrentLocation in routeList:
        for i,v in enumerate(routeList):
            if v==myCurrentLocation:
                if i==len(routeList)-1:
                    nextLocation = routeList[0]
                else:
                    nextLocation = routeList[i+1]
    else:
        for i,v in enumerate(MAIN_ROUTE):
            if v == myCurrentLocation and i==len(MAIN_ROUTE)-1:
                nextLocation = routeList[0]
                break
            else:
                if v == myCurrentLocation:
                    if MAIN_ROUTE[i+1] in routeList:
                        for m,n in enumerate(routeList):
                            if n == MAIN_ROUTE[i+1]:
                                if n != len(routeList)-1:
                                    nextLocation = routeList[0]
                                    return nextLocation
                                else:
                                    nextLocation = routeList[n+1]
                                    return nextLocation          
                else:
                    nextLocation = routeList[0]
    return nextLocation

def getDistance(l1,l2):
    dis = Distance.objects.filter(location1=l1,location2=l2)
    if not dis:
        dis = Distance.objects.filter(location1=l2,location2=l1)
    dis = dis[0]
    return dis.distance


def addStress(myGameAccount,weeks):
    alerts = []
    crews = myGameAccount.ship_info['crews']
    removeList = []
    str1 = ""
    for i,crew in enumerate(crews):
        if int(crew['stress']) == 10:
            str1 +=  f"{crew['name']}, "
            removeList.append(crew)
        else:
            increaseStress = .5
            crew['stress'] = float(("{0:.1f}".format((crew['stress']+increaseStress)*weeks)))
            if crew['stress'] > 10 : crew['stress'] = 10

    if str1 != "":
        str1 = str1[:len(str1)-2]
        str1 += "'s stress is 10"
        obj = {
            "title" : "Your Crewmates stress is getting high!",
            "details": str1
        }
        alerts.append(obj)

    str2 = ""
    for r in removeList:
        resolve = r['resolve']
        ranNumber = random.randrange(0,100+((resolve+1)*5))
        if ranNumber <=25:
            str2 += f"{r['name']}, "
            crews.remove(r)
    

    if str2 != "":
        str2 += "left the job! Because of high stress."
        obj = {
            "title" : "Your Crewmate left job!",
            "details": str2
        }
        alerts.append(obj)
    
    if alerts:
        return alerts
    else:
        return None

def reduceShipCondition(myGameAccount,weeks):
    alerts = []
    ship_info = myGameAccount.ship_info
    if ship_info['ship_condition'] <=0:
        ship_info['ship_condition'] = 0
    else:
        ranNUM = random.randint(1,5)
        # ship_info['ship_condition'] = ship_info['ship_condition'] - .25
        ship_info['ship_condition'] = ship_info['ship_condition'] - ranNUM
    
    GameAccount.objects.filter(id=myGameAccount.id).update(
        ship_info=ship_info
    )
    
    if alerts:
        return alerts
    else:
        return None

def addCIVILWAR(request,ship_info):
    mg = GameAccount.objects.get(user=request.user)
    rid = mg.ship_info['ship']['rid']
    routes = Route.objects.get(id=rid).route_details
    count = 0

    for x in ship_info['location']['cwar']:
        if x['ban'] <= ship_info['week_s']:
            print("trigger", x['ban'],ship_info['week_s'])
            ship_info['location']['cwar'].remove(x)
            
    for r in routes:
        for x in ship_info['location']['cwar']:
            if x['location'] == r:
                count += 1
    if (len(routes)-count)<=2:
        return ship_info

    if len(routes)>5:
        rint = random.randint(1,2)
    else:
        rint = random.randint(1,4)
    if rint != 1:
        return ship_info
    ranRoute =  random.sample(routes, 1)[0]

    ban = random.randint(1,len(routes)*3)
    ship_info['location']['cwar'].append({
        'location':ranRoute,
        'ban': ship_info['week_s'] + ban
    })
    
    return ship_info
    