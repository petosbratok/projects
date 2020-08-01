Eng

Python 3.7
Tic-tac-toe
How to play:
  1) Start the game (type "start [user1] [user2]") or type exit to exit.
  Instead of "user1", "user2" you have to type "user", "easy", "medium" or "hard".
  2) Table looks like this:
	   1  2  3
	  ---------
	1 |       |
	2 |       |
	3 |       |
	  ---------
  3) First you choose the row, then the column.

AI modes:

Easy: computer makes random moves.

Medium: computer makes sertain move if it can win with 1 move, else random.

Hard: this was supposed to have simple machine learning but
it was not working properly, you were able to win easiy.
So I had to hardcode the rules using game theory. PC is trying to find any
sertanly-winning 1-2-3-move combinations.
If it can't, it is using an unreliable machine learning strategy with recursion.


