## This file is part of Ya-Ge-zy.
## Copyright (C) 2019 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

from yagezyBase import YagezyGame

class Generala(YagezyGame):
  def __init__(self) :
    super().__init__("Generala")

  def gameCombinations(self, concise = False) :
    if concise:
      return ["1s", "2s", "3s", "4s", "5s", "6s", "es", "fh", "fk", "ge"]
      
    return ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Escalera", "Full", "FOAK", "Generala"]

  def rollScores(self, roll, availableCombinations) :
    r0,r1,r2,r3,r4 = roll
    assert r0 <= r1 <= r2 <= r3 <= r4

    for i,avail in enumerate(availableCombinations[:6]):
      if avail:
        d = i + 1
        n = (r0 == d) + (r1 == d) + (r2 == d) + (r3 == d) + (r4 == d)
        n *= d
        
        yield i,n

    for i,avail in enumerate(availableCombinations[6:]):
      if avail:
        i += 6
        hasMatch = False
        if i == 6:
          if tuple(roll) == (1,2,3,4,5) or tuple(roll) == (2,3,4,5,6) :
            yield i, 20
            hasMatch = True
        elif i == 7:
          if r0 == r1 and r3 == r4 and (r2 == r1 or r2 == r3) :
            yield i, 30
            hasMatch = True
        elif i == 8:
          if r1 == r2 == r3 and (r0 == r1 or r4 == r3) :
            yield i, 40
            hasMatch = True
        elif i == 9:
          if r0 == r4 :
            yield i, 50
            hasMatch = True
            
        if not hasMatch:
          yield i, 0

