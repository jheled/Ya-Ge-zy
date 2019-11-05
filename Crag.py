## This file is part of Ya-Ge-zy.
## Copyright (C) 2019 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

from yagezyBase import YagezyGame

class Crag(YagezyGame):
  def __init__(self) :
    super().__init__("Crag", 3, 1)

  def gameCombinations(self, concise = False) :
    if concise:
      return ["1s", "2s", "3s", "4s", "5s", "6s", "es", "os", "hs", "ls", "tk", "tr", "cr"]
    
    return ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Even-S", "Odd-S", "High-S", "Low-S", "3Same", "Thirteen", "Crag"]

  def rollScores(self, roll, availableCombinations) :
    r0,r1,r2 = roll;                                                assert r0 <= r1 <= r2

    for i,avail in enumerate(availableCombinations[:6]):
      if avail:
        d = i + 1
        n = (r0 == d) + (r1 == d) + (r2 == d)
        n *= d
        
        yield i,n

    notMatched = []
    i = 6
    if availableCombinations[i]:
      has = False
      if roll == (2,4,6) :
        yield i, 20
      else:
        notMatched.append(i)

    i = 7
    if availableCombinations[i]:
      if roll == (1,3,5) :
        yield i, 20
      else:
        notMatched.append(i)

    i = 8
    if availableCombinations[i]:
      if roll == (4,5,6) :
        yield i, 20
      else:
        notMatched.append(i)

    i = 9
    if availableCombinations[i]:
      if roll == (1,2,3) :
        yield i, 20
      else:
        notMatched.append(i)
        
    i = 10
    if availableCombinations[i]:
      if r0 == r1 == r2:
        yield i, 25
      else:
        notMatched.append(i)

    i = 11
    if availableCombinations[i]:
      if r0 + r1 + r2 == 13:
        yield i, 26
      else:
        notMatched.append(i)

    i = 12
    if availableCombinations[i]:
      if r0 + r1 + r2 == 13 and (r0 == r1 or r1 == r2) :
        yield i, 50
      else:
        notMatched.append(i)

    for i in notMatched:
      yield i, 0

#from yagezyBase import merge, pow6

# def merg3(sz , d) :
#   #cdef int i,j,k, ls, ld
#   i = j = k = 0
#   ls,ld = len(sz), len(d)
#   r = [-1,-1,-1]
#   while i < 3 and j < ls and k < ld:
#     if sz[j] < d[k] :
#       r[i] = sz[j]
#       j += 1
#     else :
#       r[i] = d[k]
#       k += 1
#     i += 1
#   if i < 3:
#     while j < ls:
#       r[i] = sz[j]
#       i += 1; j += 1
#     while k < ld:
#       r[i] = d[k]
#       i += 1; k += 1
#   return tuple(r)

# from collections import Counter
# import itertools

# class CragPlayer:
#   def __init__(self, name) :
#     self.name = name
#     self.nDice = nDice = 3
    
#     rts = []
#     for i in range(2**nDice) :
#       b = format(i,f"0{nDice}b")
#       a = []
#       for k,x in enumerate(b) :
#         if x == '1':
#           a.append(k)
#       rts.append(list(a))
#     self.rts = rts
#     self.rolls = [ Counter() ]
#     for n in range(nDice) :
#       self.rolls.append( Counter([tuple(sorted(x)) for x in itertools.product([1,2,3,4,5,6], repeat = n+1)]) )

#   def actionR1(self, position, dice, details = False) :
#     l3 = self.lev3(position)
#     return self.actionT(dice, l3, details)

#   def actionEndTurn(self, position, dice) :
#     assert False

#   def lev3(self, position) :
#     assert False
    
#   def actionT(self, dice, interEq, details = False) :
#     dice = tuple(sorted(dice))
#     nDice = len(dice)
    
#     rts,rolls = self.rts,self.rolls
#     cac = dict()
#     if details:
#       rep = dict()

#     #cdef int nToRoll, wt
#     #cdef double mxe, ev
    
#     mxe, keep = -float('inf'), None
#     for x in rts:
#       sz = tuple(dice[i] for i in x)
#       e = cac.get(sz)
#       if e is None:
#         nToRoll = nDice - len(sz)
#         if nToRoll == 0 :
#           ev = interEq[tuple(dice)]
#         else :
#           ct = rolls[nToRoll]
#           ev = 0
#           for d,wt in ct.items():
#             r = merge(sz, d)
#             ev += interEq[r] * wt
#           ev /= pow6[nToRoll]
#         cac[sz] = ev
#       else :
#         ev = e
#       if details:
#         rep[sz] = ev
#       if mxe < ev:
#         mxe,keep = ev, sz
#     if details:
#       return keep, (mxe,rep)
#     return keep 

# import genericPlayers
if 0:
  class SimplePlayer(CragPlayer) :
    def __init__(self) :
      self.game = Crag()
      CragPlayer.__init__(self, "simple-crag")

      self.game = game = Crag()

      nCombinations = len(game.gameCombinations())
      bx = [0]*nCombinations
      self.l3points = dict()
      for i in range(nCombinations) :
        bx[i] = 1
        avg = 0
        for dice in self.rolls[-1] :
          points = max(game.rollScores(dice, bx))[1]
          self.l3points[i,dice] = points
        bx[i] = 0

    def lev3(self, position) :
      bx,px = position[0]
      lv3 = { dice : max([self.l3points[i,dice] for i,has in enumerate(bx) if has])
              for dice in self.rolls[-1]}
      return lv3

    def actionEndTurn(self, position, dice) :
      bx,px = position[0]
      pts = [(self.l3points[i,dice],i) for i,has in enumerate(bx) if has]
      vMax = max(pts)[0]
      return [i for v,i in pts if v == vMax]

  class OSTBPlayer(CragPlayer) :
    """One-Sided-Table-Based

    One-Sided (partisan) player ignoring status/scores of other players.

    play based on a table with a 'value' for each subset of remaining combinations. This 'value' might
    be the expected score or any other heuristic.
    """

    def __init__(self, values, method="maxi") :
      self.game = game = Crag()
      super().__init__(f"ostb({method}-{game.name}")
      if isinstance(values, str) :
        values = self.loadValues(values)
      self.values = values

    def scores(self, dice, bx, pts) :
      b = list(bx)
      eqTab = self.values
      res = []
      for i,pts in self.game.rollScores(dice, bx) :
        b[i] = 0
        res.append( (pts + eqTab[tuple(b)], i, pts) )
        b[i] = 1
      return res

    def lev3(self, position) :
      bx,px = position[0]
      lv3 = { dice : max(self.scores(dice, bx, px))[0] for dice in self.rolls[-1] }
      return lv3

    def actionEndTurn(self, position, dice) :
      bx,px = position[0]
      i = max(self.scores(dice, bx, px))[1]
      return [i]

    #####################################
    ## Data generation
    def generateMaximizerValues(self) :
      self.values = dict()
      nc = len(self.game.gameCombinations())
      nDice = self.game.nDice

      self.values[(0,)*nc] = 0.0
      bfrmt = f"0{nc}b"

      rts,rolls = self.rts,self.rolls

      for n in range(1,nc+1) :
        for i in range(2**nc) :
          bx = tuple(int(x) for x in format(i, bfrmt))
          if sum(bx) == n:
            pos = [(bx,0)]
            lv3 = self.lev3(pos)
            ##lv2 = self.lev2(lv3)

            cac = dict()
            ee = 0.0
            for dice,wt in rolls[-1].items():
              mxe = -float('inf')
              for x in rts:
                sz = tuple(dice[i] for i in x)
                e = cac.get(sz)
                if e is None:
                  nToRoll = nDice - len(sz)
                  if nToRoll == 0:
                    e = lv3[sz]
                  else :
                    ct = rolls[nToRoll]
                    e = 0
                    for d,c in ct.items():
                      r = merge(sz, d);
                      e += lv3[r] * c
                    e /= pow6[nToRoll]
                  cac[sz] = e
                if mxe < e:
                  mxe = e
              ee += mxe * wt

            self.values[bx] = ee/pow6[nDice]

    def saveValues(self, fileName) :
      ff = open(fileName, 'w')
      for k,v in self.values.items():
        print( (k,v), file = ff)
      ff.close()

    def loadValues(self, fileName) :
      values = dict()
      ff = open(fileName)
      for l in ff:
        k,v = eval(l.strip())
        values[k] = v
      ff.close()
      return values

    def generateMaximizerScoreDists(self) :
      from collections import defaultdict

      dists = dict()
      nc = len(self.game.gameCombinations())
      nDice = self.game.nDice

      dists[(0,)*nc] = { 0 : 1.0 }
      bfrmt = f"0{nc}b"

      rts,rolls = self.rts,self.rolls

      ##from yagezyBase import pow6,merg5

      expandedRollsDist = dict()
      for nKept in range(1,nDice+1) :
        nToRoll = nDice - nKept
        for keep in rolls[nKept]:
          dl = []
          if nToRoll == 0:
            dl.append( (keep,1) )
          else :
            ct = rolls[nToRoll]
            f = pow6[nToRoll]
            for d,c in ct.items():
              r = merge(keep, d);
              dl.append( (r, c/f) )
          expandedRollsDist[keep] = dl

      expandedRollsDist[tuple()] = [ (dice,wt/pow6[nDice]) for dice,wt in rolls[-1].items() ]

      for n in range(1, nc+1) :
        for i in range(2**nc) :
          bx = tuple(int(x) for x in format(i, bfrmt))
          if sum(bx) == n:
            flv3 = { dice : max(self.scores(dice, bx, 0)) for dice in self.rolls[-1] }
            lv3 = { dice : x[0] for dice,x in flv3.items() }

            ## d1[dice] = probability of ending with this dice before scoring 
            d1 = defaultdict( lambda : 0 )
            for dice,wt in rolls[-1].items() :
              keep = self.actionT(dice, lv3)
              pr = wt / pow6[nDice]
              for de,pre in expandedRollsDist[keep]:
                d1[de] += pr * pre

            posDist = defaultdict( lambda : 0 )
            for dice,prDice in d1.items():
              iMove,pts = flv3[dice][1:]
              b = list(bx); b[iMove] = 0; b = tuple(b)
              for score,prScore in dists[b].items():
                posDist[score + pts] += prScore * prDice
            dists[bx] = dict(posDist)

      return dists

  def flattenDist(dist, size) :
    d = [0]*size
    for x,p in dist.items():
      d[x] = p
    cs = []
    s = 0
    for p in d:
      cs.append(s)
      s += p
    return (d,tuple(cs))

  class MindfulPlayer(CragPlayer) :
    """ Strongest player here. For generala it is only 3.5 ELO points worse than
    optimal. Yacht and Yatzy are too big to solve, so difference to optimal is unknown.
    """

    def __init__(self, scoreDists, method = "maxi") :
      self.game = game = Crag()
      super().__init__(f"mindfule({method}-{game.name}")

      scoreMax = game.maxScore() + 1
      if isinstance(scoreDists, str) :
        scoreDists = self.loadDists(scoreDists)
      self.sd = {x : { (x,1) : p for x,p in ds.items()} for x,ds in scoreDists.items()}
      self.fsd = {x : flattenDist(ds, scoreMax) for x,ds in scoreDists.items()}

    def loadDists(self, fileName) :
      dists = dict()
      with open(fileName) as ff:
        for l in ff:
          k,v = eval(l.strip())
          dists[k] = v
      return dists

    @staticmethod
    def combineDists(d1, pt1, d2, pt2) :
      d = defaultdict( lambda : 0 )
      for a,p1 in d1.items() :
        a = (a[0] + pt1,a[1])
        for b,p2 in d2.items() :
          b = (b[0] + pt2, b[1])
          d[max(a[0],b[0]),a[1]+b[1] if a[0]==b[0] else max(a,b)[1]] += p1*p2
      return d

    def combinedScoreDist(self, pos) :
      dsc,pts1 = self.sd[pos[0][0]],pos[0][1]
      if len(pos) == 1:
        return { (pts+pts1,n) : pr for (pts,n),pr in dsc.items()}

      for b,pts in pos[1:] :
        ds = self.sd[b]
        dsc = self.combineDists(dsc, pts1, ds, pts)
        pts1 = 0
      return dsc

    @staticmethod
    def eq(fd1, off, d2, n) :
      #cdef int b,nb
      #cdef double p2, pbl, p, pup, e, x

      peq,plr = fd1
      e = 0
      for (b,nb),p2 in d2.items() :
        if b < off:
          pbl,p,pup = 0,0,1
        else :
          pbl = plr[b-off]
          p = peq[b-off]
          pup = 1-(p + pbl)

        x = - p2 * pbl + pup * p2 * (n-1)
        if p > 0 :
          x += p2 * p * (n - (nb+1))/(nb+1)
        e += x
      return e

    def lev3(self, position) :
      others = position[1:]
      dsc = self.combinedScoreDist(others)
      p0b,p0n = position[0]

      cache = dict()
      lv3 = dict()
      for dice in self.rolls[-1]:
        mx = -10000
        for i,pts in self.game.rollScores(dice, p0b):
          b = list(p0b); b[i] = 0; b = tuple(b)
          ec = cache.get((b,pts))
          if ec is None:
            e = self.eq(self.fsd[b], p0n+pts, dsc, len(position))
            cache[b,pts] = e
          else :
            e = ec
          if mx < e:
            mx = e
        lv3[dice] = mx
      return lv3

    def actionEndTurn(self, position, dice, details = False) :
      bx,px = position[0]
      others = position[1:]
      dsc = self.combinedScoreDist(others)

      if details: eqs = dict()
      mx = -10000
      for i,pts in self.game.rollScores(dice, bx):
        b = list(bx); b[i] = 0; b = tuple(b)
        e = self.eq(self.fsd[b], px+pts, dsc, len(position))
        if details: eqs[i] = e,pts
        if e > mx:
          mx = e
          iMove = i
      if details:
        return ([iMove], eqs)
      return [iMove]

