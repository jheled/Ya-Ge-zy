# Ya-Ge-zy
The dice games of Generala, Yacht and Yatzy.

Initial offering. Text interface only (curses) at the moment, but extremely
strong players.

Run 'python3 generateDataFiles.py' to generate the data files.
Or better yet download them: In the Ya-Ge-zy directory do,

`>>>` wget https://filedn.com/llztAlmJ0zvkPa8QEheU5n5/yagezy-data.tar.xz

`>>>` tar xf yagezy-data.tar.xz

To play, run

`>>>` ./yagezyConsole.py -n YOUR-NAME -r FILE-TO-LOG-GAMES Generala  (or Yacht or Yatzy)

To analyze your play, run

`>>>` ./annotateGame.py FILE-TO-LOG-GAMES


