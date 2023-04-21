# from spaceGame import gameLogics
from .models import Ships,Crews,GameAccount,Location,Commodities,dotENV
import random
from .shop_logics import *  
from .views import *  
from . import MAIN_ROUTE

def executeRevent(request,weeks):
    totalRE = []
    for week in range(1,weeks+1):
        ranEs = random.randint(0,2)
        obj ={
            "week" : week,
            "reC" : ranEs,
            "allReventNo" : [],
            "events":[]
        }
        totalRE.append(obj)
    
    for i in totalRE:
        for j in range(i['reC']):
            ri = random.randint(1,21)
            if ri not in i['allReventNo']:
                i['allReventNo'].append(ri)

    for week in totalRE:
        for ReventNo in week['allReventNo']:
            obj = selectRE(request,ReventNo,week['week'])
            if obj == None:
                week['reC'] = 0
            else:
                week['events'].append(obj)
    return totalRE
    # return [Comeacrossstrandedship1(request,1)]

def selectRE(request,no,week):
    if no == 1:
        event = pirateAttack1(request,week)
        return event
    if no ==2:
        event = pirateAttack2(request,week)
        return event
    if no == 3:
        event = pirateAttack3(request,week)
        return event
    if no == 4:
        event = pirateAttack4(request,week)
        return event

    if no == 5:
        event = shipMalfunction1(request,week)
        return event
    if no == 6:
        event = shipMalfunction2(request,week)
        return event
    if no == 7:
        event = shipMalfunction3(request,week)
        return event
    if no == 8:
        event = shipMalfunction4(request,week)
        return event
    if no == 9:
        event = shipMalfunction5(request,week)
        return event
    if no == 10:
        event = shipMalfunction6(request,week)
        return event
    if no == 11:
        event = shipMalfunction7(request,week)
        return event
    if no == 12:
        event = shipMalfunction8(request,week)
        return event

    if no == 13:
        event = interceptedMessage1(request,week)
        return event
    if no == 14:
        event = interceptedMessage2(request,week)
        return event
    if no == 15:
        event = interceptedMessage3(request,week)
        return event
    if no == 16:
        event = interceptedMessage4(request,week)
        return event
    if no == 17:
        event = interceptedMessage5(request,week)
        return event
    if no == 18:
        event = interceptedMessage6(request,week)
        return event


    if no == 19:
        event = newsBroadcast1(request,week)
        return event
    if no == 20:
        event = catastrophe1(request,week)
        return event
    if no == 21:
        event = catastrophe2(request,week)
        return event
    
    if no == 22:
        event = lawEnforcement1(request,week)
        return event
    
    if no == 23:
        event = lawEnforcement2(request,week)
        return event
    
    if no == 24:
        event = aliens1(request,week)
        return event
    
    if no == 25:
        event = aliens2(request,week)
        return event
    
    if no == 26:
        event = aliens3(request,week)
        return event
    
    if no == 27:
        event = aliens4(request,week)
        return event
    
    if no == 28:
        event = aliens5(request,week)
        return event
    
    if no == 29:
        event = aliens6(request,week)
        return event
    
    if no == 30:
        event = meninBlack(request,week)
        return event
    
    if no == 31:
        event = whatHappened2(request,week)
        return event

    if no == 32:
        event = Comeacrossstrandedship1(request,week)
        return event

    if no == 33:
        event = Comeacrossstrandedship2(request,week)
        return event



# execute 2//1
def pirateAttack1(request,week):
    event = {
        "week" : week,
        "type": "Pirate Attack",
        "subtype": "Failed to evade",
        "effect":"Pirates board the ship and steal all commodities."
    }
    # CHANCE
    ri = random.randint(1,10)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE
    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    coms = ship_info['coms']
    for k in coms:
        coms[k] = 0

    cargo = ship_info['cargo']
    cargo['filled'] = 0

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )

    return event

# execute 3//2
def pirateAttack2(request,week):
    event = {
        "week" : week,
        "type": "Pirate Attack",
        "subtype": "Failed to evade",
    }
    # CHANCE
    ri = random.randint(1,4)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE
    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    crews = ship_info['crews']

    for crew in crews:
        crew['stress'] += 2
        if crew['stress'] >10:
            crew['stress'] = 10
    
    pick = random.randint(1,3)
    

    count = 0
    for _ in range(pick):
        try:
            crews.pop()
            count += 1
        except :
            pass

    event['effect'] = f"Pirates board the ship and kidnap {count} crew. Rest of crew is stressed. +2"
    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )

    return event

# execute 4//3
def pirateAttack3(request,week):
    event = {
        "week" : week,
        "type": "Pirate Attack",
        "subtype": "Failed to evade",
        "effect":"Pirates board the ship and kidnap the owner. As the ranking officer, you're now the ship Captain."
    }
    # CHANCE
    ri = random.randint(1,20)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    ship_info['title'] = "Captain"
    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )
    
    return event

# execute 5//4
def pirateAttack4(request,week):
    event = {
        "week" : week,
        "type": "Pirate Attack",
        "subtype": "Successfully evaded",
        "effect":"That was close!"
    }
    # CHANCE
    ri = random.randint(1,2)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE
    return event


# Ship Malfunction

# 14//5
def shipMalfunction1(request,week):
    event = {
        "week" : week,
        "type": "Ship Malfunction",
        "subtype": "Engine",
        "effect":"The crew's stress has increased from being stranded (+3)."
    }
    # CHANCE
    ri = random.randint(1,2)
    if ri != 1:
        # print(ri,event)
        return None
    ga = GameAccount.objects.get(user=request.user)
    if int(ga.ship_info['ship']['ship_condition']) > 35:
        return None
    # CHANCE

    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    crews = ship_info['crews']

    for crew in crews:
        crew['stress'] += 3
        if crew['stress'] >10:
            crew['stress'] = 10

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )
    
    return event

# 15//6
def shipMalfunction2(request,week):
    event = {
        "week" : week,
        "type": "Ship Malfunction",
        "subtype": "Engine",
        "effect":"Your insurance covers emergency help and they'll be here in {} weeks.".format(random.randint(1,3))
    }
    # CHANCE
    ri = random.randint(1,5)
    if ri != 1:
        # print(ri,event)
        return None
    ga = GameAccount.objects.get(user=request.user)
    if int(ga.ship_info['ship']['ship_condition']) > 35:
        return None
    # CHANCE

    return event

# 16//7
def shipMalfunction3(request,week):
    event = {
        "week" : week,
        "type": "Ship Malfunction",
        "subtype": "Nav Systems",
    }
    # CHANCE
    ri = random.randint(1,5)
    if ri != 1:
        # print(ri,event)
        return None
    ga = GameAccount.objects.get(user=request.user)
    if int(ga.ship_info['ship']['ship_condition']) > 35:
        return None
    # CHANCE

    new_location = random.sample(MAIN_ROUTE, 1)[0]

    GameAccount.objects.filter(user=request.user).update(
        location=Location.objects.filter(name=new_location)[0],
    )

    location = new_location
    commoditiesList = setCommoditiePrice(location)
    
    com_json_info = {
        "json_info" : commoditiesList,
        "travel" : 1
    }

    dotENV.objects.filter(user=request.user).update(
        com_info=com_json_info,
    )
    
    user = request.user
    myGameAccount = GameAccount.objects.get(user=user)
    expected = getMyNextLocation(myGameAccount)

    event['effect'] = f"You lost direction and ended up in {new_location} instead of {expected}"

    return event

# 17//8
def shipMalfunction4(request,week):
    event = {
        "week" : week,
        "type": "Ship Malfunction",
        "subtype": "Life Support",
        "effect":"Crew's health is declining and stress has increased. +2"
    }
    # CHANCE
    ri = random.randint(1,5)
    if ri != 1:
        # print(ri,event)
        return None
    ga = GameAccount.objects.get(user=request.user)
    if int(ga.ship_info['ship']['ship_condition']) > 35:
        return None
    # CHANCE

    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    crews = ship_info['crews']

    for crew in crews:
        crew['stress'] += 2
        if crew['stress'] >10:
            crew['stress'] = 10

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )

    return event

# 18//9
def shipMalfunction5(request,week):
    event = {
        "week" : week,
        "type": "Ship Malfunction",
        "subtype": "Private Quarters",
        "effect":"A bad leak has prevented use of the private quarters. Crew stress has increased. +2"
    }
    # CHANCE
    ri = random.randint(1,5)
    if ri != 1:
        # print(ri,event)
        return None
    ga = GameAccount.objects.get(user=request.user)
    if int(ga.ship_info['ship']['ship_condition']) > 35:
        return None
    # CHANCE

    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    crews = ship_info['crews']

    for crew in crews:
        crew['stress'] += 2
        if crew['stress'] >10:
            crew['stress'] = 10

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )

    return event

# 19//10
def shipMalfunction6(request,week):
    event = {
        "week" : week,
        "type": "Ship Malfunction",
        "subtype": "Cargo",
        "effect":"A cargo hold malfunction has caused radiation sickness on the ship. Crew health is declining and stress has increased. +2"
    }
    # CHANCE
    ri = random.randint(1,10)
    if ri != 1:
        # print(ri,event)
        return None
    ga = GameAccount.objects.get(user=request.user)
    if int(ga.ship_info['ship']['ship_condition']) > 35:
        return None
    # CHANCE

    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    crews = ship_info['crews']

    for crew in crews:
        crew['stress'] += 2
        if crew['stress'] >10:
            crew['stress'] = 10

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )

    return event

# 20//11
def shipMalfunction7(request,week):
    event = {
        "week" : week,
        "type": "Ship Malfunction",
        "subtype": "Cargo",
        "effect":"A cargo hold malfunction has caused Food Supplies to spoil."
    }
    # CHANCE
    ri = random.randint(1,1000000)
    if ri != 1:
        # print(ri,event)
        return None
    ga = GameAccount.objects.get(user=request.user)
    if int(ga.ship_info['ship']['ship_condition']) > 35:
        return None
    # CHANCE
    
    return event

# 21//12
def shipMalfunction8(request,week):
    event = {
        "week" : week,
        "type": "Ship Malfunction",
        "subtype": "Cargo",
        "effect":"A fire in the cargo hold has destroyed First Aid Supplies."
    }
    # CHANCE
    ri = random.randint(1,15)
    if ri != 1:
        # print(ri,event)
        return None
    ga = GameAccount.objects.get(user=request.user)
    if int(ga.ship_info['ship']['ship_condition']) > 35:
        return None
    # CHANCE
    
    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    coms = ship_info['coms']
    for k in coms:
        coms[k] = 0

    cargo = ship_info['cargo']
    cargo['filled'] = 0

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )
    return event


# Intercepted Message

# 25//13
def interceptedMessage1(request,week):
    event = {
        "week" : week,
        "type": "Intercepted Message",
        "subtype": "It's hard to understand...",
        # "effect":"There's about to be a surplus of commodity {} in location {}.".format(
            
        # )
    }
    # CHANCE
    ri = random.randint(1,4)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    c = random.sample([x.name for x in Commodities.objects.all()] ,1)[0],
    l = random.sample([x.name for x in Location.objects.all()] ,1)[0]

    event['effect'] = f"There's about to be a surplus of commodity {c[0]} in location {l}."

    return event

# 26//14
def interceptedMessage2(request,week):
    event = {
        "week" : week,
        "type": "Intercepted Message",
        "subtype": "It's hard to understand...",

    }
    # CHANCE
    ri = random.randint(1,4)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    c = random.sample([x.name for x in Commodities.objects.all()] ,1)[0],
    l = random.sample([x.name for x in Location.objects.all()] ,1)[0]

    event['effect'] = f"There's about to be a shortage of commodity {c[0]} in location {l}."

    return event

# 27//15
def interceptedMessage3(request,week):
    event = {
        "week" : week,
        "type": "Intercepted Message",
        "subtype": "It's hard to understand...",

    }
    # CHANCE
    ri = random.randint(1,4)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    l = random.sample([x.name for x in Location.objects.all()] ,1)[0]

    event['effect'] = f"There's pirates all around location {l}."

    return event

# 28//16
def interceptedMessage4(request,week):
    event = {
        "week" : week,
        "type": "Intercepted Message",
        "subtype": "It's hard to understand...",

    }
    # CHANCE
    ri = random.randint(1,3)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    c = random.sample([x.name for x in Commodities.objects.all()] ,1)[0],
    # l = random.sample([x.name for x in Location.objects.all()] ,1)[0]

    event['effect'] = f"Mayday, this will probably be our last transmission.We left location to deliver a load of commodity {c[0]} and suffered a critical collision."
    return event

# 29//17
def interceptedMessage5(request,week):
    event = {
        "week" : week,
        "type": "Intercepted Message",
        "subtype": "It's hard to understand...",
        "effect" :"Fortune favors the bold."

    }
    # CHANCE
    ri = random.randint(1,3)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    return event

# 30//18
def interceptedMessage6(request,week):
    event = {
        "week" : week,
        "type": "Intercepted Message",
        "subtype": "It's hard to understand...",
        "effect" : f"Looking for {random.randint(10,50)} of commodity in location {random.sample([x.name for x in Location.objects.all()] ,1)[0]} as soon as possible."
    }
    # CHANCE
    ri = random.randint(1,10)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    return event

# OTHER

# 31//19
def newsBroadcast1(request,week):
    event = {
        "week" : week,
        "type": "News Broadcast",
        "subtype": "Breaking news!",
        "effect" : f"Civil war has broken out on Location {random.sample([x.name for x in Location.objects.all()] ,1)[0]}."
    }
    # CHANCE
    ri = random.randint(1,10)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    return event

# 32//20
def catastrophe1(request,week):
    event = {
        "week" : week,
        "type": "Catastrophe!",
        "subtype": "ALERT! ALERT!",
        "effect" : "Ship collided with a meteor. You were found by a nearby ship and taken to the nearest planet but you sustained total losses. You've been taken back to random location with just your remaining credits. Game Over"
    }
    # CHANCE
    ri = random.randint(1,300)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    GameAccount.objects.filter(user=request.user).delete()
    dotENV.objects.filter(user=request.user).delete()

    return event

# 33//21
def catastrophe2(request,week):
    event = {
        "week" : week,
        "type": "Catastrophe!",
        "subtype": "ALERT! ALERT!",
        "effect" : "Something went wrong with the fuel cells. You're stranded."
    }
    # CHANCE
    ri = random.randint(1,300)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    GameAccount.objects.filter(user=request.user).delete()
    dotENV.objects.filter(user=request.user).delete()

    return event

# 34//22
def lawEnforcement1(request,week):
    event = {
        "week" : week,
        "type": "Law Enforcement!",
        "subtype": "All crew members, hands on the wall!",
        "effect" : "Police search the ship and find a crew member, a wanted fugitive. They haul him away and fine you 1,000,000$ for false manifest violations."
    }
    # CHANCE
    ri = random.randint(1,50)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    user = request.user
    credits = GameAccount.objects.get(user=user).credits
    GameAccount.objects.filter(user=user).update(
        credits=credits-1000000
    )

    return event

# 35//23
def lawEnforcement2(request,week):
    event = {
        "week" : week,
        "type": "Law Enforcement!",
        "subtype": "All crew members, hands on the wall!",
        # "effect" : "Police search the ship and inform you your cargo [commodity name] has been traced to a theft and they seize it."
    }
    # CHANCE
    ri = random.randint(1,50)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE
    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info

    clist = [x for x in ship_info['coms']]
    picked = random.sample(clist, 1)[0]
    ship_info['coms'][picked] = 0

    GameAccount.objects.filter(user=user).update(
        ship_info=ship_info
    )
    event['effect'] = f"Police search the ship and inform you your cargo {picked} has been traced to a theft and they seize it."
    return event

# 36//24
def aliens1(request,week):
    event = {
        "week" : week,
        "type": "Aliens!",
        "subtype": "Surrender",
        "effect" : "Aliens board your ship. They communicate in their own alien and do what you are sure is a laugh and vaporizes Crew Members. Then they leave. Crew stress increases greatly."
    }

    # CHANCE
    ri = random.randint(1,500)
    if ri > 3:
        # print(ri,event)
        return None
    # CHANCE

    GameAccount.objects.filter(user=request.user).delete()
    dotENV.objects.filter(user=request.user).delete()

    return event

# 37//25
def aliens2(request,week):
    event = {
        "week" : week,
        "type": "Aliens!",
        "subtype": "Surrender",
        "effect" : "Aliens board your ship. You attempt to fight but your efforts are futile. You watch in horror as they vaporize your entire crew."
    }
    # CHANCE
    ri = random.randint(1,500)
    if ri > 3:
        # print(ri,event)
        return None
    # CHANCE

    GameAccount.objects.filter(user=request.user).delete()
    dotENV.objects.filter(user=request.user).delete()

    return event

# 38//26
def aliens3(request,week):
    event = {
        "week" : week,
        "type": "Aliens!",
        "subtype": "Fight back",
        "effect" : "Aliens board your ship. They seem uninterested in the crew, but take all commodities and leave. You're thankful nobody was hurt...but your finances took a hit. Crew stress increases."
    }
    # CHANCE
    ri = random.randint(1,120)
    if ri > 3:
        # print(ri,event)
        return None
    # CHANCE
    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    coms = ship_info['coms']
    for k in coms:
        coms[k] = 0

    cargo = ship_info['cargo']
    cargo['filled'] = 0

    crews = ship_info['crews']

    for crew in crews:
        crew['stress'] += 2
        if crew['stress'] >10:
            crew['stress'] = 10

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )

    return event


# 39//27
def aliens4(request,week):
    event = {
        "week" : week,
        "type": "Aliens!",
        "subtype": "Surrender",
        "effect" : "Aliens board your ship. They do something that seems like a hysterical laugh at your attempt to fight back and then leave without further chaos. Crew stress increases."
    }
    # CHANCE
    ri = random.randint(1,300)
    if ri > 3:
        # print(ri,event)
        return None
    # CHANCE

    GameAccount.objects.filter(user=request.user).delete()
    dotENV.objects.filter(user=request.user).delete()

    return event

# 41//28
def aliens5(request,week):
    event = {
        "week" : week,
        "type": "Aliens!",
        "subtype": "Surrender",
        "effect" : "Aliens board your ship. One steps forward and speaks in a familiar language, explaining you either take aboard one of their own as a crew member or die. The crew agrees."
    }
    # CHANCE
    ri = random.randint(1,300)
    if ri > 3:
        # print(ri,event)
        return None
    # CHANCE

    GameAccount.objects.filter(user=request.user).delete()
    dotENV.objects.filter(user=request.user).delete()

    return event

# 43//29
def aliens6(request,week):
    event = {
        "week" : week,
        "type": "Aliens!",
        "subtype": "Surrender",
        "effect" : "Aliens board your ship and offer to trade . You decide against it. The aliens seem to get angry and take all of your cargo before leaving. Crew stress increases greatly."
    }

    # CHANCE
    ri = random.randint(1,150)
    if ri > 3:
        # print(ri,event)
        return None
    # CHANCE

    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    coms = ship_info['coms']
    for k in coms:
        coms[k] = 0

    cargo = ship_info['cargo']
    cargo['filled'] = 0

    crews = ship_info['crews']

    for crew in crews:
        crew['stress'] += 2
        if crew['stress'] >10:
            crew['stress'] = 10

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )

    return event

# 45//30
def meninBlack(request,week):
    event = {
        "week" : week,
        "type": "Men in Black",
        "subtype": "They do exist!",
        "effect" : "The Men in Black board your ship and tell you not to risk getting involved in alien business. They say it's the only warning you'll get."
    }
    # CHANCE
    ri = random.randint(1,200)
    if ri > 3:
        # print(ri,event)
        return None
    # CHANCE
    return event

# 46//31
def whatHappened2(request,week):
    event = {
        "week" : week,
        "type": "Men in Black",
        "subtype": "They do exist!",
        "effect" : f"You wake up in {random.sample([x.name for x in Location.objects.all()] ,1)[0]}...you can't remember the last month but you have no crew and no cargo. That's not right?"
    }
    
    # CHANCE
    ri = random.randint(1,200)
    if ri > 3:
        # print(ri,event)
        return None
    # CHANCE

    GameAccount.objects.filter(user=request.user).delete()
    dotENV.objects.filter(user=request.user).delete()

    return event

# 6//32
def Comeacrossstrandedship1(request,week):
    event = {
        "week" : week,
        "type": "Come across stranded ship",
        "subtype": "Investigate",
    }

    # CHANCE
    ri = random.randint(1,10)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    c = random.sample([x.name for x in Commodities.objects.all()] ,1)[0]
    ri = random.randint(1,10)
    event["effect"] = f"You find {c} commodity {ri}"
    
    ga = GameAccount.objects.get(user=request.user)
    ship_info = ga.ship_info
    # Overload Check
    if ship_info['cargo']['total'] <= ship_info['cargo']['filled']+ri:
        return None
    # 
    ship_info['coms'][c] = ship_info['coms'][c] + ri

    GameAccount.objects.filter(user=request.user).update(
        ship_info=ship_info
    )

    return event
# 8//33
def Comeacrossstrandedship2(request,week):
    event = {
        "week" : week,
        "type": "Come across stranded ship",
        "subtype": "Investigate",
    }

    # CHANCE
    ri = random.randint(1,3)
    if ri != 1:
        # print(ri,event)
        return None
    # CHANCE

    user = request.user
    mga = GameAccount.objects.get(user=user)
    ship_info = mga.ship_info
    
    crews = ship_info['crews']

    for crew in crews:
        crew['stress'] += 2
        if crew['stress'] >10:
            crew['stress'] = 10
    
    

    crews.pop()

    event['effect'] = f"One of your crew is killed. Rest of crew is stressed. +2"

    GameAccount.objects.filter(user=user).update(
        ship_info = ship_info,
    )

    return event

# EXTRA
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                print(comlist['name'],comlist['available'],comlist['sp'])
                if comlist['available']=="Yes":
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
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
                    comlist['stock']=random.randrange(1500,5000,10)
                elif comlist['available']=="No":
                    comlist['stock']=0
                
                s,e = priceRange(com.min_price,com.max_price,comlist['sp'])
                comlist['market_price'] = random.randrange(s,e)
                commodities.append(comlist)
        return commodities
