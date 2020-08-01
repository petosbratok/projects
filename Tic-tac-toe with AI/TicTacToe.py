import random
from collections import Counter

combs = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
         (0, 3, 6), (1, 4, 7), (2, 5, 8),
         (0, 4, 8), (2, 4, 6))
stats = 0
def main():
    #table_input = list(input('Enter cells: >'))
    table = [' ', ' ', ' ',
             ' ', ' ', ' ',
             ' ', ' ', ' ']

    user1, user2 = getParams()
    printTable(table)
    if abs(stats) > 10:
        print(stats)
        exit()
    while True:
        turn = getTurn(table)
        if turn == "X":
            input = user1(table)
        else:
            input = user2(table)
        table[input] = turn
        printTable(table)
        gameIsEnded(table)

def getTurn(table):
    c = Counter(table)
    return 'X' if c['X'] == c['O'] else 'O'

def getParams():
    commands = {'user': lambda table: getInput(table),
                'easy': lambda table: computerInputEasy(table),
                'medium': lambda table: computerInputMedium(table),
                'hard': lambda table: computerInputHard(table, init='True')}
    while True:
        user_input = input('Input command: > ').split()
        if user_input == ['exit']:
            exit()
        elif user_input.pop(0) == 'start':
            if user_input[0] in commands.keys() and user_input[1] in commands.keys():
                    return commands[user_input[0]], commands[user_input[1]]
        else:
            print('Bad parameters')

def computerInputMedium(table):
    print('Making move level "medium"')
    if oneMoveWin(table) != 'No':
        return oneMoveWin(table)
    else:
        while True:
            input = random.randint(0, 8)
            if input in availSlots(table):
                return input


def computerInputEasy(table):
    print('Making move level "easy"')
    while True:
        input = random.randint(0, 8)
        if input in availSlots(table):
            return input

def getTurn(table):
    c = Counter(table)
    return 'X' if c['X'] == c['O'] else 'O'

def availSlots(table):
    return [id for id in range(len(table)) if table[id] == ' ']

def oneMoveWin(table):
    global combs
    for comb in combs:
        if table[comb[0]] == table[comb[1]] != ' ' and table[comb[2]] == ' ':
            return comb[2]
        elif table[comb[0]] == table[comb[2]] != ' ' and table[comb[1]] == ' ':
            return comb[1]
        elif table[comb[1]] == table[comb[2]] != ' ' and table[comb[0]] == ' ':
            return comb[0]
    return False

def twoMoveWin(table, id, turn):
    count = 0
    exceptionTable = table[::]
    exceptionTable[id] = turn
    for comb in combs:
        if exceptionTable[comb[0]] == exceptionTable[comb[1]] != ' ' and exceptionTable[comb[2]] == ' ':
            count += 1
        elif exceptionTable[comb[0]] == exceptionTable[comb[2]] != ' ' and exceptionTable[comb[1]] == ' ':
            count += 1
        elif exceptionTable[comb[1]] == exceptionTable[comb[2]] != ' ' and exceptionTable[comb[0]] == ' ':
            count += 1
    return True if count >= 2 else False

def threeMoveWin(table, id):
    for slot in availSlots(table):
        exceptionTable = table[::]
        turn = getTurn(table)
        exceptionTable[id] = 'X'
        if twoMoveWin(exceptionTable, id, 'X') or twoMoveWin(exceptionTable, id, 'O') and oneMoveWin(exceptionTable) == False:
            return slot
        exceptionTable[id] = 'O'
        if twoMoveWin(exceptionTable, id, 'X') or twoMoveWin(exceptionTable, id, 'O') and oneMoveWin(exceptionTable) == False:
            return slot
    return False

def computerInputHard(table, myTurn=None, slot=None, result=None, init=False):
    turn = getTurn(table)
    global combs
    if init:
        myTurn = getTurn(table)
        print('Making move hard')
        result = {}
        for slot in availSlots(table):
            result[slot] = 0
        if oneMoveWin(table) != False:
            return oneMoveWin(table)
    for id in availSlots(table):
        if init:
            slot = id
            choice = random.randint(0, 1)
            if choice == 0:
                if threeMoveWin(table, id) != False:
                    return threeMoveWin(table, id)
            else:
                if twoMoveWin(table, id, 'X') or twoMoveWin(table, id, 'O'):
                    return id

        newTable = table[::]
        newTable[id] = turn
        gameScore = gameIsEndedAI(newTable, myTurn)
        if gameScore != None:
            result[slot] += gameScore
        else:
            computerInputHard(newTable, myTurn, slot, result)
    resultValue = sorted(result.values())[-1]
    for key, value in result.items():
        if value == resultValue:
            return key

def gameIsEndedAI(table, myTurn):
    global combs
    for comb in combs:
        if table[comb[0]] == table[comb[1]] == table[comb[2]] != ' ':
            if table[comb[0]] == myTurn:
                return 10
            else:
                return -10
    if not ' ' in table:
        return 0

def gameIsEnded(table):
    global stats
    global combs
    for comb in combs:
        if table[comb[0]] == table[comb[1]] == table[comb[2]] != ' ':
            print(f'{table[comb[0]]} wins')
            stats +=1 if table[comb[0]] == 'X' else -1
            print(f'stats is {stats}')
            main()
    if not ' ' in table:
        print('Draw')
        print(f'stats is {stats}')
        main()

def getInput(table):
    while True:
        user_input = input('Enter the coordinates: > ')
        if inputIsValid(user_input, table):
            return convertInput(user_input)

def convertInput(input):
    return (int(input.split()[0])-1)*3 + int(input.split()[1]) - 1

def inputIsValid(user_input, table):
    exception = 'no exception'
    if user_input == '':
        exception = 'you did not enter anything'
    try:
        user_input = convertInput(user_input)
        if not 0 <= user_input <= 8:
            exception = 'coordinates should be from 1 to 3!'
        if not table[user_input] == ' ':
            exception = 'this cell is occupied! Choose another one!'
    except:
        exception = 'you should enter numbers!'

    if exception == 'no exception':
        return True
    else:
        print(f'Error: {exception}')
        return False

def printTable(table):
    print('---------')
    for i in range(3):
        print(f'| {table[i*3]} {table[i*3 + 1]} {table[i*3 + 2]} |')
    print('---------')

if __name__ == '__main__':
    main()
