invent = {
    "iron": 35,
    "coal": 50,
    "adamant": 80,
    "rune": 125
}


def xp_sum(item, amount):
    return invent.get(item) * int(amount)


valid = False
while valid == False:
    ore_type = input('Enter ore type: ').lower()
    amount = input('Enter amount mined: ')
    if ore_type in invent:
        valid = True
        result = xp_sum(ore_type, amount)
        print(result)
    else:
        print('ore type not in dict, try again!')
