from django.db import models
from account.models import Account
# Create your models here.

class Distance(models.Model):
    location1 = models.CharField(max_length=20)
    location2 = models.CharField(max_length=20)
    distance = models.IntegerField()

    def __str__(self):
        return ( str(self.id)+str(self.location1)+"-"+str(self.location2))

    objects = models.Manager()
    class meta:
        managed = True
        db_table = 'Distance'

class Route(models.Model):
    rid = models.IntegerField()
    route_details = models.JSONField(null=True)

    def __str__(self):
        return ( str(self.id))

    objects = models.Manager()
    class meta:
        managed = True
        db_table = 'Route'

class Ships(models.Model):
    mid = models.IntegerField()
    name = models.CharField(max_length=40)
    size = models.CharField(max_length=40)
    type = models.CharField(max_length=40)
    value = models.IntegerField()
    crew = models.IntegerField()
    cargo = models.IntegerField()
    fuel = models.IntegerField()
    passengers = models.IntegerField()
    upgrade_slot = models.IntegerField()
    rid = models.ForeignKey(Route,on_delete=models.CASCADE)
    upgrade1 = models.CharField(max_length=40,default="")
    upgrade2 = models.CharField(max_length=40,default="")
    upgrade3 = models.CharField(max_length=40,default="")
    upgrade4 = models.CharField(max_length=40,default="")
    upgrade5 = models.CharField(max_length=40,default="")

    def __str__(self):
        return (self.name + str(self.id))

    objects = models.Manager()
    class meta:
        managed = True
        db_table = 'Ships'

class Crews(models.Model):
    name = models.CharField(max_length=40)
    profession = models.CharField(max_length=40)
    weeklySalary = models.IntegerField()
    fromW = models.CharField(max_length=40)

    health = models.IntegerField()
    stress = models.FloatField()
    resolve = models.IntegerField()
    hunger = models.IntegerField()

    condition1 = models.CharField(max_length=40)
    condition2 = models.CharField(max_length=40)
    condition3 = models.CharField(max_length=40)

    def __str__(self):
        return (self.name + str(self.id))

    objects = models.Manager()
    class meta:
        managed = True
        db_table = 'Crews'

class Location(models.Model):
    name = models.CharField(max_length=40)
    gains_tax_rate = models.IntegerField()
    docking_fee = models.IntegerField()
    weekly_interest = models.IntegerField()
    marketplace = models.CharField(max_length=40)
    repair_bay = models.CharField(max_length=40)
    med_bay = models.CharField(max_length=40)
    pasengers_crew = models.CharField(max_length=40)
    missions_reqs = models.CharField(max_length=40)
    lender = models.CharField(max_length=40)
    storage = models.CharField(max_length=40)
    ship_dealer =  models.CharField(max_length=40)
    leisure =  models.CharField(max_length=40)

    def __str__(self):
        return ( str(self.id) + " " + self.name )

    objects = models.Manager()
    class meta:
        managed = True
        db_table = 'Location'

class Commodities(models.Model):
    name = models.CharField(max_length=40)
    min_price = models.IntegerField()
    max_price = models.IntegerField()

    fragile = models.BooleanField()
    perishable = models.BooleanField()
    edible = models.BooleanField()

    earth = models.CharField(max_length=100)
    moon = models.CharField(max_length=100)
    mars = models.CharField(max_length=100)
    phobos = models.CharField(max_length=100)
    deimos = models.CharField(max_length=100)
    europa = models.CharField(max_length=100)
    titan = models.CharField(max_length=100)
    ganymede = models.CharField(max_length=100)
    enceladus = models.CharField(max_length=100)
    io = models.CharField(max_length=100)
    callisto = models.CharField(max_length=100)
    triton = models.CharField(max_length=100)

    def __str__(self):
        return ( str(self.id) + " " + self.name )

    objects = models.Manager()
    class meta:
        managed = True
        db_table = 'Commodities'


class GameAccount(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)
    # ship = models.ForeignKey(Ships, on_delete=models.CASCADE,related_name="ship",blank=True,null=True)
    # crewMembers = models.ManyToManyField(Crews, related_name="crewMembers",blank=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name="location",blank=True,null=True)
    ship_info = models.JSONField(null=True)
    game_init = models.BooleanField(default=False)
    def __str__(self):
        return ("|No:"+str(self.id)+"    |username: "+  str(self.user.username) +" "+str(self.location))
    def cargo_per(self):
        val = (self.ship_info['cargo']['filled'] / self.ship_info['cargo']['total'])*100
        return "%.2f"%val

    objects = models.Manager()
    class meta:
        managed = True
        db_table = 'GameAccount'

class dotENV(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    ga = models.OneToOneField(GameAccount, on_delete=models.CASCADE)
    com_info = models.JSONField(null=True)
    location_info = models.JSONField(null=True)

    def __str__(self):
        return ( str(self.id) + str(self.user))

    objects = models.Manager()
    class meta:
        managed = True
        db_table = 'dotENV'
