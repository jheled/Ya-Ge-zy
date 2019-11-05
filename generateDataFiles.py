## This file is part of Ya-Ge-zy.
## Copyright (C) 2019 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

import os, os.path

import Generala,Yacht,Yatzy,Crag
from genericPlayers import OSTBPlayer, MindfulPlayer

maxiSuffix = "-maxi"
scSuffix = "-scdist"

if not os.path.exists('data') :
  os.mkdir('data')
  
for gameClass in (Generala, Yacht, Yatzy, Crag) :
  gameName = gameClass.__name__
  game = getattr(gameClass, gameName)()

  fname = f'{gameName.lower()}{maxiSuffix}.txt'
  if not os.path.exists(f"data/{fname}") :
    print(f"Generating {fname}, this will take some time ...")
    maxi = OSTBPlayer(game, None, "")
    maxi.generateMaximizerValues()
    with open(f"data/{fname}", "w") as fout:
      for k,v in maxi.values.items():
        print( (k,v), file = fout)
    
  fcname = f'{gameName.lower()}{scSuffix}.txt'
  if not os.path.exists(f"data/{fcname}") :
    print(f"Generating {fname}. Might take a long time. Longer for Yatzy.")
    maxi = OSTBPlayer(game, f"data/{fname}", "")
    dists = maxi.generateMaximizerScoreDists()
    with open(f"data/{fcname}", "w") as fout:
      for k,v in dists.items():
        print( (k,v), file = fout)
    
    
