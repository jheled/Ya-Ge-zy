## This file is part of Ya-Ge-zy.
## Copyright (C) 2019 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

from yagezyBase import *

class WhateverPlayer(YagezyPlayer) :
  """Drunk player: can't be botherd to re-roll, picks (one of the) combinations which scores the most
     points."""
  
  def __init__(self, game) :
    super().__init__(f"whatever-{game.name}")
    self.game = game

  def actionR1(self, pos, dice) :
    return dice

  def actionR2(self, pos, dice) :
    return dice
  
  def actionEndTurn(self, pos, dice) :
    mpts = -1
    iScore = []
    for i,pts in self.game.rollScores(dice, pos[0][0]) :
      if mpts < pts:
        mpts = pts
        iScore = [i]
      elif mpts == pts:
        iScore.append(i)
    return iScore

class SimplePlayer(YagezyPlayer) :
  """ Simple minded player, supposed to be human level, but who knows. """
  def __init__(self, game) :
    super().__init__(f"simple-{game.name}")
    self.game = game

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

  def generateMaximizerScoreDists(self) :
    from collections import defaultdict
    
    dists = dict()
    nc = len(self.game.gameCombinations())
    dists[(0,)*nc] = { 0 : 1.0 }
    bfrmt = f"0{nc}b"

    rts,rolls = self.rts,self.rolls

    from yagezyBase import pow6,merg5

    expandedRollsDist = dict()
    for nKept in range(1,6) :
      nToRoll = 5 - nKept
      for keep in rolls[nKept]:
        dl = []
        if nToRoll == 0:
          dl.append( (keep,1) )
        else :
          ct = rolls[nToRoll]
          f = pow6[nToRoll]
          for d,c in ct.items():
            r = merg5(keep, d);
            dl.append( (r, c/f) )
        expandedRollsDist[keep] = dl

    expandedRollsDist[tuple()] = [ (dice,wt/6**5) for dice,wt in rolls[-1].items() ]
      
    for n in range(1, nc+1) :
      for i in range(2**nc) :
        bx = tuple(int(x) for x in format(i, bfrmt))
        if sum(bx) == n:
          lv3 = self.lev3( ((bx,0),) )
          flv2 = self.lev2(lv3, True)
          lv2 = { dice : x[0] for dice,x in flv2.items() }

          ## d2[dice] = probability of ending with this dice after first re-throw 
          d2 = defaultdict( lambda : 0 )
          for dice,wt in rolls[-1].items():
            keep = self.actionT(dice, lv2)
            wt /= 6**5
            for de,pr in expandedRollsDist[keep]:
              d2[de] += wt * pr
              
          ## d1[dice] = probability of ending with this dice before scoring 
          d1 = defaultdict( lambda : 0 )
          for dice,pr in d2.items():
            keep = flv2[dice][1]    # cached self.actionT(dice, lv3)

            for de,pre in expandedRollsDist[keep]:
              d1[de] += pr * pre
            
          posDist = defaultdict( lambda : 0 )
          for dice,prDice in d1.items():
            iMoves = self.actionEndTurn( ((bx,0),), dice )
            for iMove in iMoves:
              pts = self.l3points[iMove,dice]
              p = prDice/len(iMoves)
              b = list(bx); b[iMove] = 0; b = tuple(b)
              for score,prScore in dists[b].items():
                posDist[score + pts] += prScore * p
          dists[bx] = dict(posDist)
          
    return dists

# One-Sided-Table-Based

class OSTBPlayer(YagezyPlayer) :
  """One-Sided-Table-Based

  One-Sided (partisan) player ignoring status/scores of other players.

  play based on a table with a 'value' for each subset of remaining combinations. This 'value' might
  be the expected score or any other heuristic.
  """
  
  def __init__(self, game, values, method="maxi") :
    super().__init__(f"ostb({method}-{game.name}")
    self.game = game
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
    self.values[(0,)*nc] = 0.0
    bfrmt = f"0{nc}b"

    rts,rolls = self.rts,self.rolls

    from yagezyBase import pow6, merg5
    
    for n in range(1,nc+1) :
      for i in range(2**nc) :
        bx = tuple(int(x) for x in format(i, bfrmt))
        if sum(bx) == n:
          pos = [(bx,0)]
          lv3 = self.lev3(pos)
          lv2 = self.lev2(lv3)

          cac = dict()
          ee = 0.0
          for dice,wt in rolls[-1].items():
            mxe = -float('inf')
            for x in rts:
              sz = tuple(dice[i] for i in x)
              e = cac.get(sz)
              if e is None:
                nToRoll = 5 - len(sz)
                if nToRoll == 0:
                  e = lv2[sz]
                else :
                  ct = rolls[nToRoll]
                  e = 0
                  for d,c in ct.items():
                    r = merg5(sz, d);
                    e += lv2[r] * c
                  e /= pow6[nToRoll]
                cac[sz] = e
              if mxe < e:
                mxe = e
            ee += mxe * wt
          
          self.values[bx] = ee/6**5

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
    
    dists = dict() # defaultdict( lambda : defaultdict( lambda : 0 ) )
    nc = len(self.game.gameCombinations())
    dists[(0,)*nc] = { 0 : 1.0 }
    bfrmt = f"0{nc}b"

    rts,rolls = self.rts,self.rolls

    from yagezyBase import pow6,merg5

    expandedRollsDist = dict()
    for nKept in range(1,6) :
      nToRoll = 5 - nKept
      for keep in rolls[nKept]:
        dl = []
        if nToRoll == 0:
          dl.append( (keep,1) )
        else :
          ct = rolls[nToRoll]
          f = pow6[nToRoll]
          for d,c in ct.items():
            r = merg5(keep, d);
            dl.append( (r, c/f) )
        expandedRollsDist[keep] = dl

    expandedRollsDist[tuple()] = [ (dice,wt/6**5) for dice,wt in rolls[-1].items() ]
      
    for n in range(1, nc+1) :
      for i in range(2**nc) :
        bx = tuple(int(x) for x in format(i, bfrmt))
        if sum(bx) == n:
          flv3 = { dice : max(self.scores(dice, bx, 0)) for dice in self.rolls[-1] }
          lv3 = { dice : x[0] for dice,x in flv3.items() }
          flv2 = self.lev2(lv3, True)
          lv2 = { dice : x[0] for dice,x in flv2.items() }

          #l3 = self.lev3([(bx,0)]); l2 = self.lev2(l3)

          ##import pdb; pdb.set_trace()
          ## d2[dice] = probability of ending with this dice after first re-throw 
          d2 = defaultdict( lambda : 0 )
          for dice,wt in rolls[-1].items():
            keep = self.actionT(dice, lv2)
            wt /= 6**5
            for de,pr in expandedRollsDist[keep]:
              d2[de] += wt * pr
              
          ## d1[dice] = probability of ending with this dice before scoring 
          d1 = defaultdict( lambda : 0 )
          for dice,pr in d2.items():
            keep = flv2[dice][1]    # cached self.actionT(dice, lv3)

            for de,pre in expandedRollsDist[keep]:
              d1[de] += pr * pre
            
          posDist = defaultdict( lambda : 0 )
          for dice,prDice in d1.items():
            iMove,pts = flv3[dice][1:]
            b = list(bx); b[iMove] = 0; b = tuple(b)
            for score,prScore in dists[b].items():
              posDist[score + pts] += prScore * prDice
          dists[bx] = dict(posDist)
          
    return dists  ##{ x : dict(v) for x,v in dists.items() }

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

class MindfulPlayer(YagezyPlayer) :
  """ Strongest player here. For generala it is only 3.5 ELO points worse than
  optimal. Yacht and Yatzy are too big to solve, so difference to optimal is unknown.
  """
  
  def __init__(self, game, scoreDists, method = "maxi") :
    super().__init__(f"mindfule({method}-{game.name}")
    self.game = game

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
