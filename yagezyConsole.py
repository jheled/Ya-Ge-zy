#! /usr/bin/env python3
## This file is part of Ya-Ge-zy.
## Copyright (C) 2019 Joseph Heled.
## Author: Joseph Heled <jheled@gmail.com>
## See the file LICENSE for copying conditions.
#

import argparse, sys
import curses, random, time

import Generala,Yacht,Yatzy,Crag,genericPlayers

die1 = """ ▁▁▁
┃   ┃
┃ ⬤ ┃
┃   ┃
 ▔▔▔"""

die2 = """ ▁▁▁
┃⬤  ┃
┃   ┃
┃  ⬤┃
 ▔▔▔"""

die3 = """ ▁▁▁
┃⬤  ┃
┃ ⬤ ┃
┃  ⬤┃
 ▔▔▔"""

die4 = """ ▁▁▁
┃⬤ ⬤┃
┃   ┃
┃⬤ ⬤┃
 ▔▔▔"""

die5 = """ ▁▁▁
┃⬤ ⬤┃
┃ ⬤ ┃
┃⬤ ⬤┃
 ▔▔▔"""

die6 = """ ▁▁▁
┃⬤ ⬤┃
┃⬤ ⬤┃
┃⬤ ⬤┃
 ▔▔▔"""

game = None
player = None
flog = None
delay = 1
compName, opName = None, None

wCell = 6
hCell = 1

green, red ,yellow, col6 = None, None, None, None

def cell(window, y, x, name) :
  box1 = window.subwin(hCell, wCell, y, x)
  box1.box()
  box1.addstr(0, 0, " " + name + " |")
  return box1

def colorsMagic(window) :
  global green, red, yellow, col6
  
  curses.start_color()
  curses.use_default_colors()
  for i in range(0, curses.COLORS):
    curses.init_pair(i + 1, i, -1)
  green = curses.color_pair(3) | curses.A_STANDOUT
  red = curses.color_pair(2) | curses.A_STANDOUT
  yellow = curses.color_pair(7) | curses.A_STANDOUT
  col6 = curses.color_pair(6) | curses.A_STANDOUT

def showInfo(msg, info) :
  if info is not None:
    info.clear()
    info.addstr(0,0, msg, curses.color_pair(5))
    info.refresh()

dieFaces = (die1, die2, die3, die4, die5, die6)
dieHeight = len(die1.split('\n'))
dieWidth =  max([len(x) for x in die1.split('\n')])
        
def drawDie(dIndex, loc, window, y, x, attr = 0) :
  d = dieFaces[dIndex-1]
  for k,l in enumerate(d.split('\n')) :
    window.addstr(y+k, x + 6*loc, l, attr)

def clearDie(loc, window, y, x) :
  for k in range(dieHeight) :
    window.addstr(y+k, x + 6*loc, ' '*dieWidth)
    
def ut_interface(window):
  screen = curses.initscr() 
  curses.curs_set(0)
  screen.keypad(1) 
  curses.mousemask(1)
  colorsMagic(window)

  opDieColor = curses.color_pair(5)
  compDieColor = curses.color_pair(2)

  gameCombinations = game.gameCombinations(concise = True)
  nCombinations = n = len(gameCombinations)
  nDice = game.nDice
  nReRolls = game.nReRolls
  
  sepLine = '├' + (('─'*4 + "┼")*nCombinations)[:-1] + '┤'
  sepLine1 = '├' + (('─'*4 + "┴")*nCombinations)[:-1] + '┤'

  dice_x0 = 10 + (len(sepLine)- 6*nDice)//2

  info = window.subwin(10, 60, 15, 3)
  debug = None # window.subwin(1, 120, 20, 3)

  window.addstr(3, 10, '  ' + "   ".join([x.upper() if not x[0].isdigit() else x
                                          for x in gameCombinations]) + '  ')
  window.addstr(4, 10, sepLine)
  window.addstr(5, 10-len(compName), compName, col6)
  window.addstr(5, 10, "│    "*n + '│')
  window.addstr(6, 10, sepLine)
  window.addstr(7, 10-len(opName), opName, col6)
  window.addstr(7, 10, "│    "*n + '│')
  window.addstr(8, 10, '└' + sepLine1[1:-1] + '┘')
  
  while True:

    showInfo("Press space to start a new game. 'q' to exit.", info)

    ch = None
    while ch not in [' ', 'q']:
      ch = window.getkey()
    if ch == 'q':
      break

    for i in range(nCombinations) :
      window.addstr(5, 12 + i*5, '  ');
      window.addstr(7, 12 + i*5, '  ');
    for i in range(nDice) :
      clearDie(i, window, 9, dice_x0)

    window.addstr(5, 10 + len(sepLine) + 2, "   ")
    window.addstr(7, 10 + len(sepLine) + 2, "   ")
    
    showInfo("""Click on die to eliminate it.  'r' or space for re-roll.\n"""
             """Press on the score (green) to score. '1' keeps ones and\n"""
             """re-rolls others, same for '2','3' etc.""", info)

    position = game.startPosition(2)
    opTurn = random.randint(0, 1) == 0

    computerTurn = bool(random.randint(0,1))

    gameLog = []
    gameName = game.__class__.__name__.split('.')[0]
    gameLog.append( (gameName, opName, compName) if computerTurn else (gameName, compName, opName) )

    while (computerTurn and any(position[1][0])) or \
          (not computerTurn and any(position[0][0])) :
      computerTurn = not computerTurn

      mvLog = []

      if not computerTurn:
        dice = [random.randint(1, 6) for _ in range(nDice)]
        mvLog.append(tuple(dice))

        window.addstr(11, dice_x0 - 10, "1st Roll:")

        for j in range(nDice) :
          drawDie(dice[j], j, window, 9, dice_x0, opDieColor)
        stage = 1

        while stage < nReRolls + 2:

          if sum(x is not None for x in dice) == nDice:
            for i,pts in game.rollScores(tuple(sorted(dice)), position[1][0]) :
              window.addstr(7, 12 + i*5, format(pts,'2d'), curses.color_pair(3))
          else:
            for i,b in enumerate(position[1][0]) :
              if b :
                window.addstr(7, 12 + i*5, '  ');

          event = screen.getch()
          if event in [ord("q"), ord("e")] :
            break

          if stage < nReRolls+1 and (event == ord(" ") or event == ord("r")) :
            kept = [d for d in dice if d is not None]
            rolled = []
            for j,d in enumerate(dice) :
              if d is None:
                dice[j] = random.randint(1, 6)
                rolled.append(dice[j])
                drawDie(dice[j], j, window, 9, dice_x0, opDieColor)
            mvLog.append( (tuple(kept), tuple(rolled)) )
            stage += 1
          else :
            if event == curses.KEY_MOUSE:
              try:
                e = curses.getmouse()
              except:
                continue
              mx, my = e[1:3]
              showInfo(f"{(mx,my)}", debug)
              if 9 < my < 9+dieHeight-1 :
                z = mx - dice_x0
                i = z//6
                if 0 <= i < nDice and 0 < z % 6 < dieWidth-1:
                  showInfo(f"{(mx,my)} {i}", debug)
                  if dice[i] is not None:
                    clearDie(i, window, 9, dice_x0)
                    dice[i] = None

              if my == 7 :
                z = mx - 12
                i = z//5
                showInfo(f"{(mx,my,z,i)}*{0 <= i < nCombinations and 0 < (z % 5) and position[1][0][i]}", debug)

                if 0 <= i < nCombinations and 0 < (z % 5) and position[1][0][i] :
                  bx = [0]*nCombinations; bx[i] = 1
                  pts = max(game.rollScores(tuple(sorted(dice)), bx))[1]
                  window.addstr(7, 12 + i*5, format(pts,'2d'), curses.A_BOLD)
                  bx = list(position[1][0]); bx[i] = 0;
                  position = position[:1] + ( (bx,pts + position[1][1]), )
                  while len(mvLog) < nReRolls+1:
                    mvLog.append( ( (tuple(sorted(dice))), tuple()) )
                  mvLog.extend( (i, pts) )
                  stage = nReRolls+2

            elif stage < nReRolls+1 and event in range(ord("0"), ord("1")+6):
              ## speedup
              v = int(chr(event))
              kept,rolled = [], []
              for i,d in enumerate(dice):
                if d != v:
                  dice[i] = random.randint(1, 6)
                  rolled.append(dice[i])
                  drawDie(dice[i], i, window, 9, dice_x0, opDieColor)
                else :
                  kept.append(d)
              mvLog.append( (tuple(kept), tuple(rolled)) )
              stage += 1
          if stage <= nReRolls:
            window.addstr(11, dice_x0 - 10, f"{stage}nd Roll:")
          else :
            window.addstr(11, dice_x0 - 10, "         ")

        if event in [ord("q"),ord("e")] :
          break
      else :
        window.addstr(11, dice_x0 - 10, "         ")
        for i,b in enumerate(position[1][0]) :
          if b :
            window.addstr(7, 12 + i*5, '  ');

        window.addstr(7, 10 + len(sepLine) + 2, format(position[1][1],'3d'))
        window.refresh()

        ## roll 1
        dice = [random.randint(1, 6) for _ in range(nDice)]
        mvLog.append( tuple(dice) )

        for j in range(nDice) :
          drawDie(dice[j], j, window, 9, dice_x0, compDieColor)

        for nr in range(nReRolls) :
          keep = list(player.actionRoll(nr+1, position, tuple(sorted(dice))))

          showInfo(f"{dice} {keep}", debug)
          window.refresh()
          time.sleep(delay)
          
          rolled = []
          mvLog.append( (tuple(keep), None) )

          if len(keep) < nDice :
            for i,d in enumerate(dice) :
              if d not in keep:
                dice[i] = None
                clearDie(i, window, 9, dice_x0)
              else :
                keep.remove(d)
            window.refresh()
            time.sleep(delay)

            for j,d in enumerate(dice) :
              if d is None:
                dice[j] = random.randint(1, 6)
                rolled.append(dice[j])

                drawDie(dice[j], j, window, 9, dice_x0, compDieColor)

          mvLog[-1] = (mvLog[-1][0], tuple(rolled))

        dice = tuple(sorted(dice))
        iMoves = player.actionEndTurn(position, dice)
        if len(iMoves) > 1:
          iMove = random.choice(iMoves)
        else :
          iMove = iMoves[0]

        bx,n = position[0]; bx = list(bx); bx[iMove] = 0

        b = [0]*len(bx)
        b[iMove] = 1
        i,pts = max(player.game.rollScores(dice, b))
        mvLog.extend( (iMove, pts) )

        position = ( (tuple(bx),n+pts), ) +  position[1:]
        window.addstr(5, 12 + i*5, format(pts,'2d'), curses.A_BOLD)
        window.addstr(5, 10 + len(sepLine) + 2, format(position[0][1],'3d'))

        window.refresh()
        time.sleep(1.5*delay)

      gameLog.append( mvLog )

    if flog:
      print( gameLog, file = flog )
      flog.flush()
      
    
def main():
  global flog, game, player, compName, opName
  
  parser = argparse.ArgumentParser(description = """Play Yatzy/Yacht/Generala, Man against the Machine.""")

  parser.add_argument("--record", "-r", metavar="FILE", help = "Record the match in FILE.")

  parser.add_argument("--name", "-n", metavar="YOUR-NAME", default = "Human", help = "Your name.")

  parser.add_argument("--player", "-p", metavar="OPPONENT-NAME", choices=["Joe", "Maximux", "Titus"],
                      default = "Maximux", help = "")

  parser.add_argument('game', metavar='GAME', choices=["Yatzy", "Yacht", "Generala", "Crag"],
                      help="yatzy/yacht/generala/crag")
  
  options = parser.parse_args()

  try :
    flog = open(options.record, 'a') if options.record else None
  except:
    print("Error opening match log.", file = sys.stderr)
    sys.exit(1)

  try:
    gameName = options.game.capitalize()
    gameClass = globals()[gameName]
    game = getattr(gameClass, gameName)()
  except:
    print("Unrecognized game.", file = sys.stderr)
    sys.exit(1)

  opName = options.name[:10]
  compName = options.player
  if options.player == "Joe" :
    player = genericPlayers.SimplePlayer(game)
  elif options.player == "Maximux" :
    player = genericPlayers.OSTBPlayer(game, f"data/{gameName.lower()}-maxi.txt")
  elif options.player == "Titus" :
    player = genericPlayers.MindfulPlayer(game, f"data/{gameName.lower()}-scdist.txt")
  else :
    assert False

if __name__ == "__main__":
  main()

curses.wrapper(ut_interface)

if flog:
  flog.close()
  
