from yagezyBase import YagezyGame

class Yatzy(YagezyGame):
  def __init__(self) :
    super().__init__("Yatzy")

  def gameCombinations(self) :
    return ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
            "1Pair", "2Pair", "3Same", "4Same", "S-Straight", "L-Straight",
            "Full", "Choice", "Yatzy"]

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
      has = False
      if r0 == r1:
        yield i, 2*r0
        has = True
      for j in (2,3,4) :
        if roll[j-1] == roll[j] and (roll[j-2] != roll[j-1]) :
          yield i, 2*roll[j]
          has = True
      if not has:
        notMatched.append(i)

    i = 7
    if availableCombinations[i]:
      if r0 == r4:
        yield i, 4*r0
      elif r0 == r1 and r2 == r3:
        yield i, 2*(r0+r2)
      elif r0 == r1 and r3 == r4:
        yield i, 2*(r0+r3)
      elif r1 == r2 and r3 == r4:
        yield i, 2*(r1+r3)
      else:
        notMatched.append(i)
        
    i = 8
    if availableCombinations[i]:
      if r0 == r2:
        yield i, 3*r0
      elif r1 == r3 and r0 != r1:
        yield i, 3*r1
      elif r2 == r4 and r2 != r1:
        yield i, 3*r2
      else:
        notMatched.append(i)

    i = 9
    if availableCombinations[i]:
      if r1 == r2 == r3 and (r0 == r1 or r4 == r3) :
        yield i, 4*r2
      else:
        notMatched.append(i)

    i = 10
    if availableCombinations[i]:
      if tuple(roll) == (1,2,3,4,5):
        yield i, 15
      else:
        notMatched.append(i)

    i = 11
    if availableCombinations[i]:
      if tuple(roll) == (2,3,4,5,6):
        yield i, 20
      else:
        notMatched.append(i)
        
    i = 12
    if availableCombinations[i]:
      if r0 == r1 and r3 == r4 and (r2 == r1 or r2 == r3) :
        yield i, 2*r0+r2+2*r4
      else:
        notMatched.append(i)

    i = 13
    if availableCombinations[i]:
      yield i, r0+r1+r2+r3+r4

    i = 14
    if availableCombinations[i]:
      if r0 == r4:
        yield i, 50
      else:
        notMatched.append(i)

    for i in notMatched:
      yield i, 0

