#! /usr/bin/env python3
## This file is part of Ya-Ge-zy.
## Copyright (C) 2019 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

import argparse, sys
import Generala,Yacht,Yatzy,Crag,genericPlayers
from yagezyBase import annotateGame
  
parser = argparse.ArgumentParser(description = """Annotate a Yatzy/Yacht/Generala/Crag game.""")

parser.add_argument('gamelog', metavar='FILE', help="File name.")
  
options = parser.parse_args()

try :
  flog = open(options.gamelog)
except:
  print("Error opening match log.", file = sys.stderr)
  sys.exit(1)

for line in flog:
  line = line.strip()
  if line:
    gameLog = eval(line)
    name, X, O = gameLog[0]
    n = len(gameLog[1:])
    if name == "Generala" and n == 2*10:
      game = Generala.Generala()
    elif name == "Yacht" and n == 2*12:
      game = Yacht.Yacht()
    elif "Yatzy" and n == 2*15:
      game = Yatzy.Yatzy()
    elif "Crag" and n == 2*13:
      game = Crag.Crag()
    else:
      print("Corrupted match log.", file = sys.stderr)
      sys.exit(1)

    name = game.__class__.__name__.split('.')[0]
    master = genericPlayers.MindfulPlayer(game, f"data/{name.lower()}-scdist.txt")
      
    annotateGame(gameLog[1:], master, X, O, 2*1e-4)

