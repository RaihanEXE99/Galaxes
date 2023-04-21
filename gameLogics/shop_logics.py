def priceRange(low,high,type):
    if type[0].lower()=="c":
        diff = high - low
        base = int(diff/3)
        s,e = low,low+base+2
        return s,e
    elif type[0].lower()=="m":
        diff = high - low
        base = int(diff/3)
        s,e = low+base,low+base*2+2
        return s,e
    elif type[0].lower()=="e":
        diff = high - low
        base = int(diff/3)
        s,e = low+base*2,low+base*3+2
        return s,e