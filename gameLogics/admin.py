from django.contrib import admin
from .models import Ships,Crews,GameAccount,Location,Commodities,dotENV,Route,Distance
from django.http import JsonResponse
from pathlib import Path
import csv
# Register your models here.
admin.site.register(Ships)
admin.site.register(Crews)
admin.site.register(GameAccount)
admin.site.register(Location)
admin.site.register(Commodities)
admin.site.register(dotENV)
admin.site.register(Route)
admin.site.register(Distance)



def super_init_sec():
    def modValue(strAmount):
        ammount = strAmount.replace("$","").replace(".00","").replace(",","")
        return int(ammount)
    routeList = [
        ["Earth","Earth Moon","Mars","Phobos","Deimos","Europa","Titan","Ganymede","Enceladus","Io","Callisto","Triton"],
        ["Earth","Enceladus","Io","Callisto","Triton"],
        ["Earth","Earth Moon","Mars"],
        ["Earth","Phobos","Deimos","Europa","Titan"],
        ["Earth","Ganymede","Triton"],
        ["Earth","Enceladus","Io","Callisto","Triton"],
    ]
    for i in range(1,7):
        created = Route.objects.get_or_create(
            rid=i,
            route_details=routeList[i-1]
        )

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

    # distance
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = str(BASE_DIR) + "/gameLogics/csv/Distance.csv"
    with open(path) as f:
        reader = csv.reader(f)
        for row in reader:
            
            created = Distance.objects.get_or_create(
                location1=row[0],
                location2=row[1],
                distance=row[2]
            )

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
        "return" : str(BASE_DIR) + "__INIT__"
    })
