import random, itertools, time
from collections import Counter, defaultdict

class YagezyGame:
  """ Base class for Yacht/Generala/Yatzy. """
  def __init__(self, name) :
    self.name = name

  def gameCombinations(self) :
    """ Dice combinations of the game. A list of strings, each a combination name. """
    assert False

  def rollScores(self, roll, availableCombinations) :
    """ Generates possible scores for 'roll'. 'availableCombinations' is a 1/0 sequence of
        length N-Game-Combinations. Yields a sequence of (i-combination, n-points-scored).
    """
    assert False

  def startPosition(self, nPlayers) :
    n = len(self.gameCombinations())
    return tuple([ ((1,)*n,0) ]*nPlayers)

  @staticmethod
  def over(position) :
    """ game over? """
    return not any(position[0][0])

  def maxScore(self) :
    """ Maximum possible score. """
    
    n = len(self.gameCombinations())
    bx = [0]*n
    drp = DiceRacePlayer("")

    tot = 0
    for i in range(n) :
      maxi = 0

      bx[i] = 1
      for dice in drp.rolls[-1] :
        mx = max([pts for i,pts in self.rollScores(dice, bx)])
        if maxi < mx:
          maxi = mx
      bx[i] = 0
      tot += maxi
    return tot

pow6 = [6**0, 6**1, 6**2, 6**3, 6**4, 6**5]

def merg5(sz , d) :
  #cdef int i,j,k, ls, ld
  i = j = k = 0
  ls,ld = len(sz), len(d)
  r = [-1,-1,-1,-1,-1]
  while i < 5 and j < ls and k < ld:
    if sz[j] < d[k] :
      r[i] = sz[j]
      j += 1
    else :
      r[i] = d[k]
      k += 1
    i += 1
  if i < 5:
    while j < ls:
      r[i] = sz[j]
      i += 1; j += 1
    while k < ld:
      r[i] = d[k]
      i += 1; k += 1
  return tuple(r)

class YagezyPlayer:
  def __init__(self, name) :
    self.name = name
    
    rts = []
    for i in range(32) :
      b = format(i,"05b")
      a = []
      for k,x in enumerate(b) :
        if x == '1':
          a.append(k)
      rts.append(list(a))
    self.rts = rts
    self.rolls = [ Counter(),
              Counter([tuple(sorted(x)) for x in itertools.product([1,2,3,4,5,6], repeat = 1)]) ,
              Counter([tuple(sorted(x)) for x in itertools.product([1,2,3,4,5,6], repeat = 2)]) ,
              Counter([tuple(sorted(x)) for x in itertools.product([1,2,3,4,5,6], repeat = 3)]) ,
              Counter([tuple(sorted(x)) for x in itertools.product([1,2,3,4,5,6], repeat = 4)]) ,
              Counter([tuple(sorted(x)) for x in itertools.product([1,2,3,4,5,6], repeat = 5)]) ]

  def actionR1(self, position, dice, details = False) :
    l3 = self.lev3(position)
    l2 = self.lev2(l3)
    return self.actionT(dice, l2, details)

  def actionR2(self, position, dice, details = False) :
    l3 = self.lev3(position)
    return self.actionT(dice, l3, details)

  def actionEndTurn(self, position, dice) :
    assert False

  def lev3(self, position) :
    assert False
    
  def lev2(self, lv3, keepAction = False) :
    ## lv3 is equity/value for X (player)
    cac = dict()
    lv2 = dict()
    rts,rolls = self.rts,self.rolls

    #cdef double ev, mxe
    #cdef int nToRoll, wt
    
    for dice in rolls[-1]:
      mxe = -float('inf')
      for x in rts:
        sz = tuple(dice[i] for i in x)

        e = cac.get(sz)
        if e is None:
          nToRoll = 5 - len(sz)
          if nToRoll == 0 :
            ev = lv3[sz]
          else :
            ct = rolls[nToRoll]
            ev = 0
            for d,wt in ct.items():
              r = merg5(sz, d);
              ev += lv3[r] * wt
            ev /= pow6[nToRoll]
          cac[sz] = ev
        else :
          ev = e
        if ev > mxe:
          mxe,keep = ev,sz

      lv2[dice] = (mxe,keep) if keepAction else mxe
    return lv2
    
  def actionT(self, dice, interEq, details = False) :
    dice = tuple(sorted(dice))

    rts,rolls = self.rts,self.rolls
    cac = dict()
    if details:
      rep = dict()

    #cdef int nToRoll, wt
    #cdef double mxe, ev
    
    mxe, keep = -float('inf'), None
    for x in rts:
      sz = tuple(dice[i] for i in x)
      e = cac.get(sz)
      if e is None:
        nToRoll = 5 - len(sz)
        if nToRoll == 0 :
          ev = interEq[tuple(dice)]
        else :
          ct = rolls[nToRoll]
          ev = 0
          for d,wt in ct.items():
            r = merg5(sz, d)
            ev += interEq[r] * wt
          ev /= pow6[nToRoll]
        cac[sz] = ev
      else :
        ev = e
      if details:
        rep[sz] = ev
      if mxe < ev:
        mxe,keep = ev, sz
    if details:
      return keep, (mxe,rep)
    return keep 

## Play one turn of 'position', using 'player' and optional initial dice roll
#
def playTurn(position, player, dice = None) :
  if not dice:
    dice = tuple(sorted(random.randint(1,6) for _ in range(5)))
  k = player.actionR1(position, dice)
  dice = tuple(sorted(k + tuple(random.randint(1,6) for _ in range(5 - len(k)))))
  k = player.actionR2(position, dice)
  dice = tuple(sorted(k + tuple(random.randint(1,6) for _ in range(5 - len(k)))))
  iMoves = player.actionEndTurn(position, dice)
  if len(iMoves) > 1:
    iMove = random.choice(iMoves)
  else :
    iMove = iMoves[0]

  bx,n = position[0]; bx = list(bx); bx[iMove] = 0

  b = [0]*len(bx)
  b[iMove] = 1
  i,pts = max(player.game.rollScores(dice, b));          assert i == iMove

  return position[1:] + ( (tuple(bx),n+pts), ),dice


def issub(sb, st) :
  return set(sb).issubset(st) and (not Counter(sb) - Counter(st))

## play 'position' to the bitter end, using 'players'. Optionaly return game log.
#
def playToEnd(game, players, position = None, keepLog = False) :
  nCombinations = len(game.gameCombinations())
  nPlayers = len(players)

  if position is None:
    position = game.startPosition(nPlayers)
    
  if keepLog:
    movesLog = []

  iPlayer = 0
  while not game.over(position) :
    if keepLog:
      mvlog = [position]
    player = players[iPlayer]
    
    dice = tuple(sorted(random.randint(1,6) for _ in range(5)))
    if keepLog: mvlog.append(dice)
    
    k = player.actionR1(position, dice);                assert issub(tuple(k), dice),(player.name,k,dice)
    dice = k + tuple(random.randint(1,6) for _ in range(5 - len(k)))
    if keepLog: mvlog.append( (k,dice[len(k):]) )
    
    dice = tuple(sorted(dice))
    k = player.actionR2(position, dice);                assert issub(tuple(k), dice),(player.name,k,dice)
    dice = k + tuple(random.randint(1,6) for _ in range(5 - len(k)))
    if keepLog: mvlog.append( (k,dice[len(k):]) )
    dice = tuple(sorted(dice))
    
    iMoves = player.actionEndTurn(position, dice)
    if len(iMoves) > 1:
      iMove = random.choice(iMoves)
    else :
      iMove = iMoves[0]

    bx = [0]*nCombinations
    bx[iMove] = 1
    i,pts = max(game.rollScores(dice, bx));          assert i == iMove

    bx = list(position[0][0])
    bx[iMove] = 0
    if keepLog:
      mvlog.extend( (iMove, pts) )
      movesLog.append(mvlog)

    position = tuple(position[1:]) + ( (tuple(bx),position[0][1]+pts), )
    iPlayer += 1
    if iPlayer >= nPlayers :
      iPlayer = 0

  while iPlayer != 0:
    position = position[1:] + position[:1]
    iPlayer = (iPlayer+1) % nPlayers

  maxScore = max(n for p,n in position)
  nWinners = sum(n == maxScore for p,n in position)
  winAmount = (nPlayers - nWinners)/nWinners
  points = [winAmount if n == maxScore else -1 for p,n in position]

  if keepLog :
    return (position, points),movesLog
  return position, points



def boardString(pointsByCat, nameX, nameO, catMnemonics) :
  s = " | " + " | ".join([x if x[0].isdigit() else x.upper() for x in catMnemonics]) + " |"
  s = ' '*10 + s
  for n,bc in ( (nameX, pointsByCat[0]), (nameO, pointsByCat[1]) ) :
    s += '\n' + (f'{n:10s} ' + "".join(['| ' + (f'{x:2d}' if x is not None else '  ') + ' '
                                          for x in bc]) + f'| {sum([x for x in bc if x]):3d}')
  s +=  '\n' + '='*(10+1+5*len(catMnemonics)+1)
  return s

## Play one game agains a human. Very basic text interface.
#
def playGame(computerPlayer, opName, computerStarts, computerName = None,
             delay = .3, debug = False) :
  
  if computerName is None:
    computerName = computerPlayer.name
    
  formatDice = lambda dice : ",".join([str(x) for x in dice])
  issub = lambda sb, st : set(sb).issubset(st) and (not Counter(sb) - Counter(st))

  game = computerPlayer.game
  
  concise = {"Ones" : "1s", "Twos" : "2s", "Threes" : "3s", "Fours" : "4s", "Fives" : "5s", "Sixes" : "6s"}
  fcats = game.gameCombinations()[::-1]
  nCats = len(fcats)
  cats = [concise.get(x) or x for x in fcats]

  catCodes = {"Escalera" : "es", "Full" : "fh", "FOAK" : "fk", "Generala" : "gn"}
  catCodes.update( {"L-Straight" : "ls", "B-Straight" : "bs", "Choice" : "ch", "Yacht" : "ya"} )
  catCodes.update( {"1Pair" : "pr", "2Pair" : "pp", "3Same" : "ts", "4Same" : "fs",
                    "S-Straight" : "ss", "L-Straight" : "ls", "Choice" : "co", "Yatzy" : "ya"} )
  
  catCodes.update(concise)
  
  lccats = [catCodes[x] for x in fcats]
  singlelc = {k : [a[0] for a in lccats].index(k)
              for k,v in Counter([a[0] for a in lccats]).items() if v == 1}
  
  gameLog = []
  pos = game.startPosition(2)
  pointsByCat = [None,]*nCats, [None,]*nCats
  computerTurn = computerStarts
  while not game.over(pos) :
    if debug:
      print(pos)
      print()
    print(boardString(pointsByCat, computerName, opName,lccats))
    moveLog = []
    if computerTurn :
      dice = tuple(random.randint(1,6) for _ in range(5))
      print(f'{computerName} rolls {formatDice(dice)}'); time.sleep(delay)
      moveLog.append(dice)
      k = computerPlayer.actionR1(pos, tuple(sorted(dice)))
      r1 = tuple(random.randint(1,6) for _ in range(5 - len(k)))
      print(f'keeps {formatDice(k)}, rolls {formatDice(r1)}'); time.sleep(delay)
      moveLog.append((k,r1))
      dice = k + r1
      k = computerPlayer.actionR2(pos, tuple(sorted(dice)))
      r2 = tuple(random.randint(1,6) for _ in range(5 - len(k)))
      print(f'keeps {formatDice(k)}, rolls {formatDice(r2)}'); time.sleep(delay)
      moveLog.append((k,r2))
      dice = k + r2
      iMoves = computerPlayer.actionEndTurn(pos, tuple(sorted(dice)))
      if len(iMoves) > 1:
        iMove = random.choice(iMoves)
      else :
        iMove = iMoves[0]
        
      bx = [0]*nCats
      bx[iMove] = 1
      i,pts = max(game.rollScores(tuple(sorted(dice)), bx));          assert i == iMove

      moveLog.extend((iMove,pts))
      
      bx = list(pos[0][0])
      bx[iMove] = 0

      what = fcats[nCats - 1 - iMove]
      print(f'{computerName}: {formatDice(dice)}. marks {what} for {pts} points.'); time.sleep(delay)
      pointsByCat[0][nCats - 1 - iMove] = pts
      pos = tuple(pos[1:]) + ( (tuple(bx),pos[0][1]+pts), )
      computerTurn = False
    else :
      dice = tuple(random.randint(1,6) for _ in range(5))
      moveLog.append(dice)
      print(f'{opName} rolls {formatDice(dice)}');
      mark = None
      
      while True:
        toKeep = input("keep?").strip()
        if toKeep.lower() in lccats :
          k = dice
          mark = toKeep
          break
        k = tuple(int(x) for x in toKeep if x.isdigit())
        if issub(k, dice) :
          break
      r = tuple(random.randint(1,6) for _ in range(5 - len(k)))
      dice = k + r
      moveLog.append((k,r))

      if mark is None:
        print(f'dice {formatDice(dice)}')
        while True:
          toKeep = input("keep?").strip()
          if toKeep.lower() in lccats :
            k = dice
            mark = toKeep
            break
          k = tuple(int(x) for x in toKeep if x.isdigit())
          if issub(k, dice) :
            break
      r = tuple(random.randint(1,6) for _ in range(5 - len(k)))
      dice = k + r
      moveLog.append((k,r))
      if mark is None:
        print(f'final dice {formatDice(dice)}')
      while True:
        if mark is None:
          mark = input("mark?").strip()
        m = -1
        c = mark[0].lower()
        if c in singlelc:
          m = nCats - 1 - singlelc[c]
        elif mark.lower() in lccats:
          m = nCats - 1 - lccats.index(mark.lower())
        if m >= 0 and pointsByCat[1][nCats - 1 - m] is None:
          break
        mark = None

      bx = [0]*nCats
      bx[m] = 1
      i,pts = max(game.rollScores(tuple(sorted(dice)), bx));          assert i == m
      
      print(f'{pts} points.')
      pointsByCat[1][nCats-1-m] = pts
      moveLog.extend((m,pts))
      
      bx = list(pos[0][0])
      bx[m] = 0
      pos = tuple(pos[1:]) + ( (tuple(bx),pos[0][1]+pts), )
      computerTurn = True
    gameLog.append(moveLog)
    
  print()
  print(boardString(pointsByCat, computerName, opName,lccats))
  
  return gameLog

## Annotate a game using the near-optimal 'Mindfull' player.
#
def annotateGame(gameLog, gameMaster, X = 'X', O = 'O', errTH = 1e-9) :
  game = gameMaster.game

  formatDice = lambda dice : ",".join([str(x) for x in dice])
  issub = lambda sb, st : set(sb).issubset(st) and (not Counter(sb) - Counter(st))

  concise = {"Ones" : "1s", "Twos" : "2s", "Threes" : "3s", "Fours" : "4s", "Fives" : "5s", "Sixes" : "6s"}
  fcats = game.gameCombinations()[::-1]
  nCats = len(fcats)
  cats = [concise.get(x) or x for x in fcats]

  catCodes = {"Escalera" : "es", "Full" : "fh", "FOAK" : "fk", "Generala" : "gn"}
  catCodes.update( {"L-Straight" : "ls", "B-Straight" : "bs", "Choice" : "ch", "Yacht" : "ya"} )
  catCodes.update( {"1Pair" : "pr", "2Pair" : "pp", "3Same" : "ts", "4Same" : "fs",
                    "S-Straight" : "ss", "L-Straight" : "ls", "Choice" : "co", "Yatzy" : "ya"} )
  catCodes.update(concise)
  lccats = [catCodes[x] for x in fcats]
  
  pos = game.startPosition(2)

  pointsByCat = [None,]*nCats, [None,]*nCats
  totErr = [0,0]

  from math import log
  err2ELO = lambda dif : 400 * log(1/(.5-dif) - 1, 10)
  
  for nm, moveLog in enumerate(gameLog):
    pl = [X,O][nm % 2]
    print()
    print(f'{1+nm//2:2d}) {pl}')
    print(boardString(pointsByCat, X, O,lccats))

    dice0, (dice1k,dice1r), (dice2k,dice2r), iMark, pts = moveLog
    dice0,dice1k,dice1r,dice2k,dice2r = [tuple(sorted(x)) for x in (dice0,dice1k,dice1r,dice2k,dice2r)]
    k, (e,d) = gameMaster.actionR1(pos, dice0, True)
    er = d[dice1k] - d[k] if k != dice1k else 0
    if abs(er) > errTH :
      #print(pos)
      print()
      err = d[dice1k] - d[k]
      totErr[nm % 2] += err2ELO(err)
      print(f' {formatDice(dice0)}: move {formatDice(dice1k):10s} ({d[dice1k]:1.4f}), \
best  {formatDice(k):10s} ({d[k]:1.4f} [{err:.5f}])')
    else :
      if len(dice1k) < 5:
        print(f' {formatDice(dice0)}: move {formatDice(dice1k):10s} ({d[dice1k]:1.4f})')

    dice1 = tuple(sorted(dice1k + dice1r))
    k, (e,d) = gameMaster.actionR2(pos, dice1, True)
    er = d[dice2k] - d[k] if k != dice2k else 0
    if abs(er) > errTH :
      #print(pos)
      err = d[dice2k] - d[k]
      totErr[nm % 2] += err2ELO(err)
      print(f' {formatDice(dice1)}: move {formatDice(dice2k):10s} ({d[dice2k]:1.4f}), \
best  {formatDice(k):10s} ({d[k]:1.4f} [{err:.5f}])')
    else :
      if len(dice2k) < 5:
        print(f' {formatDice(dice1)}: move {formatDice(dice2k):10s} ({d[dice2k]:1.4f})')

    dice2 = tuple(sorted(dice2k + dice2r))
    
    iMoves,d = gameMaster.actionEndTurn(pos, dice2, True)
    ##if dbg: print(pos)
    iBest = iMoves[0]
    #print(pos, dice2, iMark, bestM, npos)
    eMove,pts = d[iMark]

    bx = list(pos[0][0])
    bx[iMark] = 0
    pos = tuple(pos[1:]) + ( (tuple(bx),pos[0][1]+pts), )

    s = f' {formatDice(dice2)}: {"mark" if pts>0 else "waive"} {fcats[nCats-1-iMark]}, {pts} points '
    if iBest != iMark:
      eBest,ptsBest = d[iBest]
      if abs(eMove - eBest) > errTH :
        err = eMove - eBest
        totErr[nm % 2] += err2ELO(err)
        
        s += f'({eMove:1.4f}), best play: {"mark" if ptsBest>0 else "waive"} \
{fcats[nCats-1-iBest]} ({ptsBest} points, {eBest:1.4f} [{eMove - eBest:.4f}])'
        e = None
    if e is not None:
      s += f'({eMove:1.4f})'
    print(s)
    
    pointsByCat[nm % 2][nCats-1-iMark] = pts

  print()
  print(boardString(pointsByCat, X, O,lccats))
  print()
  print(f'Players ELO rating | {X}: {2000 + totErr[0]:.0f}, {O}: {2000 + totErr[1]:.0f}')
