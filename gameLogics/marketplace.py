from .models import Ships,Crews,GameAccount,Location,Commodities,dotENV
from . import TAXRANGE 
from .views import *
def validateBuy(product,quantity,user):
    dotenv = dotENV.objects.get(user=user)
    gameAccount = GameAccount.objects.get(user=user)
    coms_info = dotenv.com_info['json_info']
    for com in coms_info:
        if com['name'] == product and com['available'] == "Yes" and int(quantity)<=int(com['stock']):
            cargo = gameAccount.ship_info['cargo']
            if (int(cargo['filled']) + int(quantity))>int(cargo['total']):
                return {
                    "res" : "Error",
                    "reason" : "No Space Left"
                }
            cost = calculate(com['market_price'],quantity)
            print(gameAccount.credits,cost)
            if int(gameAccount.credits)<cost:
                return {
                    "res" : "Error",
                    "reason" : "Insufficient Balance"
                }

            ship_info = gameAccount.ship_info
            ship_info['cargo']['filled']+=int(quantity)
            ship_info['coms'][product] += int(quantity)

            # tax = cost * (gameAccount.location.gains_tax_rate/100)

            # if tax > TAXRANGE:   return {"res" : "Error","reason" : "Too Much Tax! Pay Your Tax first"}
            # ship_info['tax']['pay'] += int(tax)

            GameAccount.objects.filter(user=user).update(
               ship_info=ship_info,
               credits=int(gameAccount.credits)-cost
            )
            json_list = dotenv.com_info
            for json_com in json_list['json_info']:
                if json_com['name'] == product:
                    json_com['stock'] -= int(quantity)
                    break
            dotENV.objects.filter(user=user).update(
                com_info=json_list
            )
            
            return {
                "res":"Success",
            }
    return {
        "res" : "Error",
        "reason" : "Purchase Failed!"
    }
def validateSell(product,quantity,user):
    dotenv = dotENV.objects.get(user=user)
    gameAccount = GameAccount.objects.get(user=user)
    coms_info = dotenv.com_info['json_info']
    ship_info = gameAccount.ship_info
    coms = ship_info['coms']
    if int(quantity)>int(coms[product]):
        return {
            "res" : "Error",
            "reason" : "You dont have that much items"
        }
    com_info = None
    for com in coms_info:
        if com['name'] == product:
            com_info=com
            break
    cost = calculate(com['market_price'],quantity)

    ship_info['cargo']['filled']-=int(quantity)
    ship_info['coms'][product] -= int(quantity)

    tax = cost * (((gameAccount.location.gains_tax_rate+1)/2)/100)

    # if tax > TAXRANGE:   return {"res" : "Error","reason" : "Too Much Tax! Pay Your Tax first"}
    ship_info['tax']['pay'] += int(tax)

    GameAccount.objects.filter(user=user).update(
            ship_info=ship_info,
            credits=int(gameAccount.credits)+cost
        )

    json_list = dotenv.com_info
    for json_com in json_list['json_info']:
        if json_com['name'] == product:
            json_com['stock'] += int(quantity)
            break
    dotENV.objects.filter(user=user).update(
        com_info=json_list
    )
    return {
        "res":"Success",
    }
    # for com in coms_info:
    #     if com['name'] == product and int(quantity)<=int(com['stock']):
    #         cargo = gameAccount.ship_info['cargo']
    #         if (int(cargo['filled']) + int(quantity))>int(cargo['total']):
    #             return {
    #                 "res" : "Error",
    #                 "reason" : "No Space Left"
    #             }
    #         cost = calculate(com['market_price'],quantity)
    #         if int(gameAccount.credits)<cost:
    #             return {
    #                 "res" : "Error",
    #                 "reason" : "Insufficient Balance"
    #             }

    #         ship_info = gameAccount.ship_info
    #         ship_info['cargo']['filled']+=int(quantity)
    #         ship_info['coms'][product] += int(quantity)

    #         GameAccount.objects.filter(user=user).update(
    #            ship_info=ship_info,
    #            credits=int(gameAccount.credits)-cost
    #         )
    #         json_list = dotenv.com_info
    #         for json_com in json_list['json_info']:
    #             if json_com['name'] == product:
    #                 json_com['stock'] -= int(quantity)
    #                 break
    #         dotENV.objects.filter(user=user).update(
    #             com_info=json_list
    #         )
    #         return {
    #             "res":"Success",
    #         }
    return {
        "res" : "Error",
        "reason" : "Purchase Failed!"
    }
def calculate(price,quantity):
    return int(price)*int(quantity)

def updateMplace(request):
    user = request.user
    mg = GameAccount.objects.get(user=user)
    ship_info = mg.ship_info
    allComs = Commodities.objects.all()
    for comKey in allComs:
        if comKey.name in ship_info['coms']:
            pass
        else:
            ship_info['coms'][comKey.name] = 0
            GameAccount.objects.filter(user=user).update(
                ship_info=ship_info,
            )
    
    rem = []
    for coms in ship_info['coms']:
        bl = False
        for ckey in allComs:
            if ckey.name == coms:
                bl = True
            else:
                pass
        # ship_info["coms"].remove(ship_info["coms"][coms])
        if bl == False:
            rem.append(coms)
    for x in rem:
        ship_info["coms"].pop(x, None)
        print(ship_info)
        GameAccount.objects.filter(user=user).update(
                ship_info=ship_info,
            )
    
    if rem != []:
        commoditiesList=setCommoditiePrice(mg.location.name)
    
        com_json_info = {
            "json_info" : commoditiesList,
            "travel" : 1
        }
        # print(com_json_info)
        dotENV.objects.filter(user=request.user).update(
            com_info=com_json_info,
        )






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
