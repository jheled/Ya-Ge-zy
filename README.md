# Ya-Ge-zy
The dice games of Generala, Yacht, Yatzy, and even Crag.

Initial offering. Text interface only at the moment (curses), but extremely
strong players.

Read all about it here
https://figshare.com/articles/Stay_in_Command_Optimal_Play_for_Two_Person_Generala/10250957 (or at
least something).

Run 'python3 generateDataFiles.py' to generate the data files.
Or better yet download them: In the Ya-Ge-zy directory do,

`>>>` wget https://filedn.com/llztAlmJ0zvkPa8QEheU5n5/yagezy-data.tar.xz

`>>>` tar xf yagezy-data.tar.xz

To play, run

`>>>` ./yagezyConsole.py -n YOUR-NAME -r FILE-TO-LOG-GAMES Generala  (or Yacht, Yatzy or Crag)

To analyze your play, run

`>>>` ./annotateGame.py FILE-TO-LOG-GAMES


