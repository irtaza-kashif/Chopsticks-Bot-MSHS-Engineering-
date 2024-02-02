def possTreeP2(posP1, posP2):
    
    # List of all possible moves that player2 can make, even if some give the exact same position, end the game, or are impossible to make
    possibilities = [[posP1, [posP2[0] + 1, posP2[1] - 1]],
            [posP1, [posP2[0] + 2, posP2[1] - 2]],
            [posP1, [posP2[0] + 3, posP2[1] - 3]],
            [posP1, [posP2[0] - 1, posP2[1] + 1]],
            [posP1, [posP2[0] - 2, posP2[1] + 2]],
            [posP1, [posP2[0] - 3, posP2[1] + 3]]]

    if posP2[0] > 0:
        if posP1[0] > 0:
            possibilities += [[[posP1[0] + posP2[0], posP1[1]], posP2]]
        if posP1[1] > 0:
            possibilities += [[[posP1[0], posP1[1] + posP2[0]], posP2]]
    if posP2[1] > 0:
        if posP1[0] > 0:
            possibilities += [[[posP1[0] + posP2[1], posP1[1]], posP2]]
        if posP1[1] > 0:
            possibilities += [[[posP1[0], posP1[1] + posP2[1]], posP2]]

    return possibilities

def possTreeP1(posP1, posP2):
    
    # List of all possibly moves that player2 can make, even if some give the exact same position, end the game, or are impossible to make
    possibilities = [[[posP1[0] + 1, posP1[1] - 1], posP2],
            [[posP1[0] + 2, posP1[1] - 2], posP2],
            [[posP1[0] + 3, posP1[1] - 3], posP2],
            [[posP1[0] - 1, posP1[1] + 1], posP2],
            [[posP1[0] - 2, posP1[1] + 2], posP2],
            [[posP1[0] - 3, posP1[1] + 3], posP2]]

    if posP1[0] > 0:
        if posP2[0] > 0:
            possibilities += [[posP1, [posP2[0] + posP1[0], posP2[1]]]]
        if posP2[1] > 0:
            possibilities += [[posP1, [posP2[0], posP2[1] + posP1[0]]]]
    if posP1[1] > 0:
        if posP2[0] > 0:
            possibilities += [[posP1, [posP2[0] + posP1[1], posP2[1]]]]
        if posP2[1] > 0:
            possibilities += [[posP1, [posP2[0], posP2[1] + posP1[1]]]]

    return possibilities

def listClean(list):
    for possibility in list:
        for player in possibility:
            while player[0] < 0:
                player[0] += 1
                player[1] -= 1
            while player[1] < 0:
                player[1] += 1
                player[0] -= 1

            # Analyzing each players hand to see if one of the posibilities is greater than or equal to 5, if it is, set that hand to 0
            if player[0] >= 5:
                player[0] = 0
            if player[1] >= 5:
                player[1] = 0

    noDupList = removeDup(list)
    
    return noDupList

def checkDup(pos1, pos2):
    return(set(pos1[0]) == set(pos2[0]) and set(pos1[1]) == set(pos2[1]))

# appends each position that is not already on the list that it appends to
def removeDup(list):
    uniqueList = []
    
    for position in list:
        if not (checkDup(position, basePos)):
            if not any(checkDup(position, uniquePositions) for uniquePositions in uniqueList):
                uniqueList.append(position)
    
    return(uniqueList)

def p1Moves(posP1, posP2):
    global basePos
    basePos = [posP1, posP2] # Original / current position
    roughTree = possTreeP1(posP1, posP2)
    return(listClean(roughTree))

def p2Moves(posP1, posP2):
    global basePos
    basePos = [posP1, posP2] # Original / current position
    roughTree = possTreeP2(posP1, posP2)
    return(listClean(roughTree))
