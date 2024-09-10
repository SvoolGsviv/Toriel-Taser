import sys, os, copy

with open(os.path.join(sys.path[0], "listofrands1.txt"), "r") as f:
    rng = f.readlines()
    for i in range(len(rng)):
        rng[i] = round(100*float(rng[i]))

################
#0-20: 1sidegen type 7
#21-40: 1sidegen type 8
#41-60: 1sidegen type 10
#61-80: bottom hand
#81-100: top hand
################

FRAMES_USED = 0
CURRENT_OFFSET = 1
MANIP_SEQUENCE = 2
TURN_NUMBER = 3
HP = 4
ATTACKS = 5
OFFSET_LIST = 6
X_LIST = 7

#Various offsets
FIRST_TURN_NO_MANIP = 94

#First turn to second turn no manip
TYPE_7 = 289           #criss-cross
TYPE_8 = 373           #helix
TYPE_10 = 329          #8-hand attack
BOTTOM_HAND = 233
TOP_HAND = 233

FIRST_TO_SECOND = 0 #definitionally
SECOND_TO_THIRD = 78 #bottom 840 - 1151 = 311
THIRD_TO_FOURTH = 90 #top 1151 - 1474 = 323
FOURTH_TO_FIFTH = -20 #type7 1474 - 1743 = 269
FIFTH_TO_SIXTH = 90 #type7 1743 - 2122 = 379
SIXTH_TO_SEVENTH = 90 #type7 2122 - 2501 = 379
SEVENTH_TO_EIGHTH = 90 #type10 2501 - 2920 = 419
EIGHTH_TO_NINTH = 90 #type8 2920 - 3383 = 463
NINTH_TO_TENTH = 48 #top 3383 - 3664 = 281
TENTH_TO_ELEVENTH = 90 #type8 3664 - 4127 = 463
ELEVENTH_TO_TWELFTH = 48 #type7 4127 - 4464 = 337

ZZ = 0
DZZ = -1
XZZ = -2
SZZ = -3
ZSZ = 38
DDZZ = -4
DXZZ = -5
DSZZ = -6
DZSZ = -7
SXZZ = -8
SSZZ = -9
SZSZ = -10
XSZZ = -11
XZSZ = -12
ZSSZ = 76
ZXZZ = 82

turndifs = ["this is a 1 based array now fuck you", FIRST_TURN_NO_MANIP, FIRST_TO_SECOND, SECOND_TO_THIRD, THIRD_TO_FOURTH, FOURTH_TO_FIFTH, FIFTH_TO_SIXTH, SIXTH_TO_SEVENTH, SEVENTH_TO_EIGHTH, EIGHTH_TO_NINTH, NINTH_TO_TENTH, TENTH_TO_ELEVENTH, ELEVENTH_TO_TWELFTH, 0]
manips = [[DDZZ, 2], [DXZZ, 2], [DSZZ, 2], [DZSZ, 2], [SXZZ, 2], [SSZZ, 2], [SZSZ, 2], [XSZZ, 2], [XZSZ, 2], [ZSSZ, 2], [ZXZZ, 2], [DZZ, 1], [XZZ, 1], [SZZ, 1], [ZSZ, 1], [ZZ, 0]]
ds = [0, 12, 24, 32, 10, 32, 32, 32, 32, 18, 32, 18]
dds = [0, 24, 48, 66, 20, 66, 66, 66, 66, 36, 66, 36, 16]
xs = [88, 96, 104, 112]

def getValidAttacks(hp, turn):
    #####################################
    # hp   2     3     4     5     6     7     8     9     10    11    12    13    14    15    16    17    18    19    20
    #turn
    # 1                                                                                                                all
    # 2                                                                                        nth   all               all
    # 3                                                                      nth   all         nth   all               all
    # 4                                                    nth   all         nth   all         nth   all               ah
    # 5                                  ALL               nth   all         nth   all         bh    ah
    # 6                            ALL   ALL               nth   all         bh    ah
    # 7                      ALL   ALL   ALL               bh    ah
    # 8                ALL   ALL   ALL   AH
    # 9          NH    ALL   ALL   AH
    #10          NH    ALL   AH
    #11          NH    AH
    #12          FA
    #
    #
    #
    if(turn == 12):
        return([41,60])
    elif(hp == 3):
        return([0,60])
    elif(hp < 8):
        if((hp + turn) == 15):
            return([61,100])
        else:
            return([0,100])
    elif(hp == 10):
        if(turn < 7):
            return([0,80])
        else:
            return([61,80])
    elif(hp == 11):
        if(turn < 7):
            return([0,100])
        else:
            return([61,100])
    elif(hp == 13):
        if(turn < 6):
            return([0,80])
        else:
            return([61,80])
    elif(hp == 14):
        if(turn < 6):
            return([0,100])
        else:
            return([61,100])
    elif(hp == 16):
        if(turn < 5):
            return([0,80])
        else:
            return([61,80])
    elif(hp == 17):
        if(turn < 5):
            return([0,100])
        else:
            return([61,100])
    elif(hp == 20):
        if(turn < 4):
            return([0,100])
        else:
            return([61,100])

def realAdj(manip, prev, turn):
    d = ds[turn - 1]      #get values for D, DD, and X for this turn
    dd = dds[turn - 1]
    smod = 0
    if (turn == 1 or prev < 30):
        x = xs[0]
        smod = 4
    elif (prev >= 90):
        x = xs[3]
    elif (prev >= 70):
        x = xs[1]
    elif (prev >= 30):
        x = xs[2]

    #long switch statement lmao
    if(manip >= 0):
        return([manip, x])
    elif(manip == DZZ):
        return([d, x])
    elif(manip == XZZ):
        return([x, [x, prev, turn]])
    elif(manip == SZZ):
        return([6 + smod, x])
    elif(manip == DDZZ):
        return([dd, x])
    elif(manip == DXZZ):
        return([d + x, x])
    elif(manip == DSZZ):
        return([d + smod + 6, x])
    elif(manip == DZSZ):
        return([d + 38, x])
    elif(manip == SXZZ):
        return([x + smod + 4, x])
    elif(manip == SSZZ):
        return([2*smod + 14, x])
    elif(manip == SZSZ):
        return([smod + 44, x])
    elif(manip == XSZZ):
        return([int(1.5*x) + 2, x])
    elif(manip == XZSZ):
        return([x + 38, x])

def search():
    #frames used, current offset, manip sequence, turn number, hp, atks, offsets, xlist
    branch0 = [0, 0, [], 1, 20, [], [], []]
    stack = [branch0]
    target_frames = 99999
    while(True):
        #get leaf node from top of stack
        try:
            parent = stack.pop()
        except:
            break
        health = parent[HP]
        turn = parent[TURN_NUMBER]
        offset = parent[CURRENT_OFFSET] + turndifs[turn]
        try:
            prev = parent[ATTACKS][-1]
        except:
            prev = 0
        #check if manip is a completed fight
        if(health == 2):
            #if manip is a completed fight, check if it is better than the current best completed fight
            if(parent[FRAMES_USED] < target_frames):
                bestresult = parent
                target_frames = parent[0]
        #if manip is not a completed fight, manip the next turn
        else:
            #find all valid children for leaf and append to stack
            valids = getValidAttacks(health, turn)
            for manip in manips:
                adj = realAdj(manip[0], prev, turn)
                newoffset = offset + adj[0]
                atk = rng[newoffset]
                if(valids[0] <= atk and atk <= valids[1] and parent[FRAMES_USED] + manip[1] < target_frames):
                    child = copy.deepcopy(parent)
                    child[FRAMES_USED] += manip[1]
                    child[CURRENT_OFFSET] = newoffset
                    child[MANIP_SEQUENCE].append(manip[0])
                    child[TURN_NUMBER] += 1
                    if(atk <= 20):
                        child[CURRENT_OFFSET] += TYPE_7
                    elif(21 <= atk and atk <= 40):
                        child[CURRENT_OFFSET] += TYPE_8
                    elif(41 <= atk and atk <= 60):
                        child[CURRENT_OFFSET] += TYPE_10
                    if(61 <= atk and atk <= 80):
                        child[CURRENT_OFFSET] += BOTTOM_HAND
                        if(child[HP] < 8):
                            child[HP] -= 1
                        elif(child[HP] == 11):
                            child[HP] -= 4
                        else:
                            child[HP] -= 3
                    elif(81 <= atk):
                        child[CURRENT_OFFSET] += TOP_HAND
                        if(child[HP] < 8):
                            child[HP] -= 1
                        else:
                            child[HP] -= 4
                    elif(turn == 12):
                        child[HP] -= 1
                    child[ATTACKS].append(atk)
                    child[OFFSET_LIST].append(newoffset)
                    child[X_LIST].append(adj[1])
                    stack.append(copy.copy(child))
    return(bestresult)

def results(atks):
    str = ""
    bottoms = 0
    for i in range(12):
        atk = atks[i]
        if(atk <= 20):
            next = "cross   "
        elif(atk <= 40):
            next = "helix   "
        elif(atk <= 60):
            next = "8hand   "
        elif(atk <= 80):
            bottoms += 1
            if(bottoms > 3):
                next = "T/B     "
            else:
                next = "Bottom  "
        else:
            next = "Top     "
        str += next
    print(str)

def readable(seq):
    str = ""
    for manip in seq:
        if (manip == ZZ):
            next = "ZZ      "
        elif (manip == DZZ):
            next = "DZZ     "
        elif (manip == XZZ):
            next = "XZZ     "
        elif (manip == SZZ):
            next = "SZZ     "
        elif (manip == ZSZ):
            next = "ZSZ     "
        elif (manip == DDZZ):
            next = "DDZZ    "
        elif (manip == DXZZ):
            next = "DXZZ    "
        elif (manip == DSZZ):
            next = "DSZZ    "
        elif (manip == DZSZ):
            next = "DZSZ    "
        elif (manip == SXZZ):
            next = "SXZZ    "
        elif (manip == SSZZ):
            next = "SSZZ    "
        elif (manip == SZSZ):
            next = "SZSZ    "
        elif (manip == XSZZ):
            next = "XSZZ    "
        elif (manip == XZSZ):
            next = "XZSZ    "
        elif (manip == ZSSZ):
            next = "ZSSZ    "
        elif (manip == ZXZZ):
            next = "ZXZZ    "
        str += next
    print(str)

def offsets(list):
    string = ""
    for offset in list:
        next = str(offset)
        for i in range(len(next), 8):
            next += " "
        string += next
    print(string)

def xout(list):
    string = ""
    for i in list:
        string += str(i)
        for j in range(8-len(str(i))):
            string += " "
    print(string)

out = search()
xout(out[ATTACKS])
results(out[ATTACKS])
readable(out[MANIP_SEQUENCE])
offsets(out[OFFSET_LIST])
