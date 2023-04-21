import random
from .models import *
def getRandomCrews(request):
    user = request.user
    ga = GameAccount.objects.get(user=user)
    ri = random.randint(1,15)
    allcrews = Crews.objects.all()
    randomCrews = random.sample([x for x in allcrews],ri)
    rc= []
    for c in randomCrews:
        alreadyIn = False
        for mc in ga.ship_info['crews']:
            if c.name == mc['name']:
                alreadyIn = True
        if alreadyIn:
            pass
        else:
            obj = {
                "id":c.id,
                "name":c.name,
                "profession":c.profession,
                "weeklySalary":c.weeklySalary,
                "sbonus":signOnLogic(c.id)
            }
            rc.append(obj)
    return rc

def signOnLogic(crew_id):
    that_crew = Crews.objects.get(id=int(crew_id))
    sbonus = None
    if that_crew.resolve < 3:
        sbonus = that_crew.weeklySalary*5
    elif that_crew.resolve < 6 and that_crew.resolve > 2:
        sbonus = that_crew.weeklySalary*5*3
    else :
        sbonus = that_crew.weeklySalary*5*5
    return sbonus

def hiring(request,crew_id):
    sbonus = signOnLogic(crew_id)
    ga = GameAccount.objects.get(user=request.user)
    that_crew = Crews.objects.get(id=int(crew_id))
    # ERRORS
    ship_crew_limit = ga.ship_info['ship']['crew']
    if ship_crew_limit < len(ga.ship_info['crews'])+1:
        return {
            "res":"Failed",
            "reason":"Already full lobby!"
        }
    credits = ga.credits
    if credits <= sbonus:
        return {
            "res":"Failed",
            "reason":"Insufficient funds!"
        }
    for mc in ga.ship_info['crews']:
        if that_crew.name == mc['name']:
            return {
                "res":"Failed",
                "reason":"This Crew Already Exist in your lobby!"
            }
    # ENDERROS
    ship_info = ga.ship_info
    ship_info['crews'].append(
        {
         "name":that_crew.name,
         "profession":that_crew.profession,
         "weeklySalary":that_crew.weeklySalary,
         "fromW":"Location 1",
         "health":that_crew.health,
         "stress":that_crew.stress,
         "resolve":that_crew.resolve,
         "hunger":that_crew.hunger,
         "condition1":"",
         "condition2":"",
         "condition3":""
      }
    )
    GameAccount.objects.filter(user=request.user).update(
        credits=credits-sbonus,
        ship_info=ship_info
    )
    return {
        "res":"Success"
    }
