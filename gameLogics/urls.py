from django.conf.urls import url
from django.urls import path
from . import views
from . import srBay
from . import lender

app_name = 'gameLogics'

urlpatterns = [
    path('areYouReady/', views.areYouReady, name="areYouReady"),
    path('allRanks/', views.allRanks, name="allRanks"),
    
    path('select-ship/', views.selectShip, name="selectShip"),
    path('selectShipAsCaptain/', views.selectShipAsCaptain, name="selectShipAsCaptain"),
    
    path('createGameAccount/', views.createGameAccount, name="createGameAccount"),
    path('game-starting/', views.gameStarting, name="gameStarting"),

    # Main Game
    path('mainGameDashboard/', views.mainGameDashboard, name="mainGameDashboard"),
    path('clickNextLocation/', views.clickNextLocation, name="clickNextLocation"),
    path('locations/', views.locations, name="locations"),
    
    path('RandR/', views.RandR, name="RandR"),
    path('refillCharge/', views.refillCharge, name="refillCharge"),
    path('payTax/', views.payTax, name="payTax"),
    path('payWages/', views.payWages, name="payWages"),

    path('terminal/', views.terminal, name="terminal"),
    path('hiringCrew/', views.hiringCrew, name="hiringCrew"),

    path('leisure/', views.leisure, name="leisure"),
    path('payLeisure/', views.payLeisure, name="payLeisure"),

    path('shipBay/', srBay.shipBay, name="shipBay"),
    
    path('showBuyableShips/', srBay.showBuyableShips, name="showBuyableShips"),
    path('purchaeShip/', srBay.purchaeShip, name="purchaeShip"),

    path('repair/', srBay.repair, name="repair"),
    path('maxRepair/', srBay.maxRepair, name="maxRepair"),

    path('loanMenu/', lender.loanMenu, name="loanMenu"),
    path('takingLoan/', lender.takingLoan, name="takingLoan"),
    path('repaymentNloan/', lender.repaymentNloan, name="repaymentNloan"),
    path('shipRepaymentSloan/', lender.shipRepaymentSloan, name="shipRepaymentSloan"),

    path('criticalSituation/<str:info>/<str:step>', views.criticalSituation, name="criticalSituation"),
    path('deleteGameAccount/', views.deleteGameAccount, name="deleteGameAccount"),

    # Marketplace
    path('marketplace/', views.marketplace, name="marketplace"),
    path('buyItem/', views.buyItem, name="buyItem"),
    path('sellItem/', views.sellItem, name="sellItem"),
    
    # path('giveRandomCrewmate/', views.giveRandomCrewmate, name="giveRandomCrewmate"),
    # path('dashboardShipAndCrew/', views.dashboardShipAndCrew, name="dashboardShipAndCrew"),
    
    # csv to db
    path('init/super/<str:csv_to_db>', views.super_init, name="super_init"),
    path('init_ships/<str:csv_to_db>', views.init_ships, name="init_ships"),
    path('init_crews/<str:csv_to_db>', views.init_crews, name="init_crews"),
    path('init_locations/<str:csv_to_db>', views.init_locations, name="init_locations"),
    path('init_commodities/<str:csv_to_db>', views.init_commodities, name="init_commodities"),
    # supertest
    path('supertest/', views.supertest, name="supertest"),
]