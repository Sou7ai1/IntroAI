**Game Rules**

The game starts with n stones numbered 1, 2, 3, ..., n. Players take turns removing one of the remaining numbered stones. At a given turn there are some restrictions on which numbers (i.e., stones) are legal candidates to be taken. The restrictions are:

* At the first move, the first player any stone.
* At subsequent moves, players alternate turns. The stone number that a player can take must be a multiple or factor of the last move (note: 1 is a factor of all other numbers). Also, this number may not be one of those that has already been taken. After a stone is taken, the number is saved as the new last move. If a player cannot take a stone, he/she loses the game.

An example game is given below for n = 7:
* Player 1: 3
* Player 2: 6
* Player 1: 2
* Player 2: 4
* Player 1: 1
* Player 2: 7
* Winner: Player 2

**Task**

Implement the function *player* in file *multiple_divisor.py*. This function is expected to make one move of a player. The function has two arguments:
* stones: A list of remaining numbers which have not been taken.
* last: A number taken in the last move.
The function is expected to return one number which can be taken to win if the position is winning, and *False* if the position is loosing.

In order to simplify the task, the function is not expected to make the first move, so the last move is always given. Submit only the file *muliple_divisor.py* which must not be renamed.
