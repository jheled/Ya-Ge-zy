## This file is part of Ya-Ge-zy.
## Copyright (C) 2019 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

from yagezyBase import YagezyGame

class Yacht(YagezyGame):
  def __init__(self) :
    super().__init__("Yacht")

  def gameCombinations(self, concise = False) :
    if concise:
      return ["1s", "2s", "3s", "4s", "5s", "6s", "fh", "fk", "ls", "bs", "ch", "ya"]
    
    return ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "Full", "FOAK", "L-Straight", "B-Straight", "Choice", "Yacht"]

  def rollScores(self, roll, availableCombinations) :
    r0,r1,r2,r3,r4 = roll
    assert r0 <= r1 <= r2 <= r3 <= r4

    for i,avail in enumerate(availableCombinations[:6]):
      if avail:
        d = i + 1
        n = (r0 == d) + (r1 == d) + (r2 == d) + (r3 == d) + (r4 == d)
        n *= d
        
        yield i,n

    notMatched = []
    i = 6
    if availableCombinations[i]:
      if r0 == r1 and r3 == r4 and (r2 == r1 or r2 == r3) :
        yield i, 2*r0+r2+2*r4
      else:
        notMatched.append(i)

    i = 7
    if availableCombinations[i]:
      if r1 == r2 == r3 and (r0 == r1 or r4 == r3) :
        yield i, 4*r2
      else:
        notMatched.append(i)

    i = 8
    if availableCombinations[i]:
      if tuple(roll) == (1,2,3,4,5):
        yield i, 30
      else:
        notMatched.append(i)

    i = 9
    if availableCombinations[i]:
      if tuple(roll) == (2,3,4,5,6):
        yield i, 30
      else:
        notMatched.append(i)

    i = 10
    if availableCombinations[i]:
      yield i, r0+r1+r2+r3+r4

    i = 11
    if availableCombinations[i]:
      if r0 == r4:
        yield i, 50
      else:
        notMatched.append(i)

    for i in notMatched:
      yield i, 0

