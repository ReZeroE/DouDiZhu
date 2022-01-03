from itertools import groupby, count

cards_dict = {
    "pass": 0,
    "3":    1,
    "4":    2,
    "5":    3,
    "6":    4,
    "7":    5,
    "8":    6,
    "9":    7,
    "10":   8,
    "J":    9,
    "Q":    10,
    "K":    11,
    "A":    12,
    "2":    13,
    "BW-Joker": 14,
    "CL-Joker": 15
}

l = ['3', '4', '5', '6', '7', '8', '8', '9', '9', '10', 'J', 'Q', 'Q', 'Q', 'K', 'K', 'K', '2', 'BW-Joker']

def process_combination(sequence):
    result = []
    for s in sequence:
        if not result or cards_dict[s] != cards_dict[result[-1][-1]] + 1:
            result.append([])
        result[-1].append(s)
    return result


print(process_combination(l))
