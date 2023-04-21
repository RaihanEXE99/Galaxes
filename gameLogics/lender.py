from django.shortcuts import redirect, render
from .models import *
from .views import *
import random

def denvFirstSetLoanOffer(request):
    denv = dotENV.objects.get(user=request.user)
    com_info = denv.com_info

    com_info['loanOffer'] = {
        "amount" : random.randint(2,10)*100000,
    }

    dotENV.objects.filter(user=request.user).update(
        com_info=com_info
    )

def setLoanOffer(request):
    denv = dotENV.objects.get(user=request.user)
    com_info = denv.com_info

    com_info['loanOffer'] = {
        "amount" : random.randint(2,10)*100000,
    }

    # dotENV.objects.filter(user=request.user).update(
    #     com_info=com_info
    # )
    return com_info['loanOffer']

def loanMenu(request):
    response = checkGameAccountState(request)
    if response['res'] == "error":
        return errorSample(response['reason'])
    if response['res'] == "success":
        return redirect(response['redirect'])

    ga = response['myGameAccount']
    if ga.location.weekly_interest == 0:
        return errorSample("Loan is not available in this location")

    ship_info = ga.ship_info
    denv = dotENV.objects.get(user=request.user)

    loanOffer = denv.com_info['loanOffer']['amount']

    isNloan = denv.com_info.get("nLoan")
    repayment = int(loanOffer+loanOffer*(int(ga.location.weekly_interest)/100))
    
    isSloan = denv.com_info.get("shipLoan")

    return render(request,"gameLogics/lender/lender.html",{
        "cred":f'{ga.credits:,}',
        "myGameAccount" : ga,
        "ship_info":ship_info,
        "loanOffer":loanOffer,
        "interest":int(ga.location.weekly_interest),
        "isNloan":isNloan,
        "repayment":repayment,
        "isSloan":isSloan
    })

def takingLoan(request):
    ga = GameAccount.objects.get(user=request.user)
    denv = dotENV.objects.get(user=request.user)

    isNloan = denv.com_info.get("nLoan")

    if isNloan:
        return errorSample("Invalid Url! 404'loan ")

    loanOffer = denv.com_info['loanOffer']['amount']
    loanObj = {
        "amount":loanOffer,
        "interest":int(ga.location.weekly_interest),
        "next":ga.ship_info['week_s']+4,
        "per":4,
        "repayment":int(loanOffer+loanOffer*(int(ga.location.weekly_interest)/100))
    }

    com_info = denv.com_info

    com_info['nLoan'] = loanObj

    dotENV.objects.filter(user=request.user).update(
        com_info=com_info
    )

    GameAccount.objects.filter(user=request.user).update(
        credits=ga.credits+loanOffer
    )

    return redirect("/")

def repaymentNloan(request):
    ga = GameAccount.objects.get(user=request.user)
    denv = dotENV.objects.get(user=request.user)

    isNloan = denv.com_info.get("nLoan")
    if not isNloan:
        return errorSample("Invalid Url! 404'loanRepayment")

    if isNloan['repayment'] > ga.credits:
        return errorSample("Can't Repayment Loan because of Insufficient Balance")
    
    GameAccount.objects.filter(user=request.user).update(
        credits=ga.credits-isNloan['repayment']
    )

    com_info = denv.com_info
    com_info.pop("nLoan",None)
    dotENV.objects.filter(user=request.user).update(
        com_info=com_info
    )
    return redirect("/")

def cutInterest(request):
    ga = GameAccount.objects.get(user=request.user)
    denv = dotENV.objects.get(user=request.user)
    isNloan = denv.com_info.get("nLoan")

    if not isNloan:
        return
    
    today = ga.ship_info['week_s']
    sums = 0
    while(today>isNloan['next']):
        print(today,isNloan['next'])
        sums += isNloan['amount']*(isNloan['interest']/100)
        print(sums)
        isNloan['next'] = isNloan['next']+isNloan["per"]

    GameAccount.objects.filter(user=request.user).update(
            credits=ga.credits-sums
        )
    com_info = denv.com_info
    com_info['nLoan']['next'] = isNloan['next']

    return com_info['nLoan']

def isNloan(request):
    ga = GameAccount.objects.get(user=request.user)
    denv = dotENV.objects.get(user=request.user)
    isNloan = denv.com_info.get("nLoan")
    if isNloan:
        return True
    if not isNloan:
        return False

def isSloan(request):
    ga = GameAccount.objects.get(user=request.user)
    denv = dotENV.objects.get(user=request.user)
    isSloan = denv.com_info.get("shipLoan")
    if isSloan:
        return True
    if not isSloan:
        return False

def initShipLoan(request):
    ga = GameAccount.objects.get(user=request.user)
    ship_price = ga.ship_info['ship']['value']
    denv = dotENV.objects.get(user=request.user)
    com_info = denv.com_info
    com_info["shipLoan"]={
      "amount":ship_price,
      "interest":15,
      "next":ga.ship_info['week_s']+4,
      "per":4,
      "repayment":int(ship_price+(ship_price*.1))
   }
    com_info = denv.com_info
    dotENV.objects.filter(user=request.user).update(
        com_info=com_info
    )

def cutShipInterest(request):
    ga = GameAccount.objects.get(user=request.user)
    denv = dotENV.objects.get(user=request.user)
    isSloan = denv.com_info.get("shipLoan")

    if not isSloan:
        return
    
    today = ga.ship_info['week_s']
    sums = 0
    while(today>isSloan['next']):
        print(today,isSloan['next'])
        sums += isSloan['amount']*(isSloan['interest']/100)
        print(sums)
        isSloan['next'] = isSloan['next']+isSloan["per"]

    GameAccount.objects.filter(user=request.user).update(
            credits=ga.credits-sums
        )
    com_info = denv.com_info
    com_info['shipLoan']['next'] = isSloan['next']

    return com_info['shipLoan']

def shipRepaymentSloan(request):
    ga = GameAccount.objects.get(user=request.user)
    denv = dotENV.objects.get(user=request.user)

    isSloan = denv.com_info.get("shipLoan")
    if not isSloan:
        return errorSample("Invalid Url! 404'ShiploanRepayment")

    if isSloan['repayment'] > ga.credits:
        return errorSample("Can't Repayment Loan because of Insufficient Balance")
    
    GameAccount.objects.filter(user=request.user).update(
        credits=ga.credits-isSloan['repayment']
    )

    com_info = denv.com_info
    com_info.pop("shipLoan",None)
    dotENV.objects.filter(user=request.user).update(
        com_info=com_info
    )
    return redirect("/")